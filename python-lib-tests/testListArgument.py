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
