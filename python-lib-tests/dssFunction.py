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