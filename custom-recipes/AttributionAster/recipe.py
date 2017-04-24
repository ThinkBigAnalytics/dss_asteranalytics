import dataiku
from dataiku.customrecipe import *
from dataiku import Dataset
from sets import Set

# -*- coding: utf-8 -*-
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import re

# Import the class that allows us to execute SQL on the Studio connections
from dataiku.core.sql import SQLExecutor2

# Recipe inputs
main_input_name = get_input_names_for_role('main')[0]
input_dataset =  dataiku.Dataset(main_input_name)
# Recipe outputs
main_output_name = get_output_names_for_role('main')[0]
output_dataset =  dataiku.Dataset(main_output_name)

executor = SQLExecutor2(dataset=input_dataset)

# output with selected function name, description and arguments


FUNCTION_NAME_COL = get_recipe_config().get('function', None)

        
partitionInputKind = FUNCTION_NAME_COL["partitionInputKind"]
hasInputTable = FUNCTION_NAME_COL.get("hasInputTable", True)
partitionKeys = ""
if not hasInputTable:
    partitionKeys = "1"
elif "PartitionByAny" in partitionInputKind:
    partitionKeys = "ANY"
elif "PartitionByKey" in partitionInputKind:
    partitionKeys = FUNCTION_NAME_COL["partitionAttributes"]
elif "PartitionByOne" in partitionInputKind:
    partitionKeys = "1"
    
partitionBy = "" if not partitionKeys else " ".join(["PARTITION BY", partitionKeys])
print("partitionInputKind: ")
print(partitionInputKind)
print("partition By: " + partitionBy)

#no empty string checking for orderByColumn since this is mandatory if isOrdered is true
orderBy = ""
if FUNCTION_NAME_COL["isOrdered"]:
    orderBy = " ".join(["ORDER BY", FUNCTION_NAME_COL["orderByColumn"]])



# Daitaiku DSS params
client = dataiku.api_client()
projectkey = main_input_name.split('.')[0]
project = client.get_project(projectkey)

#dataset params
input_name = main_input_name.split('.')[1]
inputdatasetconfig = next(i for i in project.list_datasets() if i['name'] == input_name)
inputdatasetconnectionparams = inputdatasetconfig['params']
inputdatasettable = inputdatasetconnectionparams['table']
inputdatasetschema = "" if 'schema' not in inputdatasetconnectionparams else inputdatasetconnectionparams['schema']

asterSchema = inputdatasetschema
if hasInputTable:
    inputTableName = inputdatasettable if not asterSchema else ".".join([asterSchema, inputdatasettable])
else:
    inputTableName = "(SELECT 1)"
# output with selected function name, description and arguments

arguments_list = ""
output = []
FUNCTION_NAME_COL = get_recipe_config().get('function', None)

print(FUNCTION_NAME_COL)

aster_args = {}
for argument in FUNCTION_NAME_COL["asterarguments"]:
    aster_args[argument["name"]] = argument["value"]
    
if not aster_args["schema"]:
    aster_args["schema"] = "public"

    
print(aster_args)

regex = r",\s*(?=(?:[^']*\'[^']*\')*[^']*$)"
#regex = r",\s*(?=(?:'[^']*?(?: [^']*)*))|,(?=[^',]+(?:,|$))\s*"
ar = []
for argument in FUNCTION_NAME_COL["arguments"]:
    print(argument)
    if argument["value"]:
        argvalues = ", ".join([re.sub(r"^'|'$", '', s) if (argument["datatype"].upper() == "SQLEXPR") else s if (s[:1] == "'" and s[-1:] == "'") else ("'" + s + "'") for s in re.split(regex, argument["value"])]) if argument.get("allowsLists", False) else ("'" + argument["value"] + "'")
        arguments_list += "         " + argument["name"].upper() + "(" + argvalues + ")\n"
        
output_table_type = aster_args["outputType"]
hash_column = aster_args["hashKey"]
schema = aster_args["schema"]
outputTableName = '.'.join([schema, main_output_name.split('.')[1]])
distributeBy = ""

if output_table_type == "FACT":
    distributeBy += """ DISTRIBUTE BY HASH({})
             """.format(hash_column)

query = """BEGIN TRANSACTION;
           DROP TABLE IF EXISTS {};
           CREATE {} TABLE {}{}
           AS 
           SELECT *
           FROM   {}
                  (
                    ON {}
           {}
           {}
           {}
                  ) 
        """.format(outputTableName,
                   output_table_type,
                   outputTableName,
                   distributeBy,
                   FUNCTION_NAME_COL["name"],
                   inputTableName,
                   partitionBy,
                   orderBy,
                   arguments_list)     
       
query +=""";
           COMMIT;
           END TRANSACTION;
        """   
        
executor.query_to_df(query)

print(output)        
print(FUNCTION_NAME_COL["arguments"])
print(arguments_list)
print(query)

nQuery = """SELECT * FROM {} LIMIT (1);""".format(outputTableName)
selectResult = executor.query_to_df(nQuery);
output_schema = []
for column in selectResult.columns:
    output_schema.append({"name":column, "type":"string"})
output_dataset.write_schema(output_schema)
