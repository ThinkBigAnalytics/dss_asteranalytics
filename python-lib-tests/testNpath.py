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
        expectedquery = '''CREATE DIMENSION TABLE "dss.dss_tv_show_npath"
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
