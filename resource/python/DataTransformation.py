import dataiku
from dataiku import os
import json
import os
import logging

FUNCTION_CATEGORY="Data Transformation"

# paylaod is sent from the javascript's callPythonDo()
# config and plugin_config are the recipe/dataset and plugin configured values
# inputs is the list of input roles (in case of a recipe)
def do(payload, config, plugin_config, inputs):
    map = json.loads(open('%s/mapping.json' % (os.getenv("DKU_CUSTOM_RESOURCE_FOLDER"))).read())
    files = [function["file_name"] for function in map if function["category"] == config['category']]
    
    choices = []
    for fle in files:
        try:
            aster_args = json.loads(open('%s/%s' % (os.getenv("DKU_CUSTOM_RESOURCE_FOLDER"), "asterarguments.json")).read())
            f = json.loads(open('%s/data/%s' % (os.getenv("DKU_CUSTOM_RESOURCE_FOLDER"), fle)).read())
            d = {"name":"",
                 "arguments":"",
                 "asterarguments":"",
                 "partitionInputKind":"None",
                 "partitionAttributes":"",
                 "isOrdered":False,
                 "orderByColumn":"",
                 "hasInputTable":False
                }
            keys = f.keys()
            required_input = []
            if 'function_name' in keys:
                d["name"]=f['function_name'].upper()
            if 'input_tables' in keys:
                d["hasInputTable"] = True
                partitionKeys=[]
                input_tab_lst = f['input_tables']
                for input_tab in input_tab_lst:
                    required_input_dict = {"isRequired": True, "partitionAttributes":"", "orderByColumn": ""}
                    if 'isRequired' in input_tab.keys():
                        required_input_dict['isRequired'] = input_tab['isRequired']
                    if 'requiredInputKind' in input_tab.keys():
                        partitionByKey = input_tab['requiredInputKind'][0]
                        if 'partitionByOne' in input_tab.keys() and input_tab['partitionByOne']:
                            partitionByKey = "PartitionByOne"
                        partitionKeys.append(partitionByKey)
                        required_input_dict['kind'] = partitionByKey
                    if 'isOrdered' in input_tab.keys():
                        d["isOrdered"] = input_tab['isOrdered']
                        required_input_dict['isOrdered'] = input_tab['isOrdered']
                    if 'name' in input_tab.keys():
                        required_input_dict['name'] = input_tab['name']
                        required_input_dict['value'] = ""
                    required_input.append(required_input_dict)
                d["partitionInputKind"]=partitionKeys
            d["required_input"] = required_input
            if 'argument_clauses' in keys:
                a = []
                arg_lst = f['argument_clauses']
                for argument in arg_lst:
                    arg = {"name":"","isRequired":"","value":"", "datatype": "", "allowsLists":True}
                    if 'alternateNames' in argument.keys():
                        arg["name"]=argument['alternateNames'][0].upper()
                    elif 'name' in argument.keys():
                        arg["name"]=argument['name'].upper()  
                    if 'isRequired' in argument.keys():
                        arg["isRequired"]=argument['isRequired']
                    if 'datatype' in argument.keys():
                        arg["datatype"]=argument['datatype']
                    if 'allowsLists' in argument.keys():
                        arg["allowsLists"]=argument['allowsLists']
                    if 'targetTable' in argument.keys():
                        arg["targetTable"] = argument['targetTable']
                        
                    a.append(arg)
                d["arguments"]=a
            if 'cascaded_functions' in keys:
                d["cascaded_functions"] = f['cascaded_functions']
            aster_arg_list = []
            for argument in aster_args:
                aster_arg = {"name":"","label":"","value":""}
                aster_arg["name"] = argument["name"]
                aster_arg["label"] = argument["label"]                
                aster_arg_list.append(aster_arg)
            d["asterarguments"] = aster_arg_list
            
            choices.append(d);
        except ValueError, e:
            logging.info("file is not valid json");

    # Get input table metadata.
    
    input_table_name = inputs[0]['fullName'].split('.')[1]
    input_dataset =  dataiku.Dataset(input_table_name)
    schema = input_dataset.read_schema()
    
    inputschemas = {}
    for inputdataset in inputs:
        inputtablename = inputdataset['fullName'].split('.')[1]
        inputdataset = dataiku.Dataset(inputtablename)
        inputschemas[inputtablename] = inputdataset.read_schema()
        

    return {'choices' : choices, 'schema': schema, 'inputs': inputs, 'inputschemas': inputschemas}