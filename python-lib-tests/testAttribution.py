'''
Created on May 15, 2017

@author: dt186022
'''

import unittest
from querybuilderfacade import *
from testAttributionConfig import *
from inputtableinfo import *
from outputtableinfo import *

class TestAttribution(unittest.TestCase):
    
    def createTable(self, config, metadata, mode='input'):
        if 'output' == mode:
            return outputtableinfo(config, config.get('dataset',""), metadata)
        return inputtableinfo(config, config.get('table',""),metadata)

    def testAttribution(self):
        functionFirstInputTable = self.createTable({'table': 'attribution_sample_table1', 'schema': 'dss'},
                                              attributionMultiVersionConfig)
        functionSecondInputTable = self.createTable({'table': 'attribution_sample_table2', 'schema': 'dss'},
                                               attributionMultiVersionConfig)
        functionOutputTable = self.createTable({'table': 'attributionoutput'},
                                          attributionMultiVersionConfig,
                                          'output')
        conversionEventTable = self.createTable({'table':'conversion_event_table', 'schema':'dss'},
                                           attributionMultiVersionConfig)
        excludingEventTable = self.createTable({'table':'excluding_event_table', 'schema':'dss'},
                                           attributionMultiVersionConfig)
        optionalEventTable = self.createTable({'table':'optional_event_table', 'schema':'dss'},
                                           attributionMultiVersionConfig)
        firstModelTable = self.createTable({'table':'model1_table', 'schema':'dss'},
                                           attributionMultiVersionConfig)
        secondModelTable = self.createTable({'table':'model2_table', 'schema':'dss'},
                                           attributionMultiVersionConfig)
        actualquery = getFunctionsQuery(attributionMultiVersionConfig,
                                        [functionFirstInputTable,
                                         functionSecondInputTable,
                                         conversionEventTable,
                                         excludingEventTable,
                                         optionalEventTable,
                                         firstModelTable,
                                         secondModelTable],
                                        functionOutputTable)
        expectedquery = """BEGIN TRANSACTION;
DROP TABLE IF EXISTS public.attributionoutput;
CREATE DIMENSION TABLE public.attributionoutput
AS
SELECT *
FROM   ATTRIBUTION
(
ON dss.attribution_sample_table1 PARTITION BY user_id ORDER BY time_stamp
ON dss.attribution_sample_table2 PARTITION BY user_id ORDER BY time_stamp
ON dss.conversion_event_table AS "conversion" DIMENSION
ON dss.excluding_event_table AS "excluding" DIMENSION
ON dss.optional_event_table AS "optional" DIMENSION
ON dss.model1_table AS "model1" DIMENSION
ON dss.model2_table AS "model2" DIMENSION
EVENT_COLUMN_NAME('event')
TIMESTAMP_COLUMN_NAME('time_stamp')
WINDOW('rows:10&seconds:20')

);
COMMIT;
END TRANSACTION;"""
        self.assertEqual('\n'.join(actualquery) + '\nEND TRANSACTION;', expectedquery, "Attribution")
        