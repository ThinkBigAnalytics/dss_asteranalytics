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
        