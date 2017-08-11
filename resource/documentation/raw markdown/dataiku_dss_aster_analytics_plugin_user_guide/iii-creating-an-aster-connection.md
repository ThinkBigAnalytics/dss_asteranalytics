# III. Creating an Aster Connection

---

1.    Follow the instructions in the Dataiku Reference Doc for Installing Database Drivers.
    In summary, one needs to:
    
        a.    Stop the Data Science Studio server, where DATA_DIR is the data directory where Data Science Studio is installed.
        
        &nbsp;    `DATA_DIR/bin/dss stop`
        
        b.    Copy the Aster JDBC driver to DATA_DIR/lib/jdbc directory.
        &nbsp;    
        
        c.    Restart Data Science Studio        
        &nbsp;    `DATA_DIR/bin/dss start`
        
2.    In the Dataiku DSS home page, click on Admin Tools (gear icon). Alternatively, you can go to http://dataikuhost:port/admin/.        

    ![](/assets/1.png)
    
3.    In the DSS settings page, Connections tab, Click on NEW CONNECTION. From the options that will be presented, choose Other SQL databases.

    ![](/assets/2.png)
    
4.    Fill up the following fields as appropriate:    

        **JDBC driver class**: com.asterdata.ncluster.Driver    
        **JDBC URL**: jdbc:ncluster://<queen host>:<port>/<database>    
        **JDBC properties**:
	    user:       username
	    password:	 password
        **SQL dialect (experimental)**: Aster Data
        **Naming rules for new datasets**:
	    Schema:	schema_name
	
5.    Click on Test button to verify that connection details provided in step 3 are valid.
6.	Finally, click on Save button.
