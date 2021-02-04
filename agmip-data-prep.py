#!/usr/bin/env python3
# agmip-data-prep.py - Process data for AgMIP Explorer, rcampbel, Oct 2020

import os
import pickle
import sys

import pandas as pd

if __name__ == "__main__":
    # Read file provided on command line i
    df = pd.read_csv(sys.argv[1])

    # Save input file base name (w/o extentsion)
    base_name = os.path.splitext(sys.argv[1])[0]

    # Task #1: Convert data file to HDF5
    #
    ##df.to_hdf(base_name+'.hdf5', 'data', mode='w', format='table')
    #
    #store = pd.HDFStore(base_name+'.hdf5')
    #store.append('agmipex', df, index=False)
    #
    #store.create_table_index('agmipex', columns=['Model'], optlevel=9, kind='full')
    # store.close()

    # Task #2: Get unique field values for each model

    models = set(pd.unique(df.Model))
    uniques = {}  # Where: uniques[field] = <dict>[model]
    model_recs = {}  # Where: model_recs[model] = <df>

    # Get subsets of data for each model
    for model in models:
        series = df.Model == model
        model_recs[model] = df[series]

    # Get unique field values for each model - and for all models
    for field in ['Scenario', 'Year', 'Sector', 'Region', 'Indicator', 'Unit']:
        field_uniques = {}

        # Values for each model
        for model in models:

            a_list = pd.unique(model_recs[model][field])

            # Remove NaN's

            b_list = []

            for item in a_list:
                if not (isinstance(item, float) and str(item) == 'nan'):
                    b_list.append(item)

            field_uniques[model] = set(b_list)

        # Values for all models
        a_list = pd.unique(df[field])

        # Remove NaN's

        b_list = []

        for item in a_list:
            if not (isinstance(item, float) and str(item) == 'nan'):
                b_list.append(item)

        field_uniques[''] = set(b_list)

        uniques[field] = field_uniques

    # Save uniques to pickle file
    pickle.dump((models, uniques), open(base_name+'.p', 'wb'))
