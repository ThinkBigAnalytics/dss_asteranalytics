# -*- coding: utf-8 -*-
import asterqueryutility as queryutility
import cascadequerybuilder as cascadequery
import singlequerybuilder as singlequery
from inputtableinfo import *
from outputtableinfo import *


def getSelectClause(dss_function, inputTables, config={}):
    return cascadequery.getSelectQuery(dss_function, inputTables, config)\
        if 'cascaded_functions' in \
        dss_function else singlequery.getSelectQuery(dss_function, inputTables, config)

def getCreateQuery(dss_function, inputTables, outputTable, config={}):
    return CREATE_QUERY.format(outputTable.tableType,
                       outputTable.tablename,
                       outputTable.hashKey and DISTRIBUTE_BY_HASH.format(outputTable.hashKey),
                       getSelectClause(dss_function, inputTables, config))

def getDropOutputTableArgumentsStatementFromMultipleArguments(arg):
    outputs = arg.get('value', '').split(',')
    return '\n'.join(DROP_QUERY.format(outputTableName=x)\
            for x in outputs)

def getDropOutputTableArgumentsStatements(args):
    return ['BEGIN TRANSACTION;'] + [DROP_QUERY.format(outputTablename=x.get('value', ''))\
            for x in args if x.get('isOutputTable', False) and not x.get('allowsLists', False)\
            and x.get('value','')] + [getDropOutputTableArgumentsStatementFromMultipleArguments(x)\
                                      for x in args if x.get('isOutputTable', False)\
                                      and x.get('allowsLists', False) and x.get('value', '')]\
                                       + ['COMMIT;']

def getBeginDropCreateQueries(dss_function, inputTables, outputTable, config):
     return [BEGIN_TRANSACTION_QUERY,
                    DROP_QUERY.format(outputTablename=outputTable.tablename),
                    getCreateQuery(dss_function, inputTables, outputTable, config),
                    COMMIT_QUERY]

def getFunctionsQuery(dss_function, inputTables, outputTable, config):
    return getBeginDropCreateQueries(dss_function, inputTables, outputTable, config)

