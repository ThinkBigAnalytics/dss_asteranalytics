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
