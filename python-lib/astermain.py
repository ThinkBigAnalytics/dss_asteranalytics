# -*- coding: utf-8 -*-
'''
Copyright © 2018 by Teradata.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import dataiku
from dataiku.customrecipe import *
from dataiku import Dataset
from sets import Set
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
# Import the class that allows us to execute SQL on the Studio connections
from dataiku.core.sql import SQLExecutor2
# Import plugin libs
from querybuilderfacade import *
from inputtableinfo import *
from outputtableinfo import *
from outputtableinfo import *

def asterDo():
    # Recipe inputs
    main_input_name = get_input_names_for_role('main')[0]
    input_dataset = dataiku.Dataset(main_input_name)

    # Recipe outputs
    main_output_name = get_output_names_for_role('main')[0]
    output_dataset =  dataiku.Dataset(main_output_name)
    
    # Recipe function param
    dss_function = get_recipe_config().get('function', None)
    
    # Daitaiku DSS params
    client = dataiku.api_client()
    projectkey = main_input_name.split('.')[0]
    project = client.get_project(projectkey)

    try:
        # output dataset
        outputTable = outputtableinfo(output_dataset.get_location_info()['info'], main_output_name,
                                  get_recipe_config() or {})
    except Exception as error:
        raise RuntimeError("""Error obtaining connection settings for output table."""
                           """ Make sure connection setting is set to 'Read a database table'."""
                           """ This plugin only supports Aster tables.""")

    # input datasets
    try:
        main_input_names = get_input_names_for_role('main')
        inputTables = []
        for inputname in main_input_names:
            inconnectioninfo = dataiku.Dataset(inputname).get_location_info()['info']
            inTable = inputtableinfo(inconnectioninfo, inputname, dss_function)
            inputTables.append(inTable)
    except Exception as error:
        raise RuntimeError("""Error obtaining connection settings from one of the input tables."""
                           """ Make sure connection setting is set to 'Read a database table'."""
                           """ This plugin only supports Aster tables.""")
        
    # actual query
    query = getFunctionsQuery(dss_function, inputTables, outputTable)
    print('\n'.join(query))
    executor = SQLExecutor2(dataset=input_dataset)   
    if dss_function.get('dropIfExists', False):
        dropAllQuery = getDropOutputTableArgumentsStatements(dss_function.get('arguments', []))
        executor.query_to_df('END TRANSACTION;', dropAllQuery)
    executor.query_to_df("END TRANSACTION;", pre_queries=query)
    
    # write table schema
    nQuery = '''SELECT * FROM {} LIMIT (1);'''.format(outputTable.tablename)
    selectResult = executor.query_to_df(nQuery);
    output_schema = []
    for column in selectResult.columns:
        output_schema.append({"name":column, "type":"string"})
    output_dataset.write_schema(output_schema)
