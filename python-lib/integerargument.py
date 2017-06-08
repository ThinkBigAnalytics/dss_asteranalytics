'''
Created on Jun 6, 2017

@author: DT186022
'''

from asterargument import *

class IntegerArgument(AsterArgument):
    '''
    Argument that is either 'TRUE' or 'FALSE'
    '''


    def __init__(self, argument, argumentDef):
        super(IntegerArgument, self).__init__(argument, argumentDef)
        
    def __int_try(self, value):
        try:
            return "{}".format(float(value)).split('.')[0]
        except ValueError:
            return '0'
    
    @property
    def value(self):
        return "'{}'".format(self.__int_try(self._argument.get('value','')))
