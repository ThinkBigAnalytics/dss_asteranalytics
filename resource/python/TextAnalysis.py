import dataiku
from dataiku import os
import json
import os
import logging

FUNCTION_CATEGORY="Text Analysis"

# paylaod is sent from the javascript's callPythonDo()
# config and plugin_config are the recipe/dataset and plugin configured values
# inputs is the list of input roles (in case of a recipe)
def do(payload, config, plugin_config, inputs):
    map = json.loads(open('%s/mapping.json' % (os.getenv("DKU_CUSTOM_RESOURCE_FOLDER"))).read())
    files = [function["file_name"] for function in map if function["category"] == FUNCTION_CATEGORY]
    
    choices = []
    for fle in files:
        try:
            aster_args = json.loads(open('%s/%s' % (os.getenv("DKU_CUSTOM_RESOURCE_FOLDER"), "asterarguments.json")).read())
            f = json.loads(open('%s/data/%s' % (os.getenv("DKU_CUSTOM_RESOURCE_FOLDER"), fle)).read())
            d = {"name":"",
                 "description":"",
                 "arguments":"",
                 "asterarguments":"",
                 "partitionInputKind":"None",
                 "partitionAttributes":"",
                 "isOrdered":False,
                 "orderByColumn":""}
            keys = f.keys()
            if 'function_name' in keys:
                d["name"]=f['function_name'].upper()
            if 'long_description' in keys:
                d["description"]=f['long_description']
            if 'input_tables' in keys: 
                partitionKeys=[]
                input_tab_lst = f['input_tables']
                for input_tab in input_tab_lst:
                    if 'requiredInputKind' in input_tab.keys():
                        partitionByKey = input_tab['requiredInputKind'][0]
                        if 'partitionByOne' in input_tab.keys() and input_tab['partitionByOne']:
                            partitionByKey = "PartitionByOne"    
                        partitionKeys.append(partitionByKey)
                    if 'isOrdered' in input_tab.keys() and input_tab['isOrdered']:
                        d["isOrdered"] = input_tab['isOrdered']
                d["partitionInputKind"]=partitionKeys
            if 'argument_clauses' in keys:
                a = []
                arg_lst = f['argument_clauses']
                for argument in arg_lst:
                    arg = {"name":"","isRequired":"","desc":"","value":"", "datatype": ""}
                    if 'alternateNames' in argument.keys():
                        arg["name"]=argument['alternateNames'][0].upper()
                    elif 'name' in argument.keys():
                        arg["name"]=argument['name'].upper()
                        
                    if 'isRequired' in argument.keys():
                        arg["isRequired"]=argument['isRequired']
                    if 'description' in argument.keys():
                        arg["desc"]=argument['description']
                    if 'datatype' in argument.keys():
                        arg["datatype"]=argument['datatype']
                        
                    a.append(arg)
                d["arguments"]=a
            
            aster_arg_list = []
            for argument in aster_args:
                aster_arg = {"name":"","label":"","desc":"","value":""}
                aster_arg["name"] = argument["name"]
                aster_arg["label"] = argument["label"]                
                aster_arg["desc"] = argument["desc"]
                aster_arg_list.append(aster_arg)
            d["asterarguments"] = aster_arg_list
            
            choices.append(d);
        except ValueError, e:
            logging.info("file is not valid json");

    # Get input table metadata.
    input_table_name = inputs[0]['fullName'].split('.')[1]
    input_dataset =  dataiku.Dataset(input_table_name)
    schema = input_dataset.read_schema()

    return {'choices' : choices, 'schema': schema}