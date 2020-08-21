# model.py - Storage access for datapub notebook
# rcampbel@purdue.edu - 2020-07-14

import os
import sys
import pandas as pd

class Model:

	DATA_DIR  = 'data'
	DATA_FILE = 'MergedData.csv'

	def __init__(self):
		self.view      = None
		self.ctrl      = None
		self.root      = self.DATA_DIR
		self.data      = None
		self.results   = None
		self.res_count = 0
		self.res_csv   = None
		self.headers   = None
		self.query     = ''

	def intro(self,view,ctrl):
		'''Introduce MVC modules to each other'''
		self.view = view
		self.ctrl = ctrl

	def get_data(self):
		'''Load data from file (init data access)'''
		pd.set_option('display.max_rows', 500)
		pd.set_option('display.max_columns', 500)
		pd.set_option('display.width', 1000)

		self.data = pd.read_csv(os.path.join(self.DATA_DIR,self.DATA_FILE))

		self.mods  = list(pd.unique(self.data.Model    ))
		self.scns  = list(pd.unique(self.data.Scenario ))
		self.regs  = list(pd.unique(self.data.Region   ))
		self.inds  = list(pd.unique(self.data.Indicator))
		self.secs  = list(pd.unique(self.data.Sector   ))
		self.years = sorted(pd.unique(self.data.Year))

	def describe_data(self):
		'''Render HTML string providing explanation of data'''
		self.headers = list(self.data.columns)
		return str(self.data)

	def clear_filter_results(self):
		self.results   = None
		self.res_count = 0

	def search(self,mod,scn,reg,ind,sec,yr1,yr2):
		'''Use provided values lists to search for data'''
		self.ctrl.debug('search()')

		# Build query string
		self.query  = (' & Model == '     + str(mod)) if not self.view.ALL in mod else ''
		self.query += (' & Scenario == '  + str(scn)) if not self.view.ALL in scn else ''
		self.query += (' & Region == '    + str(reg)) if not self.view.ALL in reg else ''
		self.query += (' & Indicator == ' + str(ind)) if not self.view.ALL in ind else ''
		self.query += (' & Sector == '    + str(sec)) if not self.view.ALL in sec else ''
		self.query += (' & Year >= '      + str(yr1)) if not self.view.ALL == yr1 else ''
		self.query += (' & Year <= '      + str(yr2)) if not self.view.ALL == yr2 else ''
		self.query = self.query[3:]  # Remove leading ' & '
		self.ctrl.debug('Query string: "'+self.query+'"')

		# Run query
		self.results   = self.data.query(self.query)
		self.res_count = self.results.shape[0]

	def sort(self,col_list):
		self.results = self.results.sort_values(by=col_list)

	def iterate_results(self):
		return self.results.itertuples()

	def write_results(self):
		'''Prep data for export'''
		self.ctrl.debug('write_results()')
		self.res_csv = ','.join(self.headers) + '\n'

		self.ctrl.debug('Mid write_results()')

		for i,row in enumerate(self.iterate_results()):
			self.res_csv += ','.join([
				str(row.Model     )
				,str(row.Scenario )
				,str(row.Region   )
				,str(row.Indicator)
				,str(row.Sector   )
				,str(row.Unit     )
				,str(row.Year     )
				,str(row.Value    )
			]) + '\n'

		self.ctrl.debug('Leaving write_results()')


