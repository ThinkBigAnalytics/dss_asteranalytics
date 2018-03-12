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
