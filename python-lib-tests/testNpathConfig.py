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

npathConfig = {'isOrdered': True,
               'name': 'NPATH',
               'partitionInputKind': ['PartitionByKey'],
               'orderByColumn': 'ts',
               'partitionAttributes': ['id'],
               'unaliased_inputs': {'count': 1.0,
                                    'values': ['tv_shows'],
                                    'desc': {}},
               'arguments': [{'datatype': 'STRING',
                              'isRequired': True,
                              'allowsLists': False,
                              'name': 'MODE',
                              'value': 'nonoverlapping'},
                             {'datatype': 'STRING',
                              'isRequired': True,
                              'allowsLists': True,
                              'name': 'PATTERN',
                              'value': 'S1{1,3}.S2'},
                             {'datatype': 'SQLEXPR',
                              'isRequired': True,
                              'allowsLists': True,
                              'name': 'SYMBOLS',
                              'value': "tvshow='BreakingBad' as S2\x00tvshow <> 'BreakingBad' as S1"},
                             {'datatype': 'SQLEXPR',
                              'isRequired': True,
                              'allowsLists': True,
                              'name': 'RESULT',
                              'value': 'accumulate(tvshow of any(S1,S2)) as path'}],
               'required_input': [],
               'hasInputTable': True,
               'asterarguments': [{'name': 'schema',
                                   'value': '',
                                   'label': 'Schema'},
                                  {'name': 'outputType',
                                   'value': '',
                                   'label': 'Output Table Type'},
                                  {'name': 'hashKey',
                                   'value': '',
                                   'label': 'Hash Key Column'}]}