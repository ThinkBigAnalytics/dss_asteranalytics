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

from _ast import If
try:
    from sets import Set
except ImportError:
    Set = set
import asterqueryutility as queryutility
from pseudoconstantgetters import *


def getInputTableFromDatasets(datasetname, inputDatasets):
    return next(iter(x for x in inputDatasets if x.datasetname == datasetname), None)

def getUnaliasedInputOnClause(requiredinput, inputTables):
    table = getInputTableFromDatasets(requiredinput, inputTables)
    return UNALIASED_ON_CLAUSE.format(input_table=table.tablename,
               partitionKeys=table.partitionKey, orderKeys=table.orderKey and
               " ".join(["ORDER BY", table.orderKey])).rstrip() +\
               "\n" if table else ''
               
def getInputQueryOnClause(inputquery):
    return UNALIASED_QUERY_ON_CLAUSE.format(input_query=inputquery) +\
               "\n" if inputquery else ''

def getOrderByClause(inputdef):
    orderByColumn = inputdef.get('orderByColumn', '') if\
    inputdef.get('isOrdered', False) else ''
    return orderByColumn and ("ORDER BY " + orderByColumn)

def getAliasedInputONClause(input_, jsonfile, inputTables):
    table = getInputTableFromDatasets(input_.get('value', ''), inputTables)
    table.setPropertiesFromDef(input_)
    return ALIASED_ON_CLAUSE.format(input_table=table.tablename,
           input_name=table.alias and ('AS "' + table.alias + '"'),
           partitionKeys=table.partitionKey,
           orderKeys = table.orderKey and
               " ".join(["ORDER BY", table.orderKey])).rstrip() + "\n" if table else ''
           
def getMultipleAliasedInputsClause(dss_function, jsonfile, inputTables):
    aliasedinputs = [x for x in dss_function.get('required_input', []) if
                     x.get('name', '') and x.get('value', '')]
    return ''.join(map(lambda x: getAliasedInputONClause(x, jsonfile, inputTables), aliasedinputs))

def getMultipleUnaliasedInputsClause(dss_function, inputTables):
    isQueryMode = dss_function.get('isQueryMode', False)
    if isQueryMode:
        return ''.join(map(lambda x: getInputQueryOnClause(x),
             """{}""".format(dss_function.get('queries', '')).split(DELIMITER)))
    unaliasedinputsdict = dss_function.get('unaliased_inputs', {})
    unaliasedinputs = unaliasedinputsdict.get('values', [])
    return ''.join(map(lambda x: getUnaliasedInputOnClause(x, inputTables),
                       unaliasedinputs[:int(min(unaliasedinputsdict.get('count', 1),
                                                len(unaliasedinputs)))]))
    
def getArgumentClauses(dss_function, jsonfile, inputTables):
    return queryutility.getJoinedArgumentsString(dss_function.get('arguments', []),
                                                 queryutility.getArgumentClausesFromJson(jsonfile),
                                                 inputTables)

def getOnClause(dss_function, jsonfile, inputTables):
    return (getMultipleUnaliasedInputsClause(dss_function, inputTables) +
            getMultipleAliasedInputsClause(dss_function, jsonfile, inputTables)).strip() or\
            ON_SELECT_ONE_PARTITION_BY_ONE

def getFunctionName(config, dss_function):
    aafschema = config.get('aafschema', '')
    functionname = dss_function.get('name', '')
    return (aafschema and (aafschema + '.')) + functionname
            
def getSelectQuery(dss_function, inputTables, config):
    jsonfile= queryutility.getJson(dss_function.get('name',''))
    return SELECT_QUERY.format(getFunctionName(config, dss_function),
                       getOnClause(dss_function, jsonfile, inputTables),
                       getArgumentClauses(dss_function, jsonfile, inputTables))
