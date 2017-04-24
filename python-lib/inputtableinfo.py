import tableinfo

class inputtableinfo(tableinfo.tableinfo):
    def __init__(self, connectioninfo, dss_function):
        super(inputtableinfo, self).__init__(connectioninfo)
        self.__partitionKey = self.__getPartitionKeyFromFunctionDef(dss_function)
        self.__orderKey = self.__getOrderByKeyFromFunctionDef(dss_function)
        
    @property
    def tablename(self):
        return """(SELECT 1)""" if not self._tablename else ".".join([self._schemaname,
                                                                       self._tablename])
        
    @property
    def partitionKey(self):
        return self.__partitionKey
    
    @property
    def orderKey(self):
        return self.__orderKey
    
    def __getPartitionKeyFromFunctionDef(self, dss_function):
        # partition
        partitionInputKind = dss_function.get("partitionInputKind","")
        hasInputTable = dss_function.get("hasInputTable", True)
        partitionKeys = ""
        if not hasInputTable:
            partitionKeys = "1"
        elif "PartitionByAny" in partitionInputKind:
            partitionKeys = "ANY"
        elif "PartitionByKey" in partitionInputKind:
            partitionKeys = dss_function["partitionAttributes"]
        elif "PartitionByOne" in partitionInputKind:
            partitionKeys = "1"
        return partitionKeys
    
    def __getOrderByKeyFromFunctionDef(self, dss_function):
        #no empty string checking for orderByColumn since this is mandatory if isOrdered is true
        return dss_function.get("orderByColumn", "")