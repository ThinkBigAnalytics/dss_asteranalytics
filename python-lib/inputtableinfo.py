import tableinfo

class inputtableinfo(tableinfo.tableinfo):
    def __init__(self, connectioninfo, datasetname, dss_function):
        super(inputtableinfo, self).__init__(connectioninfo, datasetname)
        self.__partitionKey = self.__getPartitionKeyFromFunctionDef(dss_function)
        self.__orderKey = self.__getOrderByKeyFromFunctionDef(dss_function)
        self.__dssfunction = dss_function
        
    @property
    def schemaname(self):
        return self._schemaname

    @property
    def tablenamewithoutschema(self):
        return self._tablename

    @property
    def partitionKey(self):
        return self.__partitionKey

    @property
    def orderKey(self):
        return self.__orderKey

    def __getPartitionKeyFromFunctionDef(self, dss_function):
        # partition
        partitionInputKind = dss_function.get("partitionInputKind","")
        partitionKeys = ""
        if "PartitionByAny" in partitionInputKind:
            partitionKeys = "ANY"
        elif "PartitionByKey" in partitionInputKind:
            partitionKeys = ", ".join(dss_function["partitionAttributes"])
        elif "PartitionByOne" in partitionInputKind:
            partitionKeys = "1"
        return partitionKeys

    def __getOrderByKeyFromFunctionDef(self, dss_function):
        #no empty string checking for orderByColumn since this is mandatory if isOrdered is true
        return dss_function.get("orderByColumn", "")