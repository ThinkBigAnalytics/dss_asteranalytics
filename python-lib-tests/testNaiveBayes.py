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
Created on Jun 8, 2017

@author: dt186022
'''
import unittest

from testNaiveBayesConfig import *
from querybuilderfacade import *
from inputtableinfo import *
from outputtableinfo import *

class TestNaiveBayes(unittest.TestCase):


    def testNaiveBayes(self):
        inputConnectionConfig = {'table': 'dss_nb_iris_dataset_train', 'schema': 'public'}
        
        outputConnectionConfig = {'table': 'naivebayestrain_out', 'schema': 'dss'}
        
        functionInputTable = inputtableinfo(inputConnectionConfig, 'dss_nb_iris_dataset_train', naiveBayesTrainConfig)
        functionOutputTable = outputtableinfo(outputConnectionConfig, 'naivebayestrain_out', naiveBayesTrainConfig)
        actualquery = getFunctionsQuery(naiveBayesTrainConfig, [functionInputTable], functionOutputTable)
        expectedquery = '''BEGIN TRANSACTION;
DROP TABLE IF EXISTS "dss.naivebayestrain_out";
CREATE DIMENSION TABLE "dss.naivebayestrain_out"
AS
(SELECT * FROM NAIVEBAYESREDUCE (ON (SELECT * FROM NAIVEBAYESMAP (ON public.dss_nb_iris_dataset_train   NUMERICINPUTS('sepal_length', 'sepal_width', 'petal_length', 'petal_width')
RESPONSE('species')
)) PARTITION BY class  ));
COMMIT;
END TRANSACTION;'''
        self.assertEqual('\n'.join(actualquery + ['END TRANSACTION;']), expectedquery, "test CASCADED FUNCTIONS NAIVEBAYESMAP AND NAIVEBAYESREDUCE")


