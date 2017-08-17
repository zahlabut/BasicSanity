import os, sys
import os.path
my_path=os.path.abspath('.')

up_dir_path=os.path.abspath(os.path.join(my_path, os.pardir))
sys.path.append(up_dir_path)

from APIs import *
from TrafficTypes import *



# if 'linux' not in platform.system().lower():
#     print 'This script is for Linux OS only!!!'
#     sys.exit(1)



######################################################################
exceptions_file='Exceptions.log'
api_log_file='APIs_Results.csv'
### For TM Sanity ###
TM_IP= '127.0.0.1'
TM_PORT= '8182'
#TM_USER= 'admin123'
#TM_PASSWORD= 'Admin123'

# TM_USER= 'admin123'
# TM_PASSWORD= 'Admin123'


TM_USER= 'NVintegrator'
TM_PASSWORD= 'Shunra_pwd1'



SAVE_CAPTURE=False
SAVE_SCREENSHOT=True
DELETE_TEST=True
TM_IS_HTTPS=False
######################################################################




print '\r\n'*10
print '#'*80
nv_feauture_is=CHOOSE_OPTION_FROM_LIST_1(['on','off'],'NV Latency Compensation is?')
configure_nv_delay=raw_input('Configure NV delay in msec:')
test_domain=raw_input('Enter your test domain:')
number_of_request=raw_input('Enter the number of requests to send:')
### Traffic without emulation
icmp_without_emulation=PING_HOST(test_domain, int(number_of_request), 0)
print icmp_without_emulation
socket_without_emulation=OPEN_AND_CLOSE_TCP_SOCKET(test_domain,loop_number=int(number_of_request))
print socket_without_emulation


### Start Emulation
start_result=START_DEFAULT_TEST(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, 'My_Flow', configure_nv_delay, '0.1', '2048.0', '2048.0', 'Latency_Compensation_'+str(time.time()), 'Stam')
print start_result
token=eval(start_result['Content'])["testToken"]


### Traffic within emulation
time.sleep(3)
icmp_with_emulation=PING_HOST(test_domain, int(number_of_request), 1)
socket_with_emulation=OPEN_AND_CLOSE_TCP_SOCKET(test_domain,loop_number=int(number_of_request),delay=1)
time.sleep(3)

### Stop emulation
STOP_TEST_BY_TOKEN(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token)


test_configuration={
    'Configured Latency:':configure_nv_delay,
    'Tested Domain':test_domain,
    'Number of Pings':number_of_request}

ping_result_dic={
    'PING - No Emulation':icmp_without_emulation['Average_Response_Time_[msec]'],
    'PING - With Emulation':icmp_with_emulation['Average_Response_Time_[msec]']}
if nv_feauture_is=='on':
    ping_result_dic['Expected latency']=int(configure_nv_delay)*2
if nv_feauture_is=='off':
    ping_result_dic['Expected latency']=int(configure_nv_delay)*2+icmp_without_emulation['Average_Response_Time_[msec]']

create_socket_result={
    'Create TCP socket - No Emulation':socket_without_emulation['Socket_Connect_Average_Time[msec]'],
    'Create TCP socket - With Emulation':socket_with_emulation['Socket_Connect_Average_Time[msec]']}
if nv_feauture_is=='on':
    create_socket_result['Expected latency']=int(configure_nv_delay)*2
if nv_feauture_is=='off':
    create_socket_result['Expected latency']=int(configure_nv_delay)*2+socket_without_emulation['Socket_Connect_Average_Time[msec]']

### Print Results Summary ***
print '\r\n'*10
PRINT_DICT(test_configuration)
PRINT_DICT(ping_result_dic)
PRINT_DICT(create_socket_result)

