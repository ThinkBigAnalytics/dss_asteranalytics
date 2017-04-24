class connectioninfo:
    def __init__(self, dataikuproject, dsstablename):
        # You are sure that a dataset has the keys name, params, and table
        # That's why you are doing null checking. It's bad practice.
        # But you know they never will be null
        tablename = dsstablename.split('.')[1]
        datasetconfig = next(i for i in dataikuproject.list_datasets() if i['name'] == tablename)
        self.__configparams = datasetconfig['params']
        
    @property
    def table(self):
        return self.__configparams['table']
    
    @property
    def schema(self):
        return "public" if 'schema' not in self.__configparams else self.__configparams['schema']