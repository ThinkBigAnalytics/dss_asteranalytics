'''
Created on Jun 6, 2017

@author: DT186022
'''

from asterargument import *

class BooleanArgument(AsterArgument):
    '''
    Argument that is either 'TRUE' or 'FALSE'
    '''


    def __init__(self, argument, argumentDef):
        super(BooleanArgument, self).__init__(argument, argumentDef)
    
    @property
    def value(self):
        return """'{}'""".format(bool(self._argument.get('value', "")))
    
    @property
    def argumentclause(self):
        if self._argument.get('value','') or self._argumentDef.get('defaultValue', False):
            return self.name + "(" + """'{}'""".format(bool(self._argument.get('value', ""))) + ")\n"
        return ''
        