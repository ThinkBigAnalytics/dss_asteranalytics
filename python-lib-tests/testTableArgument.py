'''
Created on Jun 15, 2017

@author: dt186022
'''
import unittest
from tableargument import *
from testClusterAnalysisConfig import *
from inputtableinfo import *


class TestTableArgument(unittest.TestCase):


    def setUp(self):
        self.__argumentdef = {'datatype': 'TABLE_NAME', 'isRequired': True,'allowsLists': False}

    def testTableArgument(self):
        argument = {'name': 'INPUTTABLE', 'value': 'computers_train1_public'}
        inputConnectionConfig = {'table': 'computers_train1', 'schema': 'public'}
        functionInputTable = inputtableinfo(inputConnectionConfig,
                                            'computers_train1_public',
                                            canopyConfig)
        testargument = TableArgument(argument, self.__argumentdef, [functionInputTable])
        self.assertEqual(testargument.value,
                         "'computers_train1'",
                         "Wrong input table argument")
        
    def testNonPublicTableArgument(self):
        argument = {'name': 'INPUTTABLE', 'value': 'computers_train1_public'}
        inputConnectionConfig = {'table': 'computers_train1', 'schema': 'dss'}
        functionInputTable = inputtableinfo(inputConnectionConfig,
                                            'computers_train1_public',
                                            canopyConfig)
        testargument = TableArgument(argument, self.__argumentdef, [functionInputTable])
        self.assertEqual(testargument.value,
                         "'dss.computers_train1'",
                         "Wrong input table argument")
        
    def testDatasetDoesNotExist(self):
        # dataset name is computers_train1_public but argument value is computers_train1
        argument = {'name': 'INPUTTABLE', 'value': 'computers_train1'}
        inputConnectionConfig = {'table': 'computers_train1', 'schema': 'dss'}
        functionInputTable = inputtableinfo(inputConnectionConfig,
                                            'computers_train1_public',
                                            canopyConfig)
        testargument = TableArgument(argument, self.__argumentdef, [functionInputTable])
        self.assertEqual(testargument.value,
                         '',
                         "Wrong input table argument")

    def testNullDatasetArgument(self):
        # dataset name is computers_train1_public but argument value is computers_train1
        argument = {'name': 'INPUTTABLE', 'value': None}
        inputConnectionConfig = {'table': 'computers_train1', 'schema': 'dss'}
        functionInputTable = inputtableinfo(inputConnectionConfig,
                                            'computers_train1_public',
                                            canopyConfig)
        testargument = TableArgument(argument, self.__argumentdef, [functionInputTable])
        self.assertEqual(testargument.value,
                         '',
                         "Wrong input table argument")
        
    def testEmptyStringDatasetArgument(self):
        # dataset name is computers_train1_public but argument value is computers_train1
        argument = {'name': 'INPUTTABLE', 'value': ''}
        inputConnectionConfig = {'table': 'computers_train1', 'schema': 'dss'}
        functionInputTable = inputtableinfo(inputConnectionConfig,
                                            'computers_train1_public',
                                            canopyConfig)
        testargument = TableArgument(argument, self.__argumentdef, [functionInputTable])
        self.assertEqual(testargument.value,
                         '',
                         "Wrong input table argument")
