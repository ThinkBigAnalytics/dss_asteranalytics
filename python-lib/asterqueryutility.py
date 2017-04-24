# -*- coding: utf-8 -*-
from sets import Set
import re

def getJoinedArgumentsString(cargumentslist):
    
    regex = r",\s*(?=(?:[^']*\'[^']*\')*[^']*$)"
    
    carguments = ""
    for argument in cargumentslist:
        if argument['value']:
            cargvalues = ", ".join([re.sub(r"^'|'$", '', s) if (argument["datatype"].upper() == "SQLEXPR") else (s if (s[:1] == "'" and s[-1:] == "'") else ("'" + s + "'")) for s in re.split(regex, argument["value"])]) if argument.get("allowsLists", False) else ("'" + argument["value"] + "'")
            carguments += "         " + argument["name"].upper() + "(" + cargvalues + ")\n"
    return carguments