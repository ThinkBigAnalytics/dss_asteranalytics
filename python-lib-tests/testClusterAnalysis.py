'''
Created on Jun 7, 2017

@author: DT186022
'''
import unittest

from testClusterAnalysisConfig import *
from querybuilderfacade import *
from inputtableinfo import *
from outputtableinfo import *

class TestClusterAnalysis(unittest.TestCase):


    def testCanopy(self):
        inputConnectionConfig = {'table': 'computers_train1', 'schema': 'public'}
        
        outputConnectionConfig = {'table': 'canopy_out', 'schema': 'dss'}
        
        functionInputTable = inputtableinfo(inputConnectionConfig, 'computers_train1_public', canopyConfig)
        functionOutputTable = outputtableinfo(outputConnectionConfig, 'canopy_out', canopyConfig)
        actualquery = getFunctionsQuery(canopyConfig, [functionInputTable], functionOutputTable)
        expectedquery = '''CREATE DIMENSION TABLE dss.canopy_out
AS
SELECT *
FROM   CANOPY
(
ON (SELECT 1) PARTITION BY 1


INPUTTABLE('computers_train1')
LOOSEDISTANCE('1000')
TIGHTDISTANCE('500')

);'''
        self.assertEqual(actualquery[2], expectedquery, "test TABLE_NAME argument datatype")
