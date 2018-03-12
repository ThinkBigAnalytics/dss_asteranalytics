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