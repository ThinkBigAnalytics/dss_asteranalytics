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
Created on Jun 6, 2017

@author: DT186022
'''

from asterargument import *

class TableArgument(AsterArgument):

    def __init__(self, argument, argumentDef, inputTables):
        super(TableArgument, self).__init__(argument, argumentDef)
        self.__inputTables = inputTables
        
    def __getTableNameFromArgument(self, argumentValue, inputTables):
        # this next algo here is not safe without a default value,
        # I hope you can put up a unit test and alter it
        return next(iter("'" + self.__getTableNameFromTable(x) + "'" for
                         x in inputTables if argumentValue == x.datasetname), '')

    def __getTableNameFromTable(self, inputTable):
        return inputTable.tablenamewithoutschema if \
            'public' == inputTable.schemaname else \
            inputTable.tablename

    @property
    def value(self):
        return self.__getTableNameFromArgument(self._argument.get('value', ""), self.__inputTables)
        