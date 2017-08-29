###### Test case: Start default test + start HTTP traffic + stop emulation + TcpDump######
import platform
import subprocess
import time
from APIs import *
from TrafficTypes import *
import urllib3
# import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import zipfile
import webbrowser
from Mi_Functions import *
import filecmp
import platform

def DICT_TO_STRING(dict):
    res_string='\r\n'*2
    for k,v in dict.iteritems():
        if len(dict[k])<50:
            res_string+=k+' --> '+str(dict[k])+'\r\n'
        else:
            res_string+=k+' --> '+str(dict[k])[0:20]+' ... '+str(dict[k])[-20:-1]+'\r\n'
    return res_string

def CALCULATE_PACKET_OVERHEAD():
    len_headers,len_data=0,0
    files=[f for f in os.listdir('.') if f.endswith('.txt')]
    fil=CHOOSE_OPTION_FROM_LIST_1(files,'Choose you file:')
    data=open(fil,'r').read().split('\n\n')
    for d in data:
        print d
        user_answer=CHOOSE_OPTION_FROM_LIST_1(['Headers','Data'],'Is printed above is "data" or "headers"?')
        if user_answer=="Headers":
            len_headers+=len(d)
        if user_answer=='Data':
            len_data+=len(d)
    total_len=len_data+len_headers
    po=100.0*len_headers/total_len
    return po

def TM_RUN_DEFAULT_SCENARIO_TEST(START_DEFAULT_TEST, IP, PORT, USER, PASSWORD, FLOW_ID, LATENCY, PACKETLOSS, BANDIN, BANDOUT, TEST_NAME, TEST_DESCRIPTION,PROXY_MODE,TRAFFIC_FUNC, *args):
    #try:
        #Start emulation and capture
        if 'linux' in platform.system().lower() and SAVE_CAPTURE==True:
            pcap_process = subprocess.Popen(['tcpdump', '-s', '0', '-i', 'any', '-w',TEST_NAME+'.cap'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(5)
            print '--> TcpDump PID:'+str(pcap_process.pid)

        #Start API with or without proxy
        if PROXY_MODE==False:
            start_default_test_result=START_DEFAULT_TEST(IP,PORT,USER,PASSWORD,FLOW_ID,LATENCY,PACKETLOSS,BANDIN,BANDOUT,TEST_NAME,TEST_DESCRIPTION)
        if PROXY_MODE==True:
            start_default_test_result=START_TEST_IN_PROXY_MODE(IP,PORT,USER,PASSWORD,FLOW_ID,LATENCY,PACKETLOSS,BANDIN,BANDOUT,TEST_NAME,TEST_DESCRIPTION)
        print '--> Start Result:'
        for d in start_default_test_result.iteritems():
            print d
        if start_default_test_result['Status']==201:
            token=eval(start_default_test_result['Content'])['testToken']
        else:
            print start_default_test_result['Status']

        #Start traffic
        traffic_result=TRAFFIC_FUNC(*args)
        print '-'*100
        for d in traffic_result.iteritems():
            print d
        #Stop test
        time.sleep(10)
        stop_test_result=STOP_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token)
        if 'linux' in platform.system().lower() and SAVE_CAPTURE==True:
            pcap_process.terminate()
            time.sleep(5)
            print '--> Stop result'
        for d in stop_test_result.iteritems():
            print d
        #Analyzing Test
        analyze_result=ANALYSE_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token)
        print analyze_result
        traffic_result['Test_name']=TEST_NAME

        return traffic_result
    # except Exception,e:
    #     print str(e)
    #     if 'linux' in platform.system().lower():
    #         if pcap_process.pid:
    #             print "Terminating TcpDump process!"
    #             pcap_process.terminate()
    #             return {'TM_RUN_DEFAULT_SCENARIO_TEST_Exception':str(e)}

def BROWSE_AND_SNIFF_SELENIUM(url,cap_name='NO_NV.cap'):
    #Start emulation and capture
    if 'linux' in platform.system().lower() and SAVE_CAPTURE==True:
        pcap_process = subprocess.Popen(['tcpdump', '-s', '0', '-i', 'any', '-w',cap_name],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)
        print '--> TcpDump PID:'+str(pcap_process.pid)

    #Start traffic
    traffic_result=OPEN_WEB_SITE_SELENIUM(url)
    for d in traffic_result.iteritems():
        print d

    #Stop sniff
    if 'linux' in platform.system().lower() and SAVE_CAPTURE==True:
        pcap_process.terminate()
        time.sleep(5)
        print '--> Stop result'
    traffic_result['CapName']=cap_name
    return traffic_result

def RUN_TM_SCENARIO_TEST_USING_DST_PORT(START_DEFAULT_TEST, IP, PORT, USER, PASSWORD, FLOW_ID, LATENCY, PACKETLOSS, BANDIN, BANDOUT, TEST_NAME, TEST_DESCRIPTION, DST_PORT, USE_TRANSACTIONS,TRAFFIC_FUNC, *args):
    #try:
        #Start emulation and capture
        if 'linux' in platform.system().lower() and SAVE_CAPTURE==True:
            pcap_process = subprocess.Popen(['tcpdump', '-s', '0', '-i', 'any', '-w',TEST_NAME+'.cap'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(5)
            print '--> TcpDump PID:'+str(pcap_process.pid)
        start_default_test_result=START_NV_TEST_USING_IP_AND_PORTS(IP,PORT,USER,PASSWORD,FLOW_ID,LATENCY,PACKETLOSS,BANDIN,BANDOUT,TEST_NAME,TEST_DESCRIPTION,DST_PORT)
        print '--> Start Result:'
        for d in start_default_test_result.iteritems():
            print d
        if start_default_test_result['Status']==201:
            token=eval(start_default_test_result['Content'])['testToken']
        else:
            print start_default_test_result['Status']
            return {'Test_name':TEST_NAME}


        if USE_TRANSACTIONS==False:
            #Start traffic
            #####traffic_result=TRAFFIC_FUNC(*args)
            #######print 'Traffic result --> '+str(traffic_result)
            ####for d in traffic_result.iteritems():
            ####    print d
            #Stop test
            time.sleep(1)
            stop_test_result=STOP_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token)
            print 'Stop test API result --> '+str(stop_test_result)


            if 'linux' in platform.system().lower() and SAVE_CAPTURE==True:
                pcap_process.terminate()
                time.sleep(5)
                print '--> Stop capture'
            for d in stop_test_result.iteritems():
                print d






        # if USE_TRANSACTIONS==True:
        #     #Start traffic
        #     traffic_result=TRAFFIC_FUNC(*args)
        #     print '-'*100
        #     for d in traffic_result.iteritems():
        #         print d
        #     #Stop test
        #     time.sleep(1)
        #     stop_test_result=STOP_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token)
        #     if 'linux' in platform.system().lower() and SAVE_CAPTURE==True:
        #         pcap_process.terminate()
        #         time.sleep(5)
        #         print '--> Stop capture result'
        #     for d in stop_test_result.iteritems():
        #         print d
        #
        #



        # #Analyzing Test
        print 'here1'
        analyze_result=ANALYSE_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token,DST_PORT)
        print 'here2'
        print 'Analyze API result --> '+str(analyze_result)

        if DELETE_TEST==True:
            delete_test=DELETE_TEST_BY_TOKEN(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token)
            print 'Delete test API result --> '+str(delete_test)
        traffic_result['Test_name']=TEST_NAME
        return traffic_result
    # except Exception,e:
    #     print str(e)
    #     if 'linux' in platform.system().lower():
    #         if pcap_process.pid:
    #             print "Terminating TcpDump process!"
    #             pcap_process.terminate()
    #             return {'TM_RUN_DEFAULT_SCENARIO_TEST_Exception':str(e)}

def OPT_MY_APP_TRAFFIC(nv_url,test_name,test_url,loop_number,OPT_MY_APP_API,**kwargs):
    #try:
    result={}
    ### Start capture
    if 'linux' in platform.system().lower() and SAVE_CAPTURE==True:
        print '...Starting capture'
        pcap_process = subprocess.Popen(['tcpdump', '-s', '0', '-i', 'any', '-w',test_name+'.cap'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)
        print '### TcpDump PID:'+str(pcap_process.pid)+' ###'






    ### User logIn
    print '... LogIn '+test_name
    login_response=OPT_MY_APP_API(nv_url,requestType='login',
                                  deviceId=kwargs['deviceId'],
                                  email=kwargs['email'],
                                  password=kwargs['password'],
                                  deviceInfo=kwargs['deviceInfo'])
    print login_response
    result['Log_In_API_[msec]']=login_response['API_EXECUTION_TIME']
    if 'errorCode' not in login_response.keys():
        return {'OPT_MY_APP_TRAFFIC':'LogIn API failed with: '+str(login_response)}
    if login_response['errorCode']!=0:
        return {'OPT_MY_APP_TRAFFIC':'LogIn API failed with: '+str(login_response)}

    ### Start OptMyApp
    print '... Starting OptmyApp, test name: '+test_name
    start_response=OPT_MY_APP_API(nv_url,requestType='startNVTest',
                                  deviceId=kwargs['deviceId'],
                                  userId=kwargs['userId'],
                                  networkProfile=kwargs['networkProfile'],
                                  runReplay=kwargs['runReplay'])
    result['Start_API_[msec]']=start_response['API_EXECUTION_TIME']
    if 'errorCode' not in start_response.keys():
        return {'OPT_MY_APP_TRAFFIC':'Start API failed with: '+str(start_response)}
    if start_response['errorCode']!=0:
        return {'OPT_MY_APP_TRAFFIC':'Start API failed with: '+str(start_response)}


    print '--> Start Response: '+str(start_response)
    session_id=start_response['sessionId']

    if USE_TRANSACTIONS==False:
        #Traffic HTTP through proxy using Requests module
        if loop_number!=0:
            proxies={"https":start_response['proxyIpAddr']+':'+start_response['proxyPort'],"http":start_response['proxyIpAddr']+':'+start_response['proxyPort']}
            print '... Starting HTTP traffic via Proxy:'+str(proxies)
            http_result=HTTP_GET_SITE(test_url,loop_number,proxies,None,SLEEP_DELAY)
            print '--> HTTP traffic response:'+str(http_result)
            for k,v in http_result.iteritems():
                result[k]=v

        if loop_number==0:
            #Traffic HTTP through proxy using Selenium
            proxy=start_response['proxyIpAddr']+':'+start_response['proxyPort']
            print '... Starting HTTP traffic via Proxy:'+str(proxy)
            http_result=OPEN_WEB_SITE_SELENIUM(test_url,proxy)
            print '--> HTTP traffic response:'+str(http_result,)
            for k,v in http_result.iteritems():
                result[k]=v

    if USE_TRANSACTIONS==True:
        transactions=[]
        files_to_save=[]
        send_stop_transaction=True
        if CMD_MODE==False:
            network_types=["baseline","good3G","busy3G"]
            #network_types=["baseline"]
        if CMD_MODE==True:
            network_types=["baseline"]
        for net in network_types:
            transaction={}

            transaction['Network_Type']=net
            print '... Change to '+net+' profile'
            change_response=OPT_MY_APP_API(nv_url,requestType='realtimeUpdate',
                                          deviceId=kwargs['deviceId'],
                                          userId=kwargs['userId'],
                                          networkProfile=net,
                                          sessionId=session_id)
            transaction['Change_Network_Type_[sec]']=change_response['API_EXECUTION_TIME']
            print '--> Change Network Type to: '+net+' Response: '+str(change_response)

            print '... Start Transaction'
            start_transaction=OPT_MY_APP_API(nv_url,requestType='startTransaction',
                                          deviceId=kwargs['deviceId'],
                                          userId=kwargs['userId'],
                                          transName='Transaction_'+net,
                                          sessionId=session_id)
            transaction['Start_Transaction_[sec]']=start_transaction['API_EXECUTION_TIME']
            if 'errorCode' in start_transaction.keys() and start_transaction['errorCode']!=0:
                send_stop_transaction=False
            print '--> Start '+net+' Transaction Response: '+str(start_transaction)

            #Traffic HTTP through proxy using Requests module
            if loop_number!=0:
                proxies={"https":start_response['proxyIpAddr']+':'+start_response['proxyPort'],"http":start_response['proxyIpAddr']+':'+start_response['proxyPort']}
                print '... Starting HTTP traffic via Proxy:'+str(proxies)
                http_result=HTTP_GET_SITE(test_url,loop_number,proxies,None,SLEEP_DELAY)
                print '--> HTTP traffic response:'+str(http_result)
                for k,v in http_result.iteritems():
                    transaction[k]=v


            if loop_number==0:
                #Traffic HTTP through proxy using Selenium
                proxy=start_response['proxyIpAddr']+':'+start_response['proxyPort']
                print '... Starting HTTP traffic via Proxy:'+str(proxy)
                http_result=OPEN_WEB_SITE_SELENIUM(test_url,proxy)
                print '--> HTTP traffic response:'+str(http_result,)
                if 'ScreenshootName' in http_result.keys() and http_result['ScreenshootName']!=None:
                    new_screenshot_name=net+'_'+http_result['ScreenshootName']
                    shutil.move(http_result['ScreenshootName'],new_screenshot_name)
                    files_to_save.append(new_screenshot_name)
                for k,v in http_result.iteritems():
                    transaction[k]=v


            if send_stop_transaction==True:
                print '... Stop Transaction'
                stop_transaction=OPT_MY_APP_API(nv_url,requestType='stopTransaction',
                                              deviceId=kwargs['deviceId'],
                                              userId=kwargs['userId'],
                                              sessionId=session_id)
                transaction['Stop_Transaction_[sec]']=stop_transaction['API_EXECUTION_TIME']
                print '--> Stop '+net+' Transaction Response: '+str(stop_transaction)
                transactions.append(transaction)

        WRITE_DICTS_TO_CSV('Transactions.csv',transactions)
        files_to_save.append('Transactions.csv')
        result['Files_To_Save']=files_to_save


    ### Stop OptMyApp
    print '... Stopping OptmyApp'
    stop_response=OPT_MY_APP_API(nv_url,requestType='stopNVTest',
                         deviceId=kwargs['deviceId'],
                         userId=kwargs['userId'],
                         sessionId=session_id)
    result['Stop_API_[msec]']=start_response['API_EXECUTION_TIME']
    print '--> Stop Response:'+str(stop_response)
    result['Test_Name']=test_name





    ### Check if report is ready
    sesStat=None
    start_sample_time=time.time()

    while (start_sample_time+kwargs['report_timeout']>time.time() and sesStat!='COMPLETED'):
        time.sleep(REPORT_SAMPLE_DELAY)
        print '... Starting Report sampling: '+test_name
        report_response=OPT_MY_APP_API(nv_url, requestType='getArtfct',
                                       deviceId=kwargs['deviceId'],
                                       check=True,
                                       report_name=kwargs['report_name'],
                                       userId=kwargs['userId'],
                                       sessionId=session_id)
        print '--> Report Response:',report_response
        if 'sesStat' in report_response.keys():
            sesStat=report_response['sesStat']
        else:
            continue
    stop_sample_time=time.time()
    result['Report_API_[msec]']=report_response['API_EXECUTION_TIME']
    result['Report_Execution_Time']=stop_sample_time-start_sample_time
    if start_sample_time+kwargs['report_timeout']<time.time():
        result['Report_Timeout']=str(True)
    else:
        ### Report HTML ###
        report_html_response=OPT_MY_APP_API(nv_url, requestType='getArtfct',
                                       deviceId=kwargs['deviceId'],
                                       check=False,
                                       report_name=kwargs['report_name'],
                                       userId=kwargs['userId'],
                                       sessionId=session_id)
        print '--> Report HTML Response:', report_html_response
        if 'errorCode' in report_html_response:
            if report_html_response['errorCode']!=0:
                result['errorCode']=report_html_response['errorCode']
                result['errorMsg']=report_html_response['errorMsg']
        else:
            result['HTML_FILE']=report_html_response['HTML_FILE']
            result['HTML_SIZE_KB']=report_html_response['HTML_SIZE_KB']

    ### User logOut
    print '... LogOut '+test_name
    logout_response=OPT_MY_APP_API(nv_url,requestType='logout',
                                  deviceId=kwargs['deviceId'],
                                  userId=kwargs['userId'])
    result['Log_Out_API_[msec]']=logout_response['API_EXECUTION_TIME']
    print '--> Logout Response: '+str(logout_response)

    ### Stop capture
    if 'linux' in platform.system().lower() and SAVE_CAPTURE==True:
        pcap_process.terminate()
        time.sleep(5)
        print '...Stopping capture'
    return result
    # except Exception,e:
    #     print str(e)
    #     if 'linux' in platform.system().lower():
    #         if SAVE_CAPTURE==True:
    #             if pcap_process.pid:
    #                 print "Terminating TcpDump process!"
    #                 pcap_process.terminate()
    #                 INSERT_TO_LOG(exceptions_file,str({'OPT_MY_APP_TRAFFIC_Exception':str(e)}))
    #     return {'OPT_MY_APP_TRAFFIC_Exception':str(e)}

def CLOSE_ALL_BROWSERS():
    browsers=["chrome.exe","firefox.exe","iexplorer.exe","opera.exe"]
    for b in browsers:
        try:
            os.system("taskkill /f /im "+b)
        except:
            pass

def OPEN_ZIP_REPORT_WEBBROWSER(binary_content,OPEN_WITH_BROWSER=True):
    try:
        if 'linux' in platform.system().lower():
            OPEN_WITH_BROWSER=False
        DELETE_LOG_CONTENT('content.zip')
        INSERT_TO_LOG('content.zip',binary_content)
        zip = zipfile.ZipFile('content.zip')
        html=zip.read('EmbeddedReport.html')
        #DELETE_LOG_CONTENT('Report.html')
        now=str(int(time.time()))
        INSERT_TO_LOG('Report'+now+'.html',html)
        if OPEN_WITH_BROWSER==True:
            webbrowser.open('Report'+now+'.html')
        return 'Report'+now+'.html'
    except Exception, e:
        return OPEN_REPORT_WEBBROWSER(binary_content)

def OPEN_REPORT_WEBBROWSER(content,OPEN_WITH_BROWSER=True):
    now=str(int(time.time()))
    if 'linux' in platform.system().lower():
        OPEN_WITH_BROWSER=False
    html_name='Report'+now+'.html'
    DELETE_LOG_CONTENT(html_name)
    INSERT_TO_LOG(html_name,content)
    if OPEN_WITH_BROWSER==True:
        webbrowser.open(html_name)
    return html_name

def COMPARE_TWO_DICTS(dic1,dic2):
    for k in dic1.keys():
        if k in dic2.keys() and sorted(dic1[k]) == sorted(dic2[k]):
            print '='*150
            print 'OK --> ',k
            print sorted(dic1[k])
            print sorted(dic2[k])
        if k in dic2.keys() and sorted(dic1[k]) != sorted(dic2[k]):
            print '='*150
            print 'Fail --> ',k
            print sorted(dic1[k])
            print sorted(dic2[k])

def UNZIP_SHUNRA_FILE_TO_DIRECTORY_BY_BINARY_CONTENT(binary_content,file_content_to_return):
    shutil.rmtree('SHUNRA_DIR',True)
    temp_file=open('temp.zip','wb')
    temp_file.write(binary_content)
    temp_file.close()
    zip = zipfile.ZipFile('temp.zip')
    zip.extractall('SHUNRA_DIR')
    data_to_return={}
    if file_content_to_return=='har':
        for fil in os.listdir('SHUNRA_DIR'):
            if '.har' in fil:
                data_to_return[fil]=open(os.path.join('SHUNRA_DIR',fil),'r').read()
    shutil.rmtree('SHUNRA_DIR',True)
    shutil.rmtree('temp.zip',True)
    return data_to_return

def GET_NV_RULES_FROM_NV_REPORT_JSON(nv_report_json_string):
    result={}
    true,false=True,False
    nv_report_json_string=json.loads(nv_report_json_string)
    nv_report_json_string=nv_report_json_string['transactionReports'][0]['reports']['bestPractices']['report']
    for rule in nv_report_json_string:
        result[rule['name']]=rule['violations']
    return result

def GET_REPORT_STATUS_VALUE_FROM_NV_REPORT_JSON(nv_report_json_string):
    true,false=True,False
    nv_report_json_string=json.loads(nv_report_json_string)
    Report_Status=nv_report_json_string['reportState']
    return Report_Status

def ONLINE_ANALYTICS_TESTING_BASIC_APIS(START_DEFAULT_TEST, IP, PORT, USER, PASSWORD, FLOW_ID, LATENCY, PACKETLOSS, BANDIN, BANDOUT, TEST_NAME, TEST_DESCRIPTION):
    # try:
        files_to_delete_after_test=[]
        completed_test_cases={}
        if 'linux' in platform.system().lower():
            print "Sorry this section is implemented for Windows only!!!"
            sys.exit(1)
        SPEC_PRINT(['Make sure that:',
                    '1) cassandra is up and running',
                    '2) NVD service is up and running',
                    '3) analysis_engine.properties configuration file contains:',
                    'com.hpe.analyzerexpress.onlineModeEnabled=true',
                    'com.hpe.analyzerexpress.useCassandra=true',
                    '4) nvproxy.properties configuration file contains:',
                    'com.hpe.nvproxy.includeHttpEntries = true'])
        CONTINUE('Are you ready to have some fun?')
        if 'BasicAPI' in ONLINE_ANALYSIS_TESTING['TestSections']:
            ## Test cases one by one: START API + test case 1 +...+test case n + STOP API + ANALYSE API
            #Start API with Proxy=True
            start_default_test_result=START_TEST_IN_PROXY_MODE(IP,PORT,USER,PASSWORD,FLOW_ID,LATENCY,PACKETLOSS,BANDIN,BANDOUT,TEST_NAME,TEST_DESCRIPTION)
            test_start_time=time.time()
            print '--> Start Result:'
            for d in start_default_test_result.iteritems():
                print d
            if start_default_test_result['Status']==201:
                token=eval(start_default_test_result['Content'])['testToken']
            else:
                print start_default_test_result['Status']
                print 'Test will be interrupted!!!'
                sys.exit(1)

            ### Test case 1 ###
            # ZipResult=True
            # Single WGET to cnn.com
            test_case_name='Single HTTP GET to CNN (200 OK)'
            print '\r\n'+'='*60 +test_case_name+'='*60
            CLOSE_ALL_BROWSERS()
            test_1_start=int(time.time()*1000)
            traffic_result=HTTP_GET_SITE('http://www.cnn.com',1,WGET_PROXIES)
            print traffic_result
            API_Response=GET_ONLINE_STATISTICS(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,True,test_1_start)
            files_to_delete_after_test.append(OPEN_ZIP_REPORT_WEBBROWSER(API_Response['Content']))
            SPEC_PRINT(['Validate that:',
                        '1) Browser is automatically opened with single TAB (NV Report)',
                        '2) In NV report you can see single WGET requet to CNN.COM in HTTP Analysys',
                        '3) Expected size (Received HTTP object only) and execution time are: '+str(traffic_result['Total_Download_Size_[kb]'])+'[kb] '+str(traffic_result['Traffic_Execution_Time_[sec]'])+'[sec]',
                        '4) Overview TAB - "Network time" and "Duration" are approximately: '+str(traffic_result['Traffic_Execution_Time_[sec]'])+'[sec]',
                        '5) Pass over "Optimization" TAB, verify that no rule is triggered',
                        '6) Pass over "Resources" TAB, verify that displayed data matching test traffic'])
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')





            ### Test case 2 ###
            # ZipResult=True
            # Single WGET to cnn.com/stam (404)
            test_case_name='Single HTTP GET to CNN/STAM (404)'
            print '\r\n'+'='*60 +test_case_name+'='*60
            CLOSE_ALL_BROWSERS()
            test_2_start=int(time.time()*1000)
            traffic_result=HTTP_GET_SITE('http://www.cnn.com/stam',1,WGET_PROXIES)
            print traffic_result
            API_Response=GET_ONLINE_STATISTICS(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,True,test_2_start)
            files_to_delete_after_test.append(OPEN_ZIP_REPORT_WEBBROWSER(API_Response['Content']))
            SPEC_PRINT(['Validate that:',
                        '1) Browser is automatically opened with single TAB (NV Report)',
                        '2) In NV report you can see single WGET requet to CNN.COM/STAM in HTTP Analysys (status code 4XX)',
                        '3) Expected size (Received HTTP object only) and execution time are: '+str(traffic_result['Total_Download_Size_[kb]'])+'[kb] '+str(traffic_result['Traffic_Execution_Time_[sec]'])+'[sec]',
                        '4) Overview TAB - "Network time" and "Duration" are approximately: '+str(traffic_result['Traffic_Execution_Time_[sec]'])+'[sec]',
                        '5) Pass over "Optimization" TAB, verify that "Avoid 4xx and 5xx status codes" rule is triggered',
                        '6) Pass over "Resources" TAB, verify that displayed data matching test traffic'])
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')




            ### Test case 3 ###
            # ZipResult=True
            # Single WGET to google.com (301)
            test_case_name='Single HTTP GET to GOOGLE (301)'
            print '\r\n'+'='*60 +test_case_name+'='*60
            CLOSE_ALL_BROWSERS()
            test_3_start=int(time.time()*1000)
            traffic_result=HTTP_GET_SITE('http://google.com',1,WGET_PROXIES)
            print traffic_result
            API_Response=GET_ONLINE_STATISTICS(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,True,test_3_start)
            files_to_delete_after_test.append(OPEN_ZIP_REPORT_WEBBROWSER(API_Response['Content']))
            SPEC_PRINT(['Validate that:',
                        '1) Browser is automatically opened with single TAB (NV Report)',
                        '2) In NV report you can see single WGET requet to GOOGLE.COM in "HTTP Analysys" TAB',
                        '3) Expected size (Received HTTP object only) and execution time are: '+str(traffic_result['Total_Download_Size_[kb]'])+'[kb] '+str(traffic_result['Traffic_Execution_Time_[sec]'])+'[sec]',
                        '4) Overview TAB - "Network time" and "Duration" are approximately: '+str(traffic_result['Traffic_Execution_Time_[sec]'])+'[sec]',
                        '5) Pass over "Optimization" TAB, verify that "Avoid URL redirects" rule is triggered',
                        '6) Pass over "Resources" TAB, verify that displayed data matching test traffic'])
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')



            ### Test case 4 ###
            # ZipResult=True
            # 10 WGETs to cnn.com (200)
            test_case_name='10 HTTP GET to CNN (200)'
            print '\r\n'+'='*60 +test_case_name+'='*60
            CLOSE_ALL_BROWSERS()
            test_4_start=int(time.time()*1000)
            traffic_result=HTTP_GET_SITE('http://www.cnn.com',10,WGET_PROXIES)
            print traffic_result
            API_Response=GET_ONLINE_STATISTICS(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,True,test_4_start)
            files_to_delete_after_test.append(OPEN_ZIP_REPORT_WEBBROWSER(API_Response['Content']))
            SPEC_PRINT(['Validate that:',
                        '1) Browser is automatically opened with single TAB (NV Report)',
                        '2) In NV report you can see 10 WGET requet to CNN.COM in "HTTP Analysys" TAB',
                        '3) Pass over "Resources" TAB, verify that displayed data matching test traffic'])
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')

            ### Test case 5 ###
            # Get Ananlytics report since test begining ###
            # ZipResult=True
            # Get whole report since test start
            test_case_name='Get Online Analysis report since test beginning)'
            print '\r\n'+'='*60 +test_case_name+'='*60
            CLOSE_ALL_BROWSERS()
            API_Response=GET_ONLINE_STATISTICS(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,True,test_start_time)
            files_to_delete_after_test.append(OPEN_ZIP_REPORT_WEBBROWSER(API_Response['Content']))
            #Stop test
            stop_test_result=STOP_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token)
            for d in stop_test_result.iteritems():
                print d
            #Analyzing Test
            analyze_result=ANALYSE_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token)
            print analyze_result
            traffic_result['Test_name']=TEST_NAME
            API_Response=GET_TEST_ANALYTICS_REPORT(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token)
            files_to_delete_after_test.append(OPEN_ZIP_REPORT_WEBBROWSER(API_Response['Content']))
            SPEC_PRINT(['Validate that:',
                        '1) Browser is automatically opened with single TAB (NV Report)',
                        '2) In NV report you can see all previous tests',
                        '3) Pass over all NV report TABS,verify that displayed data matching all previous tests',
                        '4) Compare between 2 reports: online and normal(offline), both are opened in your default browser in 2 TABS'])
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')


            ### Test case 6 ###
            # Test SUMMARY TCP PIE --> START API + TRAFFIC + STOP_API + DOWNLOAD SHUNRA
            # 10 HTTP and HTTPS GET requests to CNN in Proxy Mode
            test_case_name='10 HTTP and 10 HTTPS to CNN ("Summaries TAB" validation)'
            print '\r\n'+'='*60 +test_case_name+'='*60
            # Start API
            test_sites=['https://www.cnn.com','http://www.cnn.com']
            for site in test_sites:
                start_default_test_result=START_TEST_IN_PROXY_MODE(IP,PORT,USER,PASSWORD,FLOW_ID,LATENCY,PACKETLOSS,BANDIN,BANDOUT,TEST_NAME+'_'+str(int(time.time())),TEST_DESCRIPTION)
                test_start_time=time.time()
                print '--> Start Result:'
                for d in start_default_test_result.iteritems():
                    print d
                if start_default_test_result['Status']==201:
                    token=eval(start_default_test_result['Content'])['testToken']
                else:
                    print start_default_test_result['Status']
                    print 'Test will be interrupted!!!'
                    sys.exit(1)
                CLOSE_ALL_BROWSERS()
                test_5_start=int(time.time()*1000)
                traffic_result=HTTP_GET_SITE(site,10,WGET_PROXIES)
                API_Response=GET_ONLINE_STATISTICS(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,True,test_5_start)
                files_to_delete_after_test.append(OPEN_ZIP_REPORT_WEBBROWSER(API_Response['Content']))
                #Stop test
                stop_test_result=STOP_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token)
                for d in stop_test_result.iteritems():
                    print d
                #Analyzing Test
                analyze_result=ANALYSE_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token)
                print analyze_result
                traffic_result['Test_name']=TEST_NAME
                # Calculate Summary PIE using HAR file #
                shunra_content=GET_SHUNRA_FILE_BY_TEST_TOKEN(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token)
                har_data=UNZIP_SHUNRA_FILE_TO_DIRECTORY_BY_BINARY_CONTENT(shunra_content['Content'],'har')
                print har_data
                for k in har_data.keys():
                    if 'https' in k.lower() and 'https' in site:
                        har_data=har_data[k].decode('utf-8','ignore')
                    if 'https' not in k.lower() and 'https' not in site:
                        har_data=har_data[k].decode('utf-8','ignore')
                har_data = json.loads(har_data)
                entries=har_data['log']['entries']
                entry_send,entry_receive,entry_wait,entry_time,entry_connect,entry_dns=[],[],[],[],[],[]
                for entry in entries:
                    entry_dns.append(entry['timings']['dns'])
                    entry_connect.append(entry['timings']['connect'])
                    entry_send.append(entry['timings']['send'])
                    entry_wait.append(entry['timings']['wait'])
                    entry_receive.append(entry['timings']['receive'])
                    entry_time.append(entry['time'])
                if sum(entry_connect)==0:
                    transmission_percentage=round(100.0*(sum(entry_send)+sum(entry_receive))/sum(entry_time),2)
                    response_wait_percentage=round(sum(entry_wait)*100.0/sum(entry_time),2)
                    SPEC_PRINT(['Validate that:',
                            '1) Browser is automatically opened with single TAB (NV Report)',
                            '2) Open "Summaries" TAB and check that Transmission is ~'+str(transmission_percentage)+' and response Wait is ~'+str(response_wait_percentage),
                            'Note: only when "packetsProcessingEnabled" is disabled you will get the same values'
                            ])
                else:
                    transmission_percentage=round(100.0*(sum(entry_send)+sum(entry_receive))/((sum(entry_time)-sum(entry_dns))),2)
                    response_wait_percentage=round(sum(entry_wait)*100.0/((sum(entry_time)-sum(entry_dns))),2)
                    connection_percentage=round(sum(entry_connect)*100.0/((sum(entry_time)-sum(entry_dns))),2)
                    SPEC_PRINT(['Validate that:',
                            '1) Browser is automatically opened with single TAB (NV Report)',
                            '2) Open "Summaries" TAB and check that Transmission is ~'+str(transmission_percentage)+' , response Wait is ~'+str(response_wait_percentage)+' and Connection is ~'+str(connection_percentage)
                            ])
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')


            ### Test case 7 ###
            # Supported Rule's test case, browsing to user's site with Selenium
            # HTTP browsing based on WGETs + 20 sites from Alexa TOP 100
            test_case_name='Real browsing HTTP GETs and Selenium traffic (Optimization Rules validation)'
            print '\r\n'+'='*60 +test_case_name+'='*60
            # Start API
            start_default_test_result=START_TEST_IN_PROXY_MODE(IP,PORT,USER,PASSWORD,FLOW_ID,LATENCY,PACKETLOSS,BANDIN,BANDOUT,TEST_NAME+'_'+str(int(time.time())),TEST_DESCRIPTION)
            test_7_start=time.time()
            print '--> Start Result:'
            for d in start_default_test_result.iteritems():
                print d
            if start_default_test_result['Status']==201:
                token=eval(start_default_test_result['Content'])['testToken']
            else:
                print start_default_test_result['Status']
                print 'Test will be interrupted!!!'
                sys.exit(1)
            # Selenium Browsing + HTTP GET requests in order to trigger as much rules as possible
            traffic_result=HTTP_GET_SITE('http://www.cnn.com/zababun',10,WGET_PROXIES)
            traffic_result=HTTP_GET_SITE('http://www.bbc.com',10,WGET_PROXIES)
            traffic_result=HTTP_GET_SITE('http://google.co.il',10,WGET_PROXIES)
            sites=open('AlexaTopMilion.csv','r').readlines()
            sites= ['http://'+url.split(',')[-1].strip() for url in sites][0:1]# URLs to test
            #sites=['http://tianya.cn','http://ynet.co.il']
            for test_site in sites:
                traffic_result=OPEN_WEB_SITE_SELENIUM(test_site, ONLINE_ANALYSIS_TESTING['SELENIUM_PROXY'], 30)
            CLOSE_ALL_BROWSERS()
            # Online Analytics zipped response
            API_Response=GET_ONLINE_STATISTICS(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,True,test_7_start)
            files_to_delete_after_test.append(OPEN_ZIP_REPORT_WEBBROWSER(API_Response['Content']))
            # Online Analytics JSON response
            API_Response_json=GET_ONLINE_STATISTICS(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,False,test_7_start)['Content']
            online_rules=GET_NV_RULES_FROM_NV_REPORT_JSON(API_Response_json)
            #Stop test
            stop_test_result=STOP_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token)
            for d in stop_test_result.iteritems():
                print d
            # Analyzing Test - zip_result is True (default)
            analyze_result=ANALYSE_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token)
            # Analytics result is JSON
            offline_rules=ANALYSE_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token, ANALYZE_PORT=DST_PORT,zipResult=False)['Content']
            offline_rules=GET_NV_RULES_FROM_NV_REPORT_JSON(offline_rules)
            print '='*150
            traffic_result['Test_name']=TEST_NAME
            API_Response=GET_TEST_ANALYTICS_REPORT(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token)
            files_to_delete_after_test.append(OPEN_ZIP_REPORT_WEBBROWSER(API_Response['Content']))
            supported_online_rules=['Avoid404BestPractice','AvoidEmptySrcOrHrefs','AvoidImagesInCss','AvoidJavascriptsInHead',
                                    'AvoidLargeObjects (DesktopWeb)','AvoidLargeObjects (MobileSafari)','AvoidUnsupportedElementsBestPractice',
                                    'CompressionBestPractice','EnableProxyCachingBestPractice','ExpiresHeaderBestPractice','ImageScalingBestPractice',
                                    'MakeFewerRequestsBestPractice (DesktopWeb)','MakeFewerRequestsBestPractice(MobileSafari)','MinifyComponents',
                                    'OptimizeImages(DesktopWeb)','OptimizeImages(MobileSafari)','PutCssAtTheBottom','RedirectionBestPractice','ReduceCookies',
                                    'ReduceDNSLookupsBestPractice','SpecifyCharacterSet','OptimizeCachingBestPractice','UseCDNBestPractice','ThirdParties']
            SPEC_PRINT(supported_online_rules)
            COMPARE_TWO_DICTS(online_rules,offline_rules)
            SPEC_PRINT(['Validate that:',
                        '1) Browser is automatically opened with 2 TABs: Online and Offline NV Reports',
                        '2) Make sure that triggered rules are the same for both: "Online" and "Offline"',
                        'Note: comparison is automatically done by script: pass over all "OK" and "Fail" in its output above',
                        'Important: Online supports 22 optimization rules while offline supports 27 (supported are listed above)'
                        ])
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')


            ### Test case 8 ###
            # Continues testing: START API + Browse to site (Alexa  top sites) ONLINE_ANALITICS_API + STOP API
            test_case_name='Browsing to Alexa Sites and getting Online Analysis report per site (Stability)'
            print '\r\n'+'='*60 +test_case_name+'='*60
            CLOSE_ALL_BROWSERS()
            # Start API
            start_default_test_result=START_TEST_IN_PROXY_MODE(IP,PORT,USER,PASSWORD,FLOW_ID,LATENCY,PACKETLOSS,BANDIN,BANDOUT,TEST_NAME+'_'+str(int(time.time())),TEST_DESCRIPTION)
            test_7_start=time.time()
            print '--> Start Result:'
            for d in start_default_test_result.iteritems():
                print d
            if start_default_test_result['Status']==201:
                token=eval(start_default_test_result['Content'])['testToken']
            else:
                print start_default_test_result['Status']
                print 'Test will be interrupted!!!'
                sys.exit(1)
            # Selenium Browsing + HTTP GET requests in order to trigger as much rules as possible
            sites=open('AlexaTopMilion.csv','r').readlines()
            number_of_sites=CHOOSE_OPTION_FROM_LIST_1(['1','5','20','50','100','300','500'],'Number of sites to test:')
            sites= ['http://'+url.split(',')[-1].strip() for url in sites][0:int(number_of_sites)]
            online_analytics_responses=[]
            for test_site in sites:
                site_start_time=time.time()
                traffic_result=OPEN_WEB_SITE_SELENIUM(test_site, ONLINE_ANALYSIS_TESTING['SELENIUM_PROXY'], 30)
                # Online Analytics zipped response
                online_response=GET_ONLINE_STATISTICS(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,True,site_start_time)
                online_response['Tested_URL']=test_site
                online_analytics_responses.append(online_response)
            #Stop test
            stop_test_result=STOP_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token)
            for d in stop_test_result.iteritems():
                print d
            API_Response=ANALYSE_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token)
            for d in API_Response.iteritems():
                print d
            responses_for_tester=[]
            for res in online_analytics_responses:
                if 'ANALYSE_TEST_BY_TOKEN_Exception' not in res.keys():
                    responses_for_tester.append(str(res['Status'])+' --> '+res['Tested_URL'])
                else:
                    responses_for_tester.append('ANALYSE_TEST_BY_TOKEN_Exception --> '+res['STOP_TEST_BY_TOKEN_Exception'])
            SPEC_PRINT(responses_for_tester)
            SPEC_PRINT(['Validate that:',
                        '1) Online analytics report was sucsesfully received per site',
                        '   You can see "<URL> --> <STATUS>" in the output above'
                        ])
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')

            ### Test case 9 ###
            # Online analytics API tests: 304 response + ReportStatus + Fault cases
            test_case_name='Testing: "Online Analysis API (304)", "NV Report Status" and "Fault cases"'
            print '\r\n'+'='*60 +test_case_name+'='*60
            CLOSE_ALL_BROWSERS()
            test_case_result=[]
            # Start API
            start_default_test_result=START_TEST_IN_PROXY_MODE(IP,PORT,USER,PASSWORD,FLOW_ID,LATENCY,PACKETLOSS,BANDIN,BANDOUT,TEST_NAME+'_'+str(int(time.time())),TEST_DESCRIPTION)
            test_9_start=time.time()
            print '--> Start Result:'
            for d in start_default_test_result.iteritems():
                print d
            if start_default_test_result['Status']==201:
                token=eval(start_default_test_result['Content'])['testToken']
            else:
                print start_default_test_result['Status']
                print 'Test will be interrupted!!!'
                sys.exit(1)
            # Some Browsing based HTTP GETs
            traffic_result=HTTP_GET_SITE('http://www.cnn.com',10,WGET_PROXIES)

            # Online Analytics JSON response
            API_Response_json=GET_ONLINE_STATISTICS(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,False,test_9_start)['Content']
            print API_Response_json
            report_status=GET_REPORT_STATUS_VALUE_FROM_NV_REPORT_JSON(API_Response_json).lower()
            if report_status=="IN_PROGRESS".lower():
                SPEC_PRINT(['ReportStatus is "'+report_status+'" expected: "IN_PROGRESS"--> PASS'])
                test_case_result.append(['ReportStatus is "'+report_status+'" expected: "IN_PROGRESS"--> PASS'])
            else:
                SPEC_PRINT(['ReportStatus is "'+report_status+'" expected: "IN_PROGRESS"--> FAIL'])
                test_case_result.append(['ReportStatus is "'+report_status+'" expected: "IN_PROGRESS"--> FAIL'])

            # user will receive 304 NOT MODIFIED only when running cache is enabled
            time.sleep(5)
            status=str(GET_ONLINE_STATISTICS(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,False,test_9_start)['Status'])
            if status =='304':
                SPEC_PRINT(['API response ststus is "'+status+'" expected: "304"--> PASS'])
                test_case_result.append(['API response ststus is "'+status+'" expected: "304"--> PASS'])
            else:
                SPEC_PRINT(['API response ststus is "'+status+'" expected: "304"--> FAIL'])
                test_case_result.append(['API response ststus is "'+status+'" expected: "304"--> FAIL'])

            # Bad API requests
            # 'ZABABUN' instead of "ZipResult"
            API_Response=GET_ONLINE_STATISTICS(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,'ZABABUN',test_9_start)
            print 'Status Code --> ',API_Response['Status']
            print 'Content --> ', API_Response['Content']
            print 'Reason --> ',API_Response['Reason']
            if str(API_Response['Status'])=='200':
                test_case_result.append('"Zababun" instead of "ZipResult" and status is '+str(API_Response['Status'])+' --> FAIL')
            else:
                test_case_result.append('"Zababun" instead of "ZipResult" and status is '+str(API_Response['Status'])+' --> PASS')

            # 'ZABABUN' instead of "Test Token"
            API_Response=GET_ONLINE_STATISTICS(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,'ZABABUN',False,test_9_start)
            print 'Status Code --> ',API_Response['Status']
            print 'Content --> ', API_Response['Content']
            print 'Reason --> ',API_Response['Reason']
            if str(API_Response['Status'])=='200':
                test_case_result.append('"Zababun" instead of "TestToken" and status is '+str(API_Response['Status'])+' --> FAIL')
            else:
                test_case_result.append('"Zababun" instead of "TestToken" and status is '+str(API_Response['Status'])+' --> PASS')

            # 'ZABABUN' instead of "Time"
            API_Response=GET_ONLINE_STATISTICS(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,False,'ZABABUN')
            print 'Status Code --> ',API_Response['Status']
            print 'Content --> ', API_Response['Content']
            print 'Reason --> ',API_Response['Reason']
            if str(API_Response['Status'])=='200':
                test_case_result.append('"Zababun" instead of "Time" and status is '+str(API_Response['Status'])+' --> FAIL')
            else:
                test_case_result.append('"Zababun" instead of "Time" and status is '+str(API_Response['Status'])+' --> PASS')

            # Corrupted time
            API_Response=GET_ONLINE_STATISTICS(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,False,test_9_start+1231232132132132)
            print 'Status Code --> ',API_Response['Status']
            print 'Content --> ', API_Response['Content']
            print 'Reason --> ',API_Response['Reason']
            if str(API_Response['Status'])=='200':
                test_case_result.append('Time is corrupted and status is '+str(API_Response['Status'])+' --> FAIL')
            else:
                test_case_result.append('Time is corrupted and status is '+str(API_Response['Status'])+' --> PASS')

            # "Zababun" parameter at the end
            API_Response=GET_ONLINE_STATISTICS(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,False,str(test_9_start)+'&ZABABUN=ZAHLABUT')
            print 'Status Code --> ',API_Response['Status']
            print 'Content --> ', API_Response['Content']
            print 'Reason --> ',API_Response['Reason']
            if str(API_Response['Status'])=='200':
                test_case_result.append('"Zababun" parameter at the end and status is '+str(API_Response['Status'])+' --> FAIL')
            else:
                test_case_result.append('"Zababun" parameter at the end and status is '+str(API_Response['Status'])+' --> PASS')

            #Stop test
            stop_test_result=STOP_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token)
            for d in stop_test_result.iteritems():
                print d
            time.sleep(15) #Must by NV otherwise  IN_PROGRESS will ve received
            API_Response_json=GET_ONLINE_STATISTICS(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,False,test_9_start)['Content']
            print API_Response_json
            report_status=GET_REPORT_STATUS_VALUE_FROM_NV_REPORT_JSON(API_Response_json).lower()
            print report_status
            if report_status=="FINAL".lower():
                SPEC_PRINT(['ReportStatus is "'+report_status+'" expected: "FINAL" --> PASS'])
                test_case_result.append(['ReportStatus is "'+report_status+'" expected: "FINAL" --> PASS'])
            else:
                SPEC_PRINT(['ReportStatus is "'+report_status+'" expected: "FINAL" --> FAIL'])
                test_case_result.append(['ReportStatus is "'+report_status+'" expected: "FINAL" --> FAIL'])

            # Start API
            start_default_test_result=START_TEST_IN_PROXY_MODE(IP,PORT,USER,PASSWORD,FLOW_ID,LATENCY,PACKETLOSS,BANDIN,BANDOUT,TEST_NAME+'_'+str(int(time.time())),TEST_DESCRIPTION)
            test_9_start=time.time()
            print '--> Start Result:'
            for d in start_default_test_result.iteritems():
                print d
            if start_default_test_result['Status']==201:
                token=eval(start_default_test_result['Content'])['testToken']
            else:
                print start_default_test_result['Status']
                print 'Test will be interrupted!!!'
                sys.exit(1)
            # Some Browsing based HTTP GETs
            traffic_result=HTTP_GET_SITE('http://www.cnn.com',10,WGET_PROXIES)

            SPEC_PRINT(['Please restart nvd service'])
            CONTINUE('To continue?')

            # Online Analytics JSON response
            API_Response_json=GET_ONLINE_STATISTICS(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,False,test_9_start)['Content']
            print API_Response_json
            report_status=GET_REPORT_STATUS_VALUE_FROM_NV_REPORT_JSON(API_Response_json).lower()
            if report_status=="INTERRUPTED".lower():
                SPEC_PRINT(['ReportStatus is "'+report_status+'" expected: "INTERRUPTED" --> PASS'])
                test_case_result.append(['ReportStatus is "'+report_status+'" expected: "INTERRUPTED" --> PASS'])
            else:
                SPEC_PRINT(['ReportStatus is "'+report_status+'"" expected: "INTERRUPTED" --> FAIL'])
                test_case_result.append(['ReportStatus is "'+report_status+'" expected: "INTERRUPTED" --> FAIL'])
            #Stop test
            stop_test_result=STOP_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token)
            for d in stop_test_result.iteritems():
                print d

            SPEC_PRINT([str(i) for i in test_case_result])
            CLOSE_ALL_BROWSERS()
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')
            for fil in files_to_delete_after_test:
                print fil
                os.remove(fil)
            for k,v in completed_test_cases.iteritems():
                print k,'-->',v

        if 'MarkAPI' in ONLINE_ANALYSIS_TESTING['TestSections']:
            ### Test case 10 ###
            # Mark API tests
            # Test cases 1 - Start API + SET in loop with traffic and delay in each iteration ###
            completed_test_cases={}
            test_start_time=time.time()
            files_to_delete_after_test=[]
            test_case_name='Online Analysis with SET API and traffic in loop (NV Report data validation test)'
            print '\r\n'+'='*60 +test_case_name+'='*60
            CLOSE_ALL_BROWSERS()
            #Start API with Proxy=True
            start_default_test_result=START_TEST_IN_PROXY_MODE(IP,PORT,USER,PASSWORD,FLOW_ID,LATENCY,PACKETLOSS,BANDIN,BANDOUT,TEST_NAME.replace('Online_Analysis_Testing_','Online_Analysis_Testing_Mark_API_'),TEST_DESCRIPTION)
            print '--> Start Result:'
            for d in start_default_test_result.iteritems():
                print d
            if start_default_test_result['Status']==201:
                token=eval(start_default_test_result['Content'])['testToken']
            else:
                print start_default_test_result['Status']
                print 'Test will be interrupted!!!'
                sys.exit(1)
            test_case_sites=['http://www.cnn.com','http://www.bbc.com','http://www.google.com','http://www.msn.com','http://www.amazon.com']
            traffics=[]
            used_marks=[]
            nv_report_files=[]
            for x in xrange(1,6):
                traffic_result=HTTP_GET_SITE(test_case_sites[x-1],x,WGET_PROXIES,delay=1)
                traffic_result['URL']=test_case_sites[x-1]
                traffic_result['Traffic_Execution_Time_[sec]']=traffic_result['Traffic_Execution_Time_[sec]']-1 #Reduce delay from
                traffics.append(str(x)+' Requests to: '+traffic_result['URL']+' and NV Report "Nework Time" is: '+str(traffic_result['Traffic_Execution_Time_[sec]']))
                API_Response=SET_OR_GET_MARK_ONLINE_STATISTICS(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token, 'zababun_' + str(x), True)
                used_marks.append('zababun_'+str(x))
                files_to_delete_after_test.append(OPEN_ZIP_REPORT_WEBBROWSER(API_Response['Content']))
                nv_report_files=files_to_delete_after_test
            traffics.insert(0,'Verify that:')
            traffics.insert(1,'1) Browser is opened with 5 TABS (NV Reports)')
            traffics.insert(2,'2) Pass over each TAB and make sure that info in each TAB is as follow:')
            SPEC_PRINT(traffics)
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')

            ### Test case 11 ###
            test_case_name='Online Analysis SET API (Used IDs are not reusable)'
            print '\r\n'+'='*60 +test_case_name+'='*60
            print 'Trying to use previous IDs for NEW Mark Points'
            api_responses_for_old_marks=[]
            for mark in used_marks:
                API_Response=SET_OR_GET_MARK_ONLINE_STATISTICS(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token, mark, True)
                api_responses_for_old_marks.append(str({'Used_Mark':mark,'ResponseStatus':API_Response['Status'],'ResponseReason':API_Response['Reason']}))
            api_responses_for_old_marks.insert(0,'Make sure that:')
            api_responses_for_old_marks.insert(1,'All APIs failed due to the fact that "Old IDs" have been used to SET a NEW "mark point"')
            SPEC_PRINT(api_responses_for_old_marks)
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')

            ### Test case 12 ###
            test_case_name='Online Analysis SET API ("BAD IDs")'
            print '\r\n'+'='*60 +test_case_name+'='*60
            print 'Trying to use "BAD IDs" to SET a new "Mark Point" or to GET already existing report'
            bad_mark_ids=['g&*','','{}','a','0','|','@','~','g%t','k()4','           ']
            api_responses=[]
            for mark in bad_mark_ids:
                API_Response=SET_OR_GET_MARK_ONLINE_STATISTICS(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token, mark, True)
                api_responses.append(str({'RequetsType':'SET','Used_Mark':mark,'ResponseStatus':API_Response['Status'],'ResponseReason':API_Response['Reason']}))
            for mark in bad_mark_ids:
                API_Response=SET_OR_GET_MARK_ONLINE_STATISTICS(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token, mark, True,IS_SET=False)
                api_responses.append(str({'RequetsType':'GET_Option_1','Used_Mark':mark,'ResponseStatus':API_Response['Status'],'ResponseReason':API_Response['Reason']}))
            for mark in bad_mark_ids:
                API_Response=SET_OR_GET_MARK_ONLINE_STATISTICS(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token, mark, True,IS_SET=False, GET_SECOND_OPTION=True)
                api_responses.append(str({'RequetsType':'GET_Option_2','Used_Mark':mark,'ResponseStatus':API_Response['Status'],'ResponseReason':API_Response['Reason']}))
            api_responses.insert(0,'Make sure that:')
            api_responses.insert(1,'All APIs failed due to "BAD Mark ID"')
            SPEC_PRINT(api_responses)
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')


            ### Test case 13 ###
            test_case_name='Online Analysis SET API ("BAD Token")'
            print '\r\n'+'='*60 +test_case_name+'='*60
            print 'Trying to use "BAD Token" to SET a new "Mark Point" or to GET already existing report'
            api_responses=[]
            API_Response=SET_OR_GET_MARK_ONLINE_STATISTICS(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token + 'ZABABUN', 'NEW_MARK_1', True)
            api_responses.append(str({'RequetsType':'SET','Token':token+'ZABABUN','ResponseStatus':API_Response['Status'],'ResponseReason':API_Response['Reason']}))
            API_Response=SET_OR_GET_MARK_ONLINE_STATISTICS(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token + 'ZABABUN', 'NEW_MARK_1', True,IS_SET=False)
            api_responses.append(str({'RequetsType':'GET_Option_1','Token':token+'ZABABUN','ResponseStatus':API_Response['Status'],'ResponseReason':API_Response['Reason']}))
            API_Response=SET_OR_GET_MARK_ONLINE_STATISTICS(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token + 'ZABABUN', 'NEW_MARK_1', True,IS_SET=False,GET_SECOND_OPTION=True)
            api_responses.append(str({'RequetsType':'GET_Option_2','Token':token+'ZABABUN','ResponseStatus':API_Response['Status'],'ResponseReason':API_Response['Reason']}))
            #files_to_delete_after_test.append(OPEN_ZIP_REPORT_WEBBROWSER(API_Response['Content']))
            api_responses.insert(0,'Make sure that:')
            api_responses.insert(1,'APIs failed due to "BAD Token"')
            SPEC_PRINT(api_responses)
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')

            ### Test case 14 ###
            test_case_name='Online Analysis SET API ("BAD ZipResult")'
            print '\r\n'+'='*60 +test_case_name+'='*60
            print 'Trying to use "BAD ZipResult" values to set a new "Mark Point" or to GET already existing report'
            bad_zip_values=['Stam','Zababun','123']
            api_responses=[]
            for zi in bad_zip_values:
                API_Response=SET_OR_GET_MARK_ONLINE_STATISTICS(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token, str(bad_zip_values.index(zi))*5, str(zi))
                api_responses.append(str({'RequetsType':'SET','MarkID':str(bad_zip_values.index(zi))*5,'ResponseStatus':API_Response['Status'],'ResponseReason':API_Response['Reason'],'ZipResult':zi}))
            for zi in bad_zip_values:
                API_Response=SET_OR_GET_MARK_ONLINE_STATISTICS(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token, str(bad_zip_values.index(zi))*5, str(zi), IS_SET=False)
                api_responses.append(str({'RequetsType':'GET_Option_1','MarkID':str(bad_zip_values.index(zi))*5,'ResponseStatus':API_Response['Status'],'ResponseReason':API_Response['Reason'],'ZipResult':zi}))
            for zi in bad_zip_values:
                API_Response=SET_OR_GET_MARK_ONLINE_STATISTICS(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token, str(bad_zip_values.index(zi))*5, str(zi), IS_SET=False,GET_SECOND_OPTION=True)
                api_responses.append(str({'RequetsType':'GET_Option_2','MarkID':str(bad_zip_values.index(zi))*5,'ResponseStatus':API_Response['Status'],'ResponseReason':API_Response['Reason'],'ZipResult':zi}))
            api_responses.insert(0,'Make sure that:')
            api_responses.insert(1,'All APIs failed due to "BAD ZipResult" values')
            SPEC_PRINT(api_responses)
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')

            ### Test case 15 ###
            test_case_name='Online Analysis SET API (JSON response + new mark point)'
            print '\r\n'+'='*60 +test_case_name+'='*60
            print 'Trying to get JSON response "ZipResult=False" to create a new "Mark Point" or to GET already existing report'
            api_responses=[]
            API_Response=SET_OR_GET_MARK_ONLINE_STATISTICS(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token, 'AH_ID', False)
            valid_json=IS_JSON(API_Response['Content'])
            api_responses.append(str({'RequetsType':'SET','ResponseStatus':API_Response['Status'],'ResponseReason':API_Response['Reason'],'JSON_Validator_result':valid_json}))
            API_Response=SET_OR_GET_MARK_ONLINE_STATISTICS(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token, 'AH_ID', False,IS_SET=False)
            valid_json=IS_JSON(API_Response['Content'])
            api_responses.append(str({'RequetsType':'GET_Option_1','ResponseStatus':API_Response['Status'],'ResponseReason':API_Response['Reason'],'JSON_Validator_result':valid_json}))
            API_Response=SET_OR_GET_MARK_ONLINE_STATISTICS(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token, 'AH_ID', False,IS_SET=False, GET_SECOND_OPTION=True)
            valid_json=IS_JSON(API_Response['Content'])
            api_responses.append(str({'RequetsType':'GET_Option_2','ResponseStatus':API_Response['Status'],'ResponseReason':API_Response['Reason'],'JSON_Validator_result':valid_json}))
            api_responses.insert(0,'Make sure that:')
            api_responses.insert(1,'Resived JSON is valid')
            SPEC_PRINT(api_responses)
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')


            ### Test case 16 ###
            test_case_name='Getting Online Analysis report using GET API since last mark point (NV Report validation)'
            print '\r\n'+'='*60 +test_case_name+'='*60
            print 'Trying to get NV report for previous Mark Points: '+str(used_marks)+ ' using GET Mark Online Analysys Rest API while Emulation is still running'
            compare_nv_reports=[]
            for mark in used_marks:
                API_Response=SET_OR_GET_MARK_ONLINE_STATISTICS(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token, mark, True, IS_SET=False)
                original_report_file=nv_report_files[used_marks.index(mark)]
                new_report_file=OPEN_ZIP_REPORT_WEBBROWSER(API_Response['Content'],OPEN_WITH_BROWSER=False)
                files_to_delete_after_test.append(new_report_file)
                compare_nv_reports.append('Compare result for: '+original_report_file+' and '+new_report_file+' is: '+str(filecmp.cmp(original_report_file,new_report_file)))
            compare_nv_reports.insert(0,'Make sure that compare result for all NV reports bellow is TRUE')
            SPEC_PRINT(compare_nv_reports)
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')

            ### Test case 17 ###
            test_case_name='Getting Online Analysis report using GET API since test beginning (NV Report validation)'
            print '\r\n'+'='*60 +test_case_name+'='*60
            print 'Trying to get Online Report Analytics using Basic API since test case beginning'
            CLOSE_ALL_BROWSERS()
            API_Response=GET_ONLINE_STATISTICS(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,True,test_start_time)
            files_to_delete_after_test.append(OPEN_ZIP_REPORT_WEBBROWSER(API_Response['Content']))
            SPEC_PRINT(['Validate that:',
                        '1) Browser is automatically opened with single TAB (NV Report)',
                        '2) Make sure that NV Report is empty, because no traffic was sent since last "Mark Point"',
                        'and the old traffic data was removed from DB by previous "Mark Points"'])
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')



            ### Test case 18 ###
            test_case_name='Getting Online Analysis report using GET API since test beginning after sending traffic (NV Report validation)'
            print '\r\n'+'='*60 +test_case_name+'='*60
            print '\r\n'+'='*120
            print 'Trying to get Online Report Analytics, after sending NEW traffic, with Basic API since test case beginning'
            CLOSE_ALL_BROWSERS()
            traffic_result=HTTP_GET_SITE('http://www.cnn.com',10,WGET_PROXIES,delay=1)
            API_Response=GET_ONLINE_STATISTICS(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,True,test_start_time)
            files_to_delete_after_test.append(OPEN_ZIP_REPORT_WEBBROWSER(API_Response['Content']))
            SPEC_PRINT(['Validate that:',
                        '1) Browser is automatically opened with single TAB (NV Report)',
                        '2) Make sure that NV Report contains 10 WGETs to CNN'])
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')

            #Stop test
            stop_test_result=STOP_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token)
            for d in stop_test_result.iteritems():
                print d

            ### Test case 19 ###
            test_case_name='Getting Online Analysis report using GET Mark Online Analysys Rest API_Option_1 (NV Report validation)'
            print '\r\n'+'='*60 +test_case_name+'='*60
            print 'Trying to get NV report for previous Mark Points: '+str(used_marks)+ 'using GET Mark Online Analysys Rest API, no Emulation is running'
            compare_nv_reports=[]
            for mark in used_marks:
                API_Response=SET_OR_GET_MARK_ONLINE_STATISTICS(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token, mark, True, IS_SET=False)
                original_report_file=nv_report_files[used_marks.index(mark)]
                new_report_file=OPEN_ZIP_REPORT_WEBBROWSER(API_Response['Content'],OPEN_WITH_BROWSER=False)
                files_to_delete_after_test.append(new_report_file)
                compare_nv_reports.append('Compare result for: '+original_report_file+' and '+new_report_file+' is: '+str(filecmp.cmp(original_report_file,new_report_file)))
            compare_nv_reports.insert(0,'Make sure that compare result for and response Wait is all NV reports bellow is TRUE')
            SPEC_PRINT(compare_nv_reports)
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')


            ### Test case 20 ###
            test_case_name='Getting Online Analysis report using GET Mark Online Analysys Rest API_Option_2 (NV Report validation)'
            print '\r\n'+'='*60 +test_case_name+'='*60
            print 'Trying to get NV report for previous Mark Points: '+str(used_marks)+ 'using GET Mark Online Analysys Rest API, no Emulation is running (GET option No2 "token-mark")'
            compare_nv_reports=[]
            for mark in used_marks:
                API_Response=SET_OR_GET_MARK_ONLINE_STATISTICS(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token, mark, True, IS_SET=False,GET_SECOND_OPTION=True)
                original_report_file=nv_report_files[used_marks.index(mark)]
                new_report_file=OPEN_ZIP_REPORT_WEBBROWSER(API_Response['Content'],OPEN_WITH_BROWSER=False)
                files_to_delete_after_test.append(new_report_file)
                compare_nv_reports.append('Compare result for: '+original_report_file+' and '+new_report_file+' is: '+str(filecmp.cmp(original_report_file,new_report_file)))
            compare_nv_reports.insert(0,'Make sure that compare result for all NV reports bellow is TRUE')
            SPEC_PRINT(compare_nv_reports)
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')

            for k,v in completed_test_cases.iteritems():
                print k,'-->',v

            CLOSE_ALL_BROWSERS()
            for fil in files_to_delete_after_test:
                print fil
                try:
                    os.remove(fil)
                except Exception, e:
                    print str(e)


        if 'PacketProccesing' in ONLINE_ANALYSIS_TESTING['TestSections']:
            SPEC_PRINT(['Enable PacketProcessing','In "analysis_engine.properties" file','Change "com.hpe.analyzerexpress.packetsProcessingEnabled=true"','Restart NVD service'])
            CONTINUE('To continue?')
            files_to_delete_after_test=[]
            completed_test_cases={}
            if 'linux' in platform.system().lower():
                print "Sorry this section is implemented for Windows only!!!"
                sys.exit(1)
            ### Test case 21 ###
            # com.hpe.analyzerexpress.packetsProcessingEnabled=true
            traffic_types=['HTTP_Traffic','HTTPS_Traffic','Real_Site_Traffic', 'Continues_browsing']

            for traf in traffic_types:
                test_case_name=traf+' (NV Repoort validation)'
                print '\r\n'+'='*60 +test_case_name+'='*60
                CLOSE_ALL_BROWSERS()
                test_start_time=time.time()
                #Start API with Proxy=True
                start_default_test_result=START_TEST_IN_PROXY_MODE(IP,PORT,USER,PASSWORD,FLOW_ID,LATENCY,PACKETLOSS,BANDIN,BANDOUT,TEST_NAME.replace('Online_Analysis_Testing_','Online_Analysis_Testing_'+traf+'_'),TEST_DESCRIPTION)
                print '--> Start Result:'
                for d in start_default_test_result.iteritems():
                    print d
                if start_default_test_result['Status']==201:
                    token=eval(start_default_test_result['Content'])['testToken']
                else:
                    print start_default_test_result['Status']
                    print 'Test will be interrupted!!!'
                    sys.exit(1)
                #Traffic
                if traf=='Real_Site_Traffic':
                    print traf
                    traffic_result=OPEN_WEB_SITE_SELENIUM('http://fishki.net', ONLINE_ANALYSIS_TESTING['SELENIUM_PROXY'],60)
                if traf=='HTTP_Traffic':
                    print traf
                    traffic_result=HTTP_GET_SITE('http://www.cnn.com',10,WGET_PROXIES)
                if traf=='HTTPS_Traffic':
                    print traf
                    traffic_result=HTTP_GET_SITE('https://www.facebook.com/',10,WGET_PROXIES)
                if traf=='Continues_browsing':
                    print traf
                    loops=input('Enter number of sites: ')
                    sites=open('AlexaTopMilion.csv','r').readlines()
                    sites= ['http://'+url.split(',')[-1].strip() for url in sites][0:loops]
                    for site in sites:
                        test_start_time=time.time()
                        traffic_result=OPEN_WEB_SITE_SELENIUM(site, ONLINE_ANALYSIS_TESTING['SELENIUM_PROXY'],30)
                        API_Response=GET_ONLINE_STATISTICS(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,True,test_start_time)
                        print API_Response['Status']

                # Online Analysis
                API_Response=GET_ONLINE_STATISTICS(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,True,test_start_time)
                files_to_delete_after_test.append(OPEN_ZIP_REPORT_WEBBROWSER(API_Response['Content']))

                #Stop test
                stop_test_result=STOP_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token)
                for d in stop_test_result.iteritems():
                    print d

                # Offline analysis
                analyze_result=ANALYSE_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token)
                API_Response=GET_TEST_ANALYTICS_REPORT(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token)
                files_to_delete_after_test.append(OPEN_ZIP_REPORT_WEBBROWSER(API_Response['Content']))

                SPEC_PRINT(['Validate that:',
                            '1) Browser is automatically opened with 2 TABs: Online and Offline NV Reports',
                            '2) Pass over: "Summaries", "General Waterfall" and "Endpoint Latencies" TABS',
                            'Make sure that Online and Offline values are similar'
                            ])
                completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')




            print '\r\n'
            print '='*120
            for k,v in completed_test_cases.iteritems():
                print k,'-->',v
            print '='*120

        return {'Online Analysis Test Cases':'Completed'}

def SUMMARIES_TEST_CASES(START_DEFAULT_TEST, IP, PORT, USER, PASSWORD, FLOW_ID, LATENCY, PACKETLOSS, BANDIN, BANDOUT, TEST_NAME, TEST_DESCRIPTION):
    files_to_delete_after_test=[]
    completed_test_cases={}
    SPEC_PRINT(['Make sure that:','1) You are running this script locally on NV server','2) NVD service is up and running','Note: test cases in this script are not covering "Summaries" by 100%'])
    #Start emulation and capture
    if 'linux' in platform.system().lower() and SAVE_CAPTURE==True:
        pcap_process = subprocess.Popen(['tcpdump', '-s', '0', '-i', 'any', '-w',TEST_NAME+'.cap'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)
        print '--> TcpDump PID:'+str(pcap_process.pid)

    ### Test case 1 ###
    traffic_types=['HTTP','SSL','HLS','UDP','TCP']
    for type in traffic_types:
        test_case_name='HTTP - Data Validation'+' - '+type+' pie chart'
        print '\r\n'+'='*30 +' '+test_case_name+' '+'='*30
        start_default_test_result=START_DEFAULT_TEST(IP,PORT,USER,PASSWORD,FLOW_ID,LATENCY,PACKETLOSS,BANDIN,BANDOUT,TEST_NAME+'_'+type,TEST_DESCRIPTION,delay_after_stop=5)
        PRINT_DICT(start_default_test_result)
        token=eval(start_default_test_result['Content'])['testToken'] if start_default_test_result['Status']==201 else  sys.exit(1)
        #Traffic
        if type=='HTTP':
            traffic_result=HTTP_GET_SITE('http://www.cnn.com',1)
        if type=='SSL':
            traffic_result=HTTP_GET_SITE('https://www.google.com',1)
        if type=='HLS':
            traffic_result=HLS_VLC(30)
        if type=='UDP':
            traffic_result=DNS_QUERY('bbc.com',1)
        if type=='TCP':
            traffic_result=HTTP_GET_SOCKET('ynet.co.il',80,1)
        PRINT_DICT(traffic_result)


        #Stop test
        stop_test_result=STOP_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token,delay_before_stop=5)
        PRINT_DICT(stop_test_result)
        # Offline analysis
        analyze_result=ANALYSE_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token)
        API_Response=GET_TEST_ANALYTICS_REPORT(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token)
        files_to_delete_after_test.append(OPEN_ZIP_REPORT_WEBBROWSER(API_Response['Content']))

        if type=='HTTP':
            SPEC_PRINT(['Open Pl with Wireshark on your PC',
                        'Find test HTTP traffic request',
                        'Copy and Paste the content of "Follow TCP stream into some *.txt file and save'])
            CONTINUE('Continue, once file is saved')
            po=CALCULATE_PACKET_OVERHEAD()
            SPEC_PRINT(['Analyze PL with Wireshark and validate data in HTTP:',
                        '1) Total Bytes',
                        '2) Total packets',
                        '3) Application turns',
                        '4) KB per turns',
                        'Are similar in Summaries and Wireshark Conversations statistics',
                        '5) Make sure that calculated by script Packet Overhead: '+str(po)+' is similar to "Packet Overhead" value in NV Report',
                        'Note: in Wireshark find your traffic (single HTTP get) in "Statistics" --> "ConversationList" --> "IPv4"'
                        ])
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')
        if type=='SSL':
            SPEC_PRINT(['Analyze PL with Wireshark and validate data in SSL:',
                        '1) Total Bytes',
                        '2) Total packets',
                        '3) Application turns',
                        '4) KB per turns',
                        'Are similar in Summaries and Wireshark Conversations statistics',
                        'Note: in Wireshark find your traffic (single HTTPS get port 443) in "Statistics" --> "ConversationList" --> "IPv4"'
                        ])
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')
        if type=='HLS':
            SPEC_PRINT(['Analyze PL with Wireshark and validate data in HLS:',
                        '1) Total Bytes',
                        '2) Total packets',
                        '3) Application turns',
                        '4) KB per turns',
                        'Are similar in Summaries and Wireshark Conversations statistics',
                        'Note: in Wireshark find your traffic (HTTP requests) in "Statistics" --> "ConversationList" --> "IPv4"'
                        ])
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')
        if type=='UDP':
            SPEC_PRINT(['Analyze PL with Wireshark and validate data in UDP:',
                        '1) Total Bytes',
                        '2) Total packets',
                        '3) Application turns',
                        '4) KB per turns',
                        'Are similar in Summaries and Wireshark Conversations statistics',
                        'Note: in Wireshark find your traffic (DNS requests) in "Statistics" --> "ConversationList" --> "IPv4"'
                        ])
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')
        if type=='TCP':
            SPEC_PRINT(['Analyze PL with Wireshark and validate data in TCP:',
                        '1) Total Bytes',
                        '2) Total packets',
                        '3) Application turns',
                        '4) KB per turns',
                        'Are similar in Summaries and Wireshark Conversations statistics',
                        'Note: in Wireshark find your traffic (HTTP request) in "Statistics" --> "ConversationList" --> "IPv4"',
                        'Important: ALL TCP traffic is calculated, including SSH and so on...'
                        ])
            completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')
            PRINT_DICT(completed_test_cases)

    #Stop capture
    if 'linux' in platform.system().lower() and SAVE_CAPTURE==True:
        pcap_process.terminate()
        time.sleep(5)
        print '--> Stop result'

    return completed_test_cases








            # SPEC_PRINT(['1) Download PL to your OC',
            #             '2) Export *.pcap to JSON format "File --> Export Packet Dissections  --> As JSON"',
            #             '3) Save JSON file locally in with *.json extension'])
            # CONTINUE('To continue?')
            # json_file_data=json.loads(open(CHOOSE_OPTION_FROM_LIST_1([f for f in os.listdir('.') if f.endswith('.json')],'Choose your JSON file:'),'r').read().decode('utf-8','ignore'))
            # for l in json_file_data:
            #     if 'http' in l['_source']['layers'].keys():
            #         print '-'*100
            #         for k in l['_source']['layers']['http']:
            #             print k,'-->',l['_source']['layers']['http'][k]

def HTTP_WATERFALL_TEST_CASES(START_DEFAULT_TEST, IP, PORT, USER, PASSWORD, NV_PROXY_MODE,FLOW_ID, LATENCY, PACKETLOSS, BANDIN, BANDOUT, TEST_NAME, TEST_DESCRIPTION):
    files_to_delete_after_test=[]
    completed_test_cases={}
    if NV_PROXY_MODE=='yes':
        SPEC_PRINT(['Make sure that:','1) You are running this script remotely (NV in Proxy Mode)','2) NVD service is up and running'])
    if NV_PROXY_MODE=='no':
        SPEC_PRINT(['Make sure that:','1) You are running this script locally (NV is not in Proxy Mode)','2) NVD service is up and running'])

    #Start emulation and capture
    if 'linux' in platform.system().lower() and SAVE_CAPTURE==True:
        pcap_process = subprocess.Popen(['tcpdump', '-s', '0', '-i', 'any', '-w',TEST_NAME+'.cap'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)
        print '--> TcpDump PID:'+str(pcap_process.pid)

    types=['HTTP','HTTPS','SELENIUM','HTTP_IN_LOOP','HTTPS_IN_LOOP','METHODS','HTTP_AVERAGE_THROUGHPUT','TIMELINE_BREAKDOWN','MULTIPART_POST','HLS']
    #types=['HLS']



    for t in types:
        CLOSE_ALL_BROWSERS()
        test_case_name='HTTP Waterfall - '+t
        print '\r\n'+'='*30 +' '+test_case_name+' '+'='*30
        if NV_PROXY_MODE=='yes':
            start_default_test_result=START_TEST_IN_PROXY_MODE(IP,PORT,USER,PASSWORD,FLOW_ID,LATENCY,PACKETLOSS,BANDIN,BANDOUT,TEST_NAME+'_'+t,TEST_DESCRIPTION,delay_after_stop=5)
        if NV_PROXY_MODE=='no':
            start_default_test_result=START_DEFAULT_TEST(IP,PORT,USER,PASSWORD,FLOW_ID,LATENCY,PACKETLOSS,BANDIN,BANDOUT,TEST_NAME+'_'+t,TEST_DESCRIPTION,delay_after_stop=5)


        PRINT_DICT(start_default_test_result)
        token=eval(start_default_test_result['Content'])['testToken'] if start_default_test_result['Status']==201 else  sys.exit(1)
        additional_request_headers={'Zahlabut':'Zababun','Oy':'Wey','Drink':'Beer'}

        if t=='MULTIPART_POST':
            test_site='http://httpbin.org/post'
            multiple_files = [('images', ('foo.png', open('chromedriver.exe', 'rb'), 'image/png')),('images', ('bar.png', open('chromedriver.exe', 'rb'), 'image/png'))]
            if NV_PROXY_MODE=='yes':
                r = requests.post(test_site, files=multiple_files,proxies=WGET_PROXIES)
            if NV_PROXY_MODE=='no':
                r = requests.post(test_site, files=multiple_files)
            PRINT_DICT(r.headers)

        if t=='HTTP_AVERAGE_THROUGHPUT':
            test_site='http://www.cnn.com'
            if NV_PROXY_MODE=='yes':
                traffic_result=HTTP_GET_SITE(test_site, 10, WGET_PROXIES, request_headers=additional_request_headers, delay=5)
            if NV_PROXY_MODE=='no':
                traffic_result=HTTP_GET_SITE(test_site, 10, request_headers=additional_request_headers, delay=5)
            PRINT_DICT(traffic_result)

        if t=='HTTP':
            test_site='http://www.cnn.com'
            if NV_PROXY_MODE=='yes':
                traffic_result=HTTP_GET_SITE(test_site, 1, WGET_PROXIES, request_headers=additional_request_headers)
            if NV_PROXY_MODE=='no':
                traffic_result=HTTP_GET_SITE(test_site, 1, request_headers=additional_request_headers)

        if t=='HTTPS':
            test_site='https://login.yahoo.com'
            if NV_PROXY_MODE=='yes':
                traffic_result=HTTP_GET_SITE(test_site, 1, WGET_PROXIES, request_headers=additional_request_headers)
            if NV_PROXY_MODE=='no':
                traffic_result=HTTP_GET_SITE(test_site, 1, request_headers=additional_request_headers)

        if t=='HTTP_IN_LOOP':
            http_loops=10
            test_site='http://www.cnn.com'
            if NV_PROXY_MODE=='yes':
                traffic_result=HTTP_GET_SITE(test_site, http_loops, WGET_PROXIES, request_headers=additional_request_headers)
            if NV_PROXY_MODE=='no':
                traffic_result=HTTP_GET_SITE(test_site, http_loops, request_headers=additional_request_headers)

        if t=='HTTPS_IN_LOOP':
            http_loops=10
            test_site='https://login.yahoo.com'
            if NV_PROXY_MODE=='yes':
                traffic_result=HTTP_GET_SITE(test_site, http_loops, WGET_PROXIES, request_headers=additional_request_headers)
            if NV_PROXY_MODE=='no':
                traffic_result=HTTP_GET_SITE(test_site, http_loops, request_headers=additional_request_headers)


        if t=='TIMELINE_BREAKDOWN':
            print 'Send HTTP POST to Ynet (adding coment to some article)'
            test_site='http://www.ynet.co.il/YediothPortal/Ext/TalkBack/CdaTalkBackTrans/0,2499,L-4915190-0-68-190-0---0,00.html'
            comment_data='WSGBRWSR=FF&name=sadsad&email=asdasdasd&Location=sdfdsf&title=sdfsdfsdf&description=dsfdsfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdf'*1000
            if NV_PROXY_MODE=='yes':
                traffic_result=HTTP_GET_SITE(test_site, 1, WGET_PROXIES, method='POST', post_data=comment_data)
            if NV_PROXY_MODE=='no':
                traffic_result=HTTP_GET_SITE(test_site, 1, method='POST', post_data=comment_data)

        if t=='SELENIUM':
            sites=['https://www.youtube.com/watch?v=v2AC41dglnM&list=PL2MJN9x8D1E74fQH39DPaKP2b6SBMpeBi&index=5',
                   'http://ynet.co.il',
                   'http://fishki.net',
                   'http://baidu.com,'
                   'http://google.co.jp',
                   'http://sohu.com']
            for site in sites:
                if NV_PROXY_MODE=='yes':
                    traffic_result=OPEN_WEB_SITE_SELENIUM(site,SELENIUM_PROXY,30)
                if NV_PROXY_MODE=='no':
                    traffic_result=OPEN_WEB_SITE_SELENIUM(site,timeout=30)
                PRINT_DICT(traffic_result)

        if t=='HLS':
            if NV_PROXY_MODE=='no':
                traffic_result=HLS_VLC(30)
            if NV_PROXY_MODE=='yes':
                traffic_result=HLS_VLC(30,HLS_PROXY)


        if t=='METHODS':
            methods=['POST','PUT','HEAD','DELETE','OPTIONS']
            for m in methods:
                test_site='http://ynet.co.il'
                if NV_PROXY_MODE=='yes':
                    traffic_result=HTTP_GET_SITE(test_site,1,method=m,proxies=WGET_PROXIES)
                if NV_PROXY_MODE=='no':
                    traffic_result=HTTP_GET_SITE(test_site,1,method=m)
                PRINT_DICT(traffic_result)

        if t not in ['SELENIUM','METHODS','HTTP_AVERAGE_THROUGHPUT','MULTIPART_POST']:
            PRINT_DICT(traffic_result)
        #traffic_result=OPEN_WEB_SITE_SELENIUM('http://google.com',NV_REPORT_HTTP_WATERFALL_TAB['SELENIUM_PROXY'],30)

        #Stop test
        stop_test_result=STOP_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token,delay_before_stop=5)
        PRINT_DICT(stop_test_result)
        # Offline analysis
        analyze_result=ANALYSE_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token)
        API_Response=GET_TEST_ANALYTICS_REPORT(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token)
        files_to_delete_after_test.append(OPEN_ZIP_REPORT_WEBBROWSER(API_Response['Content']))

        if t=='HTTP' or t=='HTTPS':
            if NV_PROXY_MODE=='no' and t=='HTTPS':
                SPEC_PRINT(['In NV report "HTTP Waterfall" make sure that:',
                            '1) Code is: N/A',
                            '2) Size(bytes) is ~'+str(traffic_result['Total_Download_Size_[kb]'])+'[kb]',
                            '3) Time(ms) is ~'+str(traffic_result['Average_Download_Time_[msec]']),
                            '4) Use PL find server IP and make sure that it is the same IP that you see in IP field in Report'])
            else:
                SPEC_PRINT(['In NV report "HTTP Waterfall" make sure that:',
                            '1) Code is:'+str(traffic_result['Status_Code']),
                            '2) Size(bytes) is ~'+str(traffic_result['Total_Download_Size_[kb]'])+'[kb]',
                            '3) Time(ms) is ~'+str(traffic_result['Average_Download_Time_[msec]']),
                            '4) Type icon matches received content',
                            'Note: in case when test traffic is HTTPS and NV in Proxy mode',
                            '    value in "Time" field is only time from "Proxy to Xerevr"',
                            '    and does not include "Client to Proxy" (HTTP CONNECT Method) side',
                            '5) Request headers contains extra headers: '+DICT_TO_STRING(additional_request_headers),
                            '6) Response headers are: '+DICT_TO_STRING(traffic_result['Response_Headers']),
                            '7) Use PL find server IP and make sure that it is the same IP that you see in IP field in Report',
                            '8) Use PL and check that value in "Host" field matches the value in "Host" HTTP header in request',
                            '9) Make sure that "Resource" URL is: '+test_site])



        if t=='HTTP_IN_LOOP' or t=='HTTPS_IN_LOOP':
            if NV_PROXY_MODE=='no' and t=='HTTPS_IN_LOOP':
                SPEC_PRINT(['In NV report "HTTP Waterfall" make sure that:',
                            '1) There are '+str(http_loops)+' to '+test_site,
                            '2) Size and Time is approximately the same for all requests'])
            else:
                SPEC_PRINT(['In NV report "HTTP Waterfall" make sure that:',
                            '1) There are '+str(http_loops)+' to '+test_site,
                            '2) Size and Time is approximately the same for all requests',
                            '3) Type is the same for all',
                            '4) In recommendation you can see triggered rules, for example "Do not download the same data twice"'])


        if t=='SELENIUM':
            SPEC_PRINT(['In NV report "HTTP Waterfall" make sure that:',
                        '1) You see traffic of real sites',
                        '2) Verify that each request has: Size,Time,Type... ',
                        '3) Pass over several requests and validate that Type icon matching received data type (Content-Type response header)',
                        '4) Check the UI including: Sort fields, Zoom, Scrolls, Tooltips ...'])

        if t=='METHODS':
            SPEC_PRINT(['In NV report "HTTP Waterfall" make sure that:',
                        '1) You see requests methods: '+str(methods)])

        if t=='HTTP_AVERAGE_THROUGHPUT':
            SPEC_PRINT(['In NV report "HTTP Waterfall" make sure that:',
                        '1) You see 10 HTTP requests to : '+test_site,
                        '2) Download PL and open it with Wireshark',
                        '3) In Wiereshark go to --> Statistics --> TCP Stream Graphs --> Throughput',
                        '4) Make sure that "Max Throughput" and "Time Duration" are similar to displayed graph in NV Report'])

        if t=='TIMELINE_BREAKDOWN':
            SPEC_PRINT(['In NV report "HTTP Waterfall":',
                        '1) You see 1 HTTP POST to to : '+test_site,
                        '2) Download PL and open it with Wireshark',
                        '3) Filter out only your TCP stream (Filter out with "http.requests" anf then "Follow TCP stream")'
                        '4) In Wiereshark go to --> Statistics --> "Flow Graph"',
                        ' and in Show choose "Displayed packets"',
                        '''5) In NV report go to "Timeline Breakdown" and validate that displayed values are''',
                        ''' similar to "Flow Graph" (you'll need to do some manual calculations)''',
                        'Note: you have hint message for all values in "TIMELINE BREAKDOWN": TCP Setup, Client Wait, ... Response'])

        if t=='MULTIPART_POST':
            SPEC_PRINT(['In NV report "HTTP Waterfall" make sure that:',
                        '1) You see single HTTP POST requests (content-type:multipart...) to: '+test_site,
                        'Note: same TCP session is used for 2 POST requests'])

        if t=='HLS':
            SPEC_PRINT(['In NV report "HTTP Waterfall" make sure that:','1) You see HLS traffic'])

        completed_test_cases[test_case_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Test result:')


    #Stop capture
    if 'linux' in platform.system().lower() and SAVE_CAPTURE==True:
        pcap_process.terminate()
        time.sleep(5)
        print '--> Stop result'

    PRINT_DICT(completed_test_cases)
    return completed_test_cases

def GET_HAR_API_TESTING_FUNC(START_DEFAULT_TEST, IP, PORT, USER, PASSWORD, NV_PROXY_MODE,FLOW_ID, LATENCY, PACKETLOSS, BANDIN, BANDOUT, TEST_NAME, TEST_DESCRIPTION):
    null="null"
    TD_DICS_IN_LIST=[]
    SPEC_PRINT(['This step requires:',
                '1) Remote NV in Proxy Mode',
                '2) Make sure that NV is up and running',
                '3) In case of AWS make sure that NV Proxy port is in secure rule',
                '4) com.hpe.nvproxy.includeHttpEntries = true in nvproxy.properties'])
    files_to_delete_after_test=[]
    completed_test_cases={}

    test_cases=[
        {'Name':'Download HAR File - Basic',
        'Scenario':'1) Start emulation 2)Send traffic: single HTTP and single HTTPS reques 3)Send "Stop API" 4)Send "Download HAR API" to get zipped HAR files',
        'Expected Result':'Downloaded HAR files (2 in total) contains sent traffic',
        'Test Result':None},

        {'Name':'Download HAR File - Real Sites',
        'Scenario':'1) Start emulation 2)Use browser and browse to: FACEBOOK (log in page HTTPS) and CNN sites 3)Send "Stop API" 4)Send "Download HAR API" to get zipped HAR files',
        'Expected Result':'Downloaded HAR files (2 in total) contains sent traffic of real sites: images, CSS, JS... ',
        'Test Result':None},

        {'Name':'Download HAR File - Real Sites in Loop',
        'Scenario':'1) Start emulation 2)Use browser and browse to: FACEBOOK (log in page HTTPS) and CNN sites for 20 times 3)Send "Stop API" 4)Send "Download HAR API" to get zipped HAR files',
        'Expected Result':'1) Downloaded ZIP contains split HAR files HAR files (2 in total) 2) Make sure that URLs in HAR matching your traffic',
        'Test Result':None},

        {'Name':'Download HAR File - Get HAR Before stop',
        'Scenario':'1) Start emulation 2)Send traffic: single HTTP and single HTTPS requests 3)Send "Download HAR API" to get zipped HAR files 4)Send Stop API',
        'Expected Result':'Download HAR API fails with: {"ErrorMessage":"No analysis execution is allowed for non-completed tests","errorCode":-4112}',
        'Test Result':None},

        {'Name':'Download HAR File - using bad token ID',
        'Scenario':'1) Start emulation 2)Send traffic: single HTTP and single HTTPS requests 3)Send Stop API 4)Send "Download HAR API" using "bad token ID" to get zipped HAR files ',
        'Expected Result':'Download HAR API fails with: {"ErrorMessage":"The test not found, Test Token: <TOKEN>_ZABABUN","errorCode":-4109}',
        'Test Result':None},

        {'Name':'Download Merged HAR File - basic',
        'Scenario':'1) Start emulation 2)Send traffic: single HTTP and single HTTPS requests 3)Send Stop API 4)Send "Download merged HAR API" to get merged HAR file',
        'Expected Result':'Downloaded HAR file is merged, means contains both: HTTP and HTTPS traffic',
        'Test Result':None},

        {'Name':'Download Merged HAR File - bad token',
        'Scenario':'1) Start emulation 2)Send traffic: single HTTP and single HTTPS requests 3)Send Stop API 4)Send "Download merged HAR API" using "Bad Token" to get merged HAR file',
        'Expected Result':'Downloaded HAR file API fails with proper ErrorCode and ErrorMessage',
        'Test Result':None},

        {'Name':'Download Merged HAR File - ZipResult options',
        'Scenario':'1) Start emulation 2)Send traffic: single HTTP and single HTTPS requests 3)Send Stop API 4)Send "Download merged HAR API" to get merged HAR file (use: True and False otpions in ZipResult)',
        'Expected Result':'1) Downloaded HAR file is merged, means contains both: HTTP and HTTPS traffic '
                          '2) In both cases (ZipResult False/True) HAR file contains your test traffic',
        'Test Result':None},

        {'Name':'Start Analytics Merge Hars Async Request - emulation is completed',
        'Scenario':'1) Start emulation 2)Send traffic: single HTTP and single HTTPS requests 3)Send Stop API 4)Send "Start Analytics Merge Hars Async Request',
        'Expected Result':'API Respond is OK, for example: Content --> {m_data: "HAR_10e3781871aad2fa989d99157944f552_82a9e4d26595c87ab6e442391d8c5bba",m_status: "Idle",errorCode:0}',
        'Test Result':None},

        {'Name':'Start Analytics Merge Hars Async Request - bad token',
        'Scenario':'1) Start emulation 2)Send traffic: single HTTP and single HTTPS requests 3)Send Stop API 4)Send "Start Analytics Merge Hars Async Request using "bad token"',
        'Expected Result':'API fails with proper error message',
        'Test Result':None},

        {'Name':'Start Analytics Merge Hars Async Request - basic E2E scenario_option_1',
        'Scenario':'1) Start emulation 2)Send traffic: single HTTP and single HTTPS requests '
                   '3)Send Stop API '
                   '4)Send "Start Analytics Merge Hars Async Request in loop till m_status: "Finished", then download the result with "Get Merge Result" API (Use both options for zipResult: True and False)',
        'Expected Result':'1) Sampling works and you see "Finished" in "m_status" once merging is done 2) Downloaded merged HAR file contains all request sent by client, means two requests: HTTP and HTTPS '
                          '3) Verify that Execution time is OK (short) as there were only two GETs from client '
                          '4) Merged HAR is OK for both zipResult options  '
                          '5) "m_status" is changed from "idle" to "finished" during the sampling',
        'Test Result':None},

        {'Name':'Start Analytics Merge Hars Async Request - basic E2E scenario_option_2',
        'Scenario':'1) Start emulation 2)Send traffic: single HTTP and single HTTPS requests 3)Send Stop API 4)Send "Start Analytics Merge Hars Async Request, do not wait till you see'
                   '"Finished" in "m_status" and start sending "Get Merge Result" until you getting the merged HAR file in response '
                   '4) Also try to use "bad m_data value" in order to receive proper error message',
        'Expected Result':'1) Downloaded merged HAR file contains all request sent by client, means two requests: HTTP and HTTPS, '
                          '2) Verify that Execution time is OK (short) as there were only two GETs from client'
                          '3) Make sure that "m_status" is changed from "idle" to "finished" while sampling'
                          '4) Proper error received in case of "bad m_data" value',
        'Test Result':None},

        {'Name':'Start Analytics Merge Hars Async Request - real browsing',
        'Scenario':'1) Start emulation 2)Start browsing to HTTP and HTTPS sites 3)Send Stop API 4)Send "Start Analytics Merge Hars Async Request, do not wait till you see'
                   '"Finished" in "m_status" and start sending "Get Merge Result" until you getting the merged HAR file in response',
        'Expected Result':'1) Downloaded merged HAR file contains all request sent by client, means all browse you did, '
                          '2) Verify that Execution time is OK'
                          '3) Make sure that "m_status" is changed from "idle" to "finished" while sampling'
                          '4) Check ERRORs in logs + CPU and Memory during the test',
        'Test Result':None},

        {'Name':'Start Analytics Merge Hars Async Request - cancel merge operation',
        'Scenario':'1) Start emulation 2)Send traffic: single HTTP and single HTTPS requests 3)Send Stop API 4)Send "Start Analytics Merge Hars Async Request '
                   '5) Cancel merge operation with "Cancel Merge HARs Operation" API' ,
        'Expected Result':'Async HAR merge is started and interrupted immediately and response code is 204',
        'Test Result':None},

        {'Name':'Start Analytics Merge Hars Async Request - cancel merge operation BAD_TOKEN',
        'Scenario':'1) Start emulation 2)Send traffic: single HTTP and single HTTPS requests 3)Send Stop API 4)Send "Start Analytics Merge Hars Async Request '
                   '5) Cancel merge operation with "Cancel Merge HARs Operation" API", use "Bad Token ID" ',
        'Expected Result':'Cancel HAR Merge Operation fails with proper error code and error message',
        'Test Result':None},
    ]









    #### 11111111111111111 ###
    for test in test_cases:
        SPEC_PRINT([test['Name'], test['Scenario']])

        #This section is for all Download HAR API test cases
        if test['Name'] in ['Download HAR File - Basic','Download HAR File - Real Sites',
                            'Download HAR File - Real Sites in Loop','Download HAR File - Get HAR Before stop',
                            'Download HAR File - using bad token ID',]:
            #Start emulation and capture
            if 'linux' in platform.system().lower() and SAVE_CAPTURE==True:
                pcap_process = subprocess.Popen(['tcpdump', '-s', '0', '-i', 'any', '-w',TEST_NAME+'.cap'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                time.sleep(5)
                print '--> TcpDump PID:'+str(pcap_process.pid)
            start_default_test_result=START_TEST_IN_PROXY_MODE(IP,PORT,USER,PASSWORD,FLOW_ID,LATENCY,PACKETLOSS,BANDIN,BANDOUT,TEST_NAME+'_'+test['Name'],TEST_DESCRIPTION,delay_after_stop=5)
            PRINT_DICT(start_default_test_result)
            token=eval(start_default_test_result['Content'])['testToken'] if start_default_test_result['Status']==201 else  sys.exit(1)


            #Traffic
            if test['Name']=='Download HAR File - Basic' or test['Name']=='Download HAR File - Get HAR Before stop' or test['Name']=='Download HAR File - using bad token ID':
                #Start traffic
                sites=['http://www.cnn.com','https://facebook.com']
                for site in sites:
                    traffic_result=HTTP_GET_SITE(site, 1, WGET_PROXIES)
                    print traffic_result


            if test['Name']=='Download HAR File - Real Sites':
                #Start traffic
                sites=['http://www.cnn.com','https://facebook.com']
                for site in sites:
                    traffic_result=OPEN_WEB_SITE_SELENIUM(site,SELENIUM_PROXY,30)
                    print traffic_result

            if test['Name']=='Download HAR File - Real Sites in Loop':
                #Start traffic
                sites=['http://www.cnn.com','https://facebook.com']
                loops=int(raw_input('Please ENTER loop number (100): '))
                for site in sites:
                    for x in range(0,loops):
                        traffic_result=OPEN_WEB_SITE_SELENIUM(site,SELENIUM_PROXY,30)
                        print traffic_result

            #Stop test
            if test['Name']!='Download HAR File - Get HAR Before stop':
                stop_test_result=STOP_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token,delay_before_stop=5)
                PRINT_DICT(stop_test_result)

            #Download HAR
            if test['Name']=='Download HAR File - using bad token ID':
                har_result=DOWNLOAD_HAR_FILE_BY_TOKEN(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token+'_ZABABUN')
            else:
                har_result=DOWNLOAD_HAR_FILE_BY_TOKEN(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token)
            PRINT_DICT(har_result)
            if 'Request_URLs_Per_HAR_File' in har_result.keys():
                for k in har_result['Request_URLs_Per_HAR_File'].keys():
                    PRINT_DICT(har_result['Request_URLs_Per_HAR_File'][k],limit=False)

            #Stop test, for "Download HAR File - Get HAR Before stop" scenario only
            if test['Name']=='Download HAR File - Get HAR Before stop':
                stop_test_result=STOP_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token,delay_before_stop=5)
                PRINT_DICT(stop_test_result)


            #Analyze test by token
            ANALYSE_TEST_BY_TOKEN(IP,PORT,USER,PASSWORD,token)

            #Stop capture
            if 'linux' in platform.system().lower() and SAVE_CAPTURE==True:
                pcap_process.terminate()
                time.sleep(5)
                print '--> Stop result'



            # Get Test result from User and organize result
            SPEC_PRINT([test['Scenario'],test['Expected Result']])
            test_result=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAILED','N/A'],'Test case result is: ')
            test['Test Result']=test_result
            completed_test_cases[test['Name']]=test_result




        ### 2222222222 ###
        #This section is for all Download MERGED HAR API test cases
        elif test['Name'] in ['Download Merged HAR File - basic','Download Merged HAR File - bad token','Download Merged HAR File - ZipResult options']:

            #Start emulation and capture
            if 'linux' in platform.system().lower() and SAVE_CAPTURE==True:
                pcap_process = subprocess.Popen(['tcpdump', '-s', '0', '-i', 'any', '-w',TEST_NAME+'.cap'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                time.sleep(5)
                print '--> TcpDump PID:'+str(pcap_process.pid)
            start_default_test_result=START_TEST_IN_PROXY_MODE(IP,PORT,USER,PASSWORD,FLOW_ID,LATENCY,PACKETLOSS,BANDIN,BANDOUT,TEST_NAME+'_'+test['Name'],TEST_DESCRIPTION,delay_after_stop=5)
            PRINT_DICT(start_default_test_result)
            token=eval(start_default_test_result['Content'])['testToken'] if start_default_test_result['Status']==201 else  sys.exit(1)


            #Traffic
            if test['Name'] in ['Download Merged HAR File - basic','Download Merged HAR File - ZipResult options','Download Merged HAR File - bad token']:
                #Start traffic
                sites=['http://www.cnn.com','https://facebook.com']
                for site in sites:
                    traffic_result=HTTP_GET_SITE(site, 1, WGET_PROXIES)
                    print traffic_result


            #Stop test
            stop_test_result=STOP_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token,delay_before_stop=5)
            PRINT_DICT(stop_test_result)

            #Get merged HAR file
            if test['Name']=='Download Merged HAR File - basic':
                har_result=GET_MERGED_HAR_BY_TOKEN(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,zipResult=False)
                PRINT_DICT(har_result)

            if test['Name']=='Download Merged HAR File - bad token':
                har_result=GET_MERGED_HAR_BY_TOKEN(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token+'_ZABABUN',zipResult=False)
                PRINT_DICT(har_result)

            if test['Name']=='Download Merged HAR File - ZipResult options':
                options=[False,True]
                for opt in options:
                    har_result=GET_MERGED_HAR_BY_TOKEN(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,zipResult=opt)
                    PRINT_DICT(har_result)

            #Analyze test by token
            ANALYSE_TEST_BY_TOKEN(IP,PORT,USER,PASSWORD,token)

            #Stop capture
            if 'linux' in platform.system().lower() and SAVE_CAPTURE==True:
                pcap_process.terminate()
                time.sleep(5)
                print '--> Stop result'


            # Get Test result from User and organize result
            SPEC_PRINT([test['Scenario'],test['Expected Result']])
            test_result=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAILED','N/A'],'Test case result is: ')
            test['Test Result']=test_result
            completed_test_cases[test['Name']]=test_result




        ### 3333333333 ###
        #This section is for Asyncronious Analysis Merge APIs test cases
        elif test['Name'] in ['Start Analytics Merge Hars Async Request - emulation is completed',
                              'Start Analytics Merge Hars Async Request - bad token',
                              'Start Analytics Merge Hars Async Request - basic E2E scenario_option_1',
                              'Start Analytics Merge Hars Async Request - basic E2E scenario_option_2',
                              'Start Analytics Merge Hars Async Request - real browsing',
                              'Start Analytics Merge Hars Async Request - cancel merge operation',
                              'Start Analytics Merge Hars Async Request - cancel merge operation BAD_TOKEN']:

            #Start emulation and capture
            if 'linux' in platform.system().lower() and SAVE_CAPTURE==True:
                pcap_process = subprocess.Popen(['tcpdump', '-s', '0', '-i', 'any', '-w',TEST_NAME+'.cap'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                time.sleep(5)
                print '--> TcpDump PID:'+str(pcap_process.pid)
            start_default_test_result=START_TEST_IN_PROXY_MODE(IP,PORT,USER,PASSWORD,FLOW_ID,LATENCY,PACKETLOSS,BANDIN,BANDOUT,TEST_NAME+'_'+test['Name'],TEST_DESCRIPTION,delay_after_stop=5)
            PRINT_DICT(start_default_test_result)
            token=eval(start_default_test_result['Content'])['testToken'] if start_default_test_result['Status']==201 else  sys.exit(1)


            #Traffic
            if test['Name']=='Start Analytics Merge Hars Async Request - real browsing':
                sites=['http://google.com','http://ynet.co.il','http://walla.co.il', 'http://fishki.net',
                       'http://cnn.com', 'http://bbbc.com','https://twitter.com/?lang=en','http://one.co.il','https://facebook.com']
                for s in sites:
                    print OPEN_WEB_SITE_SELENIUM(s,SELENIUM_PROXY,timeout=30)

            if test['Name'] in ['Start Analytics Merge Hars Async Request - emulation is completed',
                                'Start Analytics Merge Hars Async Request - bad token',
                                'Start Analytics Merge Hars Async Request - basic E2E scenario_option_1',
                                'Start Analytics Merge Hars Async Request - basic E2E scenario_option_2',
                                'Start Analytics Merge Hars Async Request - cancel merge operation',
                                'Start Analytics Merge Hars Async Request - cancel merge operation BAD_TOKEN']:
                sites=['http://www.cnn.com','https://facebook.com']
                for site in sites:
                    traffic_result=HTTP_GET_SITE(site, 1, WGET_PROXIES)
                    print traffic_result


            #Stop test
            stop_test_result=STOP_TEST_BY_TOKEN(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, token,delay_before_stop=5)
            PRINT_DICT(stop_test_result)

            #Start Analytics Merge Hars Async Request
            if test['Name']=='Start Analytics Merge Hars Async Request - emulation is completed':
                har_result=START_HAR_ANALYTICS_MERGE_HARS_ASYNC_REQUEST(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token)
                PRINT_DICT(har_result)

            if test['Name']=='Start Analytics Merge Hars Async Request - bad token':
                har_result=START_HAR_ANALYTICS_MERGE_HARS_ASYNC_REQUEST(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,TOKEN='ZABABUN')
                PRINT_DICT(har_result)

            if test['Name']=='Start Analytics Merge Hars Async Request - cancel merge operation':
                start_result=START_HAR_ANALYTICS_MERGE_HARS_ASYNC_REQUEST(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,delay=0)
                m_data=eval(start_result['Content'])['m_data']
                PRINT_DICT(start_result)
                cancel_merge=CANCEL_MERGE_HAR_BY_TOKEN(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,delay=0)
                PRINT_DICT(cancel_merge)


            if test['Name']=='Start Analytics Merge Hars Async Request - cancel merge operation BAD_TOKEN':
                start_result=START_HAR_ANALYTICS_MERGE_HARS_ASYNC_REQUEST(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,delay=0)
                m_data=eval(start_result['Content'])['m_data']
                PRINT_DICT(start_result)
                cancel_merge=CANCEL_MERGE_HAR_BY_TOKEN(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token+'ZABABUN',delay=0)
                PRINT_DICT(cancel_merge)







            if test['Name']=='Start Analytics Merge Hars Async Request - basic E2E scenario_option_1':
                m_status=None
                start_time=time.time()
                timeout=60*5
                while_start=time.time()
                while m_status!='Finished' and while_start <start_time+timeout:
                    start_result=START_HAR_ANALYTICS_MERGE_HARS_ASYNC_REQUEST(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,delay=0)
                    m_status=eval(start_result['Content'])['m_status']
                    PRINT_DICT(start_result)
                if m_status=='Finished':
                    SPEC_PRINT(['zipResult=False'])
                    get_har=GET_READY_ASYNC_MERGED_HAR_BY_MDATA(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, eval(start_result['Content'])['m_data'], zipResult=False, returnData=True,delay=0)
                    PRINT_DICT(get_har)
                    SPEC_PRINT(['zipResult=True'])
                    get_har=GET_READY_ASYNC_MERGED_HAR_BY_MDATA(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, eval(start_result['Content'])['m_data'], zipResult=True, returnData=True,delay=0)
                    PRINT_DICT(get_har)
                else:
                    is_timeout=False
                    if while_start>start_time+timeout:
                        is_timeout=True
                    SPEC_PRINT(['Latest m_status is: '+str(m_status),'Cannot GET merged HAR files','Test Failed!!!','Is_Timeout:'+str(is_timeout)])
                SPEC_PRINT(['Test Execution time',str(time.time()-start_time)+'[sec]'])

            if test['Name'] in ['Start Analytics Merge Hars Async Request - basic E2E scenario_option_2','Start Analytics Merge Hars Async Request - real browsing']:
                start_result=START_HAR_ANALYTICS_MERGE_HARS_ASYNC_REQUEST(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,delay=0)
                m_status=eval(start_result['Content'])['m_status']
                m_data=eval(start_result['Content'])['m_data']
                PRINT_DICT(start_result)
                #Content --> {"m_data":null,"m_status":"Idle","errorCode":0}
                start_time=time.time()
                timeout=60*5
                while_start=time.time()
                while m_status!='Finished' and while_start <start_time+timeout:
                    get_result=GET_READY_ASYNC_MERGED_HAR_BY_MDATA(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, m_data, zipResult=False, returnData=False,delay=0)
                    m_status=eval(get_result['Content'])['m_status']
                    PRINT_DICT(get_result)
                if m_status=='Finished':
                    get_result=GET_READY_ASYNC_MERGED_HAR_BY_MDATA(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, eval(start_result['Content'])['m_data'], zipResult=False, returnData=True,delay=0)
                    PRINT_DICT(get_result)
                    SPEC_PRINT(['"Bad m_data value" in URL'])
                    if test['Name']=='Start Analytics Merge Hars Async Request - basic E2E scenario_option_2':
                        get_result=GET_READY_ASYNC_MERGED_HAR_BY_MDATA(TM_IP, TM_PORT, TM_USER, TM_PASSWORD, eval(start_result['Content'])['m_data']+'_ZABABUN', zipResult=False, returnData=True,delay=0)
                        PRINT_DICT(get_result)

                    if test['Name']=='Start Analytics Merge Hars Async Request - real browsing':
                        for key in get_result.keys():
                            if key=='Request_URLs_In_HAR_File':
                                for u in get_result['Request_URLs_In_HAR_File']['URLs']:
                                    print u

                else:
                    is_timeout=False
                    if while_start>start_time+timeout:
                        is_timeout=True
                    SPEC_PRINT(['Latest m_status is: '+str(m_status),'Cannot GET merged HAR files','Test Failed!!!','Is_Timeout:'+str(is_timeout)])
                SPEC_PRINT(['Test Execution time',str(time.time()-start_time)+'[sec]'])

            #Analyze test by token
            ANALYSE_TEST_BY_TOKEN(IP,PORT,USER,PASSWORD,token)


            #Stop capture
            if 'linux' in platform.system().lower() and SAVE_CAPTURE==True:
                pcap_process.terminate()
                time.sleep(5)
                print '--> Stop result'


            # Get Test result from User and organize result
            SPEC_PRINT([test['Scenario'],test['Expected Result']])
            test_result=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAILED','N/A'],'Test case result is: ')
            test['Test Result']=test_result
            completed_test_cases[test['Name']]=test_result

        else:
            print "Unknown Test Case:" +test('Name')
        TD_DICS_IN_LIST.append(test)


    WRITE_DICTS_TO_CSV('TD_HAR_APIs.csv',TD_DICS_IN_LIST)
    PRINT_DICT(completed_test_cases)
    return completed_test_cases

def RUN_MC_APIS_SCENARIOS(API_SERVER_DOMAIN, API_SERVER_PORT, IS_HTTPS_SETUP, AUTH_USER, AUTH_PASS):
    CLOSE_ALL_BROWSERS()
    CLEANER()
    test_results={}



    # ### Testing Proxy HTTPS issues for Less  ###
    # # MitmProxy #
    # url='https://sso.prologis.com/'
    # mitmproxy_ip='54.224.19.152'
    # mitmproxy_port='8080'
    # mitm_proxy=mitmproxy_ip+':'+mitmproxy_port
    # print OPEN_WEB_SITE_SELENIUM(url,mitm_proxy)
    # ### Testing via NV_Proxy ###
    # TM_IP='52.20.143.142'
    # TM_PORT='8182'
    # TM_USER='admin123'
    # TM_PASSWORD='Admin123'
    # NV_Proxy_Port='8080'
    # start_default_test_result=START_TEST_IN_PROXY_MODE(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,'My_Flow', '1', '0', '2048.0', '2048.0','test_name_'+str(time.time()),'TEST_DESCRIPTION',delay_after_stop=5)
    # Nv_Proxy=TM_IP+':'+TM_PORT
    # print OPEN_WEB_SITE_SELENIUM(url,mitm_proxy)
    # sys.exit(1)





    # ####################################################### Check proxy backdoor ######################################################################################################
    # #start_default_test_result=START_DEFAULT_TEST(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,'My_Flow', '1', '0', '2048.0', '2048.0','test_name_'+str(time.time()),'TEST_DESCRIPTION',delay_after_stop=5)
    # start_default_test_result=START_TEST_IN_PROXY_MODE(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,'My_Flow', '1', '0', '2048.0', '2048.0','test_name_'+str(time.time()),'TEST_DESCRIPTION',delay_after_stop=5)
    #
    # PRINT_DICT(start_default_test_result)
    # token=eval(start_default_test_result['Content'])['testToken'] if start_default_test_result['Status']==201 else  sys.exit(1)
    # print token
    # DST_PORT=65000
    # WGET_PROXIES = {'http': 'http://' + TM_IP + ':' + str(DST_PORT), 'https': 'https://' + TM_IP + ':' + str(DST_PORT)}
    # PRINT_DICT(HTTP_GET_SITE('https://accounts.google.com/Login#identifier',5,proxies=WGET_PROXIES))
    # PRINT_DICT(HTTP_GET_SITE('http://mail.ru',5,proxies=WGET_PROXIES))
    # time.sleep(2)
    # #PRINT_DICT(STOP_TEST_BY_TOKEN(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token))
    # #PRINT_DICT(ANALYSE_TEST_BY_TOKEN(TM_IP,TM_PORT,TM_USER,TM_PASSWORD,token,DST_PORT))
    # sys.exit(1)
    # ###################################################################################################################################################################################



    # Get Version #
    get_version=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='GET',url_path='shunra/api/configuration/version',
                         additional_headers={'Accept':'application/json'}, api_name='GET_VERSION')
    get_version_response=get_version.RUN_REQUEST()
    PRINT_DICT(get_version_response)
    SPEC_PRINT(['Check response content with JSON viewer'])


    # Get configuration settings #
    get_settings=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='GET',url_path='shunra/api/configuration/settings',
                         additional_headers={'Accept':'application/json'}, api_name='GET_SETTINGS')
    get_settings_response=get_settings.RUN_REQUEST()
    PRINT_DICT(get_settings_response)
    SPEC_PRINT(['Check response content with JSON viewer', 'As for now response should be empty'])


    ### Shunra API get profiles ###
    # Simple GET profiles
    get_profiles=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='GET',url_path='shunra/api/profile',
                         additional_headers={'Accept':'application/json'}, api_name='GET_PROFILES')
    get_profiles_response=get_profiles.RUN_REQUEST()
    PRINT_DICT(get_profiles_response)
    all_profiles=get_profiles_response['Content_As_Dict']['profiles']
    print all_profiles

    test_results['Get_Profiles']='PASS'
    #Start and Stop new emulation per profile #
    for prof in all_profiles:
        # Start #
        profile_id=prof['id']
        network_scenario=prof['name']
        test_name=prof['name'].replace(' ','_')+'_'+str(time.time())
        device_id='zababun_device_id_123'
        flow_id='zababun_flow_id_123'


        src_ip=GET_MY_PUBLIC_IP()
        #src_ip='10.40.1.89'


        pl_id='zababun_pl_id_123'
        test_description='zababun_test_description'
        start_post_data={"deviceId": device_id,
                         "flows":[{"flowId": flow_id, "srcIp": src_ip, "profileId": profile_id, "isCaptureClientPL": True}],
                         "testMetadata": {"testName":test_name, "description": test_description, "networkScenario": network_scenario}}
        start_obj=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='POST',url_path='shunra/api/emulation/custom',
                          additional_headers={'Accept':'application/json','Content-Type':'application/json'},params={'mode':'MULTI_USER','useProxy':'true'},request_payload=start_post_data, api_name='START_API')
        start_resp=start_obj.RUN_REQUEST()
        PRINT_DICT(start_resp)
        print start_resp['Content']
        test_token=start_resp['Content_As_Dict']['testToken']
        if MC_INTEGRATION_APIS['NV_PROXY_PORT']==None:
            proxy_ip=start_resp['Content_As_Dict']['proxyIpAddr']
            proxy_port=start_resp['Content_As_Dict']['proxyPort']
        else:
            proxy_ip=MC_INTEGRATION_APIS['API_SERVER_DOMAIN']
            proxy_port=MC_INTEGRATION_APIS['NV_PROXY_PORT']


        # Traffic #
        # Set proxies #
        WGET_PROXIES = {'http': 'http://' + proxy_ip + ':' + str(proxy_port), 'https': 'https://' + proxy_ip + ':' + str(proxy_port)}
        SELENIUM_PROXY=proxy_ip+':'+str(proxy_port)
        SPEC_PRINT([str(WGET_PROXIES)])
        print HTTP_GET_SITE('http://cnn.com',1,WGET_PROXIES)
        print HTTP_GET_SITE('https://facebook.com',1,WGET_PROXIES)


        # Realtime update #
        random_profile=prof
        while prof==random_profile:
            random_profile=random.choice(all_profiles)
        SPEC_PRINT([str(prof),str(random_profile)])
        profile_id=random_profile['id']
        network_scenario=random_profile['name']
        real_time_update_post_data={ "testMetadata": { "networkScenario": network_scenario}, "flows": [{ "profileId": profile_id, "isDefaultFlow": "true", "flowId":flow_id}]}
        real_time_update_obj=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='PUT',url_path='shunra/api/emulation/custom/'+test_token,
                          additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload=real_time_update_post_data,api_name='REAL_TIME_UPDATE')
        real_time_update_resp=real_time_update_obj.RUN_REQUEST()
        PRINT_DICT(real_time_update_resp)


        # Traffic #
        print HTTP_GET_SITE('http://cnn.com',1,WGET_PROXIES)
        print HTTP_GET_SITE('https://facebook.com',1,WGET_PROXIES)

        # Connect #
        connect_post_data={}
        connect_payload_options=[{"overwriteExistingConnection":"true"},
                                 #{"plId":pl_id,"overwriteExistingConnection":"true"},
                                 #{"clientId":src_ip, "overwriteExistingConnection":"true"},
                                 #{"flowId":flow_id, "overwriteExistingConnection":"true"},
                                 #{}
                                 ]
        connect_results=[]
        for connect_option in connect_payload_options:
            SPEC_PRINT([str(connect_option)])
            connect_obj=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='POST',url_path='shunra/api/transactionmanager/'+test_token,
                        additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload=connect_option, body_type='JSON',api_name='CONNECT_FOR_TRANSACTIONS')
            connect_resp=connect_obj.RUN_REQUEST()

            print connect_resp['Content_As_Dict']
            transaction_id=connect_resp['Content_As_Dict']['transactionManagerSessionIdentifier']

            PRINT_DICT(connect_resp)
            connect_results.append(transaction_id)
        SPEC_PRINT(connect_results)


        # Transactions X in total #
        for x in range(1,6):
            # Transaction Start #
            start_transaction_data={"transactionName":"Trans", "transactionDescription":"Paka_paka"}
            print start_transaction_data
            start_trans_obj=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='POST',
                                    url_path='shunra/api/transactionmanager/transaction/'+transaction_id+'?reuseExistingByName=true',
                                    additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload=start_transaction_data, body_type='JSON', api_name='START_TRANSACTION')
            start_trans_resp=start_trans_obj.RUN_REQUEST()
            PRINT_DICT(start_trans_resp)

            # Traffic #
            #OPEN_WEB_SITE_SELENIUM('http://ynet.co.il',proxy=SELENIUM_PROXY, timeout=10)
            #OPEN_WEB_SITE_SELENIUM('https://facebook.com',proxy=SELENIUM_PROXY, timeout=10)
            print HTTP_GET_SITE('http://cnn.com',1,WGET_PROXIES)
            print HTTP_GET_SITE('https://facebook.com',1,WGET_PROXIES)


            # Stop Transaction #
            #https://dev.hpenv.com/shunra/api/transactionmanager/transaction/{token}/{token}
            stop_trans_obj=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='PUT',url_path='shunra/api/transactionmanager/transaction/'+test_token+'/'+transaction_id,
                            additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload={}, body_type='JSON', api_name='STOP_TRANSACTION')
            stop_trans_resp=stop_trans_obj.RUN_REQUEST()
            PRINT_DICT(stop_trans_resp)


            # Real time update #
            random_profile=random.choice(all_profiles)
            all_profiles.remove(random_profile)
            profile_id=random_profile['id']
            network_scenario=random_profile['name']
            real_time_update_post_data={ "testMetadata": { "networkScenario": network_scenario}, "flows": [{ "profileId": profile_id, "isDefaultFlow": "true", "flowId":flow_id}]}
            real_time_update_obj=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='PUT',url_path='shunra/api/emulation/custom/'+test_token,
                              additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload=real_time_update_post_data,api_name='REAL_TIME_UPDATE')
            real_time_update_resp=real_time_update_obj.RUN_REQUEST()
            PRINT_DICT(real_time_update_resp)



        # Stop #
        stop_put_data='''{"testTokens": ["token"]}'''.replace('token',test_token)
        stop_obj=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='PUT',url_path='shunra/api/emulation/stop',
                        additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload=stop_put_data, body_type='STRING', api_name='STOP_API')
        stop_resp=stop_obj.RUN_REQUEST()
        PRINT_DICT(stop_resp)



        # Analyze #
        start_sampling=time.time()
        sampling_timeout=30
        m_status=None
        is_timeout=False
        while m_status!='Finished' and time.time()<start_sampling+sampling_timeout:
            analyze_obj=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='PUT',url_path='shunra/api/analysisexpress/analyze/'+test_token,
                            additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload={}, body_type='JSON', api_name='ANALYZE_API')
            analyze_resp=analyze_obj.RUN_REQUEST()
            m_status=analyze_resp['Content_As_Dict']['m_status']
            SPEC_PRINT([str(analyze_resp['Content_As_Dict'])])
            PRINT_DICT(analyze_resp)
            if time.time()>start_sampling+sampling_timeout:
                is_timeout=True
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
                PRINT_DICT(report_resp)
                if '''"m_status":"Empty"''' in report_resp['Content']:
                    m_status='Empty'
                else:
                    m_status='Done'
                SPEC_PRINT([m_status])
                time.sleep(5)
            if time.time()>start_sampling+sampling_timeout:
                is_timeout=True
            if zi=='true' and is_timeout==False:
                OPEN_ZIP_REPORT_WEBBROWSER(report_resp['Content'])
            if zi=='false' and is_timeout==False:
                OPEN_REPORT_WEBBROWSER(report_resp['Content'])

        ### Get HAR Async ###
        # Get HAR #
        start_sampling=time.time()
        sampling_timeout=30
        m_status=None
        is_timeout=False
        while m_status!='Finished' and time.time()<start_sampling+sampling_timeout:
            get_har_obj=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='PUT',url_path='shunra/api/analysisexpress/extract/har/'+test_token,
                            additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload={}, body_type='JSON', api_name='GET_HAR_ASYNCHRONOUS_API')
            get_har_resp=get_har_obj.RUN_REQUEST()
            m_status=get_har_resp['Content_As_Dict']['m_status']
            SPEC_PRINT([str(get_har_resp['Content_As_Dict'])])
            PRINT_DICT(get_har_resp)
            if time.time()>start_sampling+sampling_timeout:
                is_timeout=True
        if is_timeout==True:
            SPEC_PRINT(['Achtung, timeout of: '+str(sampling_timeout)+' was reached!!!'])
        # Get the HAR #
        get_har_file=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='GET',url_path='shunra/api/analysisreport/har/'+test_token,
                        additional_headers={'Accept':'application/json','Content-Type':'application/json'}, api_name='GET_READY_HAR_FILE_API')
        get_har_file_resp=get_har_file.RUN_REQUEST()
        PRINT_DICT(get_har_file_resp)

        har_file_name='Async_Har_'+profile_id+'.har'
        DELETE_LOG_CONTENT(har_file_name)
        INSERT_TO_LOG(har_file_name,get_har_file_resp['Content'])
        PRINT_DICT(GET_ALL_REQUEST_URLS_FROM_HAR(har_file_name, har_is_ziped=True))



        # This section is for testing Get Report and Get HAR in synchronous mode #
        # Start a new emulation #
        SPEC_PRINT(['#'*1000])
        start_obj_1=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='POST',url_path='shunra/api/emulation/custom',
                          additional_headers={'Accept':'application/json','Content-Type':'application/json'},params={'mode':'MULTI_USER','useProxy':'true'},request_payload=start_post_data, api_name='START_API')
        start_resp=start_obj_1.RUN_REQUEST()
        PRINT_DICT(start_resp)
        test_token=start_resp['Content_As_Dict']['testToken']
        proxy_ip=start_resp['Content_As_Dict']['proxyIpAddr']
        proxy_port=start_resp['Content_As_Dict']['proxyPort']


        # Traffic #
        # Set proxies #
        WGET_PROXIES = {'http': 'http://' + proxy_ip + ':' + str(proxy_port), 'https': 'https://' + proxy_ip + ':' + str(proxy_port)}
        SELENIUM_PROXY=proxy_ip+':'+str(proxy_port)
        SPEC_PRINT([str(WGET_PROXIES)])
        print HTTP_GET_SITE('http://cnn.com',10,WGET_PROXIES)
        print HTTP_GET_SITE('https://facebook.com',10,WGET_PROXIES)


        # ### To create large HAR for Itamar ###
        # sites=['http://cnn.com','http://walla.co.il','http://ynet.co.il','http://nana.co.il','http://fishki.net']
        # for s in sites:
        #     OPEN_WEB_SITE_SELENIUM(s,proxy=SELENIUM_PROXY, timeout=60)


        ### Browse for 8 minutes ###
        start_browsing=time.time()
        stop_browsing_at=start_browsing+8*60
        while time.time()<stop_browsing_at:
            OPEN_WEB_SITE_SELENIUM('http://ynet.co.il',proxy=SELENIUM_PROXY, timeout=20)

        # Stop #
        stop_put_data='''{"testTokens": ["token"]}'''.replace('token',test_token)
        stop_obj_1=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='PUT',url_path='shunra/api/emulation/stop',
                        additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload=stop_put_data, body_type='STRING', api_name='STOP_API')
        stop_resp=stop_obj_1.RUN_REQUEST()
        PRINT_DICT(stop_resp)


        # Get HAR synchronous mode#
        get_har_file_1=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='GET',url_path='shunra/api/analysisreport/har/'+test_token,
                        additional_headers={'Accept':'application/json','Content-Type':'application/json'}, api_name='GET_HAR_SYNCHONOUS')
        get_har_file_resp=get_har_file_1.RUN_REQUEST()
        PRINT_DICT(get_har_file_resp)
        har_file_name='Sync_Har_'+profile_id+'.har'
        DELETE_LOG_CONTENT(har_file_name)
        INSERT_TO_LOG(har_file_name,get_har_file_resp['Content'])
        PRINT_DICT(GET_ALL_REQUEST_URLS_FROM_HAR(har_file_name, har_is_ziped=True))

        # Get NV Report synchronous mode#
        get_nv_report_sync=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='PUT',url_path='shunra/api/analysisreport/analyze/'+test_token,
                        additional_headers={'Accept':'application/json','Content-Type':'application/json'}, api_name='GET_REPORT_SYNCHONOUS')
        get_nv_report_resp=get_nv_report_sync.RUN_REQUEST()
        PRINT_DICT(get_nv_report_resp)
        OPEN_ZIP_REPORT_WEBBROWSER(get_nv_report_resp['Content'])


        CONTINUE('Continue to the next profile?')




    PRINT_DICT(test_results)








    return test_results

def RUN_ESTIMATED_SERVER_TIME_TEST():
    ############################################### NV In PROXY MODE ################################################
    CLOSE_ALL_BROWSERS()
    CLEANER()
    test_results={}
    ask_to_continue_after_each_profile=CHOOSE_OPTION_FROM_LIST_1(['True','False'],'False - run all profiles, True - ask if to continue after each profile')
    ports_parameters='?ports=8888,65000,80,443,8080,8090'
    print_json=CHOOSE_OPTION_FROM_LIST_1(['True','False'],'To print JSON in prompt output or not?')

    NV_MODE=['AS_PROXY','LOCAL_NV']
    TEST=CHOOSE_OPTION_FROM_LIST_1(['WGET_Traffic - Single HTTP get per TCP Connection',
                                    'WGET Traffic - multiply HTTP gets per TCP Connection',
                                    'Real traffic to WEB site with Selenium'],'Please choose your test: ')

    if TEST=='WGET_Traffic - Single HTTP get per TCP Connection':
        number_of_test_sites=int(raw_input('Please enter the number of HTTP/HTTPS sites for your test: '))
    if TEST=='WGET Traffic - multiply HTTP gets per TCP Connection':
        number_of_test_sites=int(raw_input('Please enter the number of HTTP/HTTPS sites for your test: '))
        number_of_gets_per_tcp=int(raw_input('Please enter the number of HTTP get you would like to send per TCP connection: '))
    if TEST=='Real traffic to WEB site with Selenium':
        test_site='http://google.com'
        SPEC_PRINT([test_site +' will be used for testing!!!'])

    result_dic_list=[]
    exported_values_as_list=[]

    # Testing if Test servers: HTTP and HTTPS are up and running #
    if TEST in ['WGET_Traffic - Single HTTP get per TCP Connection','WGET Traffic - multiply HTTP gets per TCP Connection']:
        test_servers={'HTTP_SEVER':ESTIMATED_SERVER_TIME['HTTP_SERVER'],'HTTPS_SERVER':ESTIMATED_SERVER_TIME['HTTPS_SERVER']}
        for k in test_servers.keys():
            if k =='HTTP_SEVER':
                http_server_result=HTTP_GET_SITE('http://'+test_servers[k]+'/test.html',1)
            if k =='HTTPS_SERVER':
                http_server_result=HTTP_GET_SITE('https://'+test_servers[k]+'/test.html',1)
            #PRINT_DICT(http_server_result)
            if 'HTTP_GET_SITE_Exception' in http_server_result:
                print 'ERROR - Seems that your test server '+test_servers[k]+' is down!!!'
                print http_server_result['HTTP_GET_SITE_Exception']
                print 'Fix your test server to continue testing!!!'
                sys.exit(1)

    #Generate sites for testing, random delay and size in URLs
    if TEST in ['WGET_Traffic - Single HTTP get per TCP Connection','WGET Traffic - multiply HTTP gets per TCP Connection']:
        delays,sizes=range(0,5000,1),range(1,100,1)
        https_test_sites,http_test_sites=[],[]
        #if TEST=='WGET_Traffic - Single HTTP get per TCP Connection' or TEST=='WGET Traffic - multiply HTTP gets per TCP Connection':
        for x in range(0,number_of_test_sites):
            delay=str(random.choice(delays))
            size=str(random.choice(sizes))
            http_test_sites.append({'URL':'http://'+ESTIMATED_SERVER_TIME['HTTP_SERVER']+'/zababun.html?server_delay='+delay+'?body_size='+size,
                                    'ServerDelay':delay,
                                    'DataSize':size})
            https_test_sites.append({'URL':'https://'+ESTIMATED_SERVER_TIME['HTTPS_SERVER']+'/zababun.html?server_delay='+delay+'?body_size='+size,
                                    'ServerDelay':delay,
                                    'DataSize':size})


    # Per NV mode (proxy or direct), Per profile start test (sytart traffic stop)
    mode=CHOOSE_OPTION_FROM_LIST_1(NV_MODE,'Please choose your test setup mode: ')
    if mode=='AS_PROXY':
        IS_PROXY='true' #For start API
        NV_IP=TM_IP
    if mode=='LOCAL_NV':
        NV_IP='127.0.0.1'
        IS_PROXY='false'

    ### Shunra API get profiles ###
    # Simple GET profiles
    get_profiles=MC_APIS(ip=NV_IP,port=TM_PORT,user=TM_USER,password=TM_PASSWORD,https=TM_IS_HTTPS,method='GET',url_path='shunra/api/profile',
                         additional_headers={'Accept':'application/json'}, api_name='GET_PROFILES')
    get_profiles_response=get_profiles.RUN_REQUEST()
    PRINT_DICT(get_profiles_response)
    all_profiles=get_profiles_response['Content_As_Dict']['profiles']
    test_results['Get_Profiles']='PASS'

    ### Kill all running emulations on NV (FORCE STOP API)###
    kill_all=MC_APIS(ip=NV_IP,port=TM_PORT,user=TM_USER,password=TM_PASSWORD,https=TM_IS_HTTPS,method='PUT',url_path='shunra/api/emulation/resetall',
                         additional_headers={'Accept':'application/json'}, api_name='FORCE_STOP')
    kill_alls_response=kill_all.RUN_REQUEST()
    PRINT_DICT(kill_alls_response)

    for prof in all_profiles:
        if prof['name']=="Network disconnection":# and 'linux' in platform.system().lower():
            continue #Disconnect is not relevant for testing this feauture!!!

        # Start #
        profile_id=prof['id']
        network_scenario=prof['name']
        test_name=prof['name'].replace(' ','_')+'_'+str(time.time())
        device_id='zababun_device_id_123'
        flow_id='zababun_flow_id_123'
        if mode=='AS_PROXY':
            src_ip=GET_MY_PUBLIC_IP()
        if mode=='LOCAL_NV':
            src_ip=GET_PHYSICAL_INTERFACE_IP()


        pl_id='zababun_pl_id_123'
        test_description='Testing_Estimated_Server_Time'
        start_post_data={"deviceId": device_id,
                         "flows":[{"flowId": flow_id, "srcIp": src_ip, "profileId": profile_id, "isCaptureClientPL": True}],
                         "testMetadata": {"testName":test_name, "description": test_description, "networkScenario": network_scenario}}
        start_obj=MC_APIS(ip=NV_IP,port=TM_PORT,user=TM_USER,password=TM_PASSWORD,https=TM_IS_HTTPS,method='POST',url_path='shunra/api/emulation/custom',
                          additional_headers={'Accept':'application/json','Content-Type':'application/json'},params={'mode':'MULTI_USER','useProxy':IS_PROXY},request_payload=start_post_data, api_name='START_API')
        start_resp=start_obj.RUN_REQUEST()
        PRINT_DICT(start_resp)
        test_token=start_resp['Content_As_Dict']['testToken']


        # Send traffic to Test Server traffic
        sent_urls={}
        if mode=="AS_PROXY":
            WGET_PROXIES = {'http': 'http://' + TM_IP + ':' + str(DST_PORT), 'https': 'https://' + TM_IP + ':' + str(DST_PORT)}
            SELENIUM_PROXY=TM_IP+':'+str(DST_PORT)
            if TEST=='Real traffic to WEB site with Selenium':
                ynet_result=OPEN_WEB_SITE_SELENIUM(test_site,SELENIUM_PROXY,60)
            if TEST=='WGET_Traffic - Single HTTP get per TCP Connection':
                for site in http_test_sites:
                    wget_result=HTTP_GET_SITE(site['URL'],1,WGET_PROXIES)
                    wget_result['ServerDelay']=site['ServerDelay']
                    wget_result['DataSize']=site['DataSize']
                    sent_urls[site['URL']]=wget_result
                for site in https_test_sites:
                    wget_result=HTTP_GET_SITE(site['URL'],1,WGET_PROXIES)
                    wget_result['ServerDelay']=site['ServerDelay']
                    wget_result['DataSize']=site['DataSize']
                    sent_urls[site['URL']]=wget_result
            if TEST=='WGET Traffic - multiply HTTP gets per TCP Connection':
                # Server Side script has limitation as it doesn't support multiply connections
                # So NV proxy will hold connection Opened to Python HTTP Server and

                for site in http_test_sites:
                    wget_result=SEND_HTTP_GETS_ON_SAME_TCP_STREAM(site['URL'],number_of_gets_per_tcp,WGET_PROXIES)
                    for url in wget_result.keys():
                        sent_urls[url]=wget_result[url]
                        sent_urls[url]['ServerDelay']=site['ServerDelay']
                        sent_urls[url]['DataSize']=site['DataSize']
                for site in https_test_sites:
                    wget_result=SEND_HTTP_GETS_ON_SAME_TCP_STREAM(site['URL'],number_of_gets_per_tcp,WGET_PROXIES)
                    for url in wget_result.keys():
                        sent_urls[url]=wget_result[url]
                        sent_urls[url]['ServerDelay']=site['ServerDelay']
                        sent_urls[url]['DataSize']=site['DataSize']


        if mode=='LOCAL_NV':
            if TEST=='Real traffic to WEB site with Selenium':
                ynet_result=OPEN_WEB_SITE_SELENIUM(test_site,60)
            if TEST in ['WGET_Traffic - Single HTTP get per TCP Connection','WGET Traffic - multiply HTTP gets per TCP Connection']:
                if TEST=='WGET_Traffic - Single HTTP get per TCP Connection':
                    for site in http_test_sites:
                        wget_result=HTTP_GET_SITE(site['URL'],1)
                        wget_result['ServerDelay']=site['ServerDelay']
                        wget_result['DataSize']=site['DataSize']
                        sent_urls[site['URL']]=wget_result
                if TEST=='WGET Traffic - multiply HTTP gets per TCP Connection':
                    for site in http_test_sites:
                        wget_result=SEND_HTTP_GETS_ON_SAME_TCP_STREAM(site['URL'],number_of_gets_per_tcp)
                        for url in wget_result.keys():
                            sent_urls[url]=wget_result[url]
                            sent_urls[url]['ServerDelay']=site['ServerDelay']
                            sent_urls[url]['DataSize']=site['DataSize']


        # Stop API#
        time.sleep(5)
        stop_put_data='''{"testTokens": ["token"]}'''.replace('token',test_token)
        stop_obj=MC_APIS(ip=NV_IP,port=TM_PORT,user=TM_USER,password=TM_PASSWORD,https=TM_IS_HTTPS,method='PUT',url_path='shunra/api/emulation/stop',
                        additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload=stop_put_data, body_type='STRING', api_name='STOP_API')
        stop_resp=stop_obj.RUN_REQUEST()
        PRINT_DICT(stop_resp)

        # Analyze test#
        analyze_obj=MC_APIS(ip=NV_IP,port=TM_PORT,user=TM_USER,password=TM_PASSWORD,https=TM_IS_HTTPS,method='PUT',url_path='shunra/api/analysisreport/analyze/'+test_token+ports_parameters,
                        additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload={}, body_type='JSON', api_name='ANALYZE_API')
        analyze_resp=analyze_obj.RUN_REQUEST()
        #SPEC_PRINT([str(analyze_resp['Content_As_Dict'])])
        PRINT_DICT(analyze_resp)

        # Get JSON report and export all needed values for testing #
        # Needed values are:
        # 1) "usingProxy": false,
        # 2) "type": "ServerTime",
        # 3) "start": 1500970262267,
        # 4) "end": 1500970262275
        json_report_obj=MC_APIS(ip=NV_IP,port=TM_PORT,user=TM_USER,password=TM_PASSWORD,https=TM_IS_HTTPS,method='GET',url_path='shunra/api/analysisreport/'+test_token+'?zipResult=false',
                        additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload={}, body_type='JSON', api_name='GET_JSON_REPORT')
        json_report_resp=json_report_obj.RUN_REQUEST()
        SPEC_PRINT([str(json_report_resp['Content_As_Dict'])])
        PRINT_DICT(json_report_resp)
        json_report_content=json_report_resp['Content_As_Dict']
        json_report_content_as_dict=json_report_content['transactionReports'][0]
        if print_json=='True':
            print '-'*80
            print 'NV JSON Report'
            print json_report_resp['Content']
            print '-'*80
        exported_values={}

        for data in json_report_content_as_dict['reports']['waterfall']['subTransactions']:
            start='N/A'
            end='N/A'
            for typ in data['components']:
                if typ['type']=='ServerTime':
                    start=typ['start']
                    end=typ['end']
            try:
                delta_start_end=end-start
            except:
                delta_start_end='N/A'


            exported_values[data['attributes']['URI']]={'Start':start,'End':end,'UsingProxy':data['attributes']['usingProxy'],'CalculatedDelay':str(delta_start_end)}
            if TEST=='Real traffic to WEB site with Selenium':
                exported_values_as_list.append(
                    {
                        'URL':data['attributes']['URI'],
                        'Start':start,
                        'End':end,
                        'UsingProxy':data['attributes']['usingProxy'],
                        'CalculatedDelay':str(delta_start_end),
                        'WgetYnetResult':str(ynet_result),
                        'Profile_Name':prof['name']
                    })
            else:
                if end=='N/A' or start=='N/A':
                    exported_values_as_list.append(
                        {
                            'URL':data['attributes']['URI'],
                            'Start':start,
                            'End':end,
                            'UsingProxy':data['attributes']['usingProxy'],
                            'CalculatedDelay':'N/A',
                            'Profile_Name':prof['name']
                        })
                else:
                    exported_values_as_list.append(
                        {
                            'URL':data['attributes']['URI'],
                            'Start':start,
                            'End':end,
                            'UsingProxy':data['attributes']['usingProxy'],
                            'CalculatedDelay':str(end-start),
                            'Profile_Name':prof['name']
                        })

        # Compare between Traffic Result and Results exported from NV JSON Report
        result_file_name='Estimated_Server_Time_Result.csv'
        for k in sent_urls.keys():
            if k in exported_values.keys():
                if exported_values[k]['CalculatedDelay']!='N/A':
                    result_dic_list.append({'TestMode':mode,
                                            'TestName':test_name,
                                            'TestedURL':k,
                                            'UsingProxy':exported_values[k]['UsingProxy'],
                                            'ConfiguredServerDelay':sent_urls[k]['ServerDelay'],
                                            'CalculatedServerTimeDelay':exported_values[k]['CalculatedDelay'],
                                            'VarianceCalculation':abs(float(sent_urls[k]['ServerDelay'])-float(exported_values[k]['CalculatedDelay']))})
                else:
                    result_dic_list.append({'TestMode':mode,
                                            'TestName':test_name,
                                            'TestedURL':k,
                                            'UsingProxy':exported_values[k]['UsingProxy'],
                                            'ConfiguredServerDelay':sent_urls[k]['ServerDelay'],
                                            'CalculatedServerTimeDelay':exported_values[k]['CalculatedDelay'],
                                            'VarianceCalculation':'N/A'})


            else:
                print 'Warning - '+k+ ' was not found in NV Json Report!!!'
                result_dic_list.append({'TestMode':mode,
                                        'TestName':test_name,
                                        'TestedURL':k,
                                        'UsingProxy':'N/A',
                                        'ConfiguredServerDelay':sent_urls[k]['ServerDelay'],
                                        'CalculatedServerTimeDelay':'N/A',
                                        'VarianceCalculation':'N/A'})

        if ask_to_continue_after_each_profile=='True':
            ### For debug  to test single profile ###
            WRITE_DICTS_TO_CSV(result_file_name,result_dic_list)
            WRITE_DICTS_TO_CSV('AllExportedValuseFromJSON.csv',exported_values_as_list)
            CONTINUE('Continue to the next profile?')


    WRITE_DICTS_TO_CSV(result_file_name,result_dic_list)
    WRITE_DICTS_TO_CSV('AllExportedValuseFromJSON.csv',exported_values_as_list)

    return {'RunningEstimatedTimeTest':'Done'}

def GET_NV_ANALYTICS_CONFIGURATION_API_TEST():
    CLOSE_ALL_BROWSERS()
    CLEANER()
    completed_test_results={}

    # Get configuration as JSON
    test_name='GetDefaultPortsAsJSON'
    get_json_obj=MC_APIS(ip=TM_IP,port=TM_PORT,user=TM_USER,password=TM_PASSWORD,https=TM_IS_HTTPS,method='GET',url_path='shunra/api/configuration/analyticssettings',
                    additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload={}, body_type='JSON', api_name='Get_NV_Analytics_Configuration_As_JSON')
    get_json_obj_response=get_json_obj.RUN_REQUEST()
    PRINT_DICT(get_json_obj_response)
    print '\r\nMake sure that received JSON: '+get_json_obj_response['Content']+' contains default ports: 80 and 8080'
    completed_test_results[test_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Your test result:')


    # Get configuration as XML
    test_name='GetDefaultPortsAsXML'
    get_xml_obj=MC_APIS(ip=TM_IP,port=TM_PORT,user=TM_USER,password=TM_PASSWORD,https=TM_IS_HTTPS,method='GET',url_path='shunra/api/configuration/analyticssettings',
                    additional_headers={'Accept':'application/xml','Content-Type':'application/xml'},request_payload={}, body_type='JSON', api_name='Get_NV_Analytics_Configuration_As_XML')
    get_xml_obj_response=get_xml_obj.RUN_REQUEST()
    PRINT_DICT(get_xml_obj_response)
    print '\r\nMake sure that received XML: '+get_xml_obj_response['Content']+' contains default ports: 80 and 8080'
    completed_test_results[test_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Your test result:')

    # Set configuration as JSON
    test_name='SetDefaultPortsAsJSON'
    set_json_obj=MC_APIS(ip=TM_IP,port=TM_PORT,user=TM_USER,password=TM_PASSWORD,https=TM_IS_HTTPS,method='PUT',url_path='shunra/api/configuration/analyticssettings',
                    additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload={"analysisPorts":"80,8080,8181,8284,8285,65000"}, body_type='JSON', api_name='Set_NV_Analytics_Configuration_As_JSON')
    set_json_obj_response=set_json_obj.RUN_REQUEST()
    PRINT_DICT(set_json_obj_response)
    print '\r\nMake sure that received status code: '+str(set_json_obj_response['Status_Code'])+ ' is 204'
    completed_test_results[test_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Your test result:')


    # Set configuration as XML
    test_name='SetDefaultPortsAsXML'
    ports_as_xml='<AnalyticsSetting><analysisPorts>80,8080,8181,8284,8285,65000</analysisPorts></AnalyticsSetting>'
    set_xml_obj=MC_APIS(ip=TM_IP,port=TM_PORT,user=TM_USER,password=TM_PASSWORD,https=TM_IS_HTTPS,method='PUT',url_path='shunra/api/configuration/analyticssettings',
                    additional_headers={'Accept':'application/xml','Content-Type':'application/xml'},request_payload=ports_as_xml, body_type='STRING', api_name='Set_NV_Analytics_Configuration_As_XML')
    set_xml_obj_response=set_xml_obj.RUN_REQUEST()
    PRINT_DICT(set_xml_obj_response)
    print '\r\nMake sure that received status code: '+str(set_xml_obj_response['Status_Code'])+ ' is 204'
    completed_test_results[test_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Your test result:')


    # Manuel test #
    test_name='Manual_Configured_By_API_Ports_test'
    print 'Browse to you TM '+TM_IP+':'+TM_PORT+' and make sure that you see configured by API ports in:'
    print 'HTTP analysis to be conducted on port(s)'
    completed_test_results[test_name]=CHOOSE_OPTION_FROM_LIST_1(['PASS','FAIL','N/A'],'Your test result:')



    PRINT_DICT(completed_test_results)


    return {'GET_NV_ANALYTICS_CONFIGURATION_API_TEST':'Done'}

def START_TRANSACTION_API_REUSE_CHANGES_FOR_MC(test_name):
    SPEC_PRINT(['This test is developed for','NV in proxy mode only', 'Make sure your NV is configured to Proxy mode!!!'])
    CLOSE_ALL_BROWSERS()
    CLEANER()
    completed_test_results={}
    ports_parameters='?ports=8888,65000,80,443,8080,8090'


    ### Transactions with all possible options ###
    options=[{'reuseExistingByName':'false'},{'reuseExistingByName':'true'}]



    for opt in options:
        ### Kill all running emulations on NV (FORCE STOP API)###
        kill_all=MC_APIS(ip=TM_IP,port=TM_PORT,user=TM_USER,password=TM_PASSWORD,https=TM_IS_HTTPS,method='PUT',url_path='shunra/api/emulation/resetall',
                             additional_headers={'Accept':'application/json'}, api_name='FORCE_STOP')
        kill_alls_response=kill_all.RUN_REQUEST()
        PRINT_DICT(kill_alls_response)

        ### Shunra API get profiles ###
        # Simple GET profiles
        get_profiles=MC_APIS(ip=TM_IP,port=TM_PORT,user=TM_USER,password=TM_PASSWORD,https=TM_IS_HTTPS,method='GET',url_path='shunra/api/profile',
                             additional_headers={'Accept':'application/json'}, api_name='GET_PROFILES')
        get_profiles_response=get_profiles.RUN_REQUEST()
        PRINT_DICT(get_profiles_response)
        all_profiles=get_profiles_response['Content_As_Dict']['profiles']
        random_profile=random.choice(all_profiles)
        all_profiles.remove(random_profile)

        ### Start emulation API ###
        profile_id=random_profile['id']
        network_scenario=random_profile['name']
        test_name=test_name+'_'+str(time.time())
        device_id='zababun_device_id_123'
        flow_id='zababun_flow_id_123'
        src_ip=GET_MY_PUBLIC_IP()
        pl_id='zababun_pl_id_123'
        test_description='zababun_test_description'
        start_post_data={"deviceId": device_id,
                         "flows":[{"flowId": flow_id, "srcIp": src_ip, "profileId": profile_id, "isCaptureClientPL": True}],
                         "testMetadata": {"testName":test_name, "description": test_description, "networkScenario": network_scenario}}
        start_obj=MC_APIS(ip=TM_IP,port=TM_PORT,user=TM_USER,password=TM_PASSWORD,https=TM_IS_HTTPS,method='POST',url_path='shunra/api/emulation/custom',
                          additional_headers={'Accept':'application/json','Content-Type':'application/json'},params={'mode':'MULTI_USER','useProxy':'true'},request_payload=start_post_data, api_name='START_API')
        start_resp=start_obj.RUN_REQUEST()
        PRINT_DICT(start_resp)
        test_token=start_resp['Content_As_Dict']['testToken']

        ### Connect API before start transaction ###
        connect_obj=MC_APIS(ip=TM_IP,port=TM_PORT,user=TM_USER,password=TM_PASSWORD,https=TM_IS_HTTPS,method='POST',url_path='shunra/api/transactionmanager/'+test_token,
                    additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload={"overwriteExistingConnection":"true"}, body_type='JSON',api_name='CONNECT_FOR_TRANSACTIONS')
        connect_resp=connect_obj.RUN_REQUEST()
        transactionManagerSessionIdentifier=connect_resp['Content_As_Dict']['transactionManagerSessionIdentifier']
        PRINT_DICT(connect_resp)

        for x in range(1,4):
            if opt['reuseExistingByName']=='false':
                # Transaction Start #
                start_transaction_data={"transactionName":"Trans_Reuse_By_Name_Is_False", "transactionDescription":"Trans_Reuse_By_Name_Is_False"}
                start_trans_obj=MC_APIS(ip=TM_IP,port=TM_PORT,user=TM_USER,password=TM_PASSWORD,https=TM_IS_HTTPS,method='POST',
                                        url_path='shunra/api/transactionmanager/transaction/'+transactionManagerSessionIdentifier,
                                        additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload=start_transaction_data, body_type='JSON', api_name='START_TRANSACTION')
                start_trans_resp=start_trans_obj.RUN_REQUEST()
                PRINT_DICT(start_trans_resp)
                transactionIdentifier=start_trans_resp['Content_As_Dict']['transactionIdentifier']

            if opt['reuseExistingByName']=='true':
                # Transaction Start #
                start_transaction_data={"transactionName":"Trans_Reuse_By_Name_Is_True", "transactionDescription":"Trans_Reuse_By_Name_Is_True"}
                start_trans_obj=MC_APIS(ip=TM_IP,port=TM_PORT,user=TM_USER,password=TM_PASSWORD,https=TM_IS_HTTPS,method='POST',
                                        url_path='shunra/api/transactionmanager/transaction/'+transactionManagerSessionIdentifier+'?reuseExistingByName=true',
                                        additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload=start_transaction_data, body_type='JSON', api_name='START_TRANSACTION')
                start_trans_resp=start_trans_obj.RUN_REQUEST()
                PRINT_DICT(start_trans_resp)
                transactionIdentifier=start_trans_resp['Content_As_Dict']['transactionIdentifier']

            # # Testing that XML works the same as JSON #
            # if opt['reuseExistingByName']=='true':
            #     # Transaction Start #
            #     start_transaction_data={"transactionName":"Trans_Reuse_By_Name_Is_True", "transactionDescription":"Trans_Reuse_By_Name_Is_True"}
            #     start_transaction_data='<startTransactionRequest><transactionName>Trans_Reuse_By_Name_Is_True</transactionName><transactionDescription>Trans_Reuse_By_Name_Is_True</transactionDescription></startTransactionRequest>'
            #     start_trans_obj=MC_APIS(ip=TM_IP,port=TM_PORT,user=TM_USER,password=TM_PASSWORD,https=TM_IS_HTTPS,method='POST',
            #                             url_path='shunra/api/transactionmanager/transaction/'+transactionManagerSessionIdentifier+'?reuseExistingByName=true',
            #                             additional_headers={'Accept':'application/xml','Content-Type':'application/xml'},request_payload=start_transaction_data, body_type='STRING', api_name='START_TRANSACTION')
            #     start_trans_resp=start_trans_obj.RUN_REQUEST()
            #     PRINT_DICT(start_trans_resp)
            #     print start_trans_resp['Content']
            #     transactionIdentifier=start_trans_resp['Content'].split('transactionIdentifier')[0].replace('<','').replace('>','')
            #     print transactionIdentifier

            # Traffic #
            print HTTP_GET_SITE('http://cnn.com',3,WGET_PROXIES)
            print HTTP_GET_SITE('https://facebook.com',3,WGET_PROXIES)

            # Stop Transaction #
            #https://dev.hpenv.com/shunra/api/transactionmanager/transaction/{token}/{token}
            stop_trans_obj=MC_APIS(ip=TM_IP,port=TM_PORT,user=TM_USER,password=TM_PASSWORD,https=TM_IS_HTTPS,method='PUT',url_path='shunra/api/transactionmanager/transaction/'+transactionManagerSessionIdentifier+'/'+transactionIdentifier,
                            additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload={}, body_type='JSON', api_name='STOP_TRANSACTION')
            stop_trans_resp=stop_trans_obj.RUN_REQUEST()
            PRINT_DICT(stop_trans_resp)

            # Real time update #
            random_profile=random.choice(all_profiles)
            all_profiles.remove(random_profile)
            profile_id=random_profile['id']
            network_scenario=random_profile['name']
            real_time_update_post_data={ "testMetadata": { "networkScenario": network_scenario}, "flows": [{ "profileId": profile_id, "isDefaultFlow": "true", "flowId":flow_id}]}
            real_time_update_obj=MC_APIS(ip=TM_IP,port=TM_PORT,user=TM_USER,password=TM_PASSWORD,https=TM_IS_HTTPS,method='PUT',url_path='shunra/api/emulation/custom/'+test_token,
                              additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload=real_time_update_post_data,api_name='REAL_TIME_UPDATE')
            real_time_update_resp=real_time_update_obj.RUN_REQUEST()
            PRINT_DICT(real_time_update_resp)

        # Stop emulation API #
        stop_put_data='''{"testTokens": ["token"]}'''.replace('token',test_token)
        stop_obj=MC_APIS(ip=TM_IP,port=TM_PORT,user=TM_USER,password=TM_PASSWORD,https=TM_IS_HTTPS,method='PUT',url_path='shunra/api/emulation/stop',
                        additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload=stop_put_data, body_type='STRING', api_name='STOP_API')
        stop_resp=stop_obj.RUN_REQUEST()
        PRINT_DICT(stop_resp)


        # Analyze test#
        analyze_obj=MC_APIS(ip=TM_IP,port=TM_PORT,user=TM_USER,password=TM_PASSWORD,https=TM_IS_HTTPS,method='PUT',url_path='shunra/api/analysisreport/analyze/'+test_token+ports_parameters,
                        additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload={}, body_type='JSON', api_name='ANALYZE_API')
        analyze_resp=analyze_obj.RUN_REQUEST()
        #SPEC_PRINT([str(analyze_resp['Content_As_Dict'])])
        PRINT_DICT(analyze_resp)

    SPEC_PRINT(['Download NV Report for 2 scenarios:'
                '1 - reuseExistingByName=false',
                '2 - reuseExistingByName=true',
                'Make sure that you see the diference',
                'No N/A in report (where baseline) when reuseExistingByName=true'])

    PRINT_DICT(completed_test_results)
    return {'GET_NV_ANALYTICS_CONFIGURATION_API_CHANGES_FOR_MC':'Done'}
