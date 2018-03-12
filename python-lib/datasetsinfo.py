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

class datasetsinfo:
    def __init__(self, inputTable, outputTable):
        self.__inputTable = inputTable
        self.__outputTable = outputTable
    
    # input table properties, use getter at functions to extend to multiple input    
    @property
    def inputTableName(self):
        return self.__inputTable.tablename
    
    @property
    def inputTablePartitionKey(self):
        return self.__inputTable.partitionKey
    
    @property
    def inputTableOrderKey(self):
        return self.__inputTable.orderKey
    
    # output table properties
    @property
    def outputTableName(self):
        return self.__outputTable.tablename
    
    @property
    def outputTableType(self):
        return self.__outputTable.tableType
    
    @property
    def outputTableHashKey(self):
        return self.__outputTable.hashKey