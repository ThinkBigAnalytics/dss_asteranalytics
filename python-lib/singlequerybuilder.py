try:
    from sets import Set
except ImportError:
    Set = set
# -*- coding: utf-8 -*-
import asterqueryutility as queryutility

def getAsterQuery(dss_function, inputTables, outputTable):
    # query
    multiplealiasedinputs = ""
    multipleunaliasedinputs = ""
    onselect = ""
    inputTable = inputTables[0]
    
    
    if 'required_input' in dss_function:
        aliasedinputs = [x for x in dss_function['required_input'] if 'name' in x and 'value' in x and x['value']]
        for requiredinput in aliasedinputs:
            if 'value' in requiredinput and requiredinput["value"]:
                aliasedinputtableschema = next(x.schemaname for x in inputTables if x.datasetname == requiredinput['value'])
                inputkind = requiredinput['kind']
                partitionKeys = ""
                if 'Dimension' == inputkind:
                    partitionKeys = 'DIMENSION'
                elif "PartitionByAny" == inputkind:
                    partitionKeys = 'PARTITION BY ANY'
                elif "PartitionByKey" == inputkind:
                    partitionKeys = 'PARTITION BY ' + requiredinput['partitionAttributes']
                elif "PartitionByOne" == inputkind:
                    partitionKeys = 'PARTITION BY 1'
                else:
                    partitionKeys = ""
                    
                orderKeys = ""
                if requiredinput['isOrdered'] and requiredinput['orderByColumn']:
                    orderKeys = "ORDER BY " + requiredinput['orderByColumn']
                multiplealiasedinputs += '''ON {schema}.{input_table} AS "{input_name}" {partitionKeys} {orderKeys}'''.format(schema=aliasedinputtableschema,
                                                                                                                       input_table=requiredinput['value'],
                                                                                                                       input_name=requiredinput['name'],
                                                                                                                       partitionKeys=partitionKeys,
                                                                                                                       orderKeys=orderKeys).rstrip() + "\n"
    
    if 'unaliased_inputs' in dss_function and 'values' in dss_function['unaliased_inputs'] and len(dss_function['unaliased_inputs']['values']) > 0:
        unaliasedinputs = dss_function['unaliased_inputs']['values']
        unaliasedinputsdesc = dss_function['unaliased_inputs']['desc']
        for requiredinput in unaliasedinputs:
            unaliasedtable = next(x for x in inputTables if x.datasetname == requiredinput)
            partitionKeys = "" if not unaliasedtable.partitionKey else " ".join(["PARTITION BY", unaliasedtable.partitionKey])
                    
            orderKeys = "" if not unaliasedtable.orderKey else " ".join(["ORDER BY", unaliasedtable.orderKey])

            multipleunaliasedinputs += """ON {schema}.{input_table} {partitionKeys} {orderKeys}""".format(schema=unaliasedtable.schemaname,
                                                                                                          input_table=unaliasedtable.tablenamewithoutschema,
                                                                                                          partitionKeys=partitionKeys,
                                                                                                          orderKeys=orderKeys).rstrip() + "\n"
    
    if not multiplealiasedinputs and not multipleunaliasedinputs:
        onselect = "ON (SELECT 1) PARTITION BY 1"
    
    if outputTable.tableType is None or outputTable.tableType == '':
        outputTable.tableType = 'DIMENSION'
    
    query = """BEGIN TRANSACTION;
DROP TABLE IF EXISTS {};
CREATE {} TABLE {}{}
AS
SELECT *
FROM   {}
(
{}
{}
{}
{}
)""".format(outputTable.tablename,
                       outputTable.tableType,
                       outputTable.tablename,
                       " DISTRIBUTE BY HASH({})".format(outputTable.hashKey) if "FACT" == outputTable.tableType else "",
                       dss_function["name"],
                       onselect,
                       multipleunaliasedinputs,
                       multiplealiasedinputs,
                       queryutility.getJoinedArgumentsString(dss_function["arguments"], inputTables))   

       
    query +=""";
COMMIT;
END TRANSACTION;"""
        
    return query