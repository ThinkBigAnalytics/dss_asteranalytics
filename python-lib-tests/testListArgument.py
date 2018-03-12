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
from ListArgument import *


class TestListArgument(unittest.TestCase):


    def setUp(self):
        self.__argumentdef = {'datatype': 'COLUMNS', 'isRequired': False, 'allowsLists': True}


    def testListArgument(self):
        argument = {'name': 'NUMERICINPUTS',
                    'value': ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']}
        testargument = ListArgument(argument, self.__argumentdef)
        self.assertEqual("""'sepal_length', 'sepal_width', 'petal_length', 'petal_width'""",
                         testargument.value, "Test a list argument")

    def testListArgumentClause(self):
        argument = {'name': 'NUMERICINPUTS',
                    'value': ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']}
        testargument = ListArgument(argument, self.__argumentdef)
        self.assertEqual(
            """NUMERICINPUTS('sepal_length', 'sepal_width', 'petal_length', 'petal_width')\n""",
            testargument.argumentclause, "Test list argument clause")

    def testNoneListArgument(self):
        argument = {'name': 'NUMERICINPUTS',
                    'value': None}
        testargument = ListArgument(argument, self.__argumentdef)
        self.assertEqual('',
                         testargument.argumentclause,
                         "Test list when argument is None")
        
    def testNoneList(self):
        argument = {'name': 'NUMERICINPUTS',
                    'value': [None, None, None]}
        testargument = ListArgument(argument, self.__argumentdef)
        self.assertEqual("'None', 'None', 'None'",
                         testargument.value,
                         "Test list when argument is a list of None's")

    def testEmptyListArgument(self):
        argument = {'name': 'NUMERICINPUTS',
                    'value': []}
        testargument = ListArgument(argument, self.__argumentdef)
        self.assertEqual('',
                         testargument.argumentclause,
                         "Test list argument when argument is an empty array")

    def testEmptyStringListArgument(self):
        argument = {'name': 'NUMERICINPUTS',
                    'value': ''}
        testargument = ListArgument(argument, self.__argumentdef)
        self.assertEqual('',
                         testargument.argumentclause,
                         "Test list when argument is an empty string")
        
    def testNumericListArgument(self):
        argument = {'name': 'NUMERICINPUTS',
                    'value': [1,2,3]}
        testargument = ListArgument(argument, self.__argumentdef)
        self.assertEqual("'1', '2', '3'",
                         testargument.value,
                         "Test list when argument is an empty string")
