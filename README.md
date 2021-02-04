# AgMIP Explorer
AgMIP Explorer ("agmipex") is a data exploration tool for [AgMIP](https://agmip.org/) based on the Self-Contained Science App (SCSA).

## Input Files

The tool allows the user to select from mutliple data files. These are stored in the `data` subdirectory. Note that data files must meet the requirements:

1. File must be in CSV (comma separated values) format.
2. File must contain an initial header line.
3. Columns must use the following spelling and order exactly: Model, Scenario, Region, Indicator, Sector, Unit, Year, Value
4. Data in each column must be of type string, except for the "Year" (numeric integer) and "Value" (numeric float) columns. 
 
Example:
```
Model,Scenario,Region,Indicator,Sector,Unit,Year,Value
"MOD","Scenario_1","REG","INDIC","SEC","million",2001,1.23456
...
```

## Development

### Code Structure
The AgMIP Explorer tool is a Jupyter notebook -based application. User interface widgets (menus, buttons, etc.) are created using [ipywidgets](https://ipywidgets.readthedocs.io/en/stable/). 

The tool runs the '''agmipex.ipynb''' notebooxk. However, instead of storing most of the code in notebook cells, the notebook references external Python code. So, the majority of logic resides in the Python files in the '''scripts''' subdirectory. The code follows the Model-View-Controller (MVC) pattern. That is, for simple organizational reasons, logic is split between the following:

- model.py: Data access
- view.py: User interface 
- controller.py: General program logic, plotting, and coordination between model and view

[Pandas](https://pandas.pydata.org/) is used for data access and [Matplotlib](https://matplotlib.org/) is used for plotting. 

### Environment

The tools is currently hosted on [MyGeoHub](https://www.mygeohub.org). MyGeoHub is a website based on [HUBzero](https://hubzero.org/). AgMIP Explorer is therefore a HUBzero "tool". As such, supplementary files are required. This enforces most of the directory structure of this repository. Also, it requires the '''invoke''' file in the '''middleware''' subdirectory.

### Building, developing, and testing

Use of an Anaconda envirnment is highly recommended. After creating and activating the conda environment (see '''environment.yml'''), run '''jupter notebook''' to start the notebook server. Then, use the local URLs displayed by that command to access and run the notebook using your browser. Note that during development, you can change code in the .py files and simply refresh the notebook to test changes. 

