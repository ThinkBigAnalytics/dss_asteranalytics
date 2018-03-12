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
Created on May 15, 2017

@author: dt186022
'''

import unittest
from querybuilderfacade import *
from testTextAnalysisConfig import *
from inputtableinfo import *
from outputtableinfo import *
from dssFunction import *

class TestTextAnalysis(unittest.TestCase):

    def testTextTokenizer(self):
        
        textTokenizerOutputConnectionConfig = {'table': 'text_tokenized'}
        
        textTokenizerInputConnectionConfig = {'table': 'text_chunked', 'schema': 'bs186029'}
        
        functionInputTable = inputtableinfo(textTokenizerInputConnectionConfig, 'text_chunked', textTokenizerConfig)
        functionOutputTable = outputtableinfo(textTokenizerOutputConnectionConfig, 'text_tokenized', textTokenizerConfig)
        actualquery = getFunctionsQuery(textTokenizerConfig, [functionInputTable], functionOutputTable)
        expectedquery = """BEGIN TRANSACTION;
DROP TABLE IF EXISTS "public.text_tokenized";
CREATE DIMENSION TABLE "public.text_tokenized"
AS
SELECT *
FROM   TEXTTOKENIZER
(
ON bs186029.text_chunked PARTITION BY ANY
TEXTCOLUMN('chunk')

);
COMMIT;
END TRANSACTION;"""
        self.assertEqual('\n'.join(actualquery) + '\nEND TRANSACTION;', expectedquery, "TextTokenizer")

    def testEvaluateNamedEntityFinderPartition(self):
        testInputConnectionConfig = {'table' : 'textclassifier_input', 'schema':'dss'}
        testOuputConnectionConfig = {'table' : 'dss_test'}
        testfunction = dssFunction()
        testConfig = testfunction.name('EVALUATENAMEDENTITYFINDERPARTITION').unaliased_inputs_count(1).add_unaliased_input('textclassifier_input', 'PartitionByOne').build()
        functionInputTable = inputtableinfo(testInputConnectionConfig, 'textclassifier_input', testConfig)
        functionOutputTable = outputtableinfo(testOuputConnectionConfig, 'dss_test', testConfig)
        actualquery = getFunctionsQuery(testConfig, [functionInputTable], functionOutputTable)
        expectedquery = """BEGIN TRANSACTION;
DROP TABLE IF EXISTS "public.dss_test";
CREATE DIMENSION TABLE "public.dss_test"
AS
SELECT *
FROM   EVALUATENAMEDENTITYFINDERPARTITION
(
ON dss.textclassifier_input PARTITION BY 1

);
COMMIT;
END TRANSACTION;"""
        self.assertEqual('\n'.join(actualquery + ['END TRANSACTION;']), expectedquery,
                         'EvaluateNamedEntityFinderPartition')

    # 1 unaliased input, several arguments, 1 output
    def testNertrainer(self):
        testInputConnectionConfig = {'table' : 'ner_sports_train', 'schema':'dss'}
        testOutputConnectionConfig = {'table' : 'dss_nertrainer', 'schema': 'dss'}
        functionInputTable = inputtableinfo(testInputConnectionConfig, 'ner_sports_train', nertrainerConfig)
        functionOutputTable = outputtableinfo(testOutputConnectionConfig, 'dss_nertrainer', nertrainerConfig)
        actualquery = getFunctionsQuery(nertrainerConfig, [functionInputTable], functionOutputTable)
        expectedquery = """BEGIN TRANSACTION;
DROP TABLE IF EXISTS "dss.dss_nertrainer";
CREATE DIMENSION TABLE "dss.dss_nertrainer"
AS
SELECT *
FROM   NERTRAINER
(
ON dss.ner_sports_train PARTITION BY id
TEXTCOLUMN('content')
MODELFILE('ner_model.bin')
MAXITERATION('1000')
FEATURETEMPLATE('template_1.txt')

);
COMMIT;
END TRANSACTION;"""
        self.assertEqual('\n'.join(actualquery) + '\nEND TRANSACTION;', expectedquery, 'Nertrainer test INTEGER argument')

    def testNer(self):
        testInputConnectionConfig = {'table' : 'ner_sports_test', 'schema':'dss'}
        testRuleConnectionConfig = {'table' : 'rule_table1', 'schema':'dss'}
        testOutputConnectionConfig = {'table' : 'dss_ner', 'schema': 'dss'}
        functionInputTable = inputtableinfo(testInputConnectionConfig, 'ner_sports_test', nerConfig)
        ruleTable = inputtableinfo(testRuleConnectionConfig, 'rule_table', nerConfig)
        functionOutputTable = outputtableinfo(testOutputConnectionConfig, 'dss_ner', nerConfig)
        actualquery = getFunctionsQuery(nerConfig, [functionInputTable, ruleTable], functionOutputTable)
        expectedquery = """BEGIN TRANSACTION;
DROP TABLE IF EXISTS "dss.dss_ner";
CREATE DIMENSION TABLE "dss.dss_ner"
AS
SELECT *
FROM   NER
(
ON dss.ner_sports_test PARTITION BY ANY
ON dss.rule_table1 AS "rules" DIMENSION
TEXTCOLUMN('content')
MODELS('ner_model.bin')
ACCUMULATE('id')
SHOWCONTEXT('2')

);
COMMIT;
END TRANSACTION;"""
        self.assertEqual('\n'.join(actualquery) + '\nEND TRANSACTION;', expectedquery, 'Nerevaluator')

    def testNerEvaluator(self):
        testInputConnectionConfig = {'table' : 'ner_sports_test', 'schema':'dss'}
        testOutputConnectionConfig = {'table' : 'dss_nerevaluator', 'schema': 'dss'}
        functionInputTable = inputtableinfo(testInputConnectionConfig, 'ner_sports_test', nerEvaluatorConfig)
        functionOutputTable = outputtableinfo(testOutputConnectionConfig, 'dss_ner', nerEvaluatorConfig)
        actualquery = getFunctionsQuery(nerEvaluatorConfig, [functionInputTable], functionOutputTable)
        expectedquery = """BEGIN TRANSACTION;
DROP TABLE IF EXISTS "dss.dss_nerevaluator";
CREATE DIMENSION TABLE "dss.dss_nerevaluator"
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
        self.assertEqual('\n'.join(actualquery) + '\nEND TRANSACTION;', expectedquery, 'Nertrainer')
        
    def testTextParser(self):
        testInputConnectionConfig = {'table' : 'textparser_input', 'schema':'dss'}
        testOutputConnectionConfig = {'table' : 'textparser_output', 'schema': 'dss'}
        functionInputTable = inputtableinfo(testInputConnectionConfig, 'textparser_input', textParserConfig)
        functionOutputTable = outputtableinfo(testOutputConnectionConfig, 'textparser_output', textParserConfig)
        actualquery = getFunctionsQuery(textParserConfig, [functionInputTable], functionOutputTable)
        expectedquery = """CREATE DIMENSION TABLE "dss.textparser_output"
AS
SELECT *
FROM   TEXT_PARSER
(
ON dss.textparser_input PARTITION BY ANY
TEXT_COLUMN('text_data')
CASE_INSENSITIVE('True')
OUTPUT_BY_WORD('True')
REMOVE_STOP_WORDS('True')
STOP_WORDS('stopwords.txt')
PUNCTUATION('\[.,?\!\]')
LIST_POSITIONS('True')
ACCUMULATE('doc_id', 'category')

);"""
        self.assertEqual(actualquery[2], expectedquery, 'test boolean arguments')
        
    def testTfidf(self):
        inputConnectionConfig = {'table': 'tf', 'schema': 'dssenron'}
        secondinputConnectionConfig = {'table': 'doccount_trigram', 'schema': 'dssenron'}
        secondaryInputConnectionConfig = {'table': 'lp_svm_tfidf_output', 'schema': 'dssenron'}
        
        functionInputTable = inputtableinfo(inputConnectionConfig, 'tf', tfidfConfig)
        doccountInputTable = inputtableinfo(secondinputConnectionConfig, 'doccount_trigram', tfidfConfig)
        actualquery = getSelectClause(tfidfConfig, [functionInputTable, doccountInputTable])
        expectedquery = '''SELECT *
FROM   TF_IDF
(
ON dssenron.tf AS "tf" PARTITION BY term
ON dssenron.doccount_trigram AS "doccount" DIMENSION ORDER BY testColumn
ON dssenron.doccount_trigram AS "docperterm" PARTITION BY tf
ON dssenron.doccount_trigram AS "idf" PARTITION BY doccount_trigram ORDER BY testColumn2

);'''
        self.assertEqual(actualquery, expectedquery, "test UNALIASED DIMENSIONAL INPUT")
