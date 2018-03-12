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
from booleanargument import *


class TestBooleanArgument(unittest.TestCase):
    
    def setUp(self):
        self.__argumentdef = {'datatype': 'BOOLEAN', 'isRequired': False, 'allowsLists': False}

    def testSingleValuedEmptyStringBooleanArgument(self):
        argument = {'name': 'CASESENSITIVE', 'value': ''}
        testasterargument = BooleanArgument(argument, self.__argumentdef)
        self.assertEqual("'False'", testasterargument.value, "Test Empty String Boolean Argument")
        
    def testFalseBooleanArgumentClauseDefaultFalse(self):
        argument = {'name': 'CASESENSITIVE', 'value': ''}
        testasterargument = BooleanArgument(argument, self.__argumentdef)
        self.assertEqual('', testasterargument.argumentclause,
                         "Test when boolean argument is False and default is False")
        
    def testTrueBooleanArgumentClauseDefaultFalse(self):
        argument = {'name': 'CASESENSITIVE', 'value': True}
        testasterargument = BooleanArgument(argument, self.__argumentdef)
        self.assertEqual("CASESENSITIVE('True')\n", testasterargument.argumentclause,
                         "Test when boolean argument is True and default is False")
        
    def testTrueBooleanArgumentClauseDefaultTrue(self):
        argument = {'name': 'CASESENSITIVE', 'value': True}
        argumentdef = {'datatype': 'BOOLEAN', 'isRequired': False, 'allowsLists': False,
                       'defaultValue': True}
        testasterargument = BooleanArgument(argument, argumentdef)
        self.assertEqual("CASESENSITIVE('True')\n", testasterargument.argumentclause,
                         "Test when boolean argument is True and default is True")

    def testFalseBooleanArgumentClauseDefaultTrue(self):
        argument = {'name': 'CASESENSITIVE', 'value': False}
        argumentdef = {'datatype': 'BOOLEAN', 'isRequired': False, 'allowsLists': False,
                       'defaultValue': True}
        testasterargument = BooleanArgument(argument, argumentdef)
        self.assertEqual("CASESENSITIVE('False')\n", testasterargument.argumentclause,
                         "Test when boolean argument is False and default is True")
        
    def testNoneBooleanArgumentClauseDefaultTrue(self):
        argument = {'name': 'CASESENSITIVE', 'value': None}
        argumentdef = {'datatype': 'BOOLEAN', 'isRequired': False, 'allowsLists': False,
                       'defaultValue': True}
        testasterargument = BooleanArgument(argument, argumentdef)
        self.assertEqual("CASESENSITIVE('False')\n", testasterargument.argumentclause,
                         "Test when boolean argument is None and default is True")
    
    def testSingleValuedFalseStringBooleanArgument(self):
        argument = {'name': 'CASESENSITIVE', 'value': False}
        testasterargument = BooleanArgument(argument, self.__argumentdef)
        self.assertEqual("'False'", testasterargument.value, "Test False Boolean Argument")
        
    def testEmptyStringBooleanArgument(self):
        argument = {'name': 'CASESENSITIVE', 'value': True}
        testasterargument = BooleanArgument(argument, self.__argumentdef)
        self.assertEqual("'True'", testasterargument.value, "Test True Boolean Argument")
        
    def testRandomStringBooleanArgument(self):
        # 'f' will also be read as 'True' then
        argument = {'name': 'CASESENSITIVE', 'value': 't'}
        testasterargument = BooleanArgument(argument, self.__argumentdef)
        self.assertEqual("'True'", testasterargument.value, "Test Random Letter Boolean Argument")
        
    def testRandomNumberBooleanArgument(self):
        argument = {'name': 'CASESENSITIVE', 'value': 2}
        testasterargument = BooleanArgument(argument, self.__argumentdef)
        self.assertEqual("'True'", testasterargument.value, "Test Random Number Boolean Argument")
        
    def testZeroBooleanArgument(self):
        argument = {'name': 'CASESENSITIVE', 'value': 0}
        testasterargument = BooleanArgument(argument, self.__argumentdef)
        self.assertEqual("'False'", testasterargument.value, "Test when boolean argument is zero")
        
    def testNoneBooleanArgument(self):
        argument = {'name': 'CASESENSITIVE', 'value': None}
        testasterargument = BooleanArgument(argument, self.__argumentdef)
        self.assertEqual("'False'", testasterargument.value, "Test when boolean argument is null")
