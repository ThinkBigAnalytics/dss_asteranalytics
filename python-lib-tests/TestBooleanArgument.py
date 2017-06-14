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
        testasterargument = BooleanArgument(argument, self.__argumentdef)
        argumentdef = {'datatype': 'BOOLEAN', 'isRequired': False, 'allowsLists': False,
                       'defaultValue': True}
        self.assertEqual("CASESENSITIVE('True')\n", testasterargument.argumentclause,
                         "Test when boolean argument is True and default is True")
    
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
