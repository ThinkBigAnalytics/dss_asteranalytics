from sets import Set
# -*- coding: utf-8 -*-
import asterqueryutility as queryutility

def getAsterQuery(dss_function, inputTable, outputTable):
    # query
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
                      ) 
            """.format(outputTable.tablename,
                       outputTable.tableType,
                       outputTable.tablename,
                       "DISTRIBUTE BY HASH({})".format(outputTable.hashKey) if "FACT" == outputTable.tableType else "",
                       dss_function["name"],
                       inputTable.tablename,
                       "" if not inputTable.partitionKey else " ".join(["PARTITION BY", inputTable.partitionKey]),
                       "" if not inputTable.orderKey else " ".join(["ORDER BY", inputTable.orderKey]),
                       queryutility.getJoinedArgumentsString(dss_function["arguments"]))   

       
    query +=""";
           COMMIT;
           END TRANSACTION;
        """
        
    return query