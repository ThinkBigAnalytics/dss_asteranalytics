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
Created on Jun 15, 2017

@author: dt186022
'''
import unittest
from asterargumentfactory import *
from testClusterAnalysisConfig import *
from inputtableinfo import *


class TestAsterArgumentFactory(unittest.TestCase):


    def testArgumentFactoryWithList(self):
        argument = {'name': 'NUMERICINPUTS',
                    'value': ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']}
        argumentdef = {'datatype': 'COLUMNS', 'isRequired': False, 'allowsLists': True}
        testargument = AsterArgumentFactory.createArg(argument, argumentdef, None)
        self.assertEqual(
            """NUMERICINPUTS('sepal_length', 'sepal_width', 'petal_length', 'petal_width')\n""",
            testargument.argumentclause, "Test argument datatype is COLUMNS")

    def testArgumentFactoryWithInteger(self):
        argument = {'name': 'MAXITERATION', 'value': 1000.0}
        argumentdef = {'datatype': 'INTEGER', 'isRequired': False, 'allowsLists': False}
        testasterargument = AsterArgumentFactory.createArg(argument, argumentdef, None)
        self.assertEqual(testasterargument.argumentclause,
                         "MAXITERATION('1000')\n",
                         "Test when argument datatype is INTEGER")

    def testArgumentFactoryWithString(self):
        argument = {'name': 'PATTERN', 'value': 'S1{1,3}.S2\x00s3, 24'}
        argumentdef = {'datatype': 'STRING', 'isRequired': True, 'allowsLists': True}
        testarg = AsterArgumentFactory.createArg(argument, argumentdef, None)
        self.assertEqual(testarg.argumentclause,
                         """PATTERN('S1{1,3}.S2', 's3, 24')\n""",
                         "Test when argument datatype is STRING")

    def testArgumentFactoryWithBooleanTrue(self):
        argument = {'name': 'CASESENSITIVE', 'value': True}
        argumentdef = {'datatype': 'BOOLEAN', 'isRequired': False, 'allowsLists': False,
                       'defaultValue': False}
        testasterargument = AsterArgumentFactory.createArg(argument, argumentdef, None)
        self.assertEqual("CASESENSITIVE('True')\n", testasterargument.argumentclause,
                         "Test when argument datatype is BOOLEAN")

    def testArgumentFactoryWithBooleanFalse(self):
        argument = {'name': 'CASESENSITIVE', 'value': False}
        argumentdef = {'datatype': 'BOOLEAN', 'isRequired': False, 'allowsLists': False,
                       'defaultValue': True}
        testasterargument = AsterArgumentFactory.createArg(argument, argumentdef, None)
        self.assertEqual("CASESENSITIVE('False')\n", testasterargument.argumentclause,
                         "Test when argument datatype is BOOLEAN")

    def testArgumentFactoryWithTable(self):
        argument = {'name': 'INPUTTABLE', 'value': 'computers_train1_public'}
        inputConnectionConfig = {'table': 'computers_train1', 'schema': 'dss'}
        functionInputTable = inputtableinfo(inputConnectionConfig,
                                            'computers_train1_public',
                                            canopyConfig)
        argumentdef = {'datatype': 'TABLE_NAME', 'isRequired': True,'allowsLists': False}
        testargument = AsterArgumentFactory.createArg(argument, argumentdef, [functionInputTable])
        self.assertEqual(testargument.argumentclause,
                         "INPUTTABLE('dss.computers_train1')\n",
                         "Wrong input table argument")

    def testArgumentFactoryWithSqlExpr(self):
        argument = {'name': 'SYMBOLS',
                    'value': "tvshow='BreakingBad' as S2\x00tvshow <> 'BreakingBad' as S1"}
        argumentdef = {'datatype': 'SQLEXPR', 'isRequired': True, 'allowsLists': True}
        testasterargument = AsterArgumentFactory.createArg(argument, argumentdef, None)
        self.assertEqual("SYMBOLS(tvshow='BreakingBad' as S2, tvshow <> 'BreakingBad' as S1)\n",
                         testasterargument.argumentclause,
                         "Test when argument datatype is SQLEXPR")

    def testArgumentFactoryWithNone(self):
        argument = {'name': 'SYMBOLS',
                    'value': None}
        argumentdef = {'datatype': 'SQLEXPR', 'isRequired': True, 'allowsLists': True}
        testasterargument = AsterArgumentFactory.createArg(argument, argumentdef, None)
        self.assertEqual('',
                         testasterargument.argumentclause,
                         "Test when argument datatype is None")
