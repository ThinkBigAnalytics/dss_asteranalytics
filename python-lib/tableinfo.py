class tableinfo(object):
    def __init__(self, connectioninfo):
        self._schemaname = "public" if not connectioninfo.schema else connectioninfo.schema
        self._tablename = connectioninfo.table
        
    @property
    def tablename(self):
        return ".".join([self._schemaname, self._tablename])