try:
    from sets import Set
except ImportError:
    Set = set
# -*- coding: utf-8 -*-
import asterqueryutility as queryutility

def getFunctionName(config, func):
    aafschema = config.get('aafschema', '')
    return (aafschema and (aafschema + '.')) + func

def getSelectQuery(dss_function, inputTables, config):
    
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
            cquery = """SELECT * FROM {cfunction} (ON {inputInfo} {cpartitionBy} {corderBy} {carguments})""".format(cfunction=getFunctionName(config, cfunction),
                                                                      inputInfo=inputInfo,
                                                                      cpartitionBy=cpartitionBy,
                                                                      corderBy=corderBy,
                                                                      carguments=carguments)
            inputInfo = """({cquery})""".format(cquery=cquery)
        query = inputInfo + ';'
    return query
