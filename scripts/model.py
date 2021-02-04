# model.py - Storage access for scsa notebook
# rcampbel@purdue.edu - 2020-07-14

import glob
import os
import pickle
import time
import csv

import pandas as pd

from scripts.constants import *


def count(series):
    return len(series)


class Model:
    DATA_DIR = 'data'
    FLOAT_FORMAT = '0,.4f'

    def __init__(self):
        self.view = None
        self.ctrl = None
        self.data = None
        self.results = None
        self.res_row_count = 0
        self.res_csv = None
        self.headers = ''
        self.query = ''
        self.valid = False
        self.uniques = {}
        self.mods = set()
        self.processed = None

    def intro(self, view, ctrl):
        """Introduce MVC modules to each other"""
        self.view = view
        self.ctrl = ctrl

    def get_data(self, data_file):
        """Load data from file (init data access)"""
        self.ctrl.logger.debug('At')
        self.data = pd.read_csv(data_file)
        self.mods, self.uniques = pickle.load(open(os.path.splitext(data_file)[0] + '.p', 'rb'))
        self.valid = True
        self.ctrl.logger.info('Done loading data file "' + data_file + '"')

    def clear_filter_results(self):
        self.results = None
        self.res_row_count = 0

    def search(self, mod, scn, reg, ind, sec, yrs):
        """Use provided values lists to search for data"""
        self.ctrl.logger.debug('At')

        # Build query string
        self.query = (' & ' + F_MOD + ' == ' + str(mod)) if ALL not in mod else ''
        self.query += (' & ' + F_SCN + ' == ' + str(scn)) if ALL not in scn else ''
        self.query += (' & ' + F_REG + ' == ' + str(reg)) if ALL not in reg else ''
        self.query += (' & ' + F_IND + ' == ' + str(ind)) if ALL not in ind else ''
        self.query += (' & ' + F_SEC + ' == ' + str(sec)) if ALL not in sec else ''
        self.query += (' & ' + F_YER + ' == ' + str(yrs)) if ALL not in yrs else ''

        if self.query.strip() == '':
            # Return all data
            self.ctrl.logger.info('Query string empty. Returning ALL data.')
            self.results = self.data
        else:
            # Run query
            self.query = self.query[3:]  # Remove leading ' & '
            self.ctrl.logger.info('Query "' + self.query + '"')
            self.results = self.data.query(self.query)

        self.res_row_count = self.results.shape[0]
        self.ctrl.logger.info('Returned ' + str(self.res_row_count) + ' records')

    def sort(self, col_list):
        self.results = self.results.sort_values(by=col_list)

    def iterate_results(self):
        return self.results.itertuples()

    def delete_downloads(self, base_name):
        """Remove any existing download file(s) of given name"""
        self.ctrl.logger.debug('At')

        for filename in glob.glob(base_name + '.*'):
            os.remove(filename)

    def create_download_file(self, data, file_format_ext):
        """Prep data for export"""
        self.ctrl.logger.debug('At')

        # First, to save space, delete existing download file(s)
        self.delete_downloads(DOWNLOAD_DATA_NAME)

        # Create new download file

        filename = DOWNLOAD_DATA_NAME + file_format_ext

        if file_format_ext == FORMAT_EXT_CSV:
            data.to_csv(filename, index=False, quoting=csv.QUOTE_NONNUMERIC)
        elif file_format_ext == FORMAT_EXT_JSON:
            data.to_json(filename, orient='table', index=False)
        elif file_format_ext == FORMAT_EXT_HTML:
            data.to_html(filename, index=False)
        elif file_format_ext == FORMAT_EXT_EXCEL:
            data.to_excel(filename, index=False)
        elif file_format_ext == FORMAT_EXT_HDF5:
            data.to_hdf(filename, key='AgMIP')
        elif file_format_ext == FORMAT_EXT_PICKLE:
            data.to_pickle(filename)

        return filename

    def get_data_options(self):
        """Build list of (<filename>,<description>) options for data sources"""

        options = []

        for filename in glob.glob(os.path.join(self.DATA_DIR, '*.csv')):

            if os.path.isfile(filename):
                meta = os.stat(filename)
                desc = os.path.basename(filename)
                desc += ': ' + str(round(meta.st_size / (1024 ** 3), 3)) + ' GB'
                desc += ', ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(meta.st_mtime))
                options.append((desc, filename))

        return options

    def get_uniques_for(self, field_name):
        unique_values = ()

        if self.res_row_count > 0:
            unique_values = tuple(self.results[field_name].unique())

        return unique_values

    def set_disp(self, data=None, limit=None, wide=False):
        """Prep Pandas to display specific number of data lines"""

        if not limit:
            limit = data.shape[0]

        pd.set_option('display.max_rows', limit + 1)

        if wide:
            pd.set_option('display.float_format', lambda x: format(x, self.FLOAT_FORMAT))

    def init_processed(self):
        self.processed = self.results.copy(deep=True)

    def pivot(self, x_field, pivot_field, y_field, aggfunc):
        """Create pivot table from results"""
        self.ctrl.logger.debug('x=%s pivot=%s y=%s aggf=%s' % (x_field, pivot_field, y_field, aggfunc))

        if aggfunc == AGGF_COUNT:
            aggfunc = count  # Translate string to func handle

        if not aggfunc == NONE_ITEM:
            self.processed = self.processed.pivot_table(index=x_field, columns=pivot_field, values=y_field,
                                                        aggfunc=aggfunc)
        else:
            self.processed = self.processed.pivot_table(index=x_field, columns=pivot_field, values=y_field)

    def fill(self, fill_type):
        """Fill missing data (NaNs) in processed results"""
        self.ctrl.logger.debug('fill=%s' % fill_type)

        if fill_type == FILL_PAD:
            fill_type = 'nearest'
            limit_direction = 'forward'
        else:
            limit_direction = 'both'

        self.processed.interpolate(inplace=True, method=fill_type, limit_direction=limit_direction)

    def harmonize(self, base_row, base_col):
        """Harmonized pivot table based on given row and col (values)"""
        self.ctrl.logger.debug('base_row='+str(base_row)+' base_col='+str(base_col))

        # Harmonize to row by creating multiplier table

        results_mults = pd.DataFrame()

        for col in self.processed.columns.values:
            base = self.processed[col][base_row]
            results_mults[col] = self.processed[col].apply(func=lambda x: x / base)

        # Harmonize to column by applying multipliers to pivot table

        results_harm = pd.DataFrame().reindex_like(self.processed)

        for col in self.processed.columns.values:
            for row in self.processed.index.values:
                mult = results_mults[col][row]
                results_harm[col][row] = self.processed[base_col][base_row] * mult

        self.processed = results_harm

    def dropna(self):
        self.processed.dropna()

    def index(self, year, on_row=True):
        """Index pivot table based on year"""
        self.ctrl.logger.debug('At')

        results_indexed = pd.DataFrame().reindex_like(self.processed)

        if on_row:
            for col in self.processed.columns.values:
                for row in self.processed.index.values:
                    results_indexed[col][row] = self.processed[col][row] / self.processed[col][year] * 100.0
        else:
            for row in self.processed.index.values:
                for col in self.processed.columns.values:
                    results_indexed[col][row] = self.processed[col][row] / self.processed[year][row] * 100.0

        self.processed = results_indexed
