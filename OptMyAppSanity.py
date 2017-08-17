#!/usr/bin/python
import sys,shutil,os
from Mi_Functions import *
### Command Line Mode

### Runtime Log ###
RunTimeLog='Runtime.log'
DELETE_LOG_CONTENT(RunTimeLog)
sys.stdout=MyOutput(RunTimeLog)
sys.stderr=MyOutput(RunTimeLog)

CMD_MODE=False
if len(sys.argv)>1:
    CMD_MODE=True
    sites=[sys.argv[1]]
    mode=sys.argv[2]
    if mode=='replay':
        shutil.copy2(os.path.join('ParamFiles','CMD_Replay.py'), 'Params.py')
    if mode=='advanced':
        shutil.copy2(os.path.join('ParamFiles','CMD_Advanced.py'), 'Params.py')
if 'CMD_MODE' not in open('Params.py','r').read():
    INSERT_TO_LOG('Params.py','CMD_MODE='+str(CMD_MODE))

### Bring the OriginalParams.py if no Params.py exists
if 'Params.py' not in os.listdir('.'):
    print 'ParamsOriginal.py will be used!!!'
    shutil.copy2(os.path.join('ParamFiles','ParamsOriginal.py'), 'Params.py')


from HP_Functions import *
#import Cleaner

#sys.path.append(os.path.abspath('ParamFiles'))



########################################################### OPT_My_App ###############################################################
### All test results file ###
total_result_file_name='All_Tests_Results.csv'
DELETE_LOG_CONTENT(total_result_file_name)
DELETE_LOG_CONTENT(api_log_file)
all_api_result_file='ALL_'+api_log_file
DELETE_LOG_CONTENT(all_api_result_file)
ADD_LIST_AS_LINE_TO_CSV_FILE(api_log_file,['TimeStamp','RequestType','RequestData','ErrorCode','ResponseData','ExecutionTime'])

### All test results file ###
if USE_TRANSACTIONS==True:
    total_transactions_result_file_name='All_Transactions.csv'
    DELETE_LOG_CONTENT(total_transactions_result_file_name)

### Empty eceptions file ###
DELETE_LOG_CONTENT(exceptions_file)

#------------------------------ HTTP WGET TRAFFIC -----------------------------------#
params=[line.strip() for line in open('Params.py','r').readlines() if line.startswith('#')==False]
SPEC_PRINT(['---- BasicSanityTool V 1.0 --------','Designed to test TM/OptMyAPP by: Arkady Shtempler','','Script parameters:']+params+['*** Goodbye World !!! ***'])

if USE_SELENIUM==False:
    all_tests_results_list=[]
    for x in range(0, WGET_MODE_LOOPS):
        print '\r\n'
        print '------------------------------------------ Loop Number:'+str(x+1)+' --------------------------------------------------------'
        test_time=time.strftime("%Y_%m_%d_%H_%M_%S")
        files_to_save=[]

        ### Test Log (not csv) ###
        TestLogFile= 'TestResult_'+test_time+'.log'
        DELETE_LOG_CONTENT(TestLogFile)
        files_to_save.append(TestLogFile)

        ### Result Directory ###
        if USE_TRANSACTIONS==False:
            TestDirName='Test_Results_Replay_'+test_time
        if USE_TRANSACTIONS==True:
            TestDirName='Test_Results_Advanced_'+test_time
        os.mkdir(TestDirName)

        ### URL ###
        opt_my_app_url='https://' + OPT_MY_APP_DOMAIN + '/hp/nvcloud?hf=myLittlePony'
        test_all_results=[]

        test_cases=[]

        if USE_TRANSACTIONS==False:
            if REPLAY_MODE['Enabled']==True:
                test_cases.append({'networkProfile':'baseline',
                                   'test_name':'Replay_Mode_',
                                   'runReplay':True,
                                   'report_name':'ReplayReport.html',
                                   'TESTED_URL':REPLAY_MODE['URL'],
                                   'LoopNumber':REPLAY_MODE['LoopNumber']})

            if ADVANCED_MODE_BASELINE['Enabled']==True:
                test_cases.append({'networkProfile':'baseline',
                                   'test_name':'Advanced_Mode_Baseline_',
                                   'runReplay':False,
                                   'report_name':'AnalyticsReport.html',
                                   'TESTED_URL':ADVANCED_MODE_BASELINE['URL'],
                                   'LoopNumber':ADVANCED_MODE_BASELINE['LoopNumber']})


            if ADVANCED_MODE_3G_GOOD['Enabled']==True:
                test_cases.append({'networkProfile':'good3G',
                                   'test_name':'Advanced_Mode_3G_Good_',
                                   'runReplay':False,
                                   'report_name':'AnalyticsReport.html',
                                   'TESTED_URL':ADVANCED_MODE_3G_GOOD['URL'],
                                   'LoopNumber':ADVANCED_MODE_3G_GOOD['LoopNumber']})

            if ADVANCED_MODE_3G_BUSY['Enabled']==True:
                test_cases.append({'networkProfile':'busy3G',
                                   'test_name':'Advanced_Mode_3G_Busy_',
                                   'runReplay':False,
                                   'report_name':'AnalyticsReport.html',
                                   'TESTED_URL':ADVANCED_MODE_3G_BUSY['URL'],
                                   'LoopNumber':ADVANCED_MODE_3G_BUSY['LoopNumber']})

        if USE_TRANSACTIONS==True:
            test_cases=[]
            test_cases.append({'networkProfile':'baseline',
                   'test_name':'Advanced_Mode_Transaction_',
                   'runReplay':False,
                   'report_name':'AnalyticsReport.html',
                   'TESTED_URL':ADVANCED_MODE_BASELINE['URL'],
                   'LoopNumber':ADVANCED_MODE_BASELINE['LoopNumber']})

        ### Start OptMyApp + Traffic + Stop OptMyApp + sniffing ###
        for item in test_cases:
            test_name=item['test_name']+time.strftime("%Y:%m:%d_%H:%M:%S")
            INSERT_TO_LOG(TestLogFile,'Start '+test_name,1)
            test=OPT_MY_APP_TRAFFIC(opt_my_app_url, test_name, item['TESTED_URL'], item['LoopNumber'], OPT_MY_APP_API,
                                    deviceId=DEVICE_ID,
                                    userId=USER_ID,
                                    runReplay=item['runReplay'],
                                    networkProfile=item['networkProfile'],
                                    report_name=item['report_name'],
                                    report_timeout=REPORT_TIMEOUT,
                                    email=USER_EMAIL,
                                    password=USER_PASSWORD,
                                    deviceInfo=USER_DEVICE)
            capture_file=test_name+'.cap'
            test['Tested_URL']=item['TESTED_URL']
            if os.path.isfile(capture_file):
                files_to_save.append(capture_file)
                test['TCP_Dump_File']=os.path.join(os.path.abspath(TestDirName),capture_file)
            if 'HTML_FILE' in test.keys():
                new_file_name=test_name.replace(':','_')+'.html'
                INSERT_TO_LOG(new_file_name,open(test['HTML_FILE'],'r').read())
                test['HTML_FILE']=new_file_name
                files_to_save.append(new_file_name)
                test['HTML_File_Path']=os.path.join(os.path.abspath(TestDirName),new_file_name)
            if 'Files_To_Save' in test.keys():
                for fil in test['Files_To_Save']:
                    files_to_save.append(fil)
                    if fil=="Transactions.csv":
                        for line in open('Transactions.csv','r').readlines():
                            INSERT_TO_LOG(total_transactions_result_file_name,str(line.strip()))

            INSERT_TO_LOG(TestLogFile, str(test), 1)
            INSERT_TO_LOG(TestLogFile,'Stop '+test_name,1)
            test_all_results.append(test)
            all_tests_results_list.append(test)

        ### Collect and print test Results ###
        TestCsvResultFile=TestLogFile.replace('.log','.csv')
        WRITE_DICTS_TO_CSV(TestCsvResultFile,test_all_results)
        files_to_save.append(TestCsvResultFile)
        files_to_save.append(api_log_file)
        #files_to_save.append(RunTimeLog)
        for fil in files_to_save:
            if os.path.isfile(fil) and fil!=api_log_file:
                shutil.move(fil,TestDirName)
            if os.path.isfile(fil) and fil==api_log_file:
                for line in open(api_log_file,'r').readlines():
                    INSERT_TO_LOG(all_api_result_file, line.strip())
                shutil.move(fil,TestDirName)
                DELETE_LOG_CONTENT(api_log_file)
                ADD_LIST_AS_LINE_TO_CSV_FILE(api_log_file,['TimeStamp','RequestType','RequestData','ErrorCode','ResponseData','ExecutionTime'])

        ### Write all test results to total_result_file_name ###
        WRITE_DICTS_TO_CSV(total_result_file_name,all_tests_results_list)
        shutil.copy(total_result_file_name,TestDirName)
        if SAVE_ZIP==True:
            shutil.make_archive(TestDirName, 'zip',TestDirName)
            shutil.rmtree(TestDirName)
        if SAVE_ZIP==None:
            shutil.make_archive(TestDirName, 'zip',TestDirName)
        if SAVE_ZIP==False:
            shutil.rmtree(TestDirName)

#------------------------------ HTTP SELENIUM TRAFFIC -----------------------------------#
if USE_SELENIUM==True:

    all_tests_results_list=[]
    ### All test results file ###
    total_result_file_name='All_Tests_Results.csv'
    DELETE_LOG_CONTENT(total_result_file_name)

    ### Get sites from Alexa *.csv file
    if USE_ALEXA_SITES==True:
        sites=open('AlexaTopMilion.csv','r').readlines()
        sites= ['http://'+url.split(',')[-1].strip() for url in sites][SITES_RANGE[0]:SITES_RANGE[1]]# URLs to test
    if USE_HTTPS_SITES==True:
        sites=[site.strip() for site in open('HTTPS_Sites_Top_100.csv','r').readlines()][SITES_RANGE[0]:SITES_RANGE[1]]
    if USE_HLS_SITES==True:
        sites=[url.strip() for url in open('HLS_Links.csv','r').readlines() if ' ' not in url] + [url.split(' ')[0] for url in open('HLS_Links.csv','r').readlines() if ' ' in url]
        sites=sites[SITES_RANGE[0]:SITES_RANGE[1]]

    for site in sites:
        print '\r\n'
        print '-------------------------------------- Site Number:'+str(sites.index(site)+1)+' '+site+' -------------------------------------------'

        ### Start display
        if 'linux' in platform.system().lower():
            print 'Starting Display on Linux'
            display = Display(visible=0, size=(800, 600))
            print 'Start display result: ', display.start()

        test_time=string=time.strftime("%Y_%m_%d_%H_%M_%S")
        files_to_save=[]

        ### Test Log (not csv) ###
        TestLogFile= 'TestResult_'+test_time+'.log'
        DELETE_LOG_CONTENT(TestLogFile)
        files_to_save.append(TestLogFile)

        ### Result Directory ###
        if USE_TRANSACTIONS==False:
            TestDirName='Test_Results_Replay_'+test_time
        if USE_TRANSACTIONS==True:
            TestDirName='Test_Results_Advanced_'+test_time
        os.mkdir(TestDirName)

        ### NV URL ###
        opt_my_app_url='https://' + OPT_MY_APP_DOMAIN + '/hp/nvcloud?hf=myLittlePony'
        test_all_results=[]

        #USE_SELENIUM=True and USE_TRANSACTIONS==False will execute Replay + Advanced mode, means FULL
        if USE_TRANSACTIONS==False and (CMD_MODE==True or CMD_MODE==False):
            test_cases=[{'networkProfile':'baseline','test_name':'Replay_Mode_','runReplay':True,'report_name':'ReplayReport.html'}]

        #USE_SELENIUM=True and USE_TRANSACTIONS==True and CMD_MODE=False execute single 3 transactions
        if USE_TRANSACTIONS==True and CMD_MODE==False:
            test_cases=[
                {'networkProfile':'baseline','test_name':'Advanced_Mode_Baseline_','runReplay':False,'report_name':'AnalyticsReport.html'},
                ]

        #USE_SELENIUM=True and USE_TRANSACTIONS==True and CMD_MODE=True will execute single transaction for basline only
        if USE_TRANSACTIONS==True and CMD_MODE==True:
            test_cases=[
                {'networkProfile':'baseline','test_name':'Advanced_Mode_Only_Baselinse_','runReplay':False,'report_name':'AnalyticsReport.html'},
                ]

        for item in test_cases:
            ### Start OptMyApp + Selenium Traffic + Stop OptMyApp + sniffing (Replay_mode)
            test_name=item['test_name']+time.strftime("%Y:%m:%d_%H:%M:%S")
            INSERT_TO_LOG(TestLogFile,'Start '+test_name,1)
            test=OPT_MY_APP_TRAFFIC(opt_my_app_url, test_name, site, 0, OPT_MY_APP_API,
                                    use_selenium=True,
                                    deviceId=DEVICE_ID,
                                    userId=USER_ID,
                                    runReplay=item['runReplay'],
                                    networkProfile=item['networkProfile'],
                                    report_name=item['report_name'],
                                    report_timeout=REPORT_TIMEOUT,
                                    email=USER_EMAIL,
                                    password=USER_PASSWORD,
                                    deviceInfo=USER_DEVICE)
            capture_file=test_name+'.cap'
            if os.path.isfile(capture_file):
                files_to_save.append(capture_file)
                test['TCP_Dump_File']=os.path.join(os.path.abspath(TestDirName),capture_file)
            if 'ScreenshootName' in test.keys() and test['ScreenshootName']!=None:
                new_screenshot_name=test_name.replace(':','_')+'.jpg'
                shutil.move(test['ScreenshootName'],new_screenshot_name)
                files_to_save.append(new_screenshot_name)
                test['Screenshot_File_Path']=os.path.join(os.path.abspath(TestDirName),new_screenshot_name)
            if 'HTML_FILE' in test.keys():
                new_file_name=test_name.replace(':','_')+'.html'
                INSERT_TO_LOG(new_file_name,open(test['HTML_FILE'],'r').read())
                test['HTML_FILE']=new_file_name
                files_to_save.append(new_file_name)
                test['HTML_File_Path']=os.path.join(os.path.abspath(TestDirName),new_file_name)
            if 'Files_To_Save' in test.keys():
                for fil in test['Files_To_Save']:
                    files_to_save.append(fil)
                    if fil=="Transactions.csv":
                        for line in open('Transactions.csv','r').readlines():
                            INSERT_TO_LOG(total_transactions_result_file_name,str(line.strip()))

            INSERT_TO_LOG(TestLogFile,str(test),1)
            INSERT_TO_LOG(TestLogFile,'Stop '+test_name,1)
            test['Tested_URL']=site
            test_all_results.append(test)
            all_tests_results_list.append(test)

        ### Stop Linux Display
        if 'linux' in platform.system().lower():
            print 'Stop Display on Linux'
            print 'Stop display result: ',display.stop()

        ### Collect and printtest Results ###
        TestCsvResultFile=TestLogFile.replace('.log','.csv')
        WRITE_DICTS_TO_CSV(TestCsvResultFile,test_all_results)
        files_to_save.append(TestCsvResultFile)
        files_to_save.append(api_log_file)
        #files_to_save.append(RunTimeLog)
        for fil in files_to_save:
            if os.path.isfile(fil) and fil!=api_log_file:
                shutil.move(fil,TestDirName)
            if os.path.isfile(fil) and fil==api_log_file:
                for line in open(api_log_file,'r').readlines():
                    INSERT_TO_LOG(all_api_result_file, line.strip())
                shutil.move(fil,TestDirName)
                DELETE_LOG_CONTENT(api_log_file)
                ADD_LIST_AS_LINE_TO_CSV_FILE(api_log_file,['TimeStamp','RequestType','RequestData','ErrorCode','ResponseData','ExecutionTime'])

        ### Write all test results to total_result_file_name ###
        WRITE_DICTS_TO_CSV(total_result_file_name,all_tests_results_list)
        shutil.copy(total_result_file_name,TestDirName)
        if SAVE_ZIP==True:
            shutil.make_archive(TestDirName, 'zip',TestDirName)
            shutil.rmtree(TestDirName,True)
        if SAVE_ZIP==None:
            shutil.make_archive(TestDirName, 'zip',TestDirName)
        if SAVE_ZIP==False:
            shutil.rmtree(TestDirName)


exceptions=[eval(item.strip()) for item in open(exceptions_file,'r').readlines()]
WRITE_DICTS_TO_CSV('Exceptions.csv',exceptions)
# shutil.move(exceptions_file,TestDirName)
# shutil.move('Exceptions.csv',TestDirName)
if 'temp' in os.listdir('.'):
    os.remove('temp')
SPEC_PRINT(['---------------------------------OptMyAppSanity.py END ----------------------------------------------'])
print '\r\n'*10
