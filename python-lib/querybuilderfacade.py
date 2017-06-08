# -*- coding: utf-8 -*-
import asterqueryutility as queryutility
import cascadequerybuilder as cascadequery
import singlequerybuilder as singlequery
from inputtableinfo import *
from outputtableinfo import *

def getCascadedFunctionsQuery(dss_function, inputTables, outputTable):
    return cascadequery.getAsterQuery(dss_function, inputTables, outputTable)

def getSingleFunctionsQuery(dss_function, inputTables, outputTable):
    return singlequery.getAsterQuery(dss_function, inputTables, outputTable)

def getFunctionsQuery(dss_function, inputTables, outputTable):
    if 'cascaded_functions' in dss_function:
        return getCascadedFunctionsQuery(dss_function, inputTables, outputTable)
    return getSingleFunctionsQuery(dss_function, inputTables, outputTable)

def getSelectClause(dss_function, inputTables):
    return '' if 'cascaded_functions' in \
        dss_function else singlequery.getSelectQuery(dss_function, inputTables)

