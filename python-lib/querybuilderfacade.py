# -*- coding: utf-8 -*-
import asterqueryutility as queryutility
import cascadequerybuilder as cascadequery
import singlequerybuilder as singlequery
from connectioninfo import *
from inputtableinfo import *
from outputtableinfo import *

def getCascadedFunctionsQuery(dss_function, inputTable, outputTable):
    return cascadequery.getAsterQuery(dss_function, inputTable, outputTable)

def getSingleFunctionsQuery(dss_function, inputTable, outputTable):
    return singlequery.getAsterQuery(dss_function, inputTable, outputTable)

def getFunctionsQuery(dss_function, inputTable, outputTable):
    query = ""
    if 'cascaded_functions' in dss_function:
        query = getCascadedFunctionsQuery(dss_function, inputTable, outputTable)
    else:
        query = getSingleFunctionsQuery(dss_function, inputTable, outputTable)
    return query

def getQueryFromDatasetAndFunctionDef(project, inputname, outputname, dss_function):
    # input dataset
    inputconnectioninfo = connectioninfo(project,
                                         inputname if dss_function.get("hasInputTable", True) else ".")
    inputTable = inputtableinfo(inputconnectioninfo, dss_function)
    # output dataset
    outputconnectioninfo = connectioninfo(project, outputname)
    outputTable = outputtableinfo(outputconnectioninfo, dss_function)
    # return
    return getFunctionsQuery(dss_function, inputTable, outputTable)