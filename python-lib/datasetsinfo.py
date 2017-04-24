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