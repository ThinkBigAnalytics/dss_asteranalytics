'''
Created on Jun 6, 2017

@author: DT186022
'''

from integerargument import *
from booleanargument import *
from ListArgument import *
from sqlexprargument import *
from tableargument import *

class AsterArgumentFactory(object):
    '''
    Creates specific aster argument object based on data type
    '''


    def createArg(argument, argumentDef, inputTables):
        if 'BOOLEAN' == argumentDef.get('datatype',''):
            return BooleanArgument(argument, argumentDef)
        elif 'SQLEXPR' == argumentDef.get('datatype', '').upper():
            return SqlExprArgument(argument, argumentDef)
        elif ('INTEGER' == argumentDef.get('datatype', '').upper() or\
            'LONG' == argumentDef.get('datatype', '')) and\
        not argumentDef.get('allowsLists', False):
            return IntegerArgument(argument, argumentDef)
        elif 'TABLE_NAME' == argumentDef['datatype'] and not \
        argumentDef.get('allowsLists', False) \
        and not argumentDef.get('isOutputTable', False):
            return TableArgument(argument, argumentDef, inputTables)
        elif isinstance(argument.get('value',''), (list, tuple)):
            return ListArgument(argument, argumentDef)
        else:
            return AsterArgument(argument, argumentDef)
    createArg = staticmethod(createArg)
