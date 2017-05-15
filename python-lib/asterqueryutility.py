# -*- coding: utf-8 -*-
try:
    from sets import Set
except ImportError:
    Set = set
import re

def getJoinedArgumentsString(cargumentslist):
    
    regex = r",\s*(?=(?:[^']*\'[^']*\')*[^']*$)"
    
    carguments = ""
    for argument in cargumentslist:
        if 'value' in argument and argument['value']:
            if "COLUMNS" == argument["datatype"].upper() and argument.get("allowsLists", False):
                cargvalues = ", ".join("'" + astercolumn + "'" for astercolumn in argument["value"])
            else:
                cargvalues = ", ".join([re.sub(r"^'|'$", '', s) if (argument["datatype"].upper() == "SQLEXPR") else (s if (s[:1] == "'" and s[-1:] == "'") else ("'" + s + "'")) for s in re.split(regex, argument["value"])]) if argument.get("allowsLists", False) else ("'" + argument["value"] + "'")
            carguments += argument["name"].upper() + "(" + cargvalues + ")\n"
    return carguments