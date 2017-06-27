'''
Created on Jun 7, 2017

@author: DT186022
'''

from pseudoconstants import *

def getPartitionKind(kind):
    return PARTITION_KEY_MAPPING.get(kind, '')

CREATE_QUERY = '''CREATE {} TABLE "{}"{}
AS
{}'''

SELECT_QUERY = '''SELECT *
FROM   {}
(
{}
{}
);'''

ON_SELECT_ONE_PARTITION_BY_ONE = 'ON (SELECT 1) PARTITION BY 1'

ALIASED_ON_CLAUSE = '''ON {input_table} {input_name} {partitionKeys} {orderKeys}'''

UNALIASED_ON_CLAUSE = '''ON {input_table} {partitionKeys} {orderKeys}'''

DISTRIBUTE_BY_HASH = ' DISTRIBUTE BY HASH({})'

BEGIN_TRANSACTION_QUERY = 'BEGIN TRANSACTION;'

DROP_QUERY = 'DROP TABLE IF EXISTS "{outputTablename}";'

COMMIT_QUERY = "COMMIT;"

DELIMITER = chr(0)
