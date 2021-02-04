# constants.py - Shared constants for SCSA
# rcampbel@purdue.edu - 2020-07-14

# Data field names
F_MOD = 'Model'
F_SCN = 'Scenario'
F_YER = 'Year'
F_SEC = 'Sector'
F_REG = 'Region'
F_IND = 'Indicator'
F_UNI = 'Unit'
F_VAL = 'Value'
FIELDS = [F_MOD, F_SCN, F_YER, F_SEC, F_REG, F_IND, F_UNI, F_VAL]

# For menu items
ALL = '(All)'
NONE_ITEM = '(none)'

# Plot types (for matplotlib)
PLOT_TYPE_LINE = 'line'
PLOT_TYPE_BAR = 'bar'
PLOT_TYPE_HIST = 'hist'
PLOT_TYPE_BOX = 'box'

# Plot "sets" - predefined plots configurations
PLOT_SET_CUSTOM = 'Custom'
PLOT_SET_1 = 'Values for Model by Year'
PLOT_SET_2 = 'Values for Scenario by Model'
PLOT_SET_3 = 'Harmonized to Model & Year'
PLOT_SET_OPTIONS = [PLOT_SET_CUSTOM, PLOT_SET_1, PLOT_SET_2, PLOT_SET_3]

# Pivot and interpolation (for pandas)
AGGF_SUM = 'sum'
AGGF_MEAN = 'mean'
AGGF_COUNT = 'count'
FILL_LINEAR = 'linear'
FILL_CUBIC = 'cubicspline'
FILL_PAD = 'pad (use most recent value)'

# Data download formats
FORMAT_EXT_CSV = '.csv'
FORMAT_EXT_JSON = '.json'
FORMAT_EXT_HTML = '.html'
FORMAT_EXT_EXCEL = '.xls'
FORMAT_EXT_HDF5 = '.h5'
FORMAT_EXT_PICKLE = '.pickle'

# Plot image download formats
FORMAT_EXT_PNG = '.png'
FORMAT_EXT_JPG = '.jpg'
FORMAT_EXT_PDF = '.pdf'
FORMAT_EXT_SVG = '.svg'

# Misc text
NO_DATA_AVAIL = '(No  data is available. Please select a data file.)'
NO_RECS_AVAIL = '(No results data is available. Please revise your data selection.)'
CREATING_LINK = 'Creating link...'
DOWNLOAD_DATA_NAME = 'AgMIP_Explorer_Data'
DOWNLOAD_PLOT_NAME = 'AgMIP_Explorer_Plot'
FILTER_PROG = 'Searching...'

# Selection (filtering) menus
REGS = [
    ('AME, Africa and Middle East', 'AME'),
    ('ANZ, Australia and New Zealand', 'ANZ'),
    ('AUT, Austria', 'AUT'),
    ('BEL, Belgium', 'BEL'),
    ('BGR, Bulgaria', 'BGR'),
    ('BRA, Brazil', 'BRA'),
    ('CAN, Canada', 'CAN'),
    ('CAZ, CAZ', 'CAZ'),
    ('CHA, Channel Islands', 'CHA'),
    ('CHN, China, mainland', 'CHN'),
    ('CYP, Cyprus', 'CYP'),
    ('CZE, Czechia', 'CZE'),
    ('DEU, Germany', 'DEU'),
    ('DNK, Denmark', 'DNK'),
    ('ESP, Spain', 'ESP'),
    ('EST, Estonia', 'EST'),
    ('EUE, European Union (EU28', 'EUE'),
    ('EUR, Western Europe', 'EUR'),
    ('FIN, Finland', 'FIN'),
    ('FRA, France', 'FRA'),
    ('FSU, Former Soviet Union', 'FSU'),
    ('GBR, United Kingdom of Great Britain and Northern Ireland', 'GBR'),
    ('GRC, Greece', 'GRC'),
    ('HRV, Croatia', 'HRV'),
    ('HUN, Hungary', 'HUN'),
    ('IND, India', 'IND'),
    ('IRL, Ireland', 'IRL'),
    ('ITA, Italy', 'ITA'),
    ('JPN, Japan', 'JPN'),
    ('LAM, LAM', 'LAM'),
    ('LTU, Lithuania', 'LTU'),
    ('LVA, Latvia', 'LVA'),
    ('MEA, MEA', 'MEA'),
    ('MEN, Middle East (incl Turkey', 'MEN'),
    ('MLT, Malta', 'MLT'),
    ('NAM, Namibia', 'NAM'),
    ('NEU, NEU', 'NEU'),
    ('NLD, Netherlands', 'NLD'),
    ('OAM, Other America (incl Brazil', 'OAM'),
    ('OAS, Other Asia', 'OAS'),
    ('OSA, Other South & Central Amer', 'OSA'),
    ('POL, Poland', 'POL'),
    ('PRT, Portugal', 'PRT'),
    ('REF, REF', 'REF'),
    ('ROU, Romania', 'ROU'),
    ('SAS, Southern Asia', 'SAS'),
    ('SEA, South-East Asia (incl Japan and Taiwan', 'SEA'),
    ('SSA, SVub-Saharan Africa', 'SSA'),
    ('SVK, SVlovakia', 'SVK'),
    ('SVN, Slovenia', 'SVN'),
    ('SWE, Sweden', 'SWE'),
    ('USA, United States of America', 'USA'),
    ('WLD, World', 'WLD')
]

INDS = [
    ('AREA, Area harvested', 'AREA'),
    ('ARIR, Area harvested - irrigated', 'ARIR'),
    ('ARRF, Area harvested - rainfed', 'ARRF'),
    ('CALI, p.c. color intake', 'CALI'),
    ('CALO, p.c. calorie availability', 'CALO'),
    ('CONS, Domestic use', 'CONS'),
    ('CTAX, Carbon tax level', 'CTAX'),
    ('ECH4, Total CH4 emissions', 'ECH4'),
    ('ECO2, Total CO2 emissions', 'ECO2'),
    ('EMIS, Total GHG emissions', 'EMIS'),
    ('EN2O, Total N2O emissions', 'EN2O'),
    ('EXPO, Exports', 'EXPO'),
    ('FDRY, Feed use dairy', 'FDRY'),
    ('FEED, Feed use', 'FEED'),
    ('FEEF, Feed conversion efficiency (endogenous)', 'FEEF'),
    ('FFSH, Feed fish sector', 'FFSH'),
    ('FNRM, Feed use non-ruminant', 'FNRM'),
    ('FOOD, Food use', 'FOOD'),
    ('FRTN, Fertiliser N', 'FRTN'),
    ('FRUM, Feed use ruminant meat', 'FRUM'),
    ('GDPT, Total GDP (MER)', 'GDPT'),
    ('IMPO, Imports', 'IMPO'),
    ('LAND, Land cover', 'LAND'),
    ('LYLD, Livestock yield (endogenous)', 'LYLD'),
    ('LYXO, Exogenous livestock yield trend', 'LYXO'),
    ('NETT, Net trade', 'NETT'),
    ('OTHU, Other use', 'OTHU'),
    ('POPT, Total population', 'POPT'),
    ('PROD, Production', 'PROD'),
    ('PROD_tons, PROD_tons', 'PROD_tons'),
    ('WATR, Water for irrigation', 'WATR'),
    ('XPRP, Real producer price/input price', 'XPRP'),
    ('XPRP_deflated, XPRP_deflated', 'XPRP_deflated'),
    ('XPRR, XPRR', 'XPRR'),
    ('XPRX, Real export price', 'XPRX'),
    ('YECC, Climate change shifter on crop yield', 'YECC'),
    ('YEXO, Exogenous crop yield', 'YEXO'),
    ('YIIR, Crop yield - irrigated', 'YIIR'),
    ('YILD, Crop yield', 'YILD'),
    ('YIRF, Crop yield - rainfed', 'YIRF'),
    ('YILD_endoTC, YILD_endoTC', 'YILD_endoTC'),
    ('YILD_tons, YILD_tons', 'YILD_tons')
]

SECS = [
    ('AGR, All agricultural products', 'AGR'),
    ('BCR, Burning - Crop Residues', 'BCR'),
    ('BSV, Burning - Savanna', 'BSV'),
    ('CAP, Capital', 'CAP'),
    ('CGR, Other cereal grains', 'CGR'),
    ('CRP, All crops', 'CRP'),
    ('CR5, Cereal aggregate', 'CR5'),
    ('CRS, Crop Residues', 'CRS'),
    ('DRY, Dairy (raw milk equivalent)', 'DRY'),
    ('ECP, Energy crops', 'ECP'),
    ('EGG, Eggs', 'EGG'),
    ('ENT, Enteric Fermentation', 'ENT'),
    ('FOR, Forestry products', 'FOR'),
    ('FRS, Forestry products', 'FRS'),
    ('FRU, Fruits', 'FRU'),
    ('FSH, Fish', 'FSH'),
    ('GRS, Grass', 'GRS'),
    ('LAB, Labor', 'LAB'),
    ('LAM, LAM', 'LAM'),
    ('LSP, Livestock products', 'LSP'),
    ('MAS, Manure applied to Soils', 'MAS'),
    ('MGR, Manure left on Pasture', 'MGR'),
    ('MMG, Manure Management', 'MMG'),
    ('NLD, Non arable land (desert, built-up areas…)', 'NLD'),
    ('NRM, Non ruminant meats', 'NRM'),
    ('NRM|EGG, Poultry eggs', 'NRM|EGG'),
    ('NRM|ONR, Other non-ruminant', 'NRM|ONR'),
    ('NRM|PRK, Pork meat', 'NRM|PRK'),
    ('NRM|PTM, Poultry meat', 'NRM|PTM'),
    ('OAP, Other animal products (wool, honey)', 'OAP'),
    ('OCR, Other crops', 'OCR'),
    ('OFD, Other feed products', 'OFD'),
    ('OIL, Fossil fuel', 'OIL'),
    ('ONV, Other natural land', 'ONV'),
    ('OSD, Oilseeds (raw equivalent)', 'OSD'),
    ('PAS, Pasture', 'PAS'),
    ('PFB, Plant based fibres', 'PFB'),
    ('PTM, Poultry meat', 'PTM'),
    ('PRK, Pork meat', 'PRK'),
    ('RCC, Rice Cultivation', 'RCC'),
    ('RIC, Rice (paddy equivalent)', 'RIC'),
    ('RUM, Ruminant meats', 'RUM'),
    ('SFR, Synthetic Fertilizers', 'SFR'),
    ('SGC, Sugar crops (raw equivalent)', 'SGC'),
    ('TOT, Total (full economy, population, GDP, calories)', 'TOT'),
    ('URB, Urban', 'URB'),
    ('VEG, Vegetables', 'VEG'),
    ('VFN, Vegetables, fruits, nuts (incl. roots and tubers)', 'VFN'),
    ('VFN|FRU, Fruits', 'VFN|FRU'),
    ('VFN|NUT, Nuts', 'VFN|NUT'),
    ('VFN|VEG, Vegetables', 'VFN|VEG'),
    ('WHT, Wheat', 'WHT')
]
