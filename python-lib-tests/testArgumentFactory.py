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
