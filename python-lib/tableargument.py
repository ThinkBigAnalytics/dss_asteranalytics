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
        return next("'" + self.__getTableNameFromTable(x) + "'" for \
                    x in inputTables if argumentValue == x.datasetname)

    def __getTableNameFromTable(self, inputTable):
        return inputTable.tablenamewithoutschema if \
            'public' == inputTable.schemaname else \
            inputTable.tablename

    @property
    def value(self):
        return self.__getTableNameFromArgument(self._argument.get('value', ""), self.__inputTables)
        