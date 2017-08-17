### Copy and paste MonitoringOptMyApp.py content ###
import unittest
import warnings
from TrafficTypes import *
cur_path=os.path.abspath('.')
sys.path.append(cur_path)
from APIs import *
from HP_Functions import *
### Run Cleaner ###
if 'linux' in platform.system().lower() and SAVE_CAPTURE==True:
    os.system('sudo python Cleaner.py')
else:
    os.system('python Cleaner.py')



### Runtime Log ###
RunTimeLog='Runtime.log'
DELETE_LOG_CONTENT(RunTimeLog)
sys.stdout=MyOutput(RunTimeLog)
sys.stderr=MyOutput(RunTimeLog)

class MC_NV_Monitoring(unittest.TestCase):

    def setUp(self):
        MC_NV_Monitoring.test_name=[]

    def test___1_Get_Version_API___(self):
        print '-'*40+'test___1_Get_Version_API___'+'-'*40
        MC_NV_Monitoring.test_name.append('test___1_Get_Version_API___')
        get_version=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='GET',url_path='shunra/api/configuration/version',
                         additional_headers={'Accept':'application/json'}, api_name='GET_VERSION')
        get_version_response=get_version.RUN_REQUEST()
        #PRINT_DICT(get_version_response)
        self.assertEqual(get_version_response['Status_Code'],200,'ACHTUNG !!! - '+'Received status code is: '+str(get_version_response['Status_Code']))
        self.assertEqual(IS_JSON(get_version_response['Content']),True,'ACHTUNG !!! - '+'Received content is not JSON!!!')
        self.assertIn('versionProperties',get_version_response['Content'],'ACHTUNG !!! - '+'"versionProperties" key was not found in API Received content is API response!!!')
        self.assertLess(get_version_response['Execution_Time'], API_EXECUTION_TIME_THRESHOLD, 'ACHTUNG !!! - API execution took: ' +str(get_version_response['Execution_Time'])+' API threshold was reached!!!')
        print 'Test --> PASS'





    def test___2_API_Get_Configuration_Settings___(self):
        print '-'*40+'test___2_API_Get_Configuration_Settings___'+'-'*40
        MC_NV_Monitoring.test_name.append('test___2_API_Get_Configuration_Settings___')
        # Get configuration settings #
        get_settings=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='GET',url_path='shunra/api/configuration/settings',
                             additional_headers={'Accept':'application/json'}, api_name='GET_SETTINGS')
        get_settings_response=get_settings.RUN_REQUEST()
        #PRINT_DICT(get_settings_response)
        self.assertEqual(get_settings_response['Status_Code'],200,'ACHTUNG !!! - '+'Received status code is: '+str(get_settings_response['Status_Code']))
        self.assertEqual(IS_JSON(get_settings_response['Content']),True,'ACHTUNG !!! - '+'Received content is not JSON!!!')
        self.assertIn('startedSessions',get_settings_response['Content'],'ACHTUNG !!! - '+'"startedSessions" key was not found in API Received content is API response!!!')
        self.assertLess(get_settings_response['Execution_Time'], API_EXECUTION_TIME_THRESHOLD, 'ACHTUNG !!! - API execution took: ' +str(get_settings_response['Execution_Time'])+' API threshold was reached!!!')
        print 'Test --> PASS'



    def test___3_API_Get_Profiles___(self):
        print '-'*40+'test___3_API_Get_Profiles___'+'-'*40
        MC_NV_Monitoring.test_name.append('test___3_API_Get_Profiles___')
        get_profiles=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='GET',url_path='shunra/api/profile',
                             additional_headers={'Accept':'application/json'}, api_name='GET_PROFILES')
        get_profiles_response=get_profiles.RUN_REQUEST()
        #PRINT_DICT(get_profiles_response)
        self.assertEqual(get_profiles_response['Status_Code'],200,'ACHTUNG !!! - '+'Received status code is: '+str(get_profiles_response['Status_Code']))
        self.assertEqual(IS_JSON(get_profiles_response['Content']),True,'ACHTUNG !!! - '+'Received content is not JSON!!!')
        self.assertIn('profiles',get_profiles_response['Content'],'ACHTUNG !!! - '+'"profiles" key was not found in API Received content is API response!!!')
        self.assertLess(get_profiles_response['Execution_Time'], API_EXECUTION_TIME_THRESHOLD, 'ACHTUNG !!! - API execution took: ' +str(get_profiles_response['Execution_Time'])+' API threshold was reached!!!')
        MC_NV_Monitoring.profiles=get_profiles_response['Content_As_Dict']['profiles']
        print 'Test --> PASS'


    def test___4_E2E_Transaction_Mode_and_APIs_are_Asynchronous____(self):
        print '-'*40+'test___4_E2E_Transaction_Mode_and_APIs_are_Asynchronous____'+'-'*40
        MC_NV_Monitoring.test_name.append('test___4_E2E_Transaction_Mode_and_APIs_are_Asynchronous____')
        prof=random.choice(MC_NV_Monitoring.profiles)
        profile_id=prof['id']
        network_scenario=prof['name']
        test_name=prof['name'].replace(' ','_')+'_'+str(time.time())
        device_id='zababun_device_id_123'
        flow_id='zababun_flow_id_123'
        src_ip=GET_MY_PUBLIC_IP()
        pl_id='zababun_pl_id_123'
        test_description='zababun_test_description'
        start_post_data={"deviceId": device_id,
                         "flows":[{"flowId": flow_id, "srcIp": src_ip, "profileId": profile_id, "isCaptureClientPL": True}],
                         "testMetadata": {"testName":test_name, "description": test_description, "networkScenario": network_scenario}}
        start_obj=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='POST',url_path='shunra/api/emulation/custom',
                          additional_headers={'Accept':'application/json','Content-Type':'application/json'},params={'mode':'MULTI_USER','useProxy':'true'},request_payload=start_post_data, api_name='START_API')
        start_resp=start_obj.RUN_REQUEST()
        #PRINT_DICT(start_resp)
        self.assertEqual(start_resp['Status_Code'],201,'ACHTUNG !!! - '+'Received status code for START_API is: '+str(start_resp['Status_Code']))
        self.assertEqual(IS_JSON(start_resp['Content']),True,'ACHTUNG !!! - '+'Received content is not JSON!!!')
        self.assertIn('testToken',start_resp['Content'],'ACHTUNG !!! - '+'"testToken" key was not found in API Received content is API response!!!')
        self.assertLess(start_resp['Execution_Time'], API_EXECUTION_TIME_THRESHOLD, 'ACHTUNG !!! - API execution took: ' +str(start_resp['Execution_Time'])+' API threshold was reached!!!')
        test_token=start_resp['Content_As_Dict']['testToken']
        proxy_ip=start_resp['Content_As_Dict']['proxyIpAddr']
        proxy_port=start_resp['Content_As_Dict']['proxyPort']
        cert_url=start_resp['Content_As_Dict']['certUrl']
        DELAY(5)


        ### Use NV certificate ###
        get_cert_result=HTTP_GET_SITE(cert_url,1)
        PRINT_DICT(get_cert_result)
        self.assertEqual(get_cert_result['Status_Code'],200,'ACHTUNG !!! - failed to download NV certificate, received HTTP response code: '+str(get_cert_result['Status_Code'])+' !!!')
        DELAY(5)

        # Set proxies #
        WGET_PROXIES = {'http': 'http://' + proxy_ip + ':' + str(proxy_port), 'https': 'https://' + proxy_ip + ':' + str(proxy_port)}
        SELENIUM_PROXY=proxy_ip+':'+str(proxy_port)
        SPEC_PRINT([str(WGET_PROXIES),cert_url])

        # Realtime update #
        random_profile=prof
        while prof==random_profile:
            random_profile=random.choice(MC_NV_Monitoring.profiles)
        profile_id=random_profile['id']
        network_scenario=random_profile['name']
        real_time_update_post_data={ "testMetadata": { "networkScenario": network_scenario}, "flows": [{ "profileId": profile_id, "isDefaultFlow": "true", "flowId":flow_id}]}
        real_time_update_obj=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='PUT',url_path='shunra/api/emulation/custom/'+test_token,
                          additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload=real_time_update_post_data,api_name='REAL_TIME_UPDATE')
        real_time_update_resp=real_time_update_obj.RUN_REQUEST()
        #PRINT_DICT(real_time_update_resp)
        self.assertEqual(real_time_update_resp['Status_Code'],200,'ACHTUNG !!! - '+'Received status code for REAL_TIME_UPDATE is: '+str(start_resp['Status_Code']))
        self.assertLess(real_time_update_resp['Execution_Time'], API_EXECUTION_TIME_THRESHOLD, 'ACHTUNG !!! - API execution took: ' +str(real_time_update_resp['Execution_Time'])+' API threshold was reached!!!')
        DELAY(5)

        # Connect #
        connect_post_data={}
        connect_payload_options=[{"overwriteExistingConnection":"true"},
                                 {"plId":pl_id,"overwriteExistingConnection":"true"},
                                 {"clientId":src_ip, "overwriteExistingConnection":"true"},
                                 {"flowId":flow_id, "overwriteExistingConnection":"true"},
                                 {}
                                 ]
        connect_results=[]
        for connect_option in connect_payload_options:
            #SPEC_PRINT([str(connect_option)])
            connect_obj=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='POST',url_path='shunra/api/transactionmanager/'+test_token,
                        additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload=connect_option, body_type='JSON',api_name='CONNECT_FOR_TRANSACTIONS')
            connect_resp=connect_obj.RUN_REQUEST()
            #print connect_resp['Content_As_Dict']
            transaction_id=connect_resp['Content_As_Dict']['transactionManagerSessionIdentifier']
            #PRINT_DICT(connect_resp)
            connect_results.append(transaction_id)
            self.assertEqual(connect_resp['Status_Code'],200,'ACHTUNG !!! - '+'Received status code for CONNECT_FOR_TRANSACTIONS is: '+str(connect_resp['Status_Code']))
            self.assertEqual(IS_JSON(connect_resp['Content']),True,'ACHTUNG !!! - '+'Received content is not JSON!!!')
            self.assertLess(start_resp['Execution_Time'], API_EXECUTION_TIME_THRESHOLD, 'ACHTUNG !!! - API execution took: ' +str(connect_resp['Execution_Time'])+' API threshold was reached!!!')
            DELAY(5)



        # Transactions X in total #
        completed_transactions=[]
        for x in range(1,4):
            # Transaction Start #
            start_transaction_data={"transactionName":"Trans_"+str(x), "transactionDescription":"Monitoring_Script_transaction_"+str(x)}
            start_trans_obj=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='POST',url_path='shunra/api/transactionmanager/transaction/'+transaction_id,
                            additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload=start_transaction_data, body_type='JSON', api_name='START_TRANSACTION')
            start_trans_resp=start_trans_obj.RUN_REQUEST()
            #PRINT_DICT(start_trans_resp)
            self.assertEqual(start_trans_resp['Status_Code'],200,'ACHTUNG !!! - '+'Received status code for START_TRANSACTION is: '+str(start_trans_resp['Status_Code']))
            self.assertEqual(IS_JSON(start_trans_resp['Content']),True,'ACHTUNG !!! - '+'Received content is not JSON!!!')
            self.assertIn('testToken',start_trans_resp['Content'],'ACHTUNG !!! - '+'"testToken" key was not found in API Received content is API response!!!')
            self.assertLess(start_resp['Execution_Time'], API_EXECUTION_TIME_THRESHOLD, 'ACHTUNG !!! - API execution took: ' +str(start_trans_resp['Execution_Time'])+' API threshold was reached!!!')
            DELAY(5)
            completed_transactions.append("Trans_"+str(x))

            # Traffic #
            transaction_test_site='http://facebook.com'
            retry_number=1
            interrupt_test=False
            if USE_SELENIUM==True:
                DELAY(5)
                final_url='N/A'
                while final_url=='N/A' and retry_number<4:
                    traffic_result=OPEN_WEB_SITE_SELENIUM(transaction_test_site,proxy=SELENIUM_PROXY, timeout=SELENIUM_TIMEOUT)
                    PRINT_DICT(traffic_result)
                    final_url=traffic_result['Final_URL']
                    if final_url=='N/A':
                        warnings.warn('WARNING !!! - Selenium traffic has failed, no "http" was found in "Final_URL" returned value!!!')
                        retry_number+=1
                        print 'Retry number: '+str(retry_number)
                        time.sleep(5)
                #self.assertIn('http',final_url,'ACHTUNG !!! - Selenium traffic has failed, no "http" was found in "Final_URL" returned value!!!')
                if 'http' not in final_url:
                    print 'ACHTUNG !!! - Selenium traffic has failed, no "http" was found in "Final_URL" returned value!!!'
                    interrupt_test=True

            if USE_SELENIUM==False:
                DELAY(5)
                status_code=None
                while status_code==None and retry_number<4:
                    traffic_result=HTTP_GET_SITE(transaction_test_site,1,proxies=WGET_PROXIES)
                    PRINT_DICT(traffic_result)
                    if 'Status_Code' in traffic_result.keys():
                        status_code=traffic_result['Status_Code']
                    else:
                        warnings.warn('WARNING !!! - WGET traffic has failed '+str(traffic_result)+'!!!')
                        retry_number+=1
                        print 'Retry number: '+str(retry_number)
                        time.sleep(5)
                if 'HTTP_GET_SITE_Exception' in traffic_result.keys():
                    exception_string=traffic_result['HTTP_GET_SITE_Exception']
                else:
                    exception_string=None
                #self.assertNotIn('HTTP_GET_SITE_Exception', traffic_result.keys(),'ACHTUNG !!! - WGET traffic has failed '+str(exception_string)+'!!!' )
                if 'HTTP_GET_SITE_Exception' in traffic_result.keys():
                    print 'ACHTUNG !!! - WGET traffic has failed '+str(exception_string)+'!!!'
                    interrupt_test=True

            # Stop Transaction #
            #https://dev.hpenv.com/shunra/api/transactionmanager/transaction/{token}/{token}
            stop_trans_obj=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='PUT',url_path='shunra/api/transactionmanager/transaction/'+test_token+'/'+transaction_id,
                            additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload={}, body_type='JSON', api_name='STOP_TRANSACTION')
            stop_trans_resp=stop_trans_obj.RUN_REQUEST()
            #PRINT_DICT(stop_trans_resp)
            self.assertEqual(stop_trans_resp['Status_Code'],200,'ACHTUNG !!! - '+'Received status code for STOP_TRANSACTION is: '+str(stop_trans_resp['Status_Code']))
            self.assertEqual(IS_JSON(stop_trans_resp['Content']),True,'ACHTUNG !!! - '+'Received content is not JSON!!!')
            self.assertIn('testToken',stop_trans_resp['Content'],'ACHTUNG !!! - '+'"testToken" key was not found in API Received content is API response!!!')
            self.assertLess(start_resp['Execution_Time'], API_EXECUTION_TIME_THRESHOLD, 'ACHTUNG !!! - API execution took: ' +str(stop_trans_resp['Execution_Time'])+' API threshold was reached!!!')
            DELAY(5)


        # Stop Test#
        stop_put_data='''{"testTokens": ["token"]}'''.replace('token',test_token)
        stop_obj=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='PUT',url_path='shunra/api/emulation/stop',
                        additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload=stop_put_data, body_type='STRING', api_name='STOP_API')
        stop_resp=stop_obj.RUN_REQUEST()
        #PRINT_DICT(stop_resp)
        self.assertEqual(stop_resp['Status_Code'],200,'ACHTUNG !!! - '+'Received status code for STOP_API is: '+str(stop_resp['Status_Code']))
        self.assertEqual(IS_JSON(stop_resp['Content']),True,'ACHTUNG !!! - '+'Received content is not JSON!!!')
        self.assertIn('analysisResourcesLocation',stop_resp['Content'],'ACHTUNG !!! - '+'"testToken" key was not found in API Received content is API response!!!')
        self.assertLess(start_resp['Execution_Time'], API_EXECUTION_TIME_THRESHOLD, 'ACHTUNG !!! - API execution took: ' +str(stop_resp['Execution_Time'])+' API threshold was reached!!!')
        DELAY(5)

        # Analyze #
        if interrupt_test==False:
            start_sampling=time.time()
            sampling_timeout=SAMPLING_TIMEOUT
            m_status=None
            is_timeout=False
            while m_status!='Finished' and time.time()<start_sampling+sampling_timeout:
                analyze_obj=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='PUT',url_path='shunra/api/analysisexpress/analyze/'+test_token,
                                additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload={}, body_type='JSON', api_name='ANALYZE_API')
                analyze_resp=analyze_obj.RUN_REQUEST()
                m_status=analyze_resp['Content_As_Dict']['m_status']
                #SPEC_PRINT([str(analyze_resp['Content_As_Dict'])])
                #PRINT_DICT(analyze_resp)
                self.assertEqual(analyze_resp['Status_Code'],200,'ACHTUNG !!! - '+'Received status code for ANALYZE_API is: '+str(analyze_resp['Status_Code']))
                self.assertEqual(IS_JSON(analyze_resp['Content']),True,'ACHTUNG !!! - '+'Received content is not JSON!!!')
                self.assertIn('errorCode',analyze_resp['Content'],'ACHTUNG !!! - '+'"errorCode" key was not found in API received content!!!')
                self.assertLess(start_resp['Execution_Time'], API_EXECUTION_TIME_THRESHOLD, 'ACHTUNG !!! - API execution took: ' +str(stop_trans_resp['Execution_Time'])+' API threshold was reached!!!')
                if time.time()>start_sampling+sampling_timeout:
                    is_timeout=True
                time.sleep(3)
            if is_timeout==True:
                SPEC_PRINT(['Achtung, timeout of: '+str(sampling_timeout)+' was reached!!!'])


            # Get the Report # (Result is always zipped)
            #to_zip=['true','false']
            to_zip=['true']
            for zi in to_zip:
                start_sampling=time.time()
                sampling_timeout=60
                m_status='Empty'
                is_timeout=False
                while m_status=='Empty' and time.time()<start_sampling+sampling_timeout:
                    get_report_zip=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='GET',url_path='shunra/api/analysisexpress/analysis/'+test_token,
                                    additional_headers={'Accept':'application/json','Content-Type':'application/json'}, api_name='GET_REPORT', params={'zipResult':zi,'returnData':'true'})
                    report_resp=get_report_zip.RUN_REQUEST()
                    #PRINT_DICT(report_resp)
                    self.assertEqual(report_resp['Status_Code'],200,'ACHTUNG !!! - '+'Received status code for GET_REPORT_API is: '+str(report_resp['Status_Code']))
                    self.assertLess(start_resp['Execution_Time'], API_EXECUTION_TIME_THRESHOLD, 'ACHTUNG !!! - API execution took: ' +str(report_resp['Execution_Time'])+' API threshold was reached!!!')
                    if '''"m_status":"Empty"''' in report_resp['Content']:
                        m_status='Empty'
                    else:
                        m_status='Done'
                    #SPEC_PRINT([m_status])
                    time.sleep(5)
                if time.time()>start_sampling+sampling_timeout:
                    is_timeout=True
                if zi=='true' and is_timeout==False:
                    OPEN_ZIP_REPORT_WEBBROWSER(report_resp['Content'])
                    nv_html_content=UNZIP_ZIPPED_NV_REPORT(report_resp['Content'])
                if zi=='false' and is_timeout==False:
                    OPEN_REPORT_WEBBROWSER(report_resp['Content'])
                    nv_html_content=report_resp['Content']
            strings_to_validate_in_report=completed_transactions
            strings_to_validate_in_report.append(transaction_test_site.split('://')[-1].strip())
            for string in strings_to_validate_in_report:
                self.assertIn(string,nv_html_content,'ACHTUNG !!! - "'+string+'" was not found in NV report content (inside the HTML source) !!!')


            ### Get HAR Async ###
            # Get HAR #
            start_sampling=time.time()
            sampling_timeout=SAMPLING_TIMEOUT
            m_status=None
            is_timeout=False
            while m_status!='Finished' and time.time()<start_sampling+sampling_timeout:
                get_har_obj=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='PUT',url_path='shunra/api/analysisexpress/extract/har/'+test_token,
                                additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload={}, body_type='JSON', api_name='GET_HAR_ASYNCHRONOUS_API')
                get_har_resp=get_har_obj.RUN_REQUEST()
                m_status=get_har_resp['Content_As_Dict']['m_status']
                #SPEC_PRINT([str(get_har_resp['Content_As_Dict'])])
                #PRINT_DICT(get_har_resp)
                self.assertEqual(get_har_resp['Status_Code'],200,'ACHTUNG !!! - '+'Received status code for GET_HAR_API is: '+str(get_har_resp['Status_Code']))
                self.assertEqual(IS_JSON(get_har_resp['Content']),True,'ACHTUNG !!! - '+'Received content is not JSON!!!')
                self.assertIn('errorCode',get_har_resp['Content'],'ACHTUNG !!! - '+'"errorCode" key was not found in API received content!!!')
                self.assertLess(start_resp['Execution_Time'], API_EXECUTION_TIME_THRESHOLD, 'ACHTUNG !!! - API execution took: ' +str(get_har_resp['Execution_Time'])+' API threshold was reached!!!')
                if time.time()>start_sampling+sampling_timeout:
                    is_timeout=True
            if is_timeout==True:
                SPEC_PRINT(['Achtung, timeout of: '+str(sampling_timeout)+' was reached!!!'])
            # Get the HAR #
            get_har_file=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='GET',url_path='shunra/api/analysisreport/har/'+test_token,
                            additional_headers={'Accept':'application/json','Content-Type':'application/json'}, api_name='GET_READY_HAR_FILE_API')
            get_har_file_resp=get_har_file.RUN_REQUEST()
            #PRINT_DICT(get_har_file_resp)
            self.assertEqual(get_har_file_resp['Status_Code'],200,'ACHTUNG !!! - '+'Received status code for GET_HAR_ASYNCHRONOUS_API is: '+str(get_har_file_resp['Status_Code']))
            self.assertLess(start_resp['Execution_Time'], API_EXECUTION_TIME_THRESHOLD, 'ACHTUNG !!! - API execution took: ' +str(get_har_resp['Execution_Time'])+' API threshold was reached!!!')

            har_file_name='Async_Har_'+profile_id+'.zip'
            DELETE_LOG_CONTENT(har_file_name)
            INSERT_TO_LOG(har_file_name,get_har_file_resp['Content'])
            PRINT_DICT(GET_ALL_REQUEST_URLS_FROM_HAR(har_file_name, har_is_ziped=True))
            urls_in_har=GET_ALL_REQUEST_URLS_FROM_HAR(har_file_name, har_is_ziped=True)
            self.assertIn(transaction_test_site.split('://')[-1].strip(),str(urls_in_har),'ACHTUNG !!! - no transaction test URL ('+transaction_test_site+') was found in received HAR file!!!')
            print 'Test --> PASS'

    def test___5_E2E_Normal_Mode_and_APIs_are_Synchronized____(self):
        print '-'*40+'test___5_E2E_Normal_Mode_and_APIs_are_Synchronized____'+'-'*40
        MC_NV_Monitoring.test_name.append('test___5_E2E_Normal_Mode_and_APIs_are_Synchronized____')
        # This section is for testing Get Report and Get HAR in synchronous mode #
        # Start a new emulation #

        prof=random.choice(MC_NV_Monitoring.profiles)
        profile_id=prof['id']
        network_scenario=prof['name']
        test_name=prof['name'].replace(' ','_')+'_'+str(time.time())
        device_id='zababun_device_id_123'
        flow_id='zababun_flow_id_123'
        src_ip=GET_MY_PUBLIC_IP()
        pl_id='zababun_pl_id_123'
        test_description='zababun_test_description'
        start_post_data={"deviceId": device_id,
                         "flows":[{"flowId": flow_id, "srcIp": src_ip, "profileId": profile_id, "isCaptureClientPL": True}],
                         "testMetadata": {"testName":test_name, "description": test_description, "networkScenario": network_scenario}}



        start_obj_1=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='POST',url_path='shunra/api/emulation/custom',
                          additional_headers={'Accept':'application/json','Content-Type':'application/json'},params={'mode':'MULTI_USER','useProxy':'true'},request_payload=start_post_data, api_name='START_API')
        start_resp=start_obj_1.RUN_REQUEST()
        #PRINT_DICT(start_resp)
        self.assertEqual(start_resp['Status_Code'],201,'ACHTUNG !!! - '+'Received status code for START_API is: '+str(start_resp['Status_Code']))
        self.assertEqual(IS_JSON(start_resp['Content']),True,'ACHTUNG !!! - '+'Received content is not JSON!!!')
        self.assertIn('testToken',start_resp['Content'],'ACHTUNG !!! - '+'"testToken" key was not found in API Received content is API response!!!')
        self.assertLess(start_resp['Execution_Time'], API_EXECUTION_TIME_THRESHOLD, 'ACHTUNG !!! - API execution took: ' +str(start_resp['Execution_Time'])+' API threshold was reached!!!')
        test_token=start_resp['Content_As_Dict']['testToken']
        proxy_ip=start_resp['Content_As_Dict']['proxyIpAddr']
        proxy_port=start_resp['Content_As_Dict']['proxyPort']
        DELAY(5)


        # Traffic #
        # Set proxies #
        interrupt_test=False
        WGET_PROXIES = {'http': 'http://' + proxy_ip + ':' + str(proxy_port), 'https': 'https://' + proxy_ip + ':' + str(proxy_port)}
        SELENIUM_PROXY=proxy_ip+':'+str(proxy_port)
        SPEC_PRINT([str(WGET_PROXIES)])
        test_sites=['http://google.com','http://cnn.com']
        for site in test_sites:
            retry_number=0
            if USE_SELENIUM==True:
                DELAY(5)
                final_url='N/A'
                while final_url=='N/A' and retry_number<4:
                    traffic_result=OPEN_WEB_SITE_SELENIUM(site,proxy=SELENIUM_PROXY, timeout=SELENIUM_TIMEOUT)
                    PRINT_DICT(traffic_result)
                    final_url=traffic_result['Final_URL']
                    if final_url=='N/A':
                        warnings.warn('WARNING !!! - Selenium traffic has failed, no "http" was found in "Final_URL" returned value!!!')
                        retry_number+=1
                        print 'Retry number: '+str(retry_number)
                        time.sleep(5)
                #self.assertIn('http',final_url,'ACHTUNG !!! - Selenium traffic has failed, no "http" was found in "Final_URL" returned value!!!')
                if 'http' not in final_url:
                    print 'ACHTUNG !!! - Selenium traffic has failed, no "http" was found in "Final_URL" returned value!!!'
                    interrupt_test=True


            if USE_SELENIUM==False:
                DELAY(5)
                status_code=None
                while status_code==None and retry_number<4:
                    traffic_result=HTTP_GET_SITE(site,1,proxies=WGET_PROXIES)
                    PRINT_DICT(traffic_result)
                    if 'Status_Code' in traffic_result.keys():
                        status_code=traffic_result['Status_Code']
                    else:
                        warnings.warn('WARNING !!! - WGET traffic has failed '+str(traffic_result)+'!!!')
                        retry_number+=1
                        print 'Retry number: '+str(retry_number)
                        time.sleep(5)
                    if 'HTTP_GET_SITE_Exception' in traffic_result.keys():
                        exception_string=traffic_result['HTTP_GET_SITE_Exception']
                    else:
                        exception_string=None
                #self.assertNotIn('HTTP_GET_SITE_Exception', traffic_result.keys(),'ACHTUNG !!! - WGET traffic has failed '+str(exception_string)+'!!!' )
                if 'HTTP_GET_SITE_Exception' in traffic_result.keys():
                    print 'ACHTUNG !!! - WGET traffic has failed '+str(exception_string)+'!!!'
                    interrupt_test=True






        # Stop #
        stop_put_data='''{"testTokens": ["token"]}'''.replace('token',test_token)
        stop_obj_1=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='PUT',url_path='shunra/api/emulation/stop',
                        additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload=stop_put_data, body_type='STRING', api_name='STOP_API')
        stop_resp=stop_obj_1.RUN_REQUEST()
        #PRINT_DICT(stop_resp)
        self.assertEqual(stop_resp['Status_Code'],200,'ACHTUNG !!! - '+'Received status code for STOP_API is: '+str(stop_resp['Status_Code']))
        self.assertEqual(IS_JSON(stop_resp['Content']),True,'ACHTUNG !!! - '+'Received content is not JSON!!!')
        self.assertIn('analysisResourcesLocation',stop_resp['Content'],'ACHTUNG !!! - '+'"testToken" key was not found in API Received content is API response!!!')
        self.assertLess(start_resp['Execution_Time'], API_EXECUTION_TIME_THRESHOLD, 'ACHTUNG !!! - API execution took: ' +str(stop_resp['Execution_Time'])+' API threshold was reached!!!')

        if interrupt_test==False:
            # Get the Report # (Result is always zipped)
            #to_zip=['true','false']
            to_zip=['true']
            for zi in to_zip:
                start_sampling=time.time()
                sampling_timeout=SAMPLING_TIMEOUT
                Content_As_Dict={}
                is_timeout=False
                while Content_As_Dict!=None and time.time()<start_sampling+sampling_timeout:
                    get_report_zip=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='GET',url_path='shunra/api/analysisexpress/analysis/'+test_token,
                                    additional_headers={'Accept':'application/json','Content-Type':'application/json'}, api_name='GET_REPORT', params={'zipResult':zi,'returnData':'true'})
                    report_resp=get_report_zip.RUN_REQUEST()
                    #PRINT_DICT(report_resp)
                    self.assertEqual(report_resp['Status_Code'],200,'ACHTUNG !!! - '+'Received status code for GET_REPORT_API is: '+str(report_resp['Status_Code']))
                    self.assertLess(start_resp['Execution_Time'], API_EXECUTION_TIME_THRESHOLD, 'ACHTUNG !!! - API execution took: ' +str(report_resp['Execution_Time'])+' API threshold was reached!!!')
                    Content_As_Dict=report_resp['Content_As_Dict']
                    time.sleep(5)
                if time.time()>start_sampling+sampling_timeout:
                    is_timeout=True
                if zi=='true' and is_timeout==False:
                    OPEN_ZIP_REPORT_WEBBROWSER(report_resp['Content'])
                    nv_html_content=UNZIP_ZIPPED_NV_REPORT(report_resp['Content'])
                if zi=='false' and is_timeout==False:
                    OPEN_REPORT_WEBBROWSER(report_resp['Content'])
                    nv_html_content=report_resp['Content']
            for string in test_sites:
                self.assertIn(string.split('://')[-1].strip(),str(nv_html_content),'ACHTUNG !!! - "'+string+'" was not found in NV report content (inside the HTML source) !!!')
            print 'Test --> PASS'

            # Get HAR synchronous mode#
            get_har_file_1=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='GET',url_path='shunra/api/analysisreport/har/'+test_token,
                            additional_headers={'Accept':'application/json','Content-Type':'application/json'}, api_name='GET_HAR_SYNCHONOUS')
            get_har_file_resp=get_har_file_1.RUN_REQUEST()
            #PRINT_DICT(get_har_file_resp)
            self.assertEqual(get_har_file_resp['Status_Code'],200,'ACHTUNG !!! - '+'Received status code for GET_HAR_SYNCHONOUS is: '+str(get_har_file_resp['Status_Code']))
            self.assertLess(get_har_file_resp['Execution_Time'], API_EXECUTION_TIME_THRESHOLD, 'ACHTUNG !!! - API execution took: ' +str(stop_resp['Execution_Time'])+' API threshold was reached!!!')
            har_file_name='Sync_Har_'+profile_id+'.zip'
            DELETE_LOG_CONTENT(har_file_name)
            INSERT_TO_LOG(har_file_name,get_har_file_resp['Content'])
            PRINT_DICT(GET_ALL_REQUEST_URLS_FROM_HAR(har_file_name, har_is_ziped=True))
            urls_in_har=GET_ALL_REQUEST_URLS_FROM_HAR(har_file_name, har_is_ziped=True)
            for site in test_sites:
                self.assertIn(site.split('://')[-1].strip(),str(urls_in_har),'ACHTUNG !!! - no test URL ('+site+') was found in received HAR file!!!')

    # Save all result files to folder #
    def tearDown(self):
        print '-'*40+'tearDown'+'-'*40
        test_result_folder= MC_NV_Monitoring.test_name[-1]
        shutil.rmtree(test_result_folder,ignore_errors=True)
        os.mkdir(test_result_folder)
        if 'MC_APIs.csv' in os.listdir('.'):
            shutil.copy('MC_APIs.csv',test_result_folder)
        if 'build.log' in os.listdir('.'):
            shutil.copy('build.log',test_result_folder)
        ext_to_save=['.log','.jpg','.html','.har']
        for ext in ext_to_save:
            for fil in os.listdir('.'):
                if fil.endswith(ext) and fil!='Empty_Screenshot.jpg':
                    try:
                        shutil.copy(fil,test_result_folder)
                    except Exception, e:
                        print e
        shutil.make_archive(test_result_folder+'_'+str(time.time()), 'zip', test_result_folder)






