# -*- coding: utf-8 -*-
try:
    from sets import Set
except ImportError:
    Set = set
import re
import json


def getTableNameFromArgument(argumentValue, inputTables):
    return next("'" + getTableNameFromTable(x) + "'" for x in inputTables if argumentValue == x.datasetname)

def getTableNameFromTable(inputTable):
    return inputTable.tablenamewithoutschema if 'public' == inputTable.schemaname else '.'.join([inputTable.schemaname, inputTable.tablenamewithoutschema])

def getJoinedArgumentsString(cargumentslist, arg_dict, inputTables=[]):
    regex = r",\s*(?=(?:[^']*\'[^']*\')*[^']*$)"
    
    carguments = ""
    for argument in cargumentslist:
        if "BOOLEAN" == argument.get('datatype','').upper():
            argument_filtered = [x for x in arg_dict if argument.get('name','').upper() == x.get('name','').upper() or argument.get('name','').upper() in [y.upper() for y in x.get('alternateNames', [])]]
            argumentdef = {}
            
            if 0 < len(argument_filtered):
                argumentdef = argument_filtered[0]
            if argument.get('value','') or argumentdef.get('defaultValue',False):
                carguments += argument["name"].upper() + "(" + """'{}'""".format(bool(argument.get('value', ""))) + ")\n"
        elif 'value' in argument and argument['value']:
            if ("COLUMNS" == argument["datatype"].upper() or "COLUMN_NAMES" == argument.get('datatype', '').upper()) and argument.get("allowsLists", False):
                cargvalues = ", ".join("'" + astercolumn + "'" for astercolumn in argument["value"])
            elif 'TABLE_NAME' == argument['datatype'] and not argument.get('allowsLists', False) and not argument.get('isOutputTable', False):
                cargvalues = getTableNameFromArgument(argument.get('value', ""), inputTables)
            else:
                cargvalues = ", ".join([re.sub(r"^'|'$", '', s) if (argument["datatype"].upper() == "SQLEXPR") else (s if (s[:1] == "'" and s[-1:] == "'") else ("'" + s + "'")) for s in re.split(regex, argument["value"])]) if argument.get("allowsLists", False) else ("""'{}'""".format(argument.get('value', "")))
            carguments += argument["name"].upper() + "(" + cargvalues + ")\n"
    return carguments

def getArgumentClausesFromJson(f):
    return f.get('argument_clauses',[])
try:
    from dataiku.customrecipe import *
    def getJson(function_name):
        return json.loads(open('%s/data/%s' % (get_recipe_resource(), function_name + '.json')).read())
except ImportError:
    def getJson(function_name):
        return json.loads(open('%s/data/%s' % ('../resource', function_name + '.json')).read())