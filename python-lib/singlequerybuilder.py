from _ast import If
try:
    from sets import Set
except ImportError:
    Set = set
# -*- coding: utf-8 -*-
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
            
def getSelectQuery(dss_function, inputTables):
    jsonfile= queryutility.getJson(dss_function.get('name',''))
    return SELECT_QUERY.format(dss_function.get('name', ''),
                       getOnClause(dss_function, jsonfile, inputTables),
                       getArgumentClauses(dss_function, jsonfile, inputTables))
