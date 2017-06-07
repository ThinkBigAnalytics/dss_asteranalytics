'''
Created on Jun 6, 2017

@author: DT186022
'''
from asterargument import *

class ListArgument(AsterArgument):

    def __init__(self, argument, argumentDef):
        super(ListArgument, self).__init__(argument, argumentDef)

    @property
    def value(self):
        return ", ".join("'" + x + "'" for x in self._argument.get('value'))