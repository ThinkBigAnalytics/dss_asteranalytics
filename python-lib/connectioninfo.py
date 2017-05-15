class connectioninfo:
    def __init__(self, dataikuproject, dsstablename):
        # You are not checking whether dsstablename is actually of the form schema.tablename
        tablename = dsstablename.split('.')[1] if dsstablename else ""
        if (dataikuproject):
            datasetconfig = next(i for i in dataikuproject.list_datasets() if i['name'] == tablename)
            self.__configparams = datasetconfig['params']
        else:
            self.__configparams = {}
        
    @property
    def table(self):
        return self.__configparams['table']
    
    @property
    def schema(self):
        return "public" if 'schema' not in self.__configparams else self.__configparams['schema']
    
    @table.setter
    def table(self,value):
        self.__configparams['table'] = value
        
    @schema.setter
    def schema(self, value):
        self.__configparams['schema'] = value