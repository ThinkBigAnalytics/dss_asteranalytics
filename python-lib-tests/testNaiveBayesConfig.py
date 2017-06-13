'''
Created on Jun 8, 2017

@author: dt186022
'''

naiveBayesTrainConfig = {'isOrdered': False,
                         'asterarguments': [{'name': 'schema',
                                             'value': '',
                                             'label': 'Schema'},
                                            {'name': 'outputType',
                                             'value': '',
                                             'label': 'Output Table Type'},
                                            {'name': 'hashKey',
                                             'value': '',
                                             'label': 'Hash Key Column'}],
                         'partitionInputKind': ['PartitionByAny'],
                         'orderByColumn': '',
                         'partitionAttributes': '',
                         'unaliased_inputs': {'count': 1.0,
                                              'values': ['dss_nb_iris_dataset_train'],
                                              'desc': {}},
                         'arguments': [{'datatype': 'COLUMNS',
                                        'isRequired': False,
                                        'allowsLists': True,
                                        'name': 'CATEGORICALINPUTS',
                                        'value': ''},
                                       {'datatype': 'COLUMNS',
                                        'isRequired': False,
                                        'allowsLists': True,
                                        'name': 'NUMERICINPUTS',
                                        'value': ['sepal_length',
                                                  'sepal_width',
                                                  'petal_length',
                                                  'petal_width']},
                                       {'datatype': 'COLUMNS',
                                        'isRequired': True,
                                        'allowsLists': False,
                                        'name': 'RESPONSE',
                                        'value': 'species'}],
                         'cascaded_functions': [{'name': 'NAIVEBAYESMAP',
                                                 'arguments_clauses': ['CATEGORICALINPUTS',
                                                                       'NUMERICINPUTS',
                                                                       'RESPONSE']},
                                                {'arguments_clauses': [],
                                                 'arguments_nonuserdefined': [],
                                                 'name': 'NAIVEBAYESREDUCE',
                                                 'partitionBy': {'isSetByUser': False,
                                                                 'key': 'class'}}],
                         'required_input': [], 'hasInputTable': True, 'name': 'NAIVEBAYESTRAIN'}