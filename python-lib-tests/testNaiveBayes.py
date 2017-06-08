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
DROP TABLE IF EXISTS dss.naivebayestrain_out;
CREATE DIMENSION TABLE dss.naivebayestrain_out
AS
(SELECT * FROM NAIVEBAYESREDUCE (ON (SELECT * FROM NAIVEBAYESMAP (ON public.dss_nb_iris_dataset_train   NUMERICINPUTS('sepal_length', 'sepal_width', 'petal_length', 'petal_width')
RESPONSE('species')
)) PARTITION BY class  ));
COMMIT;
END TRANSACTION;'''
        self.assertEqual('\n'.join(actualquery + ['END TRANSACTION;']), expectedquery, "test CASCADED FUNCTIONS NAIVEBAYESMAP AND NAIVEBAYESREDUCE")


