# -*- coding: utf-8 -*-
'''
Copyright © 2018 by Teradata.
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

'''
Created on Jun 7, 2017

@author: DT186022
'''

from pseudoconstants import *

def getPartitionKind(kind):
    return PARTITION_KEY_MAPPING.get(kind, '')

CREATE_QUERY = '''CREATE {} TABLE {}{}
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

UNALIASED_QUERY_ON_CLAUSE = '''ON {input_query}'''

DISTRIBUTE_BY_HASH = ' DISTRIBUTE BY HASH({})'

BEGIN_TRANSACTION_QUERY = 'BEGIN TRANSACTION;'

DROP_QUERY = 'DROP TABLE IF EXISTS {outputTablename};'

COMMIT_QUERY = "COMMIT;"

DELIMITER = chr(0)
