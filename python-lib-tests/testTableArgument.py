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
