# plotter.py - plot code for view
# rcampbel@purdue.edu - 2020-07-14

import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from IPython.display import clear_output

import random # TODO remove testing code

class Plotter:
	PLOT_OPTIONS   = ['Values for Model(s) by Sector','(plot)','(plot)']
	PLOT_LIMIT     =  100
	INIT_TITLE     = '(No results.)'
	PROMPT_TITLE   = '(Please select plot type.)'
	UPDATE_TITLE   = 'Updating plot...'
	PREFIX_TITLE   = '(prefix title)'
	AXIS_TITLE_X   = 'Model'
	AXIS_TITLE_Y   = 'Value'
	GRID_COLOR	   = 'whitesmoke'
	BACKGROUND	   = 'white'

	def __init__(self,model):
		self.model = model
		init_notebook_mode(connected=False)
		data = []

		for i in range(self.PLOT_LIMIT):
			bar = go.Bar(
				x     = []
				,y    = []
				,name = ''
			)
			data.append(bar)

		self.fig = go.FigureWidget(
			data = data
			,layout = go.Layout(
				title  = self.INIT_TITLE
				,yaxis = dict(
					title	  = self.AXIS_TITLE_Y
					,showgrid  = True
					,gridcolor = self.GRID_COLOR
				)
				,xaxis = dict(
					title	   = self.AXIS_TITLE_X
					,showgrid  = True
					,gridcolor = self.GRID_COLOR
				)
				,plot_bgcolor = self.BACKGROUND  # TODO Still needed?
				,dragmode     = 'select'         # TODO Still needed?
				,barmode      = 'group'
			)
		)

#	var bar1 = {
#		x: ['giraffes', 'orangutans', 'monkeys'],  x    --> Model
#		y: [20, 14, 23],                           y    --> Value
#		name: 'SF Zoo',                            name --> Scenario
#		type: 'bar'
#	};
#
#	var bar2 = {
#		x: ['giraffes', 'orangutans', 'monkeys'],  x    --> Model
#		y: [12, 18, 29],                           y    --> Value
#		name: 'LA Zoo',                            name --> Scenario
#		type: 'bar'
#	};

#	var data = [trace1, trace2];

	def draw_plot(self,plot_type,results):
		'''Redraw plot based on new plot type and data'''
		self.fig.layout.title = self.UPDATE_TITLE
		self.model.sort(['Scenario','Model'])

		# Clear plot data
		for i in range(self.PLOT_LIMIT):
			self.fig.data[i].x    = []
			self.fig.data[i].y    = []
			self.fig.data[i].name = ''

		# Init loop state vars
		cur   = []
		latch = False
		bar   = 0
		total = 0.0
		x     = []
		y     = []

		for row in self.model.iterate_results():

			# First iteration?
			if not latch:
				latch = True
				cur   = row

			# Model or Scenario changed?
			if not  (row.Model    == cur.Model and \
					 row.Scenario == cur.Scenario ):

				# Record model and total value
				x.append(cur.Model)
				y.append(total)
				total = 0.0

				# Record scenario
				if not row.Scenario == cur.Scenario:
					self.fig.data[bar].x    = x
					self.fig.data[bar].y    = y
					self.fig.data[bar].name = cur.Scenario
					bar += 1
					x    = []
					y    = []

				cur = row

			total += row.Value

		# Finish final one
		if latch:
			x.append(cur.Model)
			y.append(total)
			self.fig.data[bar].x    = x
			self.fig.data[bar].y    = y
			self.fig.data[bar].name = cur.Scenario

		self.fig.layout.title = plot_type



