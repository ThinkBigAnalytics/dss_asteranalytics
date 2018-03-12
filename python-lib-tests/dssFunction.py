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
Created on May 17, 2017

@author: dt186022
'''

class dssFunction(object):
    '''
    Test input recipe config builder
    '''


    def __init__(self):
        self.__dss_function = {'isOrdered': False,
                    'name':'',
                    'partitionInputKind': [],
                    'orderByColumn': '',
                    'partitionAttributes': '',
                    'unaliased_inputs': {'count': 0.0, 'values': [], 'desc': {}},
                    'arguments': '',
                    'required_input': [], 
                    'hasInputTable': False, 
                    'asterarguments': [
                        {'name': 'schema', 'value': '', 'label': 'Schema'},
                        {'name': 'outputType', 'value': '', 'label': 'Output Table Type'},
                        {'name': 'hashKey', 'value': '', 'label': 'Hash Key Column'}
                        ]
                    }

    def name(self, value):
        self.__dss_function['name'] = value
        return self
        
    def unaliased_inputs_count(self, value):
        self.__dss_function['unaliased_inputs']['count'] = value
        return self
        
    def add_unaliased_input(self, inputdataset, partition):
        self.__dss_function['hasInputTable'] = True
        self.__dss_function['unaliased_inputs']['values'].append(inputdataset)
        self.__dss_function['partitionInputKind'].append(partition)
        return self
        
    def build(self):
        return self.__dss_function