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

def getAliasClause(inputdef):
    return '' if 'Dimension' == inputdef.get('name') else\
        ('AS "' + inputdef.get('name', '') + '"')

def getAliasedInputONClause(requiredinput, inputTables):
    inputtable = getInputTableFromDatasets(requiredinput.get('value', ''), inputTables)
    return ALIASED_ON_CLAUSE.format(input_table=inputtable.tablename,
           input_name= getAliasClause(requiredinput),
           partitionKeys = getPartitionKind(requiredinput.get('kind','')),
           orderKeys = getOrderByClause(requiredinput)).rstrip() + "\n" if inputtable else ''
           
def getMultipleAliasedInputsClause(dss_function, inputTables):
    aliasedinputs = [x for x in dss_function.get('required_input', []) if
                     x.get('name', '') and x.get('value', '')]
    return ''.join(map(lambda x: getAliasedInputONClause(x, inputTables), aliasedinputs))

def getMultipleUnaliasedInputsClause(dss_function, inputTables):
    unaliasedinputsdict = dss_function.get('unaliased_inputs', {})
    unaliasedinputs = unaliasedinputsdict.get('values', [])
    return ''.join(map(lambda x: getUnaliasedInputOnClause(x, inputTables),
                       unaliasedinputs[:int(min(unaliasedinputsdict.get('count', 1),
                                                len(unaliasedinputs)))]))
    
def getArgumentClauses(dss_function, inputTables):
    return queryutility.getJoinedArgumentsString(dss_function.get('arguments', []),
                                                 queryutility.getArgumentClausesFromJson(
                                                     queryutility.getJson(dss_function.get('name',''))),
                                                 inputTables)

def getOnClause(dss_function, inputTables):
    return (getMultipleUnaliasedInputsClause(dss_function, inputTables) +
            getMultipleAliasedInputsClause(dss_function, inputTables)).strip() or\
            ON_SELECT_ONE_PARTITION_BY_ONE
            
def getSelectQuery(dss_function, inputTables):
    return SELECT_QUERY.format(dss_function.get('name', ''),
                       getOnClause(dss_function, inputTables),
                       getArgumentClauses(dss_function, inputTables))


