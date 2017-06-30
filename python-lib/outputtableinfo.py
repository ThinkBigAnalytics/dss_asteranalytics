import tableinfo

class outputtableinfo(tableinfo.tableinfo):
    def __init__(self, connectioninfo, datasetname, config):
        super(outputtableinfo, self).__init__(connectioninfo, datasetname)
        self.__distributionType = config.get('distribution', 'DIMENSION').upper()
        self.__distributionKey = config.get('distribution_key', '')
        
    @property
    def tableType(self):
        return self.__distributionType or 'DIMENSION'
       
    @property
    def hashKey(self):
        return '' if 'DIMENSION' == self.__distributionType else self.__distributionKey
