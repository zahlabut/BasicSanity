import os, sys
import os.path
my_path=os.path.abspath('.')

up_dir_path=os.path.abspath(os.path.join(my_path, os.pardir))
sys.path.append(up_dir_path)

from APIs import *
from TrafficTypes import *


######################################################################
ynet_ip='23.38.111.151'
msn_ip='13.82.28.61'
source_port_to_bind=65000
exceptions_file='Exceptions.log'
api_log_file='APIs_Results.csv'
### For TM Sanity ###
TM_IP= '127.0.0.1'
TM_PORT= '8182'
TM_USER= 'admin123'
TM_PASSWORD= 'Admin123'
SAVE_CAPTURE=False
SAVE_SCREENSHOT=True
DELETE_TEST=True
TM_IS_HTTPS=False
######################################################################


scenario=['Reuse', 'Normal']
for s in scenario:
    print '\r\n'*10
    print '#'*80
    print 'Scenario is: '+s
    start_result=START_DEFAULT_TEST(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, 'My_Flow', '20', '0.1', '2048.0', '2048.0', 'SourcePortReuseBug_'+s, 'Stam')
    token=eval(start_result['Content'])["testToken"]
    print token
    print HTTP_GET_SOCKET(ynet_ip,80,1,source_port=source_port_to_bind, path_to_request='index.html')
    time.sleep(10)
    if s=='Reuse':
        print HTTP_GET_SOCKET(ynet_ip,80,1,source_port=source_port_to_bind, path_to_request='zababun.html')
    if s=='Normal':
        print HTTP_GET_SOCKET(ynet_ip,80,1,source_port=source_port_to_bind-1, path_to_request='zababun.html')
    time.sleep(3)
    STOP_TEST_BY_TOKEN(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token)







