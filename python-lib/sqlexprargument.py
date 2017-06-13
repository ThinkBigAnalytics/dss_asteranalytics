'''
Created on Jun 6, 2017

@author: DT186022
'''

from asterargument import *

class SqlExprArgument(AsterArgument):

    def __init__(self, argument, argumentDef):
        super(SqlExprArgument, self).__init__(argument, argumentDef)
    
    @property
    def value(self):
        DELIMITER = chr(0)
        return ", ".join('{}'.format(self._argument.get('value','')).split(DELIMITER))
        