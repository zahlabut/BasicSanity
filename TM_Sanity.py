#!/usr/bin/python
import sys
from APIs import *
from TrafficTypes import *
from datetime import datetime
from HP_Functions import *
from Mi_Functions import *


### Runtime Log ###
RunTimeLog='Runtime.log'
DELETE_LOG_CONTENT(RunTimeLog)
sys.stdout=MyOutput(RunTimeLog)
sys.stderr=MyOutput(RunTimeLog)
PROXY_MODE=False

### API CSV Result File ###
DELETE_LOG_CONTENT(api_log_file)
ADD_LIST_AS_LINE_TO_CSV_FILE(api_log_file,['Request_Type','URL','Payload','Response_Headers','Response_Status','Reason','Response_Content','API_Execution_time'])




params=[line.strip() for line in open('Params.py','r').readlines() if line.startswith('#')==False]
SPEC_PRINT(['---- BasicSanityTool V 1.0 --------','Designed to test TM/OptMyAPP by: Arkady Shtempler','','Script parameters:']+params+['*** Goodbye World !!! ***'])

#loop_number=raw_input('Please enter loop number: ')
loop_number=TEST_LOOP_NUMBER
for x in range(0,int(loop_number)):
    print '------------------ Loop Number:'+str(x+1)+' ------------------------------------------'

    test_time=string=time.strftime("%Y_%m_%d_%H_%M_%S")
    files_to_save=[]


    ### Runtime Log ###
    RunTimeLog='Runtime.log'
    DELETE_LOG_CONTENT(RunTimeLog)
    sys.stdout=MyOutput(RunTimeLog)
    sys.stderr=MyOutput(RunTimeLog)

    ### Test Log (not csv) ###
    TestLogFile= 'TestResult_'+test_time+'.log'
    DELETE_LOG_CONTENT(TestLogFile)
    files_to_save.append(TestLogFile)

    ### Result Directory ###
    TestDirName='Test_Results_'+test_time
    os.mkdir(TestDirName)

    test_all_results=[]


    ###### Test case: Start NV test using pre defined traffic DST port  + start HTTP traffic using pre definedDST port + stop emulation + analyze results ######
    if HTTP_GETS_USING_PRE_DEFINED_DST_PORT['ENABLED']==True:
        SPEC_PRINT(['Required actions for this test are:',
                    '1) 2 AWS servers: Client','\r\n(BasicSanity script) and Server (MITMPROXY and NV)'
                    '2) On Server side - NV is UP and Running',
                    '3) On Server side -MITMPROXY','\r\nis installed and all Proxies port are listening',
                    '4) NV is configured to use all Proxies ports','\r\nfor its analytics (add all to HTTP ports in settings)'
                    '5) In order to start proxy on background use:','\r\n"mitmdump -p <PORT> --no-upstream-cert &"',
                    '6) Add all proxy ports to AWS security group,','\r\ndo not forget to reboot AWS server after changes in security group!!!',
                    '7) User server AWS ip from ifconfig output as TM_IP in Params.py'])
        test_name='Test_HTTP_PreDefined_DST_Port_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        test_result=RUN_TM_SCENARIO_TEST_USING_DST_PORT(START_DEFAULT_TEST, TM_IP, TM_PORT, TM_USER, TM_PASSWORD, 'My_Flow', '20', '0.1', '2048.0', '2048.0', test_name, 'Stam', DST_PORT,
                                                        HTTP_GET_SITE, HTTP_GETS_USING_PRE_DEFINED_DST_PORT['URL'], HTTP_GETS_USING_PRE_DEFINED_DST_PORT['LOOP_NUMBER'], HTTP_GETS_USING_PRE_DEFINED_DST_PORT['PROXY'], None, 1)
        INSERT_TO_LOG(TestLogFile,str(test_result))
        test_all_results.append(test_result)
        if 'linux' in platform.system().lower():
            files_to_save.append(test_name+'.cap')




    ###### Test case: Start NV test using pre defined traffic DST port  + start HTTP traffic (selenium based) using pre definedDST port + stop emulation + analyze results ######
    if HTTP_SELENIUM_USING_PRE_DEFINED_DST_PORT['ENABLED']==True:
        SPEC_PRINT(['Required actions for this test are:',
                    '1) 2 AWS servers: Client','\r\n(BasicSanity script) and Server (MITMPROXY and NV)'
                    '2) On Server side - NV is UP and Running',
                    '3) On Server side -MITMPROXY','\r\nis installed and all Proxies port are listening',
                    '4) NV is configured to use all Proxies ports','\r\nfor its analytics (add all to HTTP ports in settings)'
                    '5) In order to start proxy on background use:','\r\n"nohup mitmdump -p <PORT> --no-upstream-cert &"',
                    '6) Add all proxy ports to AWS security group,','\r\ndo not forget to reboot AWS server after changes in security group!!!',
                    '7) User server AWS ip from ifconfig output as TM_IP in Params.py'])
        for x in range(HTTP_SELENIUM_USING_PRE_DEFINED_DST_PORT['TEST_LOOP_NUMBER']):
            test_name='Test_HTTP_PreDefined_DST_Port_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            test_result=RUN_TM_SCENARIO_TEST_USING_DST_PORT(START_DEFAULT_TEST, TM_IP, TM_PORT, TM_USER, TM_PASSWORD, 'My_Flow', '20', '0.1', '2048.0', '2048.0', test_name, 'Stam', DST_PORT,
                                                            HTTP_SELENIUM_USING_PRE_DEFINED_DST_PORT['USE_TRANSACTIONS'],
                                                            OPEN_WEB_SITE_SELENIUM, HTTP_SELENIUM_USING_PRE_DEFINED_DST_PORT['URL'], HTTP_SELENIUM_USING_PRE_DEFINED_DST_PORT['PROXY'])
            INSERT_TO_LOG(TestLogFile,str(test_result))
            test_all_results.append(test_result)
            if 'linux' in platform.system().lower():
                files_to_save.append(test_name+'.cap')


    if HLS_TEST_SETTINGS['ENABLED']==True:
        test_name='Test_HLS_' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        test_result=TM_RUN_DEFAULT_SCENARIO_TEST(START_DEFAULT_TEST, TM_IP, TM_PORT, TM_USER, TM_PASSWORD, 'My_Flow', '20', '0.1', '2048.0', '2048.0', test_name, 'Stam',False,HLS_VLC)
        print test_result
        INSERT_TO_LOG(TestLogFile,str(test_result))
        test_all_results.append(test_result)
        if 'linux' in platform.system().lower():
            files_to_save.append(test_name+'.cap')




    ###### Test case: Start default test + start HTTP traffic + stop emulation + analyze results ######
    if HTTP_TEST_SETTINGS['ENABLED']==True:
        proxy_mode=False
        if HTTP_TEST_SETTINGS['PROXY']!=None:
            proxy_mode=True
        test_name='Test_HTTP_' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        test_result=TM_RUN_DEFAULT_SCENARIO_TEST(START_DEFAULT_TEST, TM_IP, TM_PORT, TM_USER, TM_PASSWORD, 'My_Flow', '20', '0.1', '2048.0', '2048.0', test_name, 'Stam',proxy_mode,
                                                 HTTP_GET_SITE,HTTP_TEST_SETTINGS['URL'], HTTP_TEST_SETTINGS['LOOP_NUMBER'], HTTP_TEST_SETTINGS['PROXY'], None, 1)
        INSERT_TO_LOG(TestLogFile,str(test_result))
        test_all_results.append(test_result)
        if 'linux' in platform.system().lower():
            files_to_save.append(test_name+'.cap')

    ###### Test case: Start default test + start HTTP traffic + stop emulation + analyze results ######
    if HTTP_TEST_SELENIUM_SETTINGS['ENABLED']==True:
        proxy_mode=False
        if HTTP_TEST_SELENIUM_SETTINGS['PROXY']!=None:
            proxy_mode=True

        if 'linux' in platform.system().lower():
            display = Display(visible=0, size=(800, 600))
            print 'Start display result: ', display.start()

        ###This is browse without NV, saving cap file
        no_nv_browse_result=BROWSE_AND_SNIFF_SELENIUM(HTTP_TEST_SELENIUM_SETTINGS['URL'])
        print no_nv_browse_result
        files_to_save.append(no_nv_browse_result['CapName'])
        files_to_save.append(no_nv_browse_result['ScreenshootName'])


        test_name='Test_HTTP_Selenium_' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

        test_result=TM_RUN_DEFAULT_SCENARIO_TEST(START_DEFAULT_TEST, TM_IP, TM_PORT, TM_USER, TM_PASSWORD, 'My_Flow', '1', '0', '2048.0', '2048.0', test_name, 'Stam',proxy_mode,
                                                 OPEN_WEB_SITE_SELENIUM,HTTP_TEST_SELENIUM_SETTINGS['URL'],HTTP_TEST_SELENIUM_SETTINGS['PROXY'])
        files_to_save.append(test_result['ScreenshootName'])
        INSERT_TO_LOG(TestLogFile,str(test_result))
        test_all_results.append(test_result)
        if 'linux' in platform.system().lower():
            files_to_save.append(test_name+'.cap')
            print 'Stop Display on Linux'
            print 'Stop display result: ',display.stop()




    ###### Test case: Start default test + start HTTP traffic + stop emulation + analyze results ######
    if HTTP_TEST_ALEXA_SITES_SELENIUM_SETTINGS['ENABLED']==True:
        proxy_mode=False
        if HTTP_TEST_ALEXA_SITES_SELENIUM_SETTINGS['PROXY']!=None:
            proxy_mode=True
        if 'linux' in platform.system().lower():
            display = Display(visible=0, size=(800, 600))
            print 'Start display result: ', display.start()

        sites=open('AlexaTopMilion.csv','r').readlines()
        sites= ['http://'+url.split(',')[-1].strip() for url in sites][0:HTTP_TEST_ALEXA_SITES_SELENIUM_SETTINGS['Number_Of_Sites']]




        # for site in sites:
        #     print site
        #     print OPEN_WEB_SITE_SELENIUM(site)
        for site in sites:
            SPEC_PRINT([str(sites.index(site)+1)+' --> '+site])
            test_name='Test_'+site.split('://')[-1]+'_'+datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            print test_name
            test_result=TM_RUN_DEFAULT_SCENARIO_TEST(START_DEFAULT_TEST, TM_IP, TM_PORT, TM_USER, TM_PASSWORD, 'My_Flow', '1', '0', '2048.0', '2048.0', test_name, 'Stam',proxy_mode,
                                                     OPEN_WEB_SITE_SELENIUM, site, HTTP_TEST_ALEXA_SITES_SELENIUM_SETTINGS['PROXY'])
            files_to_save.append(test_result['ScreenshootName'])
            INSERT_TO_LOG(TestLogFile,str(test_result))
            test_all_results.append(test_result)

        if 'linux' in platform.system().lower():
            files_to_save.append(test_name+'.cap')
            print 'Stop Display on Linux'
            print 'Stop display result: ',display.stop()






    ###### Test cases for: "Get Online Analysis Report - REST API"######
    if ONLINE_ANALYSIS_TESTING['ENABLED']==True:
        test_name='Online_Analysis_Testing_' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        test_result=ONLINE_ANALYTICS_TESTING_BASIC_APIS(START_DEFAULT_TEST, TM_IP, TM_PORT, TM_USER, TM_PASSWORD, 'My_Flow', '20', '0.1', '2048.0', '2048.0', test_name, 'Stam')
        INSERT_TO_LOG(TestLogFile,str(test_result))
        test_all_results.append(test_result)


    ###### Test cases for: "SUMMARIESI TAB" in NV Report, data validation test cases ######
    if NV_REPORT_SUMMARIES_TAB['ENABLED']==True:
        test_name='SUMMARIES_TAB_' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        test_result=SUMMARIES_TEST_CASES(START_DEFAULT_TEST, TM_IP, TM_PORT, TM_USER, TM_PASSWORD, 'My_Flow', '20', '0.1', '2048.0', '2048.0', test_name, 'Stam')
        INSERT_TO_LOG(TestLogFile,str(test_result))
        test_all_results.append(test_result)

    ###### Test cases for: "HTTP_WATERFALL TAB" in NV Report, data validation test cases ######
    if NV_REPORT_HTTP_WATERFALL_TAB['ENABLED']==True:
        test_name='HTTP_WATERFALL_TAB_' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        NV_PROXY_MODE=NV_REPORT_HTTP_WATERFALL_TAB['NV_IN_PROXY_MODE']
        test_result=HTTP_WATERFALL_TEST_CASES(START_DEFAULT_TEST, TM_IP, TM_PORT, TM_USER, TM_PASSWORD, NV_PROXY_MODE,'My_Flow', '20', '0.1', '2048.0', '2048.0', test_name, 'Stam')
        INSERT_TO_LOG(TestLogFile,str(test_result))
        test_all_results.append(test_result)


    ###### Test cases for: "GET_HAR_API" ######
    if GET_HAR_API_TESTING['ENABLED']==True:
        NV_PROXY_MODE='yes'
        test_name='HAR_API_' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        test_result=GET_HAR_API_TESTING_FUNC(START_DEFAULT_TEST, TM_IP, TM_PORT, TM_USER, TM_PASSWORD, NV_PROXY_MODE,'My_Flow', '20', '0.1', '2048.0', '2048.0', test_name, 'Stam')
        INSERT_TO_LOG(TestLogFile,str(test_result))
        test_all_results.append(test_result)




    ###### Test cases for: "GET_HAR_API" ######
    if MC_INTEGRATION_APIS['ENABLED']==True:
        test_name='MC_APIs_' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        test_result=RUN_MC_APIS_SCENARIOS(MC_INTEGRATION_APIS['API_SERVER_DOMAIN'], MC_INTEGRATION_APIS['API_SERVER_PORT'], MC_INTEGRATION_APIS['IS_HTTPS_SETUP'],  MC_INTEGRATION_APIS['AUTH_USER'], MC_INTEGRATION_APIS['AUTH_PASS'])
        INSERT_TO_LOG(TestLogFile,str(test_result))
        test_all_results.append(test_result)



    ###### Test cases for: "Estimated server time" ######
    if ESTIMATED_SERVER_TIME['ENABLED']==True:
        test_name='Estimated_Server_Time_' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        test_result=RUN_ESTIMATED_SERVER_TIME_TEST()
        INSERT_TO_LOG(TestLogFile,str(test_result))
        test_all_results.append(test_result)

    ###### Test cases for: "Estimated server time" ######
    if GET_NV_ANALYTICS_CONFIGURATION_API['ENABLED']==True:
        test_name='Get_NV_Analytics_Configuration_API_' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        test_result=GET_NV_ANALYTICS_CONFIGURATION_API_TEST(GET_NV_ANALYTICS_CONFIGURATION_API['TEST_SERVER_URL'])
        INSERT_TO_LOG(TestLogFile,str(test_result))
        test_all_results.append(test_result)









    ##### Test case: Start default test + start PING traffic + stop emulation #+ analyze result #####
    test_name='Test_PING_' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    proxy_mode=False
    if PING_TEST_SETTINGS['ENABLED']==True:
        test_result=TM_RUN_DEFAULT_SCENARIO_TEST(START_DEFAULT_TEST, TM_IP, TM_PORT, TM_USER, TM_PASSWORD, 'My_Flow', '0', '0.1', '2048.0', '2048.0',test_name, 'Stam',proxy_mode,
                                     PING_HOST,PING_TEST_SETTINGS['DST_IP'],PING_TEST_SETTINGS['LOOP_NUMBER'])
        INSERT_TO_LOG(TestLogFile,str(test_result))
        test_all_results.append(test_result)
        if 'linux' in platform.system().lower():
            files_to_save.append(test_name+'.cap')

    ###### Test case: Start default test + start DNS queries traffic + stop emulation #+ analyze result #####
    if DNS_TEST_SETTINGS['ENABLED']==True:
        proxy_mode=False
        test_name='Test_DNS_' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        test_result=TM_RUN_DEFAULT_SCENARIO_TEST(START_DEFAULT_TEST, TM_IP, TM_PORT, TM_USER, TM_PASSWORD, 'My_Flow', '20', '0.1', '2048.0', '2048.0',test_name, 'Stam',proxy_mode,
                                     DNS_QUERY,DNS_TEST_SETTINGS['DOMAIN'],DNS_TEST_SETTINGS['LOOP_NUMBER'])
        INSERT_TO_LOG(TestLogFile,str(test_result))
        test_all_results.append(test_result)
        if 'linux' in platform.system().lower():
            files_to_save.append(test_name+'.cap')

    ###### Test case: Start default test + start HTTP traffic (TCP - GET based soccket) + stop emulation + analyze results ######
    if TCP_TEST_SETTINGS['ENABLED']==True:
        proxy_mode=False
        test_name='Test_TCP_' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        test_result=TM_RUN_DEFAULT_SCENARIO_TEST(START_DEFAULT_TEST, TM_IP, TM_PORT, TM_USER, TM_PASSWORD, 'My_Flow', '20', '0.1', '2048.0', '2048.0',test_name, 'Stam',proxy_mode,
                                     HTTP_GET_SOCKET,TCP_TEST_SETTINGS['URL'], TCP_TEST_SETTINGS['DST_PORT'], TCP_TEST_SETTINGS['LOOP_NUMBER'])
        INSERT_TO_LOG(TestLogFile,str(test_result))
        test_all_results.append(test_result)
        if 'linux' in platform.system().lower():
            files_to_save.append(test_name+'.cap')
    #
    # ###### Test case: Start default test + start SSH traffic (UDP - based soccket) + stop emulation + analyze results ######
    # ##RUN_DEFAULT_SCENARIO_TEST(START_DEFAULT_TEST,TM_IP,TM_PORT,TM_USER, TM_PASSWORD,'My_Flow', '20', '0.1', '2048.0', '2048.0','Test_UDP_' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S'), 'Stam',
    # ##                          SSH_QUERY_SOCKET,'16.59.58.70',22,'zababun'*100,10)
    # #print SSH_QUERY_SOCKET('16.59.58.70',22,'zababun'*100,10)


    ### Collect and printtest Results ###
    print '#'*100

    print 'Test_Results:'
    print open(TestLogFile,'r').read()
    for item in test_all_results:
        print item
    TestCsvResultFile=TestLogFile.replace('.log','.csv')
    WRITE_DICTS_TO_CSV(TestCsvResultFile,test_all_results)
    files_to_save.append(TestCsvResultFile)
    files_to_save.append(RunTimeLog)
    for fil in files_to_save:
        if os.path.isfile(fil):
            try:
                shutil.move(os.path.abspath(fil),os.path.abspath(TestDirName))
            except Exception,e:
                print str(e)



    # #### Remarked are using Accept-Encoding:zababun ###
    # ###### Test case: Start default test + start HTTP traffic (TCP - GET based soccket) + stop emulation + analyze results ######
    # test_name='Test_TCP_' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    # test_result=TM_RUN_DEFAULT_SCENARIO_TEST(START_DEFAULT_TEST, tm_ip, tm_port, tm_user, tm_password, 'My_Flow', '20', '0.1', '2048.0', '2048.0',test_name, 'Stam',
    #                              HTTP_GET_SITE,'http://www.cnn.com',10,None,{'Accept-Encoding':'Zababun'})
    # INSERT_TO_LOG(TestLogFile,str(test_result))
    # test_all_results.append(test_result)
    # if 'linux' in platform.system().lower():
    #     files_to_save.append(test_name+'.cap')
    #
    #
    # test_name='Test_TCP_' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    # test_result=TM_RUN_DEFAULT_SCENARIO_TEST(START_DEFAULT_TEST, tm_ip, tm_port, tm_user, tm_password, 'My_Flow', '20', '0.1', '2048.0', '2048.0',test_name, 'Stam',
    #                              HTTP_GET_SITE,'http://ynet.co.il',10,None,{'Accept-Encoding':'gzip'})
    # INSERT_TO_LOG(TestLogFile,str(test_result))
    # test_all_results.append(test_result)
    # if 'linux' in platform.system().lower():
    #     files_to_save.append(test_name+'.cap')
    #
    #
    #
    #
    # test_name='Test_TCP_' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    # test_result=TM_RUN_DEFAULT_SCENARIO_TEST(START_DEFAULT_TEST, tm_ip, tm_port, tm_user, tm_password, 'My_Flow', '20', '0.1', '2048.0', '2048.0',test_name, 'Stam',
    #                              HTTP_GET_SITE,'http://ynet.co.il',10,None,{'Accept-Encoding':'Deflate'})
    # INSERT_TO_LOG(TestLogFile,str(test_result))
    # test_all_results.append(test_result)
    # if 'linux' in platform.system().lower():
    #     files_to_save.append(test_name+'.cap')
    #
    #
    #
    #
    # test_name='Test_TCP_' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    # test_result=TM_RUN_DEFAULT_SCENARIO_TEST(START_DEFAULT_TEST, tm_ip, tm_port, tm_user, tm_password, 'My_Flow', '20', '0.1', '2048.0', '2048.0',test_name, 'Stam',
    #                              HTTP_GET_SITE,'http://ynet.co.il',10,None,{'Accept-Encoding':''})
    # INSERT_TO_LOG(TestLogFile,str(test_result))
    # test_all_results.append(test_result)
    # if 'linux' in platform.system().lower():
    #     files_to_save.append(test_name+'.cap')






if exceptions_file in os.listdir('.'):
    exceptions=[eval(item.strip()) for item in open(exceptions_file,'r').readlines()]
    WRITE_DICTS_TO_CSV('Exceptions.csv',exceptions)






