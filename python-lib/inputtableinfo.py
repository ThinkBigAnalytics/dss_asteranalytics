import tableinfo
from pseudoconstantgetters import *

class inputtableinfo(tableinfo.tableinfo):
    def __init__(self, connectioninfo, datasetname, dss_function):
        super(inputtableinfo, self).__init__(connectioninfo, datasetname)
        self.__partitionKey = self.__getPartitionKeyFromFunctionDef(dss_function)
        self.__orderKey = self.__getOrderByKeyFromInputDef(dss_function)
        self.__dssfunction = dss_function
        self.__alias = ''
        
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
    
    @property
    def alias(self):
        return self.__alias

    def setPropertiesFromDef(self, inputdef):
        tablealias = inputdef.get('name', '')
        self.__alias = '' if 'Dimension' == tablealias else tablealias
        self.__partitionKey = self.__getPartitionClauseFromInputDef(
            inputdef.get('kind', 'DSSOTHERS'), inputdef)
        self.__orderKey = self.__getOrderByKeyFromInputDef(inputdef)

    def __getPartitionAttributes(self, inputdef):
        return ', '.join(inputdef.get('partitionAttributes', []))

    def __getPartitionClauseFromInputDef(self, kind, inputdef):
        return getPartitionKind(kind) +\
            (self.__getPartitionAttributes(inputdef) if 'PartitionByKey' == kind else '')

    def __getPartitionKeyFromFunctionDef(self, dss_function):
        # partition
        kind = next(iter(dss_function.get("partitionInputKind",[])),'DSSOTHERS')
        return self.__getPartitionClauseFromInputDef(kind, dss_function)

    def __getOrderByKeyFromInputDef(self, inputdef):
        #no empty string checking for orderByColumn since this is mandatory if isOrdered is true
        return inputdef.get("orderByColumn", "")
