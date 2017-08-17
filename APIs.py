import requests,base64,json,time,sys,os
from Mi_Functions import *
import time
from Params import *
import zipfile


def START_DEFAULT_TEST(IP,PORT,USER,PASSWORD,FLOW_ID,LATENCY,PACKETLOSS,BANDIN,BANDOUT,TEST_NAME,TEST_DESCRIPTION,delay_after_stop=0):
    try:
        URL='http://'+IP+':'+PORT+'/shunra/api/emulation/custom?mode=MULTI_USER'
        if TM_IS_HTTPS==True:
            URL=URL.replace('http','https')
        payload={"flows": [{
        "flowId": FLOW_ID,
        "latency": LATENCY,
        "packetloss": PACKETLOSS,
        "bandwidthIn": BANDIN,
        "bandwidthOut": BANDOUT,
        "isCaptureClientPL": "true"
        } ],
        "testMetadata": {
        "testName":TEST_NAME,
        "description":TEST_DESCRIPTION,
        "networkScenario":"3G"
        }
        }
        headers = {'Authorization':'Basic '+base64.b64encode(USER+':'+PASSWORD),'Content-Type':'application/json','Accept':'application/json'}
        start_time=time.time()
        r = requests.post(URL, data=json.dumps(payload), headers=headers,verify=False)
        stop_time=time.time()
        INSERT_TO_LOG(exceptions_file,str({'START_DEFAULT_TEST_Exception':None}))
        ADD_LIST_AS_LINE_TO_CSV_FILE(api_log_file,['StartDefaultTest',URL,payload,r.headers,r.status_code,r.reason,r.content,stop_time-start_time])
        time.sleep(delay_after_stop)
        return {'Function':'START_DEFAULT_TEST','URL':URL,'Headers':r.headers,'Status':r.status_code,'Reason':r.reason,'Content':r.content,'Execution_time':stop_time-start_time}
    except Exception, e:
        INSERT_TO_LOG(exceptions_file,str({'START_DEFAULT_TEST_Exception':str(e)}))
        return {'Function':'START_DEFAULT_TEST','URL':URL,'START_DEFAULT_TEST_Exception':str(e)}

def START_TEST_IN_PROXY_MODE(IP,PORT,USER,PASSWORD,FLOW_ID,LATENCY,PACKETLOSS,BANDIN,BANDOUT,TEST_NAME,TEST_DESCRIPTION,delay_after_stop=5):
    try:
        URL='http://'+IP+':'+PORT+'/shunra/api/emulation/custom?mode=MULTI_USER&useProxy=true'
        if TM_IS_HTTPS==True:
            URL=URL.replace('http','https')



        # payload={"flows":[{
        #     "flowId":FLOW_ID,
        #     #"srcIp":CLIENT_SOURCE_IP,
        #     "latency":LATENCY,
        #     "packetloss":PACKETLOSS,
        #     "bandwidthIn":BANDIN,
        #     "bandwidthOut":BANDOUT,
        #     "isCaptureClientPL":"true",
        #     "srcIpRange":{"include":[{"from":CLIENT_SOURCE_IP,"to":CLIENT_SOURCE_IP,"port":0,"protocol":0}],"exclude":[]},
        #     "destIpRange":{"include":[{"from":"0.0.0.1","to":"255.255.255.255","port":0,"protocol":0}],"exclude":[{"from":TM_IP,"to":TM_IP,"port":0,"protocol":0}]}}],
        #     "testMetadata":{"testName":TEST_NAME,"isCustom":"true","networkScenario":"Network scenario 1","emulationMode":"MULTI_USER"}}


        payload={"flows": [{
            "flowId":FLOW_ID,
            "srcIp":CLIENT_SOURCE_IP,
            "latency": LATENCY,
            "packetloss": PACKETLOSS,
            "bandwidthIn": BANDIN,
            "bandwidthOut": BANDOUT,
            "isCaptureClientPL": "true",
            "sharedBandwidth": "false"}],
            "testMetadata": {"testName":TEST_NAME,"description":TEST_NAME,"networkScenario":"NetworkScenario"}}


        headers = {'Authorization':'Basic '+base64.b64encode(USER+':'+PASSWORD),'Content-Type':'application/json','Accept':'application/json'}
        start_time=time.time()
        r = requests.post(URL, data=json.dumps(payload), headers=headers,verify=False)
        stop_time=time.time()
        INSERT_TO_LOG(exceptions_file,str({'START_TEST_IN_PROXY_MODE':None}))
        ADD_LIST_AS_LINE_TO_CSV_FILE(api_log_file,['StartDefaultInProxyMode',URL,payload,r.headers,r.status_code,r.reason,r.content,stop_time-start_time])
        time.sleep(delay_after_stop)
        return {'Function':'START_TEST_IN_PROXY_MODE','URL':URL,'Headers':r.headers,'Status':r.status_code,'Reason':r.reason,'Content':r.content,'Execution_time':stop_time-start_time}
    except Exception, e:
        INSERT_TO_LOG(exceptions_file,str({'START_TEST_IN_PROXY_MODE':str(e)}))
        return {'Function':'START_TEST_IN_PROXY_MODE','URL':URL,'START_TEST_IN_PROXY_MODE':str(e)}

def START_NV_TEST_USING_IP_AND_PORTS(IP,PORT,USER,PASSWORD,FLOW_ID,LATENCY,PACKETLOSS,BANDIN,BANDOUT,TEST_NAME,TEST_DESCRIPTION,DST_PORT):
    try:
        URL='http://'+IP+':'+PORT+'/shunra/api/emulation/custom?mode=MULTI_USER'
        if TM_IS_HTTPS==True:
            URL=URL.replace('http','https')
        payload={
          "flows": [
            {
              "flowId": FLOW_ID,
              "srcIpRange": {
                "include": [
                  {
                    "from": "0.0.0.1",
                    "to": "255.255.255.255",
                    "port": 0,
                    "protocol": 0
                  }
                ],
                "exclude": [
                  {
                    "from": TM_IP,
                    "to": TM_IP,
                    "port": 0,
                    "protocol": 0
                  }
                ]
              },
              "destIpRange": {
                "include": [
                  {
                    "from": TM_IP,
                    "to": TM_IP,
                    "port": DST_PORT,
                    "protocol": 17
                  },
                  {
                    "from": TM_IP,
                    "to": TM_IP,
                    "port": DST_PORT,
                    "protocol": 6
                  }
                ]
              },
              "latency": LATENCY,
              "packetloss": PACKETLOSS,
              "bandwidthIn": BANDIN,
              "bandwidthOut": BANDOUT,
              "isCaptureClientPL": "true"
            }
          ],
          "testMetadata": {
            "testName": TEST_NAME,
            "description": TEST_DESCRIPTION,
            "networkScenario": 'Network_Stam'
          }
        }
        headers = {'Authorization':'Basic '+base64.b64encode(USER+':'+PASSWORD),'Content-Type':'application/json','Accept':'application/json'}
        start_time=time.time()
        r = requests.post(URL, data=json.dumps(payload), headers=headers, verify=False)
        stop_time=time.time()
        INSERT_TO_LOG(exceptions_file,str({'START_NV_TEST_USING_IP_AND_PORTS_Exception':None}))
        ADD_LIST_AS_LINE_TO_CSV_FILE(api_log_file,['StartTestUsingIpAndPOrt',URL,payload,r.headers,r.status_code,r.reason,r.content,stop_time-start_time])
        return {'Function':'START_NV_TEST_USING_IP_AND_PORTS','URL':URL,'Headers':r.headers,'Status':r.status_code,'Reason':r.reason,'Content':r.content,'Execution_time':stop_time-start_time}
    except Exception, e:
        INSERT_TO_LOG(exceptions_file,str({'START_NV_TEST_USING_IP_AND_PORTS_Exception':str(e)}))
        return {'Function':'START_NV_TEST_USING_IP_AND_PORTS','URL':URL,'START_DEFAULT_TEST_Exception':str(e)}

def STOP_TEST_BY_TOKEN(IP,PORT,USER,PASSWORD,TOKEN,delay_before_stop=0):
    try:
        time.sleep(delay_before_stop)
        URL='http://'+IP+':'+PORT+'/shunra/api/emulation/stop'
        if TM_IS_HTTPS==True:
            URL=URL.replace('http','https')
        payload={"testTokens": [TOKEN]}
        headers = {'Authorization':'Basic '+base64.b64encode(USER+':'+PASSWORD),'Content-Type':'application/json','Accept':'application/json'}
        start_time=time.time()
        r = requests.put(URL, data=json.dumps(payload), headers=headers, verify=False)
        stop_time=time.time()
        INSERT_TO_LOG(exceptions_file,str({'STOP_TEST_BY_TOKEN_Exception':None}))
        ADD_LIST_AS_LINE_TO_CSV_FILE(api_log_file,['StopTestByToken',URL,payload,r.headers,r.status_code,r.reason,r.content,stop_time-start_time])
        return {'Function':'STOP_TEST_BY_TOKEN','URL':URL,'Headers':r.headers,'Status':r.status_code,'Reason':r.reason,'Content':r.content,'Execution_time':stop_time-start_time}
    except Exception, e:
        INSERT_TO_LOG(exceptions_file,str({'STOP_TEST_BY_TOKEN_Exception':str(e)}))
        return {'Function':'STOP_TEST_BY_TOKEN','URL':URL,'STOP_TEST_BY_TOKEN_Exception':str(e)}

def ANALYSE_TEST_BY_TOKEN(IP,PORT,USER,PASSWORD,TOKEN,ANALYZE_PORT=80,zipResult=True):
    try:
        time.sleep(1)
        if zipResult==True:
            URL='http://'+IP+':'+PORT+'/shunra/api/analysisreport/analyze/'+TOKEN+'?ports=80,3128,3132,5985,8080,8088,11371,1900,2869,2710,8182,443,'+str(ANALYZE_PORT)
        if zipResult==False:
            URL='http://'+IP+':'+PORT+'/shunra/api/analysisreport/analyze/'+TOKEN+'?ports=80,3128,3132,5985,8080,8088,11371,1900,2869,2710,8182,443,'+str(ANALYZE_PORT)+'&zipResult=false'
        if TM_IS_HTTPS==True:
            URL=URL.replace('http','https')
        #payload={"testTokens": [TOKEN]}
        headers = {'Authorization':'Basic '+base64.b64encode(USER+':'+PASSWORD),'Content-Type':'multipart/form-data','Accept-Ranges':'bytes'}
        start_time=time.time()
        r = requests.put(URL,headers=headers,verify=False)
        stop_time=time.time()
        INSERT_TO_LOG(exceptions_file,str({'ANALYSE_TEST_BY_TOKEN_Exception':None}))
        ADD_LIST_AS_LINE_TO_CSV_FILE(api_log_file,['AnalyseTestByToken',URL,None,r.headers,r.status_code,r.reason,'Content_Size_Is: '+str(len(r.content)),stop_time-start_time])
        if zipResult==False:
            return {'Function':'ANALYSE_TEST_BY_TOKEN','URL':URL,'Headers':r.headers,'Status':r.status_code,'Reason':r.reason,'Content':r.content,'Content_Size_Is':str(len(r.content)),'Execution_time':stop_time-start_time}
        if zipResult==True:
            return {'Function':'ANALYSE_TEST_BY_TOKEN','URL':URL,'Headers':r.headers,'Status':r.status_code,'Reason':r.reason,'Content_Size_Is':str(len(r.content)),'Execution_time':stop_time-start_time}
    except Exception, e:
        INSERT_TO_LOG(exceptions_file,str({'ANALYSE_TEST_BY_TOKEN_Exception':str(e)}))
        return {'Function':'ANALYSE_TEST_BY_TOKEN','URL':URL,'ANALYSE_TEST_BY_TOKEN_Exception':str(e)}

def GET_ONLINE_STATISTICS(IP,PORT,USER,PASSWORD,TOKEN,ZIP_RESULT,LAST_UPDATE=None):
    try:
        time.sleep(1)
        if LAST_UPDATE==None:
            URL='http://'+IP+':'+PORT+'/shunra/api/analysisreport/online/'+TOKEN+'?zipResult='+str(ZIP_RESULT).lower()
        if LAST_UPDATE!=None:
            URL='http://'+IP+':'+PORT+'/shunra/api/analysisreport/online/'+TOKEN+'?zipResult='+str(ZIP_RESULT).lower()+'&lastUpdate='+str(LAST_UPDATE)
        if TM_IS_HTTPS==True:
            URL=URL.replace('http','https')
        #payload={"testTokens": [TOKEN]}
        headers = {'Authorization':'Basic '+base64.b64encode(USER+':'+PASSWORD),'Content-Type':'multipart/form-data','Accept-Ranges':'bytes'}
        start_time=time.time()
        r = requests.get(URL,headers=headers,verify=False,proxies=None)
        stop_time=time.time()
        INSERT_TO_LOG(exceptions_file,str({'GET_ONLINE_STATISTICS_Exception':None}))
        ADD_LIST_AS_LINE_TO_CSV_FILE(api_log_file,['AnalyseTestByToken',URL,None,r.headers,r.status_code,r.reason,'Content_Size_Is: '+str(len(r.content)),stop_time-start_time])
        return {'Function':'GET_ONLINE_STATISTICS','URL':URL,'Headers':r.headers,'Status':r.status_code,'Reason':r.reason,'Content':'Content_Size_Is: '+str(len(r.content)),'Execution_time':stop_time-start_time,'Content':r.content}
    except Exception, e:
        INSERT_TO_LOG(exceptions_file,str({'GET_ONLINE_STATISTICS_Exception':str(e)}))
        return {'Function':'GET_ONLINE_STATISTICS','URL':URL,'ANALYSE_TEST_BY_TOKEN_Exception':str(e)}

def SET_OR_GET_MARK_ONLINE_STATISTICS(IP, PORT, USER, PASSWORD, TOKEN, MARKID, ZIP_RESULT, IS_SET=True, GET_SECOND_OPTION=False):
    try:
        time.sleep(1)
        URL='http://'+IP+':'+PORT+'/shunra/api/analysisreport/online/'+TOKEN+'/mark/'+MARKID+'?zipResult='+str(ZIP_RESULT).lower()
        if GET_SECOND_OPTION==True:
            URL='http://'+IP+':'+PORT+'/shunra/api/analysisreport/online/'+TOKEN+'-'+MARKID+'?zipResult='+str(ZIP_RESULT).lower()
        if TM_IS_HTTPS==True:
            URL=URL.replace('http','https')
        headers = {'Authorization':'Basic '+base64.b64encode(USER+':'+PASSWORD),'Content-Type':'multipart/form-data','Accept-Ranges':'bytes'}
        start_time=time.time()
        if IS_SET==True:
            r = requests.put(URL,headers=headers,verify=False,proxies=None)
        if IS_SET==False:
            r = requests.get(URL,headers=headers,verify=False,proxies=None)
        stop_time=time.time()
        INSERT_TO_LOG(exceptions_file,str({'SET_MARK_ONLINE_STATISTICS_Exception':None}))
        ADD_LIST_AS_LINE_TO_CSV_FILE(api_log_file,['AnalyseTestByToken',URL,None,r.headers,r.status_code,r.reason,'Content_Size_Is: '+str(len(r.content)),stop_time-start_time])
        return {'Function':'SET_OR_GET_MARK_ONLINE_STATISTICS','URL':URL,'Headers':r.headers,'Status':r.status_code,'Reason':r.reason,'Content':'Content_Size_Is: '+str(len(r.content)),'Execution_time':stop_time-start_time,'Content':r.content}
    except Exception, e:
        INSERT_TO_LOG(exceptions_file,str({'SET_MARK_ONLINE_STATISTICS_Exception':str(e)}))
        return {'Function':'SET_OR_GET_MARK_ONLINE_STATISTICS','URL':URL,'SET_MARK_ONLINE_STATISTICS_Exception':str(e)}

def GET_SHUNRA_FILE_BY_TEST_TOKEN(IP,PORT,USER,PASSWORD,TOKEN):
    try:
        URL='http://'+IP+':'+PORT+'/shunra/api/trafficresource/analysis/'+TOKEN
        if TM_IS_HTTPS==True:
            URL=URL.replace('http','https')
        headers = {'Authorization':'Basic '+base64.b64encode(USER+':'+PASSWORD),'Accept':'application/octet-stream'}
        start_time=time.time()
        r = requests.get(URL, headers=headers, verify=False)
        stop_time=time.time()
        INSERT_TO_LOG(exceptions_file,str({'GET_SHUNRA_FILE_BY_TEST_TOKEN':None}))
        ADD_LIST_AS_LINE_TO_CSV_FILE(api_log_file,['GetShunraFileByToken',URL,'',r.headers,r.status_code,r.reason,r.content,stop_time-start_time])
        return {'Function':'GET_SHUNRA_FILE_BY_TEST_TOKEN','URL':URL,'Headers':r.headers,'Status':r.status_code,'Reason':r.reason,'Content':r.content,'Execution_time':stop_time-start_time}
    except Exception, e:
        INSERT_TO_LOG(exceptions_file,str({'GET_SHUNRA_FILE_BY_TEST_TOKEN':str(e)}))
        return {'Function':'GET_SHUNRA_FILE_BY_TEST_TOKEN','URL':URL,'GET_SHUNRA_FILE_BY_TEST_TOKEN':str(e)}

def GET_TEST_ANALYTICS_REPORT(IP,PORT,USER,PASSWORD,TOKEN):
    try:
        URL='http://'+IP+':'+PORT+'/shunra/api/analysisreport/'+TOKEN+'?zipResult=true'
        if TM_IS_HTTPS==True:
            URL=URL.replace('http','https')
        #payload={"testTokens": [TOKEN]}
        headers = {'Authorization':'Basic '+base64.b64encode(USER+':'+PASSWORD),'Content-Type':'multipart/form-data','Accept-Ranges':'bytes','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

        start_time=time.time()
        r = requests.get(URL,headers=headers,verify=False,proxies=None)
        stop_time=time.time()
        INSERT_TO_LOG(exceptions_file,str({'GET_ONLINE_STATISTICS_Exception':None}))
        ADD_LIST_AS_LINE_TO_CSV_FILE(api_log_file,['AnalyseTestByToken',URL,None,r.headers,r.status_code,r.reason,'Content_Size_Is: '+str(len(r.content)),stop_time-start_time])
        return {'Function':'GET_TEST_ANALYTICS_REPORT','URL':URL,'Headers':r.headers,'Status':r.status_code,'Reason':r.reason,'Content':'Content_Size_Is: '+str(len(r.content)),'Execution_time':stop_time-start_time,'Content':r.content}
    except Exception, e:
        INSERT_TO_LOG(exceptions_file,str({'GET_ONLINE_STATISTICS_Exception':str(e)}))
        return {'Function':'GET_TEST_ANALYTICS_REPORT','URL':URL,'ANALYSE_TEST_BY_TOKEN_Exception':str(e)}

def DELETE_TEST_BY_TOKEN(IP,PORT,USER,PASSWORD,TOKEN):
    try:
        URL='http://'+IP+':'+PORT+'/shunra/api/test/'+TOKEN
        if TM_IS_HTTPS==True:
            URL=URL.replace('http','https')
        headers = {'Authorization':'Basic '+base64.b64encode(USER+':'+PASSWORD),'Content-Type':'multipart/form-data','Accept-Ranges':'bytes'}
        start_time=time.time()
        r = requests.delete(URL,headers=headers,verify=False)
        stop_time=time.time()
        INSERT_TO_LOG(exceptions_file,str({'DELETE_TEST_BY_TOKEN_Exception':None}))
        ADD_LIST_AS_LINE_TO_CSV_FILE(api_log_file,['DeleteTestByToken',URL,payload,r.headers,r.status_code,r.reason,r.content,stop_time-start_time])
        return {'Function':'DELETE_TEST_BY_TOKEN','URL':URL,'Headers':r.headers,'Status':r.status_code,'Reason':r.reason,'Content':r.content,'Execution_time':stop_time-start_time}
    except Exception, e:
        INSERT_TO_LOG(exceptions_file,str({'DLETE_TEST_BY_TOKEN_Exception':str(e)}))
        return {'Function':'DELETE_TEST_BY_TOKEN','URL':URL,'DELETE_TEST_BY_TOKEN_Exception':str(e)}

def ADD_NEW_USER(URL,USER,PASSWORD,JSON):
    try:
        headers = {'Authorization':'Basic '+base64.b64encode(USER+':'+PASSWORD),'Content-Type':'application/json','Accept':'application/json'}
        start=time.time()
        r = requests.post(URL,data=json.dumps(JSON),headers=headers)
        stop=time.time()
        return {'Response_Headers':r.headers,'Response_Status':r.status_code,'Reason':r.reason,'Response_Content':r.content,'Execution_Time':stop-start}
    except Exception, e:
        return {'ADD_NEW_USER':str(e)}

def OPT_MY_APP_API(url,**kwargs):
    global number_of_api_failures
    user_agent='Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    try:
        payload={}
        if 'requestType' in kwargs.keys():
            payload['requestType']=kwargs['requestType']
        if 'deviceId' in kwargs.keys():
            payload['deviceId']=kwargs['deviceId']
        if 'userId' in kwargs.keys():
            payload['userId']=kwargs['userId']
        if 'networkProfile' in kwargs.keys():
            payload['networkProfile']=kwargs['networkProfile']
        if 'runReplay' in kwargs.keys():
            payload['runReplay']=kwargs['runReplay']
        if 'check' in kwargs.keys():
            payload['check']=kwargs['check']
        if 'report_name' in kwargs.keys():
            payload['name']=kwargs['report_name']
        if 'sessionId' in kwargs.keys():
            payload['sessionId']=kwargs['sessionId']
        if 'startTransaction' in kwargs.keys():
            payload['startTransaction']=kwargs['startTransaction']
        if 'stopTransaction' in kwargs.keys():
            payload['stopTransaction']=kwargs['stopTransaction']
        if 'transName' in kwargs.keys():
            payload['transName']=kwargs['transName']
        if 'email' in kwargs.keys():
            payload['email']=kwargs['email']
        if 'password' in kwargs.keys():
            payload['password']=kwargs['password']
        if 'deviceInfo' in kwargs.keys():
            payload['deviceInfo']=kwargs['deviceInfo']


        if 'password' in kwargs.keys():
            payload['password']=kwargs['password']
        if 'firstName' in kwargs.keys():
            payload['firstName']=kwargs['firstName']
        if 'lastName' in kwargs.keys():
            payload['lastName']=kwargs['lastName']
        if 'company' in kwargs.keys():
            payload['company']=kwargs['company']
        if 'country' in kwargs.keys():
            payload['country']=kwargs['country']
        if 'passcode' in kwargs.keys():
            payload['passcode']=kwargs['passcode']

        headers = {'Host':url[url.find('://')+3:url.find('/hp')],'User-Agent':user_agent,'CSRF':'NV_Insights'}

        print '--> API Payload: '+str(payload)
        if kwargs['requestType']=='stopNVTest':
            print '...Delay before '+kwargs['requestType']+'is:'+str(STOP_START_DELAY)
            time.sleep(STOP_START_DELAY)
        start_time=time.time()
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        stop_time=time.time()


        if kwargs['requestType']=='startNVTest' or kwargs['requestType']=='realtimeUpdate' or kwargs['requestType']=='startTransaction' or kwargs['requestType']=='login' or kwargs['requestType']=='logout':
            print '...Delay after '+kwargs['requestType']+' is:'+str(STOP_START_DELAY)
            time.sleep(STOP_START_DELAY)


        if '<!doctype html' not in r.content.lower():
            if len(r.content)>0:
                print '--> API Response: ',r.content
                json_result=json.loads(r.content)
                json_result['API_EXECUTION_TIME']=stop_time-start_time
                INSERT_TO_LOG(exceptions_file,str({'OPT_MY_APP_API_Exception':None}))
                if json_result['errorCode']!=0:
                    number_of_api_failures -= 1
                if number_of_api_failures<0:
                    SPEC_PRINT(['*** ACHTUNG ACHTUNG ***','MAX number of API failures (errorCode!=0) is reached!!!','Test execution will be stopped!!!','Looks like "NV HARAKIRI :( "'])
                    sys.exit('MAX number of API failures (errorCode!=0) is reached!!!')
                ADD_LIST_AS_LINE_TO_CSV_FILE(api_log_file,[time.strftime("%Y_%m_%d_%H_%M_%S"),payload['requestType'],payload,json_result['errorCode'],r.content,json_result['API_EXECUTION_TIME']])
                return json_result
            if len(r.content)==0:
                ADD_LIST_AS_LINE_TO_CSV_FILE(api_log_file,[time.strftime("%Y_%m_%d_%H_%M_%S"),payload['requestType'],payload,'N/A','',stop_time-start_time])
                SPEC_PRINT(['*** ACHTUNG ACHTUNG ***','API Response is EMPTY!!','Looks like "NV HARAKIRI :( "'])
                sys.exit('API Response is EMPTY!!')

        if '<!doctype html' in r.content.lower():
            html_result=r.content
            DELETE_LOG_CONTENT('temp')
            INSERT_TO_LOG('temp',html_result)
            INSERT_TO_LOG(exceptions_file,str({'OPT_MY_APP_API_Exception':None}))
            if kwargs['requestType']!='getArtfct':
                ADD_LIST_AS_LINE_TO_CSV_FILE(api_log_file,[time.strftime("%Y_%m_%d_%H_%M_%S"),payload['requestType'],payload,'N/A',r.content,stop_time-start_time])
                SPEC_PRINT(['*** ACHTUNG ACHTUNG ***','API Response is HTML and not JSON as expected!!!','Test execution will be stopped!!!','Looks like "NV HARAKIRI :( "'])
                print 'HTML Content is:'
                print '\r\n'+html_result
                sys.exit('API Response is HTML and not JSON as expected!!!')
            ADD_LIST_AS_LINE_TO_CSV_FILE(api_log_file,[time.strftime("%Y_%m_%d_%H_%M_%S"),payload['requestType'],payload,'N/A',r.content[0:500]+'\r\n...'*5+'\r\n'+r.content[-500:],stop_time-start_time])
            return {'HTML_FILE':'temp','API_EXECUTION_TIME':stop_time-start_time,'HTML_SIZE_KB':len(html_result)/1024}
    except Exception,e:
        print str(e)
        INSERT_TO_LOG(exceptions_file,str({'OPT_MY_APP_API_Exception':str(e)}))
        ADD_LIST_AS_LINE_TO_CSV_FILE(api_log_file,[time.strftime("%Y_%m_%d_%H_%M_%S"),payload['requestType'],payload,'N/A','N/A',time.time()-start_time])
        return {'OPT_MY_APP_API_Exception':str(e),'API_EXECUTION_TIME':time.time()-start_time}

def GET_MERGED_HAR_BY_TOKEN(IP,PORT,USER,PASSWORD,TOKEN,zipResult=True, delay=2):
    try:
        if zipResult==True:
            URL='http://'+IP+':'+PORT+'/shunra/api/analysisreport/har/'+TOKEN+'?zipResult=true'
        if zipResult==False:
            URL='http://'+IP+':'+PORT+'/shunra/api/analysisreport/har/'+TOKEN+'?zipResult=false'
        if TM_IS_HTTPS==True:
            URL=URL.replace('http','https')

        headers = {'Authorization':'Basic '+base64.b64encode(USER+':'+PASSWORD),'Content-Type':'application/json','Accept':'application/json'}
        start_time=time.time()
        r = requests.get(URL,headers=headers,verify=False)
        stop_time=time.time()
        if 'errorCode' in str(r.content):
            error_code=eval(r.content)['errorCode']
            if error_code!=0:
                return {'Function':'GET_MERGED_HAR_BY_TOKEN','URL':URL,'Headers':r.headers,'Status':r.status_code,'Reason':r.reason,'Content':r.content,'Content_Size_Is':str(len(r.content)),'Execution_time':stop_time-start_time}

        stop_time=time.time()
        INSERT_TO_LOG(exceptions_file,str({'GET_MERGED_HAR_BY_TOKEN':None}))
        ADD_LIST_AS_LINE_TO_CSV_FILE(api_log_file,['GetMergedHarByToken',URL,None,r.headers,r.status_code,r.reason,'Content_Size_Is: '+str(len(r.content)),stop_time-start_time])
        time.sleep(delay)
        if zipResult==False:
            # Get all URLs from HAR content
            temp_har_name='har.har'
            DELETE_LOG_CONTENT(temp_har_name)
            INSERT_TO_LOG(temp_har_name,r.content)
            urls_in_har={}
            urls_in_har=GET_ALL_REQUEST_URLS_FROM_HAR(os.path.abspath(temp_har_name))
            return {'Function':'GET_MERGED_HAR_BY_TOKEN','URL':URL,'Headers':r.headers,'Status':r.status_code,'Reason':r.reason,'Content':r.content,'Content_Size_Is':str(len(r.content)),
                    'Execution_time':stop_time-start_time,'URLs_In_Har':urls_in_har}
        if zipResult==True:

            # Save downloaded HARs into directory
            temp_zip_file_name='temp.zip'
            unzip_dir_name='HARs_'+str(time.time())
            INSERT_TO_LOG(temp_zip_file_name,r.content)
            zip_ref = zipfile.ZipFile(temp_zip_file_name, 'r')
            zip_ref.extractall(unzip_dir_name)
            zip_ref.close()

            # Get all URLs from all HAR files in ZIP
            urls_in_har={}
            for fil in os.listdir(os.path.abspath(unzip_dir_name)):
                urls_in_har[fil]=GET_ALL_REQUEST_URLS_FROM_HAR(os.path.join(unzip_dir_name,fil))

            return {'Function':'GET_MERGED_HAR_BY_TOKEN','URL':URL,'Headers':r.headers,'Status':r.status_code,'Reason':r.reason,'Content_Size_Is':str(len(r.content)),'Execution_time':stop_time-start_time,
                    'HAR_Directory_Name':unzip_dir_name,'Request_URLs_Per_HAR_File':urls_in_har}
    except Exception, e:
        INSERT_TO_LOG(exceptions_file,str({'GET_MERGED_HAR_BY_TOKEN_Exception':str(e)}))
        return {'Function':'GET_MERGED_HAR_BY_TOKEN','GET_MERGED_HAR_BY_TOKEN_Exception':str(e),'URL':URL,}

def GET_READY_ASYNC_MERGED_HAR_BY_MDATA(IP, PORT, USER, PASSWORD, MDATA, zipResult=True, returnData=True, delay=2):
    try:
        null="null"
        false=False
        true=True
        if zipResult==True:
            URL='http://'+IP+':'+PORT+'/shunra/api/analysisexpress/analysis/'+MDATA+'?zipResult=true'
        if zipResult==False:
            URL='http://'+IP+':'+PORT+'/shunra/api/analysisexpress/analysis/'+MDATA+'?zipResult=false'
        if returnData==True:
            URL+='&returnData=true'
        if returnData==False:
            URL+='&returnData=false'
        if TM_IS_HTTPS==True:
            URL=URL.replace('http','https')
        headers = {'Authorization':'Basic '+base64.b64encode(USER+':'+PASSWORD),'Accept':'application/json'}#,'Content-Type':'application/json'}
        start_time=time.time()
        r = requests.get(URL,headers=headers,verify=False)
        stop_time=time.time()
        INSERT_TO_LOG(exceptions_file,str({'GET_READY_ASYNC_MERGED_HAR_BY_MDATA':None}))
        ADD_LIST_AS_LINE_TO_CSV_FILE(api_log_file,['GetMergedHarByToken',URL,None,r.headers,r.status_code,r.reason,'Content_Size_Is: '+str(len(r.content)),stop_time-start_time])
        time.sleep(delay)
        returned_error_code=0
        if 'errorCode' in str(r.content):
            returned_error_code=eval(r.content)['errorCode']
        if returned_error_code==0:
            if returnData==False:
                return {'Function':'GET_READY_ASYNC_MERGED_HAR_BY_MDATA','Headers':r.headers,'Status':r.status_code,'Reason':r.reason,'Content':r.content,'Content_Size_Is':str(len(r.content)),'Execution_time':stop_time-start_time}
            if returnData==True:
                if zipResult==False:
                    # Save downloaded HARs into directory
                    temp_file_name='temp.txt'
                    DELETE_LOG_CONTENT(temp_file_name)
                    INSERT_TO_LOG(temp_file_name,r.content)
                    urls_in_har=GET_ALL_REQUEST_URLS_FROM_HAR(os.path.abspath(temp_file_name))
                    time.sleep(delay)
                    return {'Function':'GET_READY_ASYNC_MERGED_HAR_BY_MDATA','Headers':r.headers,'Status':r.status_code,'Reason':r.reason,'Content_Size_Is':str(len(r.content)),'Execution_time':stop_time-start_time,'Request_URLs_In_HAR_File':urls_in_har,'Content':r.content}
                if zipResult==True:
                    # Save downloaded HARs into directory
                    temp_zip_file_name='temp.zip'
                    unzip_dir_name='HARs_'+str(time.time())
                    INSERT_TO_LOG(temp_zip_file_name,r.content)
                    zip_ref = zipfile.ZipFile(temp_zip_file_name, 'r')
                    zip_ref.extractall(unzip_dir_name)
                    zip_ref.close()
                    # Get all URLs from all HAR files in ZIP
                    urls_in_har={}
                    for fil in os.listdir(os.path.abspath(unzip_dir_name)):
                        urls_in_har[fil]=GET_ALL_REQUEST_URLS_FROM_HAR(os.path.join(unzip_dir_name,fil))
                    time.sleep(delay)
                    return {'Function':'GET_READY_ASYNC_MERGED_HAR_BY_MDATA','URL':URL,'Headers':r.headers,'Status':r.status_code,'Reason':r.reason,'Content':r.content,'Content_Size_Is':str(len(r.content)),'Execution_time':stop_time-start_time,
                        'HAR_Directory_Name':unzip_dir_name,'Request_URLs_Per_HAR_File':urls_in_har}
        else:
            SPEC_PRINT(['Returned error code is '+str(returned_error_code)])
            return {'URL':URL,'Headers':r.headers,'Status':r.status_code,'Reason':r.reason,'Content':r.content,'Content_Size_Is':str(len(r.content)),'Execution_time':stop_time-start_time}
    except Exception, e:
       INSERT_TO_LOG(exceptions_file,str({'GET_READY_ASYNC_MERGED_HAR_BY_MDATA_Exception':str(e)}))
       return {'URL':URL,'GET_READY_ASYNC_MERGED_HAR_BY_MDATA_Exception':str(e),'Content':r.content}

def START_HAR_ANALYTICS_MERGE_HARS_ASYNC_REQUEST(IP,PORT,USER,PASSWORD,TOKEN, delay=2):
    try:
        URL='http://'+IP+':'+PORT+'/shunra/api/analysisexpress/extract/har/'+TOKEN
        if TM_IS_HTTPS==True:
            URL=URL.replace('http','https')
        headers = {'Authorization':'Basic '+base64.b64encode(USER+':'+PASSWORD)}#,'Content-Type':'application/json'}
        start_time=time.time()
        r = requests.put(URL,headers=headers,verify=False)
        stop_time=time.time()
        INSERT_TO_LOG(exceptions_file,str({'START_HAR_ANALYTICS_MERGE_HARS_ASYNC_REQUEST':None}))
        ADD_LIST_AS_LINE_TO_CSV_FILE(api_log_file,['StartHarAnalyticsMergeHarsAsyncRequest',URL,None,r.headers,r.status_code,r.reason,'Content_Size_Is: '+str(len(r.content)),stop_time-start_time])
        time.sleep(delay)
        return {'Function':'START_HAR_ANALYTICS_MERGE_HARS_ASYNC_REQUEST','URL':URL,'Headers':r.headers,'Status':r.status_code,'Reason':r.reason,'Content':r.content,'Content_Size_Is':str(len(r.content)),'Execution_time':stop_time-start_time}
    except Exception, e:
        INSERT_TO_LOG(exceptions_file,str({'START_HAR_ANALYTICS_MERGE_HARS_ASYNC_REQUEST_Exception':str(e)}))
        return {'Function':'START_HAR_ANALYTICS_MERGE_HARS_ASYNC_REQUEST','START_HAR_ANALYTICS_MERGE_HARS_ASYNC_REQUEST_Exception':str(e)}

def DOWNLOAD_HAR_FILE_BY_TOKEN(IP,PORT,USER,PASSWORD,TOKEN,delete_hars_dir=False,delay=2):
    try:
        time.sleep(1)
        URL='http://'+IP+':'+PORT+'/shunra/api/trafficresource/harfiles/'+TOKEN
        if TM_IS_HTTPS==True:
            URL=URL.replace('http','https')
        headers = {'Authorization':'Basic '+base64.b64encode(USER+':'+PASSWORD),'Accept':'application/zip'}
        start_time=time.time()
        r = requests.get(URL,headers=headers,verify=False)
        stop_time=time.time()
        if 'errorCode' in str(r.content):
            error_code=eval(r.content)['errorCode']
            if error_code!=0:
                return {'Function':'DOWNLOAD_HAR_FILE_BY_TOKEN','URL':URL,'Headers':r.headers,'Status':r.status_code,'Reason':r.reason,'Content':r.content,'Content_Size_Is':str(len(r.content)),'Execution_time':stop_time-start_time}

        INSERT_TO_LOG(exceptions_file,str({'DOWNLOAD_HAR_FILE_BY_TOKEN':None}))
        ADD_LIST_AS_LINE_TO_CSV_FILE(api_log_file,['DownloadHarFileByToken',URL,None,r.headers,r.status_code,r.reason,'Content_Size_Is: '+str(len(r.content)),stop_time-start_time])

        # Save downloaded HARs into directory
        temp_zip_file_name='temp.zip'
        unzip_dir_name='HARs_'+str(time.time())
        INSERT_TO_LOG(temp_zip_file_name,r.content)
        zip_ref = zipfile.ZipFile(temp_zip_file_name, 'r')
        zip_ref.extractall(unzip_dir_name)
        zip_ref.close()

        # Get all URLs from all HAR files in ZIP
        urls_in_har={}
        for fil in os.listdir(os.path.abspath(unzip_dir_name)):
            urls_in_har[fil]=GET_ALL_REQUEST_URLS_FROM_HAR(os.path.join(unzip_dir_name,fil))

        # Delete HAR directories
        if delete_hars_dir==True:
            shutil.rmtree(unzip_dir_name, ignore_errors=True)
        time.sleep(delay)
        return {'URL':URL,'Headers':r.headers,'Status':r.status_code,'Reason':r.reason,'Content':r.content,'Content_Size_Is':str(len(r.content)),'Execution_time':stop_time-start_time,
                'HAR_Directory_Name':unzip_dir_name,'Request_URLs_Per_HAR_File':urls_in_har}
    except Exception, e:
        INSERT_TO_LOG(exceptions_file,str({'DOWNLOAD_HAR_FILE_BY_TOKEN_Exception':str(e)}))
        return {'URL':URL,'DOWNLOAD_HAR_FILE_BY_TOKEN_Exception':str(e)}

def LOCAL_EDITOR_API(IP,PORT,USER,PASSWORD):
    url='http://'+IP+':'+PORT+'/shunra/api/locationeditor/location/custom'
    headers = {'Authorization':'Basic '+base64.b64encode(USER+':'+PASSWORD),'Content-Type':'application/json','Accept':'application/json'}
    payload={"settings":{"isCaptureClientPl":False,"packetListMaxSizeMB":300,"isPacketListCaptureCyclic":True},"excludeIps":[{"from":"8.8.8.8","to":"8.8.8.12","protocol":6,"port":8183}]}
    r = requests.post(url,headers=headers,verify=False,data=json.dumps(payload))
    return {'Function':'LOCAL_EDITOR_API','URL':url,'Headers':r.headers,'Status':r.status_code,'Reason':r.reason,'Content':r.content,'Content_Size_Is':str(len(r.content))}

def CANCEL_MERGE_HAR_BY_TOKEN(IP,PORT,USER,PASSWORD,TOKEN,delay=2):
    try:
        URL='http://'+IP+':'+PORT+'/shunra/api/analysisexpress/analysis/'+TOKEN
        if TM_IS_HTTPS==True:
            URL=URL.replace('http','https')
        headers = {'Authorization':'Basic '+base64.b64encode(USER+':'+PASSWORD)}
        start_time=time.time()
        r = requests.delete(URL,headers=headers,verify=False)
        stop_time=time.time()
        if 'errorCode' in str(r.content):
            error_code=eval(r.content)['errorCode']
            if error_code!=0:
                return {'Function':'CANCEL_MERGE_HAR_BY_TOKEN','URL':URL,'Headers':r.headers,'Status':r.status_code,'Reason':r.reason,'Content':r.content,'Content_Size_Is':str(len(r.content)),'Execution_time':stop_time-start_time}

        INSERT_TO_LOG(exceptions_file,str({'CANCEL_MERGE_HAR_BY_TOKEN':None}))
        ADD_LIST_AS_LINE_TO_CSV_FILE(api_log_file,['CancelMergeHarByToken',URL,None,r.headers,r.status_code,r.reason,'Content_Size_Is: '+str(len(r.content)),stop_time-start_time])

        time.sleep(delay)
        return {'Function':'CANCEL_MERGE_HAR_BY_TOKEN','URL':URL,'Headers':r.headers,'Status':r.status_code,'Reason':r.reason,'Content':r.content,'Content_Size_Is':str(len(r.content)),'Execution_time':stop_time-start_time}

    except Exception, e:
        INSERT_TO_LOG(exceptions_file,str({'CANCEL_MERGE_HAR_BY_TOKEN_Exception':str(e)}))
        return {'Function':'CANCEL_MERGE_HAR_BY_TOKEN','URL':URL,'CANCEL_MERGE_HAR_BY_TOKEN_Exception':str(e)}

class MC_APIS():
    def __init__(self, ip, port, https, method, request_payload='', body_type='JSON', url_path='', params={}, delay=0, additional_headers={}, api_name='API_NAME_UKNOWN',user=None, password=None, save_csv_file=True):
        self.api_name=api_name
        self.ip=ip
        self.port=port
        self.user=user
        self.password=password
        self.https=https
        self.url_path=url_path
        self.method=method
        self.request_payload=request_payload
        self.delay=delay
        self.body_type=body_type
        self.params=params
        self.additional_headers=additional_headers
        self.save_csv_file=save_csv_file

    def MAKE_URL(self):
        self.url='http://'+self.ip+':'+self.port+'/'+self.url_path
        if self.params!={}:
            self.params_string='?'
            for k in self.params.keys():
                self.params_string+=k+'='+self.params[k]+'&'
            self.url='http://'+self.ip+':'+self.port+'/'+self.url_path+self.params_string.strip('&')
        if self.https==True:
            self.url=self.url.replace('http','https')
        return self.url

    def GENERATE_REQUEST_HEADERRS(self):
        if self.user==None and self.password==None:
             self.req_headers = {'Authorization':'Basic TVVFV1NrTVBjVmJna3RVQ25JWEpwZz09Om1jMDFAIzRyZg=='} #### This is needed for MC cloud only
        else:
            self.req_headers = {'Authorization':'Basic '+base64.b64encode(self.user+':'+self.password)}
        if self.additional_headers!={}:
            for k in self.additional_headers.keys():
                self.req_headers[k]=self.additional_headers[k]
        return self.req_headers

    def RUN_REQUEST(self):
        #try:
            self.url=self.MAKE_URL()
            self.req_headers=self.GENERATE_REQUEST_HEADERRS()
            self.content_as_dic=None
            self.error=None
            self.start_time=time.time()
            if self.method=='GET':
                r = requests.get(self.url,headers=self.req_headers,verify=False, allow_redirects=True)
            if self.method=='POST':
                if self.body_type=='JSON':
                    r = requests.post(self.url,headers=self.req_headers,verify=False,json=self.request_payload, allow_redirects=False)
                    if r.status_code==301:
                        r=requests.post(r.headers['Location'],headers=self.req_headers,verify=False,json=self.request_payload, allow_redirects=False)
                if self.body_type=='STRING':
                    r = requests.post(self.url,headers=self.req_headers,verify=False,data=self.request_payload, allow_redirects=False)
                    if r.status_code==301:
                        r=requests.post(r.headers['Location'],headers=self.req_headers,verify=False,data=self.request_payload, allow_redirects=False)
            if self.method=="PUT":
                if self.body_type=='JSON':
                    r = requests.put(self.url,headers=self.req_headers,verify=False,json=self.request_payload,allow_redirects=False)
                    if r.status_code==301:
                        r=requests.put(r.headers['Location'],headers=self.req_headers,verify=False,json=self.request_payload, allow_redirects=False)
                if self.body_type=='STRING':
                    r = requests.put(self.url,headers=self.req_headers,verify=False,data=self.request_payload,allow_redirects=False)
                    if r.status_code==301:
                        r=requests.put(r.headers['Location'],headers=self.req_headers,verify=False,data=self.request_payload, allow_redirects=False)
            self.execution_time=time.time()-self.start_time


            print str(r.headers.keys())
            if 'content-type' in str(r.headers.keys()).lower() and 'json' in  r.headers['Content-Type'].lower():
                content_as_dict_value=json.loads(r.content)
            else:
                content_as_dict_value=None

            dic_to_return={'URL':self.url,'Execution_Time':self.execution_time,'Content':r.content,'Content_As_Dict':content_as_dict_value,'Status_Code':r.status_code,
                           'Request_Headers':self.req_headers,'Response_Headers':r.headers,'Exception':self.error,'Final_URL':r.url, 'API_Name':self.api_name,
                           'Request_Payload':self.request_payload, 'HTTP_Method':self.method,'Content_Size':str(len(r.content)/1024.0)+' [kb]'}

            if self.save_csv_file==True:
                first_raw=['API_Name','HTTP_Method','Status_Code','Content_Size','Execution_Time','Content','URL','Request_Headers','Response_Headers','Final_URL','Exception']
                file_name='MC_APIs.csv'
                if file_name not in os.listdir('.'):
                    ADD_LIST_AS_LINE_TO_CSV_FILE(file_name,first_raw)
                line=[]
                for k in first_raw:
                    if k!='Content':
                        line.append(dic_to_return[k])
                    if k=='Content':
                        if dic_to_return['Content_Size']<200:
                            line.append(dic_to_return['Content'])
                        else:
                            line.append(str(dic_to_return['Content'])[0:200])
                ADD_LIST_AS_LINE_TO_CSV_FILE(file_name,line)
            return dic_to_return


        # except Exception, e:
        #     self.error=e
        #     self.execution_time=time.time()-self.start_time
        #     return {'URL':self.url,'Execution_Time':self.execution_time,'Request_Headers':self.req_headers,'Exception':self.error,'API_Name':self.api_name,'HTTP_Method':self.method}



























# my_nv=MC_APIS(ip='52.20.143.142',port='8182',user='admin123',password='Admin123',https=True,method='GET',url_path='shunra/auth/login',
#                 additional_headers={'Accept':'application/json'},params={'stam1':'1','stam2':'2'})
# print my_nv.MAKE_URL()
# api_resp=my_nv.START_API()
# PRINT_DICT(api_resp)





