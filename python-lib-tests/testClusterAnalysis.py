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
        expectedquery = '''CREATE DIMENSION TABLE "dss.canopy_out"
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
        
    def testKmeansPlot(self):
        inputConnectionConfig = {'table': 'computers_train1', 'schema': 'dss'}
        secondaryInputConnectionConfig = {'table': 'kmeanssample_centroid', 'schema': 'dss'}
        
        functionInputTable = inputtableinfo(inputConnectionConfig, 'computers_train1', kmeansplotConfig)
        centroidTable = inputtableinfo(secondaryInputConnectionConfig, 'kmeanssample', kmeansplotConfig)
        actualquery = getSelectClause(kmeansplotConfig, [functionInputTable, centroidTable])
        expectedquery = '''SELECT *
FROM   KMEANSPLOT
(
ON dss.computers_train1 PARTITION BY ANY
ON dss.kmeanssample_centroid  DIMENSION
CENTROIDSTABLE('dss.kmeanssample_centroid')

);'''
        self.assertEqual(actualquery, expectedquery, "test UNALIASED DIMENSIONAL INPUT")

