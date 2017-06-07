'''
Created on Jun 6, 2017

@author: DT186022
'''
import unittest
from querybuilderfacade import *
from testNpathConfig import *
from inputtableinfo import *
from outputtableinfo import *


class Test(unittest.TestCase):


    def testNpath(self):
        inputConnectionConfig = {'table': 'tv_shows'}
        
        outputConnectionConfig = {'table': 'dss_tv_show_npath', 'schema': 'dss'}
        
        functionInputTable = inputtableinfo(inputConnectionConfig, 'tv_shows', npathConfig)
        functionOutputTable = outputtableinfo(outputConnectionConfig, 'dss_tv_show_npath', npathConfig)
        actualquery = getFunctionsQuery(npathConfig, [functionInputTable], functionOutputTable)
        expectedquery = '''CREATE DIMENSION TABLE dss.dss_tv_show_npath
AS
SELECT *
FROM   NPATH
(

ON public.tv_shows PARTITION BY id ORDER BY ts


MODE('nonoverlapping')
PATTERN('S1{1,3}.S2')
SYMBOLS(tvshow='BreakingBad' as S2, tvshow <> 'BreakingBad' as S1)
RESULT(accumulate(tvshow of any(S1,S2)) as path)

);'''
        self.assertEqual(actualquery[2], expectedquery, "Npath")
