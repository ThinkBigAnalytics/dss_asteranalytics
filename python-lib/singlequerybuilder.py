from sets import Set
# -*- coding: utf-8 -*-
import asterqueryutility as queryutility

def getAsterQuery(dss_function, inputTable, outputTable):
    # query
    multipleinputs = ""
    if 'required_input' in dss_function.keys():
        requiredinputs = dss_function['required_input']
        for requiredinput in requiredinputs:
            if 'value' in requiredinput.keys() and requiredinput["value"]:
                multipleinputs += """ON {input_table} AS {input_name} {kind}\n""".format( input_table=requiredinput['value'],
                                                                                          input_name=requiredinput['name'],
                                                                                          kind=requiredinput['kind'])
    query = """BEGIN TRANSACTION;
               DROP TABLE IF EXISTS {};
               CREATE {} TABLE {}{}
               AS 
               SELECT *
               FROM   {}
                      (
                        ON {}
               {}
               {}
                       {}
               {}
                      ) 
            """.format(outputTable.tablename,
                       outputTable.tableType,
                       outputTable.tablename,
                       " DISTRIBUTE BY HASH({})".format(outputTable.hashKey) if "FACT" == outputTable.tableType else "",
                       dss_function["name"],
                       inputTable.tablename,
                       "" if not inputTable.partitionKey else " ".join(["PARTITION BY", inputTable.partitionKey]),
                       "" if not inputTable.orderKey else " ".join(["ORDER BY", inputTable.orderKey]),
                       multipleinputs,
                       queryutility.getJoinedArgumentsString(dss_function["arguments"]))   

       
    query +=""";
           COMMIT;
           END TRANSACTION;
        """
        
    return query