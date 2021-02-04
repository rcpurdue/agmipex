# controller.py - Central logic for scsa notebook
# rcampbel@purdue.edu - 2020-07-14

import logging
import time
import traceback
import warnings  # Avoids warning: "numpy.dtype size changed, may indicate binary incompatibility"
from matplotlib import pyplot as plt
from IPython.core.display import display, clear_output

from scripts.constants import *

warnings.filterwarnings('ignore')  # TODO Confirm still needed?

PLOT_LINE_DATA_MARKER = 'o'
PLOT_WIDTH = 12  # inches
PLOT_HEIGHT = 6  # inches
PLOT_EMPTY_X_AXIS = 'X Axis'
PLOT_EMPTY_Y_AXIS = 'Y Axis'


class CombineLogFields(logging.Filter):
    def filter(self, record):
        record.filename_lineno = "%s:%d" % (record.filename, record.lineno)
        return True


class Controller(logging.Handler):
    VALUE = 'value'  # for observe calls

    def __init__(self, log_mode):  # 0=none 1=info 2=debug

        # TODO Remove testing code below
        # log_mode += 2

        self.display_log = log_mode > 0
        self.debug_buffer = []
        self.display_ready = False

        if log_mode == 2:
            log_format = '%(levelname)1.1s %(asctime)s %(filename_lineno)-18s %(message)s (%(funcName)s)'
            log_level = logging.DEBUG
        else:
            log_format = '%(asctime)s %(message)s'
            log_level = logging.INFO

        self.plot_figure = None

        logging.Handler.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.setFormatter(logging.Formatter(log_format, '%Y-%m-%dT%H:%M:%S'))
        self.logger.addHandler(self)
        self.logger.addFilter(CombineLogFields())
        self.logger.setLevel(log_level)
        self.setLevel(log_level)

        self.model = None
        self.view = None

    def intro(self, model, view):
        """Introduce MVC modules to each other"""
        self.model = model
        self.view = view

    def emit(self, message):
        """Pass new log msg to view for display"""
        if self.display_log:

            text = self.format(message)
            self.debug_buffer.append(text)

            if self.display_ready:

                for line in self.debug_buffer:
                    self.view.debug(line)

                self.debug_buffer = []

    def start(self):
        """Load data, build UI, setup callbacks"""
        self.logger.debug('At')

        try:
            # Set up user interface
            self.view.display(self.display_log)
            self.display_ready = True

            # Connect UI widgets to callback methods ("cb_...").
            #   Methods listed below will be called when user activates widget.
            #   Format: <widget>.on_click/observe(<method_to_be_called>...)
            self.view.data_ddn_src.observe(self.cb_data_source_selected, self.VALUE)
            self.view.filter_mod.observe(self.cb_model_selected, self.VALUE)
            self.view.filter_btn_apply.on_click(self.cb_apply_filter)
            self.view.filter_ddn_ndisp.observe(self.cb_ndisp_changed, self.VALUE)
            self.view.filter_btn_refexp.on_click(self.cb_fill_results_export)
            self.view.viz_ddn_plot_set.observe(self.cb_plot_menu, self.VALUE)
            self.view.viz_btn_plot_generate.on_click(self.cb_plot_button)
            self.view.viz_ddn_plot_xaxis.observe(self.cb_refresh_harmonizers, self.VALUE)
            self.view.viz_ddn_plot_pivot.observe(self.cb_refresh_harmonizers, self.VALUE)
            self.view.data_btn_refexp.on_click(self.cb_fill_data_export)
            self.view.viz_btn_plot_refexp.on_click(self.cb_fill_plot_export)

        except Exception:
            self.logger.error('EXCEPTION\n' + traceback.format_exc())
            raise

    def cb_data_source_selected(self, change):
        """User selected a data file"""
        self.logger.debug('At')

        try:
            choice = change['owner'].value

            if not choice == self.view.EMPTY:
                self.view.update_data_status(self.view.DATA_LOAD)
                self.model.get_data(choice)
                self.view.update_data_status(self.model.data)
                self.view.update_dynamic_selections()
        except Exception:
            self.logger.error('EXCEPTION\n' + traceback.format_exc())
            raise

    def cb_model_selected(self, change):
        """User changed their model filter selection"""
        self.logger.debug('At')

        try:
            self.view.model_selected(change['owner'].value)
        except Exception:
            self.logger.error('EXCEPTION\n' + traceback.format_exc())
            raise

    def cb_apply_filter(self, _):
        """User hit button to search for data"""
        self.logger.debug('At')

        if not self.model.valid:
            return

        try:
            self.view.output(FILTER_PROG, self.view.filter_output)
            self.view.filter_out_export.clear_output()

            # Use specified criteria to search for data, (results stored in model)
            self.model.clear_filter_results()
            self.model.search(
                list(self.view.filter_mod.value),
                list(self.view.filter_scn.value),
                list(self.view.filter_reg.value),
                list(self.view.filter_ind.value),
                list(self.view.filter_sec.value),
                list(self.view.filter_yrs.value)
            )

            # Refresh output widgets
            self.view.update_filtered_output()
            self.view.set_plot_status()
            self.cb_refresh_harmonizers()

        except Exception:
            self.logger.error('EXCEPTION\n' + traceback.format_exc())
            raise

    def cb_ndisp_changed(self, _):
        """User changed number of recs to display"""
        try:
            self.view.update_filtered_output()
        except Exception:
            self.logger.error('EXCEPTION\n' + traceback.format_exc())
            raise

    def cb_fill_data_export(self, _):
        """User hit button to bulk download all data"""
        self.logger.debug('At')

        try:
            # First, clear _RESULTS_ link because it might point to same file
            self.view.export_msg('', self.view.filter_out_export)

            # Create link for bulk data
            if self.model.valid:
                self.view.export_msg(CREATING_LINK, self.view.data_out_export)
                filename = self.model.create_download_file(self.model.data, self.view.data_ddn_format.value)
                self.view.export_link(filename, self.view.data_out_export)
            else:
                self.view.export_msg(NO_DATA_AVAIL, self.view.data_out_export)
        except Exception:
            self.logger.debug('EXCEPTION\n' + traceback.format_exc())
            raise

    def cb_fill_plot_export(self, _):
        """User hit button to download image of plot"""
        self.logger.debug('At')

        try:
            self.view.export_msg('...', self.view.viz_out_plot_export)
            time.sleep(1)

            # First, to save space, delete existing download file(s)
            self.model.delete_downloads(DOWNLOAD_PLOT_NAME)

            # Create link for image file
            filename = DOWNLOAD_DATA_NAME + self.view.viz_ddn_plot_format.value
            self.plot_figure.savefig(filename)
            self.view.export_link(filename, self.view.viz_out_plot_export)
        except Exception:
            self.logger.debug('EXCEPTION\n' + traceback.format_exc())
            raise

    def cb_fill_results_export(self, _):
        """User hit button to download results"""
        self.logger.debug('At')

        try:
            # First, clear _DATA_ link because it might point to same file
            self.view.export_msg('', self.view.data_out_export)

            # Create link for filter results
            if self.model.res_row_count > 0:
                self.view.export_msg(CREATING_LINK, self.view.filter_out_export)
                filename = self.model.create_download_file(self.model.results, self.view.filter_ddn_format.value)
                self.view.export_link(filename, self.view.filter_out_export)
            else:
                self.view.export_msg(NO_RECS_AVAIL, self.view.filter_out_export)
        except Exception:
            self.logger.debug('EXCEPTION\n' + traceback.format_exc())
            raise

    def cb_refresh_harmonizers(self, _=None):
        """User changed plot options, update harmonize widgets with values"""
        self.logger.debug('At')

        try:
            self.view.set_harmonize(self.model.get_uniques_for(self.view.viz_ddn_plot_xaxis.value),
                                    self.model.get_uniques_for(self.view.viz_ddn_plot_pivot.value))
        except Exception:
            self.logger.debug('EXCEPTION\n' + traceback.format_exc())
            raise

    def cb_plot_menu(self, change):
        """User selected item from plot menu"""
        # noinspection PyBroadException
        try:
            if not change['owner'].value == PLOT_SET_CUSTOM:
                self.set_plot_config(change['owner'].value)
                self.process_and_plot()
        except Exception:
            self.empty_plot(error=True)
            self.logger.debug('EXCEPTION\n' + traceback.format_exc())

    def cb_plot_button(self, _):
        """User pressed plot button"""
        # noinspection PyBroadException
        try:
            self.view.viz_ddn_plot_set.value = PLOT_SET_CUSTOM
            self.process_and_plot()
        except Exception:
            self.empty_plot(error=True)
            self.logger.debug('EXCEPTION\n' + traceback.format_exc())

    def process_and_plot(self):
        """Process data and plot it"""
        self.logger.debug('At')

        x = self.view.viz_ddn_plot_xaxis.value
        y = self.view.viz_ddn_plot_yaxis.value
        pivot = self.view.viz_ddn_plot_pivot.value
        fill = self.view.viz_ddn_plot_fill.value
        harm_row = self.view.viz_ddn_plot_harm_row.value
        harm_col = self.view.viz_ddn_plot_harm_col.value

        # Specify numeric axis(es)
        numeric_xy = (x == F_VAL or x == F_YER,
                      y == F_VAL or y == F_YER)

        # Plot will be based on model's "processed" data
        self.model.init_processed()

        # Clear pivot table data
        with self.view.viz_out_plot_data:
            clear_output(wait=True)

        self.model.pivot(x, pivot, y, self.view.viz_ddn_plot_aggfunc.value)

        # Fill missing values (interpolate)?
        if not fill == NONE_ITEM:
            self.model.fill(fill)

        # Index to year?

        indexed_by = None

        if self.view.viz_ckb_plot_index.value:

            if x == F_YER and not harm_row == NONE_ITEM:
                indexed_by = harm_row
            elif y == F_YER and not harm_col == NONE_ITEM:
                self.model.index(harm_col, on_row=False)
                indexed_by = harm_col

            if indexed_by is not None:
                self.model.index(indexed_by)

        # Harmonize?

        harmonized = False

        if (not harm_row == NONE_ITEM) and (not harm_col == NONE_ITEM):
            self.model.harmonize(harm_row, harm_col)
            harmonized = True

        # Title

        title = y + ' for ' + pivot + ' by ' + x

        if indexed_by is not None:
            if harmonized:
                title += ', Harmonized: '

                if indexed_by == harm_row:
                    title += str(harm_col)
                else:
                    title += str(harm_row)

            title += ', Index: ' + str(indexed_by) + '=100'

        elif harmonized:
            title += ', Harmonized: ' + str(harm_row) + ', ' + str(harm_col)

        self.model.dropna()

        # Show plot data
        with self.view.viz_out_plot_data:
            self.model.set_disp(self.model.processed, wide=True)
            clear_output(wait=True)
            display(self.model.processed)

        # Draw plot based on processed data
        self.draw_plot(title, x, y, numeric_xy)

    def set_plot_config(self, choice):
        """Update plot options"""
        self.logger.debug('At, choice='+str(choice))

        if choice == PLOT_SET_1:
            self.view.viz_ddn_plot_type.value = PLOT_TYPE_LINE
            self.view.viz_ddn_plot_xaxis.value = F_YER
            self.view.viz_ddn_plot_yaxis.value = F_VAL
            self.view.viz_ddn_plot_pivot.value = F_MOD
            self.view.viz_ddn_plot_aggfunc.value = AGGF_SUM
            self.view.viz_ddn_plot_fill.value = FILL_LINEAR
        elif choice == PLOT_SET_2:
            self.view.viz_ddn_plot_type.value = PLOT_TYPE_BAR
            self.view.viz_ddn_plot_xaxis.value = F_MOD
            self.view.viz_ddn_plot_yaxis.value = F_VAL
            self.view.viz_ddn_plot_pivot.value = F_SCN
            self.view.viz_ddn_plot_aggfunc.value = AGGF_MEAN
            self.view.viz_ddn_plot_fill.value = NONE_ITEM
        elif choice == PLOT_SET_3:
            self.view.viz_ddn_plot_type.value = PLOT_TYPE_LINE
            self.view.viz_ddn_plot_xaxis.value = F_YER
            self.view.viz_ddn_plot_yaxis.value = F_VAL
            self.view.viz_ddn_plot_pivot.value = F_MOD
            self.view.viz_ddn_plot_aggfunc.value = AGGF_SUM
            self.view.viz_ddn_plot_fill.value = FILL_CUBIC
            self.view.viz_ddn_plot_harm_row.value = self.view.viz_ddn_plot_harm_row.options[1]
            self.view.viz_ddn_plot_harm_col.value = self.view.viz_ddn_plot_harm_col.options[1]

    def empty_plot(self, error=None):
        """Display empty plot frame, with optional error message, in provided output widget"""
        self.logger.debug('At, error='+str(error))

        # noinspection PyBroadException
        try:
            if error:
                title = self.view.PLOT_ERROR_MSG
            else:
                title = 'Plot'

            with self.view.viz_out_plot_output:
                clear_output(wait=True)
                print()
                fig, ax = plt.subplots(figsize=(PLOT_WIDTH, PLOT_HEIGHT))
                ax.set_xlabel(PLOT_EMPTY_X_AXIS)
                ax.set_ylabel(PLOT_EMPTY_Y_AXIS)
                plt.title(title)
                plt.grid()
                self.plot_figure = plt.gcf()
                plt.show()
        except Exception:
            plt.close()  # Clear any partial plot output
            self.logger.debug('raising exception')
            raise

    def draw_plot(self, title, x_label, y_label, numeric_xy):
        """Create plot image and display it in provided output widget"""
        self.logger.debug('title=%s labels="%s","%s" num-xy=%s' % (title, x_label, y_label, str(numeric_xy)))

        # noinspection PyBroadException
        try:
            with self.view.viz_out_plot_output:
                # Clear existing plot output, including previous error msg
                clear_output(wait=True)
                print()

                # Render plot - NOTE Assumes data is pandas datatframe TODO Abstract that?

                fig, ax = plt.subplots()

                if self.view.viz_ddn_plot_type.value == PLOT_TYPE_LINE:
                    self.model.processed.plot(kind=PLOT_TYPE_LINE,
                                              ax=ax, grid=True, title=title,
                                              figsize=(PLOT_WIDTH, PLOT_HEIGHT),
                                              marker=PLOT_LINE_DATA_MARKER)
                else:
                    self.model.processed.plot(kind=self.view.viz_ddn_plot_type.value,
                                              ax=ax, grid=True, title=title,
                                              figsize=(PLOT_WIDTH, PLOT_HEIGHT))
                # Label axes
                ax.set_xlabel(x_label)
                ax.set_ylabel(y_label)

                # Avoid scientific notation for limits on numeric axis(es)
                if numeric_xy[0]:
                    ax.ticklabel_format(axis='x', useOffset=False, style='plain')
                if numeric_xy[1]:
                    ax.ticklabel_format(axis='y', useOffset=False, style='plain')

                # Update output widget with new plot
                self.plot_figure = plt.gcf()
                plt.show()
                self.logger.debug('after plt.show()')
        except Exception:
            plt.close()  # Clear any partial plot output
            self.logger.debug('raising exception')
            raise
