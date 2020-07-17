# model.py - Storage access for datapub notebook
# rcampbel@purdue.edu - 2020-07-14

import os
import sys
import pandas as pd

class Model:

	DATA_DIR	   = 'data'
	DATA_FILE      = 'MergedData.csv'

	def __init__(self):
		self.view = None
		self.ctrl = None
		self.root = self.DATA_DIR
		self.data = None

	def intro(self,view,ctrl):
		self.view = view
		self.ctrl = ctrl

	def get_data(self):
		'''Load data from file (init data access)'''
		pd.set_option('display.max_rows', 500)
		pd.set_option('display.max_columns', 500)
		pd.set_option('display.width', 1000)

		self.data = pd.read_csv(os.path.join(self.DATA_DIR,self.DATA_FILE))

	def describe_data(self):
		'''Render HTML string providing explanation of data'''
		self.ctrl.debug('model.describe_dataa()...')
		self.ctrl.debug(str(self.data.head()))
		self.ctrl.debug(str(self.data.columns))
		self.ctrl.debug(str(self.data.shape))
		return str(self.data)

	def write_data(self):
		'''Prep data for export'''
		# TODO Render data
		pass
		#return data



