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
