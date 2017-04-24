from dataiku import os
import json
import os
import logging

# paylaod is sent from the javascript's callPythonDo()
# config and plugin_config are the recipe/dataset and plugin configured values
# inputs is the list of input roles (in case of a recipe)
def do(payload, config, plugin_config, inputs):
    lst=os.listdir('%s/data/' % os.getenv("DKU_CUSTOM_RESOURCE_FOLDER"))
    choices = []
    try:
        f = json.loads(open('%s/data/%s' % (os.getenv("DKU_CUSTOM_RESOURCE_FOLDER"), "ngram.json")).read())
        d = {"name":"","description":"","arguments":""}
        keys = f.keys()
        if 'function_name' in keys:
            d["name"]=f['function_name']
        if 'long_description' in keys:
            d["description"]=f['long_description']
        if 'argument_clauses' in keys:
            a = []
            arg_lst = f['argument_clauses']
            for argument in arg_lst:
                arg = {"name":"","is_Required":"","desc":"","value":""}
                if 'alternateNames' in argument.keys():
                    arg["name"]=argument['alternateNames'][0]
                elif 'name' in argument.keys():
                    arg["name"]=argument['name']

                if 'isRequired' in argument.keys():
                    arg["is_Required"]=argument['isRequired']
                if 'description' in argument.keys():
                    arg["desc"]=argument['description']
                a.append(arg)
            d["arguments"]=a
        choices.append(d);
    except ValueError, e:
        logging.info("file is not valid json");
    return {'choices' : choices}