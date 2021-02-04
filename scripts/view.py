# view.py - User interface for scsa notebook
# rcampbel@purdue.edu - 2020-07-14

import ipywidgets as ui
from IPython.core.display import display
from IPython.display import FileLink

from scripts.constants import *


def section(title, contents):
    """Create a collapsible widget container"""

    if type(contents) == str:
        contents = [ui.HTML(value=contents)]

    ret = ui.Accordion(children=tuple([ui.VBox(contents)]))
    ret.set_title(0, title)
    return ret


class View:
    TAB_TITLES = ['Welcome', 'Data', 'Selection', 'Visualize']
    EMPTY_LIST_MSG = "(There's no data to display.)"
    ALL_LBLVAL = (ALL, ALL)
    EMPTY = ''
    DATA_NONE = '(No data loaded.)'
    DATA_LOAD = 'Loading data...\nThis might take a few moments.'
    DATA_INTRO = 'Here is an overview of the current full dataset:'
    USING_TITLE = 'Using This App'
    USING_TEXT = '''<p>
    First, in the <b>Data</b> tab above, select and review a dataset.
    Next, go to the <b>Selection</b> tab to search for and download data of interest.
    After selecting your data, create and download plots in the <b>Visualize</b> tab.
    </p>'''
    SOURCES_TITLE = 'Notes'
    SOURCES_TEXT = '''<p>
    <b>AgMIP</b>
    </p><p>
    <a href="https://agmip.org/" target="_blank">Agricultural Model Intercomparison and Improvement Project </a>
    </p><p>
    This tool is based on the Self-Contained Science App.
    </p>'''
    SECTION_TITLE = 'Data'
    DATA_SOURCE_TITLE = 'Source'
    DDN_PROMPT = 'Please select a data file:'
    DATA_OVERVIEW_TITLE = 'Overview'
    DATA_COVERAGE_TITLE = 'Coverage'
    SEL_INST = 'Select values for query. Use Ctrl (Cmd) key while selecting additional values. Use Shift key to ' \
               'select a range of values. '
    CRITERIA_TITLE = 'Data Selection'
    CRITERIA_APPLY = 'Search'
    OUTPUT_TITLE = 'Results'
    OUTPUT_PRE = 'Limit display to '
    OUTPUT_POST = 'lines'
    EXPORT_BULK_TITLE = 'Export Entire Dataset'
    EXPORT_RESULTS_TITLE = 'Export All Results'
    EXPORT_PLOT_TITLE = 'Export Plot Image'
    EXPORT_BUTTON = 'Create Download '
    EXPORT_LINK_PROMPT = "Click here to save file: "

    PLOT_STATUS_TEMPLATE = """
    <p>NOTE: The plots below will use your most recent query results from the Selection tab.</p>
    <p>Your query, "%s", returned <b>%s</b> records.</p>
    """
    SUMM_PLOT_OPTIONS = ['Values for Model(s) by Scenario', 'Values for Model(s) by Sector',
                         'Values for Model(s) by Region']
    PLOT_PLOT_LABEL = 'Plot:'
    PLOT_NOTE_TITLE = 'Plot Data'
    PLOT_ERROR_MSG = 'ERROR - Cannot generate plot using current options.'
    PLOT_TYPES = [('Line', PLOT_TYPE_LINE), ('Bar', PLOT_TYPE_BAR),
                  ('Histogram', PLOT_TYPE_HIST), ('Box', PLOT_TYPE_BOX)]
    PLOT_TITLE = 'Create Plot'
    PLOT_X_LABEL = 'X Axis:'
    PLOT_Y_LABEL = 'Y Axis:'
    PLOT_TYPE_LABEL = 'Plot Type:'
    PLOT_PIVOT_LABEL = 'Pivot on Field:'
    PLOT_AGGFUNC_LABEL = 'Pivot Aggregation:'
    PLOT_FILL_LABEL = 'Fill missing:'
    PLOT_AGGFUNC_OPTIONS = [AGGF_SUM,
                            AGGF_MEAN,
                            AGGF_COUNT]
    PLOT_FILL_OPTIONS = [(NONE_ITEM, NONE_ITEM),
                         ('Linear Interpolation', FILL_LINEAR),
                         ('Cubic Spline Interpolation', FILL_CUBIC),
                         ('Pad', FILL_PAD)]
    PLOT_HARM_ROW_LABEL = 'Harmonize Row:'
    PLOT_HARM_COL_LABEL = 'Harmonize Column:'
    PLOT_INDEX_LABEL = 'Index:'
    PLOT_GENERATE_LABEL = 'Update Plot'
    PIVOT_TITLE = 'Plot Data'

    DOWNLOAD_DATA_FORMAT_LABEL = 'File Format:'
    DOWNLOAD_DATA_FORMAT_OPTIONS = [
        ('CSV, Comma Separated (.csv)', FORMAT_EXT_CSV),
        ('JSON (.json)', FORMAT_EXT_JSON),
        ('HTML (.html)', FORMAT_EXT_HTML),
        ('Excel (.xls)', FORMAT_EXT_EXCEL),
        ('HDF5 (.h5)', FORMAT_EXT_HDF5),
        ('Pickle, Python (.pickle)', FORMAT_EXT_PICKLE)]

    DOWNLOAD_PLOT_FORMAT_LABEL = 'Image Format:'
    DOWNLOAD_PLOT_FORMAT_OPTIONS = [
        ('Portable Network Graphics (.png)', FORMAT_EXT_PNG),
        ('Scalable Vector Graphics (.svg)', FORMAT_EXT_SVG),
        ('Portable Document Format (.pdf)', FORMAT_EXT_PDF),
        ('JPEG (.jpg)', FORMAT_EXT_JPG)]

    LO10 = ui.Layout(width='10%')
    LO15 = ui.Layout(width='15%')
    LO20 = ui.Layout(width='20%')
    LO25 = ui.Layout(width='25%')
    LOSEL = ui.Layout(width='33%')

    DATA_PRESENT_INDICATOR = '&#x2588'
    DATA_ABSENT_INDICATOR = '&#x2591'

    DATA_PRESENT_DESC = '&nbsp;Data contains records with model and field value'
    DATA_ABSENT_DESC = '&nbsp;No records exist for given model and field value'

    def __init__(self):
        # MVC objects
        self.model = None
        self.ctrl = None

        # User interface widgets

        # General
        self.tabs = None  # Main UI container
        self.debug_output = None

        # Data source, overview, download, and coverage
        self.data_ddn_src = None
        self.desc_output = None
        self.cover_output = None
        self.data_btn_refexp = None
        self.data_out_export = None
        self.data_ddn_format = None

        # Data selection ("filter") widgets
        self.filter_mod = None
        self.filter_scn = None
        self.filter_yrs = None
        self.filter_sec = None
        self.filter_ind = None
        self.filter_reg = None
        self.filter_btn_apply = None
        self.filter_ddn_ndisp = None
        self.filter_output = None
        self.filter_btn_refexp = None
        self.filter_out_export = None
        self.filter_nrec_output = None
        self.filter_ddn_format = None

        # Visualization (plots)
        self.plot_note_html = None
        self.viz_ddn_plot_type = None
        self.viz_ddn_plot_xaxis = None
        self.viz_ddn_plot_yaxis = None
        self.viz_out_plot_output = None
        self.viz_ddn_plot_pivot = None
        self.viz_ddn_plot_aggfunc = None
        self.viz_btn_plot_generate = None
        self.viz_ddn_plot_fill = None
        self.viz_ddn_plot_set = None
        self.viz_out_plot_data = None
        self.viz_ddn_plot_harm_row = None
        self.viz_ddn_plot_harm_col = None
        self.viz_btn_plot_refexp = None
        self.viz_out_plot_export = None
        self.viz_ddn_plot_format = None
        self.viz_ckb_plot_index = None

    def intro(self, model, ctrl):
        """Introduce MVC modules to each other"""
        self.ctrl = ctrl
        self.model = model

    def display(self, display_log):
        """Build and show notebook user interface"""
        self.build()

        if display_log:
            self.debug_output = ui.Output(layout={'border': '1px solid black'})

            # noinspection PyTypeChecker
            display(ui.VBox([self.tabs, section('Log', [self.debug_output])]))
        else:
            display(self.tabs)

    def debug(self, text):
        with self.debug_output:
            print(text)

    def build(self):
        """Create user interface"""
        self.tabs = ui.Tab()

        # Set title for each tab
        for i in range(len(self.TAB_TITLES)):
            self.tabs.set_title(i, self.TAB_TITLES[i])

        # Build content (widgets) for each tab
        tab_content = [self.welcome(), self.data(), self.selection(), self.visualize()]

        # Fill with content
        self.tabs.children = tuple(tab_content)

        # Initialize plotter
        self.ctrl.empty_plot()

    def welcome(self):
        """Create widgets for introductory tab content"""
        content = [section(self.USING_TITLE, self.USING_TEXT), section(self.SOURCES_TITLE, self.SOURCES_TEXT)]

        return ui.VBox(content)

    def data(self):
        """Create widgets for data tab content"""
        self.data_ddn_src = ui.Dropdown(options=self.model.get_data_options(), value=None)
        self.desc_output = ui.Output(layout={'border': '1px solid black'})
        self.cover_output = ui.Output(layout={'border': '1px solid black'})
        self.data_btn_refexp = ui.Button(description=self.EXPORT_BUTTON, icon='download', layout=self.LO20)
        self.data_out_export = ui.Output(layout={'border': '1px solid black'})
        self.data_ddn_format = ui.Dropdown(value=self.DOWNLOAD_DATA_FORMAT_OPTIONS[0][1],
                                           options=self.DOWNLOAD_DATA_FORMAT_OPTIONS, layout=self.LO25)

        self.update_data_status(self.DATA_NONE)

        content = []

        row = [ui.HTML(value=self.DDN_PROMPT), self.data_ddn_src]

        content.append(section(self.DATA_SOURCE_TITLE, [ui.HBox(row)]))
        content.append(section(self.DATA_OVERVIEW_TITLE, [ui.VBox([self.desc_output])]))
        content.append(section(self.DATA_COVERAGE_TITLE, [ui.VBox([self.cover_output])]))

        # Bulk download

        spacer = ui.Label(value='    ', layout=self.LO10)
        row = ui.HBox([ui.Label(value=self.DOWNLOAD_DATA_FORMAT_LABEL, layout=self.LO10),
                       self.data_ddn_format,
                       spacer,
                       self.data_btn_refexp])

        # TODO Remove temporary note and related lines from code below
        note = ui.Label(value='PLEASE NOTE: This feature is a work in progress. Downloads may time out.',
                        layout=ui.Layout(width='100%', display='flex', alight_items="left"))
        widgets = [ui.VBox([note, row, spacer, self.data_out_export])]
        sec = section(self.EXPORT_BULK_TITLE, widgets)
        sec.selected_index = None  # Collapse due to work-in-progress
        content.append(sec)

        return ui.VBox(content)

    def selection(self):
        """Create widgets for selection tab content"""
        # Create data selection widgets
        self.filter_mod = ui.SelectMultiple(options=[ALL], value=[ALL], rows=5, description=F_MOD,
                                            disabled=False, layout=self.LOSEL)
        self.filter_scn = ui.SelectMultiple(options=[ALL], value=[ALL], rows=5, description=F_SCN,
                                            disabled=False, layout=self.LOSEL)
        self.filter_yrs = ui.SelectMultiple(options=[ALL], value=[ALL], rows=5, description=F_YER,
                                            disabled=False, layout=self.LOSEL)

        self.filter_sec = ui.SelectMultiple(options=[self.ALL_LBLVAL] + SECS, value=[ALL], rows=10,
                                            description=F_SEC, disabled=False, layout=self.LOSEL)
        self.filter_ind = ui.SelectMultiple(options=[self.ALL_LBLVAL] + INDS, value=[ALL], rows=10,
                                            description=F_IND, disabled=False, layout=self.LOSEL)
        self.filter_reg = ui.SelectMultiple(options=[self.ALL_LBLVAL] + REGS, value=[ALL], rows=10,
                                            description=F_REG, disabled=False, layout=self.LOSEL)

        # Create other widgets
        self.filter_btn_apply = ui.Button(description=self.CRITERIA_APPLY, icon='search', layout=self.LO20)
        self.filter_ddn_ndisp = ui.Dropdown(options=['25', '50', '100', ALL], layout=self.LO10)
        self.filter_output = ui.Output()
        self.filter_btn_refexp = ui.Button(description=self.EXPORT_BUTTON, icon='download', layout=self.LO20)
        self.filter_out_export = ui.Output(layout={'border': '1px solid black'})
        self.filter_nrec_output = ui.HTML('')
        self.filter_ddn_format = ui.Dropdown(value=self.DOWNLOAD_DATA_FORMAT_OPTIONS[0][1],
                                             options=self.DOWNLOAD_DATA_FORMAT_OPTIONS, layout=self.LO25)

        content = []

        # Section: Selection criteria

        widgets = [
            (ui.HTML('<div style="text-align: left;">' + self.SEL_INST + '</div>')),
            ui.Label(value='', layout=ui.Layout(width='60%')),
            ui.HBox([
                self.filter_mod,
                self.filter_scn,
                self.filter_yrs]),
            ui.Label(value='', layout=ui.Layout(width='60%')),
            ui.HBox([
                self.filter_reg,
                self.filter_sec,
                self.filter_ind]),
            ui.Label(value='', layout=ui.Layout(width='60%')),
            self.filter_btn_apply
        ]

        content.append(section(self.CRITERIA_TITLE, widgets))

        # Section: Output (with apply button)

        widgets = []
        row = [self.filter_nrec_output,
               ui.HTML('</span><div style="text-align: right;">' + self.OUTPUT_PRE + '</div>', layout=self.LO15),
               self.filter_ddn_ndisp,
               ui.HTML('<div style="text-align: left;">' + self.OUTPUT_POST + '</div>', layout=self.LO10)]
        widgets.append(ui.HBox(row))

        widgets.append(ui.HBox([self.filter_output], layout={'width': '90vw'}))

        content.append(section(self.OUTPUT_TITLE, widgets))

        # Section: Export (download)

        spacer = ui.Label(value='    ', layout=self.LO10)
        row = ui.HBox([ui.Label(value=self.DOWNLOAD_DATA_FORMAT_LABEL, layout=self.LO10),
                       self.filter_ddn_format,
                       spacer,
                       self.filter_btn_refexp])

        widgets = [ui.VBox([row, spacer, self.filter_out_export])]
        content.append(section(self.EXPORT_RESULTS_TITLE, widgets))

        return ui.VBox(content)

    def visualize(self):
        """Create widgets for visualize tab content"""
        content = []

        # Note about data
        self.plot_note_html = ui.HTML(self.PLOT_STATUS_TEMPLATE % (NONE_ITEM, 0))
        content.append(section(self.PLOT_NOTE_TITLE, [self.plot_note_html]))

        # Plotting

        widgets = []

        label = ui.Label(value=self.PLOT_PLOT_LABEL, layout=ui.Layout(display="flex",
                                                                      justify_content="flex-start",
                                                                      width="5%"))
        self.viz_ddn_plot_set = ui.Dropdown(options=PLOT_SET_OPTIONS, layout=self.LO25)
        spacer = ui.Label(value='    ', layout=self.LO10)
        self.viz_btn_plot_generate = ui.Button(description=self.PLOT_GENERATE_LABEL, icon='line-chart', disabled=True,
                                               layout=ui.Layout(width='auto'))
        widgets.append(ui.HBox([label, self.viz_ddn_plot_set, spacer, self.viz_btn_plot_generate]))

        # Settings grid
        w1 = ui.Label(value=self.PLOT_TYPE_LABEL,
                      layout=ui.Layout(width='auto', grid_area='w1'))
        w2 = self.viz_ddn_plot_type = ui.Dropdown(options=self.PLOT_TYPES,
                                                  layout=ui.Layout(width='auto', grid_area='w2'))
        w3 = ui.Label(value=self.PLOT_X_LABEL,
                      layout=ui.Layout(width='auto', grid_area='w3'))
        w4 = self.viz_ddn_plot_xaxis = ui.Dropdown(options=FIELDS,
                                                   layout=ui.Layout(width='auto', grid_area='w4'))
        w5 = ui.Label(value=self.PLOT_Y_LABEL,
                      layout=ui.Layout(width='auto', grid_area='w5'))
        w6 = self.viz_ddn_plot_yaxis = ui.Dropdown(options=FIELDS,
                                                   layout=ui.Layout(width='auto', grid_area='w6'))
        w7 = ui.Label(value=self.PLOT_PIVOT_LABEL,
                      layout=ui.Layout(width='auto', grid_area='w7'))
        w8 = self.viz_ddn_plot_pivot = ui.Dropdown(options=FIELDS,
                                                   layout=ui.Layout(width='auto', grid_area='w8'))
        w9 = ui.Label(value=self.PLOT_AGGFUNC_LABEL,
                      layout=ui.Layout(width='auto', grid_area='w9'))
        w10 = self.viz_ddn_plot_aggfunc = ui.Dropdown(options=[NONE_ITEM] + self.PLOT_AGGFUNC_OPTIONS,
                                                      layout=ui.Layout(width='auto', grid_area='w10'))
        w11 = ui.Label(value=self.PLOT_FILL_LABEL,
                       layout=ui.Layout(width='auto', grid_area='w11'))
        w12 = self.viz_ddn_plot_fill = ui.Dropdown(options=self.PLOT_FILL_OPTIONS,
                                                   layout=ui.Layout(width='auto', grid_area='w12'))
        w13 = ui.Label(value=self.PLOT_INDEX_LABEL, layout=ui.Layout(width='auto', grid_area='w13'))
        w14 = self.viz_ckb_plot_index = ui.Checkbox(indent=False, layout=ui.Layout(width='auto', grid_area='w14'))
        w15 = ui.Label(value=self.PLOT_HARM_ROW_LABEL,
                       layout=ui.Layout(width='auto', grid_area='w15'))
        w16 = self.viz_ddn_plot_harm_row = ui.Dropdown(options=[NONE_ITEM],
                                                       disabled=True,
                                                       layout=ui.Layout(width='auto', grid_area='w16'))
        w17 = ui.Label(value=self.PLOT_HARM_COL_LABEL,
                       layout=ui.Layout(width='auto', grid_area='w17'))
        w18 = self.viz_ddn_plot_harm_col = ui.Dropdown(options=[NONE_ITEM],
                                                       disabled=True,
                                                       layout=ui.Layout(width='auto', grid_area='w18'))
        widgets.append(ui.GridBox(
            children=[w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18],
            layout=ui.Layout(
                width='100%',
                grid_template_rows='auto auto auto',
                grid_template_columns='auto auto auto auto auto auto',
                grid_template_areas='''"w3 w4 w7 w8 w15 w16"
                                       "w5 w6 w9 w10 w17 w18"
                                       "w1 w2 w11 w12 w13 w14"''')))

        self.viz_out_plot_output = ui.Output()
        widgets.append(self.viz_out_plot_output)

        content.append(section(self.PLOT_TITLE, widgets))

        # Pivot output
        self.viz_out_plot_data = ui.Output()
        sec = section(self.PIVOT_TITLE, [self.viz_out_plot_data])
        sec.selected_index = None
        content.append(sec)

        # Plot download
        self.viz_ddn_plot_format = ui.Dropdown(value=self.DOWNLOAD_PLOT_FORMAT_OPTIONS[0][1],
                                               options=self.DOWNLOAD_PLOT_FORMAT_OPTIONS, layout=self.LO25)
        self.viz_btn_plot_refexp = ui.Button(description=self.EXPORT_BUTTON, icon='download', layout=self.LO20)
        self.viz_out_plot_export = ui.Output(layout={'border': '1px solid black'})
        spacer = ui.Label(value='    ', layout=self.LO10)
        row = ui.HBox([ui.Label(value=self.DOWNLOAD_PLOT_FORMAT_LABEL, layout=self.LO10),
                       self.viz_ddn_plot_format,
                       spacer,
                       self.viz_btn_plot_refexp])
        widgets = [ui.VBox([row, spacer, self.viz_out_plot_export])]
        content.append(section(self.EXPORT_PLOT_TITLE, widgets))

        return ui.VBox(content)

    def set_harmonize(self, row_options=None, col_options=None, disable=False):
        """Update status and values of harmonize widgets"""
        self.viz_ddn_plot_harm_row.disabled = disable
        self.viz_ddn_plot_harm_col.disabled = disable
        self.viz_ddn_plot_harm_row.options = [NONE_ITEM]
        self.viz_ddn_plot_harm_col.options = [NONE_ITEM]

        if not disable:
            self.viz_ddn_plot_harm_row.options += row_options
            self.viz_ddn_plot_harm_col.options += col_options

    def update_data_status(self, content):
        """Change text in data overview section of data tab"""
        self.desc_output.clear_output(wait=True)

        with self.desc_output:

            if isinstance(content, str):
                # noinspection PyTypeChecker
                display(ui.HTML(content))
            else:
                # Content is dataframe, will show nice html summary
                self.model.set_disp(limit=10)
                display(content)

        # Display data coverage tables

        self.cover_output.clear_output(wait=True)

        html = '&nbsp;'

        if (not isinstance(content, str)) and self.model.valid:

            # First, initialize output by defining styles for table elements
            html = '''
                <style>
                    .vert {
                        writing-mode: vertical-rl;
                        transform: rotate(180deg);
                    }
                    .bot {
                        vertical-align: bottom;
                        line-height: 110%;
                    }
                </style>'''

            # Add legend - covers all tables
            html += '<div style="margin:20px">'
            html += '<p></p>'
            html += '<p>&nbsp;&nbsp;&nbsp;' + self.DATA_PRESENT_INDICATOR + self.DATA_PRESENT_DESC + '</p>'
            html += '<p>&nbsp;&nbsp;&nbsp;' + self.DATA_ABSENT_INDICATOR + self.DATA_ABSENT_DESC + '</p>'

            # One table for each field
            for field in FIELDS[1:-1]:  # ['Scenario', 'Year', 'Sector', 'Region', 'Indicator', 'Unit']:

                html += '<table line-height="110%"><tr><td><b>' + field + '</b>&nbsp;</td>'

                # Column headers: values for field
                for item in sorted(self.model.uniques[field]['']):

                    if not str(item).strip() == '':
                        html += '<td class="bot"><div class="vert"><span>&nbsp;' + str(item) + '</span></div></td>'

                html += '</tr>'

                # Rows: models
                for model in sorted(self.model.mods):
                    html += '<tr style="line-height:150%;"><td style="text-align:right;">' + model + '&nbsp;&nbsp' \
                                                                                                     ';&nbsp;</td> '
                    # Columns: data absent/present indicators
                    for item in self.model.uniques[field]['']:

                        if item in self.model.uniques[field][model]:
                            html += '<td>' + self.DATA_PRESENT_INDICATOR + '</td>'
                        else:
                            html += '<td>' + self.DATA_ABSENT_INDICATOR + '</td>'

                    html += '</tr>'

                html += '</table><br>'

            html += '</div>'

        with self.cover_output:
            # noinspection PyTypeChecker
            display(ui.HTML(html))

    def update_dynamic_selections(self):
        """Populate non-static selection option widgets based on new data"""

        self.filter_mod.options = [ALL] + sorted(list(self.model.mods))
        self.filter_scn.options = [ALL] + sorted(list(self.model.uniques[F_SCN]['']))
        self.filter_yrs.options = [ALL] + sorted(list(self.model.uniques[F_YER]['']))

        self.filter_mod.value = [ALL]
        self.filter_scn.value = [ALL]
        self.filter_yrs.value = [ALL]

    def model_selected(self, mods):
        """React to user changing a filter selection"""
        self.filter_scn.options = self.update_filter('Scenario', mods)

        if ALL in self.filter_scn.options:
            self.filter_scn.value = [ALL]

        # self.filter_yrs.options = self.update_filter('Year', mods)

        if ALL in self.filter_yrs.options:
            self.filter_yrs.value = [ALL]

    def update_filter(self, name, mods):
        """Adjust available filter items based on current selections"""
        self.ctrl.logger.debug('At')

        if mods == ():
            return []
        else:
            setlist = []

            for mod in mods:

                if mod == ALL:
                    setlist = [self.model.uniques[name]['']]
                    break

                setlist.append(self.model.uniques[name][mod])

            return [ALL] + sorted(list(set.intersection(*setlist)))

    def update_filtered_output(self):
        """Display new data in filtered output"""

        self.filter_nrec_output.value = 'Total: <b>' + format(self.model.res_row_count, ',') + '</b> records'

        if self.model.res_row_count < 1:
            self.output(self.EMPTY_LIST_MSG, self.filter_output)
        else:
            # Calc output line limit
            if self.filter_ddn_ndisp.value == ALL:
                limit = self.model.res_row_count
            else:
                limit = int(self.filter_ddn_ndisp.value)

            self.model.set_disp(limit=limit)
            self.output(self.model.results.head(limit), self.filter_output)

    def set_plot_status(self):
        """Change status of plot-related widgets based on availability of filter results"""
        self.ctrl.logger.debug('At')

        # Update plot note
        self.plot_note_html.value = self.PLOT_STATUS_TEMPLATE % (self.model.query,
                                                                 format(self.model.res_row_count, ','))
        if self.model.res_row_count > 0:
            self.viz_btn_plot_generate.disabled = False
        else:
            self.viz_btn_plot_generate.disabled = True
            self.ctrl.empty_plot()

        self.set_harmonize(disable=True)

    def export_msg(self, text, output):
        """Clear export output area then write text to it"""
        self.ctrl.logger.debug('At')
        output.clear_output()

        with output:
            # noinspection PyTypeChecker
            display(ui.HTML('<p>' + text + '</p>'))

    def export_link(self, filepath, output):
        """Create data URI link and add it to export output area"""
        self.ctrl.logger.debug('At')
        output.clear_output()

        link = FileLink(filepath, result_html_prefix=self.EXPORT_LINK_PROMPT)

        with output:
            # noinspection PyTypeChecker
            display(link)

    def output(self, content, widget):
        """Reset output area with contents (text or data)"""
        self.ctrl.logger.debug('At')
        widget.clear_output(wait=True)

        if isinstance(content, str):
            content = ui.HTML(content)

        with widget:
            display(content)
