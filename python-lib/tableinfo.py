class tableinfo(object):
    def __init__(self, connectioninfo, datasetname):
        self._schemaname = "public" if not connectioninfo.get('schema', "") else connectioninfo['schema']
        self._tablename = connectioninfo['table']
        self._datasetname = datasetname
        
    @property
    def tablename(self):
        return ".".join(['"{}"'.format(self._schemaname),
                         '"{}"'.format(self._tablename)])
    
    @property
    def datasetname(self):
        dname = self._datasetname.split('.')
        return dname[len(dname) - 1] if dname else ""
