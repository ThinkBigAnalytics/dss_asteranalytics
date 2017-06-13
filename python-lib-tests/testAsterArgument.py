'''
Created on Jun 13, 2017

@author: dt186022
'''
import unittest
import re
from asterargument import *


class TestAsterArgument(unittest.TestCase):


    def testSingleValuedAsterArgument(self):
        argument = {'name': 'PATTERN', 'value': 'S1{1,3}.S2'}
        argumentdef = {'datatype': 'STRING',
                       'isRequired': True,
                       'allowsLists': True}
        testasterargument = AsterArgument(argument, argumentdef)
        self.assertEqual("""'S1{1,3}.S2'""", testasterargument.value, "Test Aster Argument")
        
    def testNullSeparatedAsterArgument(self):
        argument = {'name': 'PATTERN', 'value': 'S1{1,3}.S2\x00s3, 24'}
        argumentdef = {'datatype': 'STRING',
                       'isRequired': True,
                       'allowsLists': True}
        testasterargument = AsterArgument(argument, argumentdef)
        self.assertEqual("""'S1{1,3}.S2', 's3, 24'""", testasterargument.value, "Test Aster Argument")
    
    def testNoneDefaultAsterArgument(self):
        argument = {'name': 'PATTERN', 'value': None}
        argumentdef = {'datatype': 'STRING',
                       'isRequired': True,
                       'allowsLists': True}
        testasterargument = AsterArgument(argument, argumentdef)
        self.assertEqual("'None'", testasterargument.value, "Test Aster Argument")
        
