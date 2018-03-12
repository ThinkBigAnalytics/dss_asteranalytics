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

try:
    from sets import Set
except ImportError:
    Set = set
import asterqueryutility as queryutility

def getSelectQuery(dss_function, inputTables):
    
    # query, not yet supporting partition by and order by clauses from recipe settings,
    # but not needed for naiveBayes
    query = ""
    cascadedFunctions = dss_function['cascaded_functions']
    if 0 < len(cascadedFunctions):
        cquery = ""
        selectedInputTable = inputTables[0] if (0 == len(dss_function['unaliased_inputs']['values'])) else dss_function['unaliased_inputs']['values'][0]
        inputInfo = next(x.tablename for x in inputTables if x.datasetname == selectedInputTable)
        for fun in cascadedFunctions:
            cpartitionBy = ""
            if 'partitionBy' in fun:
                cpartitionByNode = fun['partitionBy']
                if not cpartitionByNode['isSetByUser']:
                    cpartitionBy = "PARTITION BY {}".format(cpartitionByNode['key'])
            corderBy = ""
            if 'orderBy' in fun:
                corderByNode = fun['orderBy']
                if not corderByNode['isSetByUser']:
                    corderBy = "ORDER BY {}".format(corderByNode['key'])
            carguments = ""
            jsonFunction = queryutility.getJson(fun.get('name',''))
            if 'arguments_clauses' in fun:
                cargumentslist = [n for n in dss_function['arguments'] if n.get('name',"").upper() in fun['arguments_clauses']]
                carguments += queryutility.getJoinedArgumentsString(cargumentslist,
                                                                    queryutility.getArgumentClausesFromJson(jsonFunction))
            if 'arguments_nonuserdefined' in fun:
                carguments += queryutility.getJoinedArgumentsString(fun['arguments_nonuserdefined'],
                                                                    queryutility.getArgumentClausesFromJson(jsonFunction))      
            cfunction = fun.get('name',"")
            cquery = """SELECT * FROM {cfunction} (ON {inputInfo} {cpartitionBy} {corderBy} {carguments})""".format(cfunction=cfunction,
                                                                      inputInfo=inputInfo,
                                                                      cpartitionBy=cpartitionBy,
                                                                      corderBy=corderBy,
                                                                      carguments=carguments)
            inputInfo = """({cquery})""".format(cquery=cquery)
        query = inputInfo + ';'
    return query
