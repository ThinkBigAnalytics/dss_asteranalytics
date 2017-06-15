'''
Created on Jun 15, 2017

@author: dt186022
'''

import unittest
from sqlexprargument import *


class TestSqlExprArguments(unittest.TestCase):


    def setUp(self):
        self.__argumentdef = {'datatype': 'SQLEXPR', 'isRequired': True, 'allowsLists': True}

    def testMultipleSymbols(self):
        argument = {'name': 'SYMBOLS',
                    'value': "tvshow='BreakingBad' as S2\x00tvshow <> 'BreakingBad' as S1"}
        testasterargument = SqlExprArgument(argument, self.__argumentdef)
        self.assertEqual("tvshow='BreakingBad' as S2, tvshow <> 'BreakingBad' as S1",
                         testasterargument.value, "Test multiple symbols")
        
    def testMultipleSymbolsSingleQuote(self):
        argument = {'name': 'SYMBOLS',
                    'value': "'tvshow'='BreakingBad' as S2\x00tvshow <> 'BreakingBad' as 'S1'"}
        testasterargument = SqlExprArgument(argument, self.__argumentdef)
        self.assertEqual("'tvshow'='BreakingBad' as S2, tvshow <> 'BreakingBad' as 'S1'",
                         testasterargument.value, "Test multiple symbols with many single quotes")

    def testSingleAggregateFunction(self):
        argument = {'name': 'RESULT', 'value': 'accumulate(tvshow of any(S1,S2)) as path'}
        testasterargument = SqlExprArgument(argument, self.__argumentdef)
        self.assertEqual("accumulate(tvshow of any(S1,S2)) as path",
                         testasterargument.value, "Test single aggregate function")

    def testMultipleSymbolsArgumentClause(self):
        argument = {'name': 'SYMBOLS',
                    'value': "tvshow='BreakingBad' as S2\x00tvshow <> 'BreakingBad' as S1"}
        testasterargument = SqlExprArgument(argument, self.__argumentdef)
        self.assertEqual("SYMBOLS(tvshow='BreakingBad' as S2, tvshow <> 'BreakingBad' as S1)\n",
                         testasterargument.argumentclause,
                         "Test argument clause formultiple symbols")

    def testSingleAggregateFunctionArgumentClause(self):
        argument = {'name': 'RESULT', 'value': 'accumulate(tvshow of any(S1,S2)) as path'}
        testasterargument = SqlExprArgument(argument, self.__argumentdef)
        self.assertEqual("RESULT(accumulate(tvshow of any(S1,S2)) as path)\n",
                         testasterargument.argumentclause,
                         "Test argument clause for single aggregate function")
        
    def testNoneSqlExprArgumentClause(self):
        argument = {'name': 'RESULT', 'value': None}
        testasterargument = SqlExprArgument(argument, self.__argumentdef)
        self.assertEqual('',
                         testasterargument.argumentclause,
                         "Test argument clause for single aggregate function when"
                         "argument is none")
    
    def testEmptyStringSqlExprArgumentClause(self):
        argument = {'name': 'RESULT', 'value': ''}
        testasterargument = SqlExprArgument(argument, self.__argumentdef)
        self.assertEqual('',
                         testasterargument.argumentclause,
                         "Test argument clause for single aggregate when argument is empty")
    