'''
Created on Jun 6, 2017

@author: DT186022
'''
import re

class AsterArgument(object):
    '''
    Base class for aster arguments
    '''


    def __init__(self, argument, argumentDef):
        self._argument = argument
        self._argumentDef = argumentDef
    
    @property
    def name(self):
        return self._argument.get('name', '').upper()
    
    @property
    def value(self):
        regex = chr(0)
        return ", ".join(\
                         [(s if (s[:1] == "'" and s[-1:] == "'") else \
                           ("'" + s + "'")) for s in \
                          re.split(regex, """'{}'""".format(self._argument.get('value','')))])
    @property
    def argumentclause(self):
        return """{argumentname}({argumentvalue})\n""". \
            format(argumentname=self.name,
                   argumentvalue=self.value) if self._argument.get('value', '') else \
                   ''
        
    @property
    def allowsLists(self):
        return argumentDef.get('allowsLists', False)
    
    @property
    def datatype(self):
        return argumentDef.get('datatype', 'STRING')
    
    @property
    def isOuputTable(self):
        return argumentDef.get('isOutputTable', False)
