# controller.py - Central logic for datapub notebook
# rcampbel@purdue.edu - 2020-07-14

import os
import sys
import traceback
from inspect import getframeinfo, stack

# Avoids warning: "numpy.dtype size changed, may indicate binary incompatibility"
import warnings
warnings.filterwarnings('ignore')

class Controller:

	VALUE = 'value' # for observe calls

	def __init__(self):
		self.debugging     = False # NOTE Change to False to hide debug output
		self.debug_buffer  = []
		self.display_ready = False

	def intro(self,model,view):
		'''Introduce MVC modules to each other'''
		self.model = model
		self.view  = view

	def start(self):
		'''Load data, build UI, setup callbacks'''
		self.debug('Starting...')

		try:
			# Load data
			self.model.get_data()

			# Set up user interface
			self.view.display(debug=self.debugging)
			self.display_ready = True

			# Connect UI widgets to callback methods ("cb_...").
			# These methods will be run when user changes widget.

			# ________ Widget ___________________ _____________Method to call ___________________
			self.view.filter_btn_apply.on_click(  self.cb_apply_filter)
			self.view.filter_ddn_ndisp.observe(   self.cb_ndisp_changed,self.VALUE)
			self.view.filter_btn_refexp.on_click( self.cb_fill_results_export)
			self.view.viz_ddn_plot_type.observe(  self.cb_plot_type_selected,self.VALUE)
		except:
			self.debug('EXCEPTION\n'+traceback.format_exc())
			raise

	def cb_apply_filter(self,change):
		'''User hit button to search for data'''
		self.debug()

		try:
			self.view.filter_html_output.value = self.view.FILTER_PROG
			self.view.filter_out_export.clear_output()
			self.view.viz_ddn_plot_type.value = self.view.EMPTY

			# Use specified criteria to search for data, (results stored in model)
			self.model.clear_filter_results()
			self.model.search(
				list(self.view.filter_mod.value)
				,list(self.view.filter_scn.value)
				,list(self.view.filter_reg.value)
				,list(self.view.filter_ind.value)
				,list(self.view.filter_sec.value)
				,self.view.filter_yr1.value
				,self.view.filter_yr2.value
			)

			# Refresh output widgets
			self.view.update_filtered_output()
			self.view.set_plot_status()
		except:
			self.debug('EXCEPTION\n'+traceback.format_exc())
			raise

	def cb_ndisp_changed(self,change):
		'''User changed number of recs to display'''
		try:
			self.view.update_filtered_output()
			self.view.set_plot_status()
		except:
			self.debug('EXCEPTION\n'+traceback.format_exc())
			raise

	def cb_fill_results_export(self,change):
		'''User hit button to make download link'''
		self.debug()

		try:
			if self.model.res_count > 0:
				self.view.export_msg(self.view.CREATING_LINK)
				self.model.write_results() # creates csv string, stored in model
				self.view.export_link()
			else:
				self.view.export_msg(self.view.NO_RECS_AVAIL)
		except:
			self.debug('EXCEPTION\n'+traceback.format_exc())
			raise

	def cb_plot_type_selected(self,change):
		'''User selected plot option'''
		self.debug()

		try:
			choice = change['owner'].value

			if not choice == self.view.EMPTY:
				self.view.draw_plot(choice)
		except:
			self.debug('EXCEPTION\n'+traceback.format_exc())
			raise

	def debug(self,text=None):
		'''Log info for debugging during development or maintenence'''

		if self.debugging:

			if not text:
				text = '()' # Caller just registering progress

			caller = getframeinfo(stack()[1][0])
			caller = caller.filename.split('/')[-1] + ':' + str(caller.lineno)
			self.debug_buffer.append(caller + ': ' + text)

			if self.display_ready:

				for line in self.debug_buffer:
					self.view.debug(line)

				self.debug_buffer = []



