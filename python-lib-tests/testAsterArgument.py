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
