# II. Requirements

---

1. **Dataiku Data Science Studio version 4.0.1 or later**

   Dataiku DSS enterprise edition is required to import datasets from Aster tables. Dataiku offers both downloadable and online options which can be     obtained from their company [website](https://www.dataiku.com/dss/trynow/). The downloadable option can be configured to use the free or the enterprise edition, while the online option only comes in enterprise edition with free trial for a period of 14 days. A comparison between the two editions can be seen in the features table for [Dataiku DSS Editions](https://www.dataiku.com/dss/editions/).

   Teradata Aster Analytics plugin has been tested on Dataiku DSS version 4.0.1.  
   &nbsp; 

2. **Aster Analytics Plugin**

   AsterAnalytics.zip contains the Aster Analytics plugin program and metadata. Please see Appendix A section to obtain a copy of this plugin.   
   &nbsp;  

3. **Access Credentials**

   The first set of credentials required is the Aster Credentials which allow the user to read and write tables into an Aster Database. These credentials are used as input to the Dataiku-Aster connector. Section 3 provides instructions on how to setup a Dataiku connection to an Aster database. It is suggested to create one connection per database schema where one intends to store output tables.

   The next set is the Dataiku User Credentials which allow the user to login to     Dataiku DSS. Section 4 outlines the steps in creating a user in Dataiku.  
   &nbsp;  

4. **Aster JDBC Driver**

   The Aster JDBC Driver is required to establish a connection between an Aster Database and Dataiku. A copy of the jar file for the driver is appended to this document \(Appendix B\).



