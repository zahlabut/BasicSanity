import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from TrafficTypes import *
from APIs import *


### In case when Jenkins JOB is configured to use NV as remote proxy ###
NV_IS_USED_AS_PROXY=False
NV_IP='52.3.119.102'
NV_PORT='65000'
WGET_PROXIES = {'http': 'http://' + NV_IP + ':' + str(NV_PORT), 'https': 'https://' + NV_IP + ':' + str(NV_PORT)}


######################################################################

import random
try:
    import unittest2 as unittest
except ImportError:
    import unittest

class SimpleTest(unittest.TestCase):

    def test_YNET_WGET(self):
        if NV_IS_USED_AS_PROXY==True:
            print WGET_PROXIES
            get_result=HTTP_GET_SITE('http://www.cnn.com',1,WGET_PROXIES)
        else:
            get_result=HTTP_GET_SITE('http://www.cnn.com',1)
        PRINT_DICT(get_result)
        execution_time=get_result['Traffic_Execution_Time_[sec]']
        status_code=get_result['Status_Code']
        expected_execution_time=30
        self.assertGreater(expected_execution_time,execution_time,'Execution time: '+str(execution_time)+' is > than '+str(expected_execution_time)+'!!!')

