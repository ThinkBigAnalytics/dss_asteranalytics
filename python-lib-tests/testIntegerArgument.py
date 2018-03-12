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
Created on Jun 14, 2017

@author: dt186022
'''
import unittest
from integerargument import *


class TestIntegerArgument(unittest.TestCase):

    
    def setUp(self):
        self.__argumentdef = {'datatype': 'INTEGER', 'isRequired': False, 'allowsLists': False}

    def testIntegerArgument(self):
        argument = {'name': 'MAXITERATION', 'value': 1000.0}
        testasterargument = IntegerArgument(argument, self.__argumentdef)
        self.assertEqual("'1000'", testasterargument.value,
                         "Test when integer argument has a decimal place")
        
    def testHappyTrailIntegerArgument(self):
        argument = {'name': 'MAXITERATION', 'value': 1000}
        testasterargument = IntegerArgument(argument, self.__argumentdef)
        self.assertEqual("'1000'", testasterargument.value,
                         "Test integer argument, happy trail")
        
    def testIntegerArgumentAsString(self):
        argument = {'name': 'MAXITERATION', 'value': '1000.0'}
        testasterargument = IntegerArgument(argument, self.__argumentdef)
        self.assertEqual("'1000'", testasterargument.value,
                         "Test integer argument, happy trail")
        
    def testEmptyIntegerArgument(self):
        argument = {'name': 'MAXITERATION', 'value': ''}
        testasterargument = IntegerArgument(argument, self.__argumentdef)
        self.assertEqual("'0'", testasterargument.value,
                         "Test when integer argument is an empty string")
        
    def testZeroIntegerArgument(self):
        argument = {'name': 'MAXITERATION', 'value': 0}
        testasterargument = IntegerArgument(argument, self.__argumentdef)
        self.assertEqual("'0'", testasterargument.value,
                         "Test when integer argument is zero")
        
    def testNonparsableIntegerArgument(self):
        argument = {'name': 'MAXITERATION', 'value': 'a'}
        testasterargument = IntegerArgument(argument, self.__argumentdef)
        self.assertEqual("'0'", testasterargument.value,
                         "Test when integer argument cannot be parsed to int")
        
    def testNoneIntegerArgument(self):
        argument = {'name': 'MAXITERATION', 'value': None}
        testasterargument = IntegerArgument(argument, self.__argumentdef)
        self.assertEqual("'0'", testasterargument.value,
                         "Test when integer argument is None")
