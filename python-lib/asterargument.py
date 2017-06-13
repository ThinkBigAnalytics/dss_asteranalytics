'''
Created on Jun 6, 2017

@author: DT186022
'''

from pseudoconstantgetters import *

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
        print (self._argument.get('value', ''))
        return ", ".join(
            ["'{}'".format(s) for s in
             """{}""".format(self._argument.get('value', '')).split(DELIMITER)])
    
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
