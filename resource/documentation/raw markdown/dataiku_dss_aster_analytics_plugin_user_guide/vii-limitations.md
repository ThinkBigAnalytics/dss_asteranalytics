#  VII. Limitations

---

1.    As of this writing, Aster is not an officially supported database in Dataiku. Some tables, those with special characters in column names in particular, may not be properly imported into datasets. This is not a major problem since all SQL-MR functions are performed in the Aster environment and not in the Dataiku virtual machine.

2.    DISTRIBUTE BY HASH error is encountered when creating new datasets manually in Dataiku. To work around this issue, go to the Settings page of the newly created dataset. In the SQL section, set table creation mode to Manually define. Then, set table creation SQL to CREATE TABLE "<tablename>" ($DKU_CREATE_TABLE_FIELDS) DISTRIBUTE BY HASH(<hash_column>)
This error is not encountered when creating output datasets through the Create Recipe popup.

3.    For SQL-MR functions that take in output table names as arguments and where the select query produces only a message table indicating the name of the output model/metrics table, it is the responsibility of the user to specify output table names that are not the same with that of an existing table. Some SQL-MR functions provide an option to delete an already existing output table prior to executing an algorithm, others do not. If the former is the case, Aster Database throws an ‘<output table> already exists’ exception.

4.    The appended version of the Dataiku DSS Aster Analytics plugin was tested against Aster 6.20 SQL-MR functions. Earlier or later function versions may require different functions metadata.

5.    In case HTTP error 413 (Request entity too large) or HTTP error 414 (Request URI too long) is encountered after reloading a saved recipe in Dataiku versions earlier than 4.0.4, one can edit Dataiku’s code itself. This is an issue that will be resolved in Dataiku’s next release. To fix this without updating Dataiku, open INSTALL_DIR/frontend/static/dataiku/js/mainpack.js. Locate the  callPythonDo function, and change the HTTP method associated with it from GET to POST.

6.    As of this writing, Aster Analytics plugin could only refer to SQL-MR functions installed in the public schema.
