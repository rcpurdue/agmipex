# view.py - User interface for datapub notebook
# rcampbel@purdue.edu - 2020-07-14

import sys
import ipywidgets as ui
import urllib
from scripts import plotter

class View:

	FILTER_PROG    = 'Searching...'
	EMPTY_LIST_MSG = '''<br>(There's no data to display.)'''
	ALL            = '(All)'
	EMPTY          = ''
	CREATING_LINK  = 'Creating link...'
	NO_RECS_AVAIL  = '(No records available.)'
	NOTE_TEXT_PRE  = 'The plot is based on results from the Selection tab.'

	LO10 = ui.Layout(width='10%')
	LO15 = ui.Layout(width='15%')
	LO20 = ui.Layout(width='20%')
	LO25 = ui.Layout(width='25%')

	def __init__(self):
		self.tabs	= None # Main UI container

	def intro(self,model,ctrl):
		'''Introduce MVC modules to each other'''
		self.model = model
		self.ctrl  = ctrl

	def display(self,debug=False):
		'''Build and show notebook user interface'''
		self.plotter = plotter.Plotter(self.model)
		self.build()

		if debug:
			self.debug_output = ui.Output(layout={'border': '1px solid black'})
			display(ui.VBox([self.tabs,self.section('Debug',[self.debug_output])]))
		else:
			display(self.tabs)

	def debug(self,text):
		with self.debug_output:
			print(text)

	def section(self,title,contents):
		'''Create a collapsible widget container'''

		if type(contents) == str:
			contents = [ui.HTML(value=contents)]

		ret = ui.Accordion(children=tuple([ui.VBox(contents)]))
		ret.set_title(0,title)
		return ret

	def build(self):
		'''Create user interface'''
		TITLES = ['Welcome','Data','Selection','Visualize']

		self.tabs = ui.Tab()

		# Set title for each tab
		for i in range(len(TITLES)):
			self.tabs.set_title(i,TITLES[i])

		# Build conent (widgets) for each tab
		tab_content = []
		tab_content.append(self.welcome())
		tab_content.append(self.data())
		tab_content.append(self.selection())
		tab_content.append(self.visualize())

		# Fill with content
		self.tabs.children = tuple(tab_content)

	def welcome(self):
		'''Create widgets for introductory tab content'''
		USING_TITLE = 'Using This App'
		USING_TEXT  = '''<p>
		In the <b>Data</b> tab above, you can review the dataset.
		Go to the <b>Selection</b> tab to search for and download data of interest.
		After selecting your data, create and download charts in the <b>Visualize</b> tab.
		</p>'''
		SOURCES_TITLE = 'Data Sources'
		SOURCES_TEXT  = '''<p>
		<b>AgMIP</b>
		</p><p>
		<a href="https://agmip.org/" target="_blank">Agricultural Model Intercomparison and Improvement Project </a>
		</p><p>
		This site is based on the MergedData.csv file retrieved on 2020-07-17.
		</p>'''

		content = []
		content.append(self.section(USING_TITLE  ,USING_TEXT  ))
		content.append(self.section(SOURCES_TITLE,SOURCES_TEXT))

		return ui.VBox(content)

	def data(self):
		'''Create widgets for data tab content'''
		SECTION_TITLE = 'Data'
		DATA_INTRO    = "Here's an overview of the current full dataset:"

		#content = []
        #
		##html = '<p>'+DATA_INTRO+'</p>'
        #
		## Set table format using CSS and start the HTML table
		#html += '''<style>
		#				.data_cell {padding-right: 32px	 }
		#				.data_even {background   : White	}
		#				.data_odd  {background   : Gainsboro}
		#			</style><table>'''
        #
		### Table column headers
		##for item in self.model.HEADERS:
		##	html += '<th class="data_cell">' + item + '</th>'
        #
		## Table items - alternate row background colors
		#for i,line in enumerate(self.model.describe_data()):
        #
		#	if i % 2 == 0:
		#		html += '<tr class="data_even">'
		#	else:
		#		html += '<tr class="data_odd">'
        #
		#	for item in line:
		#		html += '<td class="data_cell">' + item + '</td>'
        #
		#	html += '</tr>'
        #
		#html += '</table>'
        #
		#widgets = []
		#widgets.append(ui.HTML(value=html))
		#content.append(self.section(SECTION_TITLE,widgets)) # TODO Constant
        #
		#return ui.VBox(content)

		DATA_SECTION_TITLE = 'Data Overview'

		self.desc_output = ui.Output(layout={'border': '1px solid black'})

		with self.desc_output:
			print(DATA_INTRO)
			print()
			print(self.model.describe_data())
			print()
			print()

		return self.section(DATA_SECTION_TITLE,[ui.VBox([self.desc_output])])

	def selection(self):
		'''Create widgets for selection tab content'''
		CRITERIA_TITLE = 'Selection'
		CRITERIA_APPLY = 'Search'
		OUTPUT_TITLE   = 'Results'
		OUTPUT_PRE     = 'Limit display to '
		OUTPUT_POST    = 'lines'
		EXPORT_TITLE   = 'Export'
		EXPORT_BUTTON  = 'Create Download Link'

		MOD            = 'Model'
		SCN            = 'Scenario'
		REG            = 'Region'
		IND            = 'Indicator'
		SEC            = 'Sector'
		YEAR           = 'Year(s)'

		# Create data selection widgets
		self.filter_mod = ui.SelectMultiple(options=[self.ALL]+self.model.mods,value=[self.ALL],rows=5,description=MOD,disabled=False)
		self.filter_scn = ui.SelectMultiple(options=[self.ALL]+self.model.scns,value=[self.ALL],rows=5,description=SCN,disabled=False)
		self.filter_reg = ui.SelectMultiple(options=[self.ALL]+self.model.regs,value=[self.ALL],rows=5,description=REG,disabled=False)
		self.filter_ind = ui.SelectMultiple(options=[self.ALL]+self.model.inds,value=[self.ALL],rows=5,description=IND,disabled=False)
		self.filter_sec = ui.SelectMultiple(options=[self.ALL]+self.model.secs,value=[self.ALL],rows=5,description=SEC,disabled=False)

		self.filter_yr1 = ui.Dropdown(options=[self.ALL]+self.model.years,value=self.ALL,description=YEAR,disabled=False,layout=self.LO15)
		self.filter_yr2 = ui.Dropdown(options=[self.ALL]+self.model.years,value=self.ALL,description=''  ,disabled=False,layout=self.LO10)

		# Create other widgets
		self.filter_btn_apply   = ui.Button(description=CRITERIA_APPLY,icon='filter',layout=self.LO20)
		self.filter_ddn_ndisp   = ui.Dropdown(options=['25','50','100',self.ALL],layout=self.LO10)
		self.filter_html_output = ui.HTML(self.EMPTY_LIST_MSG)
		self.filter_btn_refexp  = ui.Button(description=EXPORT_BUTTON,icon='download',layout=self.LO20)
		self.filter_out_export  = ui.Output(layout={'border': '1px solid black'})
		self.filter_nrec_output = ui.HTML('')

		content = []

		# Section: Selection criteria

		widgets = []

		widgets.append(ui.HBox([
			self.filter_mod
			,self.filter_scn
			,self.filter_reg
		]))

		widgets.append(ui.HBox([
			self.filter_ind
			,self.filter_sec
		]))

		widgets.append(ui.HBox([
			self.filter_yr1
			,self.filter_yr2
		]))

		widgets.append(self.filter_btn_apply)

		content.append(self.section(CRITERIA_TITLE,widgets))

		# Section: Output (with apply button)

		widgets = []

		row = []
		row.append(self.filter_nrec_output)
		row.append(ui.HTML('</span><div style="text-align: right;">'+OUTPUT_PRE+'</div>',layout=self.LO15))
		row.append(self.filter_ddn_ndisp)
		row.append(ui.HTML('<div style="text-align: left;">' +OUTPUT_POST+'</div>',layout=self.LO10))
		widgets.append(ui.HBox(row))

		widgets.append(ui.HBox([self.filter_html_output],layout={'width':'90vw'}))

		content.append(self.section(OUTPUT_TITLE,widgets))

		# Section: Export (download)

		widgets = []
		widgets.append(ui.VBox([self.filter_btn_refexp,self.filter_out_export])) # TODO VBox required here?
		content.append(self.section(EXPORT_TITLE,widgets))

		return ui.VBox(content)

	def visualize(self):
		'''Create widgets for visualizea tab content'''
		NOTE_TITLE    = 'Note'
		PLOT_TITLE    = 'Plot'
		PLOT_LABEL    = 'Select data fields'

		content = []
		self.plot_note_html = ui.HTML(self.NOTE_TEXT_PRE)
		content.append(self.section(NOTE_TITLE,[self.plot_note_html]))

		self.viz_ddn_plot_type = ui.Dropdown(options=[self.EMPTY]+self.plotter.PLOT_OPTIONS,value=None,disabled=True)

		widgets = []

		row = []
		row.append(ui.HTML(value=PLOT_LABEL))
		row.append(ui.Label(value='',layout=ui.Layout(width='60%'))) # Cheat: spacer
		widgets.append(ui.HBox(row))

		widgets.append(self.viz_ddn_plot_type)
		widgets.append(self.plotter.fig) # Use widget from plotter
		content.append(self.section(PLOT_TITLE,widgets))

		return ui.VBox(content)

	def update_filtered_output(self):
		'''Display new data in filtered output'''

		self.filter_nrec_output.value = 'Total: <b>' + format(self.model.res_count,',') + '</b> records'

		if self.model.res_count < 1:
			self.filter_html_output.value = self.EMPTY_LIST_MSG
			return

		# Calc output line limit
		if self.filter_ddn_ndisp.value == self.ALL:
			limit = self.model.res_count
		else:
			limit = int(self.filter_ddn_ndisp.value)

		# CSS (style)
		output = '''<style>
					.op th {
						padding         : 3px;
						border          : 1px solid black;
						font-size       : 14px !important;
						text-align      : center;
						line-height     : 14px;
						background-color: lightgray;
					}
					.op td {
						padding         : 3px;
						border          : 1px solid black;
						font-size       : 14px !important;
						text-align      : left;
						line-height     : 14px;
					}
					</style>'''

		# Table start and header start
		output += '<br><table class="op" style="border-spacing: 0px !important; border-collapse: collapse !important;"><tr>'

		# Column headers
		for hdr in self.model.headers:
			output += '<th class="op">'+hdr+'</th>'

		output += '</tr>'

		# Build table rows

		for i,row in enumerate(self.model.iterate_results()):
			output += '<tr>'
			output += '<td class="op">'+str(row.Model    )+'</td>'
			output += '<td class="op">'+str(row.Scenario )+'</td>'
			output += '<td class="op">'+str(row.Region   )+'</td>'
			output += '<td class="op">'+str(row.Indicator)+'</td>'
			output += '<td class="op">'+str(row.Sector   )+'</td>'
			output += '<td class="op">'+str(row.Unit     )+'</td>'
			output += '<td class="op">'+str(row.Year     )+'</td>'
			output += '<td class="op">'+str(row.Value    )+'</td>'
			output += '</tr>'

			if i+1 == limit:
				break

		output += '</table>' # End table

		self.filter_html_output.value = output  # Update UI

	def set_plot_status(self):
		'''Change status of plot-related widgets based on availability of filter results'''
		self.ctrl.debug()

		if self.model.res_count > 0:
			self.viz_ddn_plot_type.disabled = False
			self.plotter.fig.layout.title   = self.plotter.PROMPT_TITLE
			self.plot_note_html.value       = '<p>'+self.NOTE_TEXT_PRE+'</p>' + '<p>Query: '+self.model.query+'</p>'
		else:
			self.viz_ddn_plot_type.disabled = True
			self.plotter.fig.layout.title   = self.plotter.INIT_TITLE
			self.plot_note_html.value       = '<p>'+self.NOTE_TEXT_PRE+'</p>' + '<p>'+self.NO_RECS_AVAIL+'</p>'

	def draw_plot(self,choice):
		'''Update plot'''
		self.ctrl.debug()

		# Send plot chhoice and data to plotter
		self.plotter.draw_plot(choice,self.model.results)

	def export_msg(self,text):
		'''Clear export output area then write text to it'''
		self.ctrl.debug()
		self.filter_out_export.clear_output()

		with self.filter_out_export:
			display(ui.HTML('<p>'+text+'</p>'))

	def export_link(self):
		'''Create data URI link and add it to export output area'''
		self.ctrl.debug()
		self.filter_out_export.clear_output()

		# Get human readable data size, see https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python

		size   = len(self.model.res_csv)
		suffix = ['B','KB','MB','GB','TB']
		index  = 0

		while size > 1024 and not suffix[index] == suffix[-1]:
			index += 1
			size   = size / 1024.0

		size_str = '%.0f %s' % (size,suffix[index])

		# Output an encoded data URI for given string

		pre  = '<a download="data.csv" target="_blank" href="data:text/csv;charset=utf-8,'
		post = '">Download ('+size_str+')</a>'

		with self.filter_out_export:
			display(ui.HTML(pre+urllib.parse.quote(self.model.res_csv)+post))
