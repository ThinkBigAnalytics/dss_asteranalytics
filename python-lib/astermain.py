import dataiku
from dataiku.customrecipe import *
from dataiku import Dataset
from sets import Set
# -*- coding: utf-8 -*-
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
# Import the class that allows us to execute SQL on the Studio connections
from dataiku.core.sql import SQLExecutor2
# Import plugin libs
from querybuilderfacade import *
from inputtableinfo import *
from outputtableinfo import *
from outputtableinfo import *
from connectioninfo import *

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

    # output dataset
    outputTable = outputtableinfo(output_dataset.get_location_info()['info'], main_output_name,
                                  dss_function)

    # input datasets
    main_input_names = get_input_names_for_role('main')
    inputTables = []
    for inputname in main_input_names:
        inconnectioninfo = dataiku.Dataset(inputname).get_location_info()['info']
        inTable = inputtableinfo(inconnectioninfo, inputname, dss_function)
        inputTables.append(inTable)
        
    # actual query
    query = getFunctionsQuery(dss_function, inputTables, outputTable)
    executor = SQLExecutor2(dataset=input_dataset)                
    executor.query_to_df(query)
    print(query)
    
    # write table schema
    nQuery = """SELECT * FROM {} LIMIT (1);""".format(outputTable.tablename)
    selectResult = executor.query_to_df(nQuery);
    output_schema = []
    for column in selectResult.columns:
        output_schema.append({"name":column, "type":"string"})
    output_dataset.write_schema(output_schema)
