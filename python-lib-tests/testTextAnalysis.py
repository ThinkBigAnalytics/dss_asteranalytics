'''
Created on May 15, 2017

@author: dt186022
'''

import unittest
from querybuilderfacade import *
from testTextAnalysisConfig import *
from inputtableinfo import *
from outputtableinfo import *
from connectioninfo import *
from dssFunction import *

class TestTextAnalysis(unittest.TestCase):

    def testTextTokenizer(self):
        
        textTokenizerOutputConnectionConfig = {'table': 'text_tokenized'}
        
        textTokenizerInputConnectionConfig = {'table': 'text_chunked', 'schema': 'bs186029'}
        
        functionInputTable = inputtableinfo(textTokenizerInputConnectionConfig, 'text_chunked', textTokenizerConfig)
        functionOutputTable = outputtableinfo(textTokenizerOutputConnectionConfig, 'text_tokenized', textTokenizerConfig)
        actualquery = getFunctionsQuery(textTokenizerConfig, [functionInputTable], functionOutputTable)
        expectedquery = """BEGIN TRANSACTION;
DROP TABLE IF EXISTS public.text_tokenized;
CREATE DIMENSION TABLE public.text_tokenized
AS
SELECT *
FROM   TEXTTOKENIZER
(

ON bs186029.text_chunked PARTITION BY ANY


TEXTCOLUMN('chunk')

);
COMMIT;
END TRANSACTION;"""
        self.assertEqual(actualquery, expectedquery, "Ohno")

    def testEvaluateNamedEntityFinderPartition(self):
        testInputConnectionConfig = {'table' : 'textclassifier_input', 'schema':'dss'}
        testOuputConnectionConfig = {'table' : 'dss_test'}
        testfunction = dssFunction()
        testConfig = testfunction.name('EVALUATENAMEDENTITYFINDERPARTITION').unaliased_inputs_count(0).add_unaliased_input('textclassifier_input', 'PartitionByOne').build()
        functionInputTable = inputtableinfo(testInputConnectionConfig, 'textclassifier_input', testConfig)
        functionOutputTable = outputtableinfo(testOuputConnectionConfig, 'dss_test', testConfig)
        actualquery = getFunctionsQuery(testConfig, [functionInputTable], functionOutputTable)
        expectedquery = """BEGIN TRANSACTION;
DROP TABLE IF EXISTS public.dss_test;
CREATE DIMENSION TABLE public.dss_test
AS
SELECT *
FROM   EVALUATENAMEDENTITYFINDERPARTITION
(

ON dss.textclassifier_input PARTITION BY 1



);
COMMIT;
END TRANSACTION;"""
        self.assertEqual(actualquery, expectedquery, 'EvaluateNamedEntityFinderPartition')

    # 1 unaliased input, several arguments, 1 output
    def testNertrainer(self):
        testInputConnectionConfig = {'table' : 'ner_sports_train', 'schema':'dss'}
        testOutputConnectionConfig = {'table' : 'dss_nertrainer', 'schema': 'dss'}
        functionInputTable = inputtableinfo(testInputConnectionConfig, 'ner_sports_train', nertrainerConfig)
        functionOutputTable = outputtableinfo(testOutputConnectionConfig, 'dss_nertrainer', nertrainerConfig)
        actualquery = getFunctionsQuery(nertrainerConfig, [functionInputTable], functionOutputTable)
        expectedquery = """BEGIN TRANSACTION;
DROP TABLE IF EXISTS dss.dss_nertrainer;
CREATE DIMENSION TABLE dss.dss_nertrainer
AS
SELECT *
FROM   NERTRAINER
(

ON dss.ner_sports_train PARTITION BY id


TEXTCOLUMN('content')
MODELFILE('ner_model.bin')
FEATURETEMPLATE('template_1.txt')

);
COMMIT;
END TRANSACTION;"""
        self.assertEqual(actualquery, expectedquery, 'Nertrainer')

    def testNer(self):
        testInputConnectionConfig = {'table' : 'ner_sports_test', 'schema':'dss'}
        testRuleConnectionConfig = {'table' : 'rule_table', 'schema':'dss'}
        testOutputConnectionConfig = {'table' : 'dss_ner', 'schema': 'dss'}
        functionInputTable = inputtableinfo(testInputConnectionConfig, 'ner_sports_test', nerConfig)
        ruleTable = inputtableinfo(testRuleConnectionConfig, 'rule_table', nerConfig)
        functionOutputTable = outputtableinfo(testOutputConnectionConfig, 'dss_ner', nerConfig)
        actualquery = getFunctionsQuery(nerConfig, [functionInputTable, ruleTable], functionOutputTable)
        expectedquery = """BEGIN TRANSACTION;
DROP TABLE IF EXISTS dss.dss_ner;
CREATE DIMENSION TABLE dss.dss_ner
AS
SELECT *
FROM   NER
(

ON dss.ner_sports_test PARTITION BY ANY

ON dss.rule_table AS "rules" DIMENSION

TEXTCOLUMN('content')
MODELS('ner_model.bin')
ACCUMULATE('id')
SHOWCONTEXT('2')

);
COMMIT;
END TRANSACTION;"""
        self.assertEqual(actualquery, expectedquery, 'Nerevaluator')

    def testNerEvaluator(self):
        testInputConnectionConfig = {'table' : 'ner_sports_test', 'schema':'dss'}
        testOutputConnectionConfig = {'table' : 'dss_nerevaluator', 'schema': 'dss'}
        functionInputTable = inputtableinfo(testInputConnectionConfig, 'ner_sports_test', nerEvaluatorConfig)
        functionOutputTable = outputtableinfo(testOutputConnectionConfig, 'dss_ner', nerEvaluatorConfig)
        actualquery = getFunctionsQuery(nerEvaluatorConfig, [functionInputTable], functionOutputTable)
        expectedquery = """BEGIN TRANSACTION;
DROP TABLE IF EXISTS dss.dss_nerevaluator;
CREATE DIMENSION TABLE dss.dss_nerevaluator
AS
SELECT *
FROM   NEREVALUATOR
(

ON dss.ner_sports_test PARTITION BY id


TEXTCOLUMN('content')
MODEL('ner_model.bin')

);
COMMIT;
END TRANSACTION;"""
        self.assertEqual(actualquery, expectedquery, 'Nertrainer')