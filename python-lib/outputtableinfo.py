import tableinfo

class outputtableinfo(tableinfo.tableinfo):
    def __init__(self, connectioninfo, dss_function):
        super(outputtableinfo, self).__init__(connectioninfo)
        self.__asterArgs = self.__getAsterArgsFromFunctionDef(dss_function)
        
    @property
    def tableType(self):
        return self.__asterArgs.get("outputType", "")
    
    @tableType.setter
    def tableType(self,value):
        self.__asterArgs["outputType"] = value
    
    @property
    def hashKey(self):
        return self.__asterArgs.get("hashKey", "")
    
    def __getAsterArgsFromFunctionDef(self, dss_function):
        # ASTER arguments (schema, output table type, hash key)
        aster_args = {}
        for argument in dss_function["asterarguments"]:
            aster_args[argument["name"]] = argument["value"] if 'value' in argument else ""
        return aster_args
    