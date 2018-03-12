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
Created on Jun 13, 2017

@author: dt186022
'''
import unittest
from asterargument import *


class TestAsterArgument(unittest.TestCase):
    
    def setUp(self):
        self.__argumentdef = {'datatype': 'STRING', 'isRequired': True, 'allowsLists': True}

    def testSingleValuedAsterArgument(self):
        argument = {'name': 'PATTERN', 'value': 'S1{1,3}.S2'}
        testasterargument = AsterArgument(argument, self.__argumentdef)
        self.assertEqual("""'S1{1,3}.S2'""", testasterargument.value, "Test Aster Argument")
        
    def testNullSeparatedAsterArgument(self):
        argument = {'name': 'PATTERN', 'value': 'S1{1,3}.S2\x00s3, 24'}
        argumentdef = {'datatype': 'STRING', 'isRequired': True, 'allowsLists': True}
        testasterargument = AsterArgument(argument, self.__argumentdef)
        self.assertEqual("""'S1{1,3}.S2', 's3, 24'""", testasterargument.value,
                         "Test Aster Argument")
        
    def testBooleanAllowListsSeparatedAsterArgument(self):
        # In STRINGSIMILARITY, BOOLEAN datatypes can be lists
        # But this is confusing to the user so we are not supporting boolean lists
        argument = {'name': 'PATTERN', 'value': 'True\x00False'}
        argumentdef = {'datatype': 'STRING', 'isRequired': True, 'allowsLists': True}
        testasterargument = AsterArgument(argument, self.__argumentdef)
        self.assertEqual("""'True', 'False'""", testasterargument.value,
                         "Test Aster Argument")
    
    def testNoneDefaultAsterArgument(self):
        argument = {'name': 'PATTERN', 'value': None}
        testasterargument = AsterArgument(argument, self.__argumentdef)
        self.assertEqual("'None'", testasterargument.value, "Test Aster Argument")       
