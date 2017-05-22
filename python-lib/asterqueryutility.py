# -*- coding: utf-8 -*-
try:
    from sets import Set
except ImportError:
    Set = set
import re

def getTableNameFromArgument(argumentValue, inputTables):
    return next("'" + x.schemaname + '.' + x.tablenamewithoutschema + "'" for x in inputTables if argumentValue == x.datasetname)

def getJoinedArgumentsString(cargumentslist, inputTables=[]):
    
    regex = r",\s*(?=(?:[^']*\'[^']*\')*[^']*$)"
    
    carguments = ""
    for argument in cargumentslist:
        if 'value' in argument and argument['value']:
            print('argument name: ' + argument['name'])
            print('argument value: ')
            print(argument.get('value', ''))
            if ("COLUMNS" == argument["datatype"].upper() or "COLUMN_NAMES" == argument.get('datatype', '').upper()) and argument.get("allowsLists", False):
                cargvalues = ", ".join("'" + astercolumn + "'" for astercolumn in argument["value"])
            elif 'TABLE_NAME' == argument['datatype'] and not argument.get('allowsLists', False) and not argument.get('isOutputTable', False):
                cargvalues = getTableNameFromArgument(argument.get('value', ""), inputTables)
            else:
                cargvalues = ", ".join([re.sub(r"^'|'$", '', s) if (argument["datatype"].upper() == "SQLEXPR") else (s if (s[:1] == "'" and s[-1:] == "'") else ("'" + s + "'")) for s in re.split(regex, argument["value"])]) if argument.get("allowsLists", False) else ("""'{}'""".format(argument.get('value', "")))
            carguments += argument["name"].upper() + "(" + cargvalues + ")\n"
    return carguments