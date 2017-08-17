###############################################################################
# This script generates HTTP traffic while NV emulation                      ##
# Main idea is to use this script for NV report created with LR replay mode  ##
###############################################################################

import urllib2
import BeautifulSoup
import requests
import time
from APIs import *
import warnings
import SimpleHTTPServer
import SocketServer
import os
import sys
from urllib2 import urlopen

exceptions_file='Exceptions.csv'

def INSERT_TO_LOG(log_file, msg, time_flag=0):
    log_file = open(log_file, 'a')
    if time_flag==0:
        string=msg
    if time_flag==1:
        string=time.strftime("%Y-%m-%d %H:%M:%S")+' '+msg
    log_file.write(string+'\n')
    log_file.close()

def HTTP_GET_SITE(site_url,loops_number,proxies=None,request_headers=None,delay=0,method='GET',post_data='POST_DATA'*100):
    #user_agent={'User-agent':'''Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'''}
    try:
        start_total_time=time.time()
        times=[]
        sizes=[]
        for x in range(0,loops_number):
            test_site=site_url
            start_time=time.time()

            if method=="GET":
                if proxies==None:
                    r = requests.get(test_site,headers=request_headers,verify=False)
                else:
                    r = requests.get(test_site,headers =request_headers,proxies=proxies,timeout=(5, 10),verify=False)

            if method=="POST":
                if proxies==None:
                    r = requests.post(test_site,headers=request_headers,verify=False,data='POST_DATA'*100)
                else:
                    r = requests.post(test_site,headers =request_headers,proxies=proxies,timeout=(5, 10),verify=False,data=post_data)

            if method=="PUT":
                if proxies==None:
                    r = requests.put(test_site,headers=request_headers,verify=False,data='PUT_DATA'*100)
                else:
                    r = requests.put(test_site,headers =request_headers,proxies=proxies,timeout=(5, 10),verify=False,data='PUT_DATA'*100)

            if method=="DELETE":
                if proxies==None:
                    r = requests.delete(test_site,headers=request_headers,verify=False)
                else:
                    r = requests.delete(test_site,headers =request_headers,proxies=proxies,timeout=(5, 10),verify=False)

            if method=="OPTIONS":
                if proxies==None:
                    r = requests.options(test_site,headers=request_headers,verify=False)
                else:
                    r = requests.options(test_site,headers =request_headers,proxies=proxies,timeout=(5, 10),verify=False)

            if method=="HEAD":
                if proxies==None:
                    r = requests.head(test_site,headers=request_headers,verify=False)
                else:
                    r = requests.head(test_site,headers =request_headers,proxies=proxies,timeout=(5, 10),verify=False)

            if 'content-length' in str(r.headers).lower():
                content_length_found=True
                size=int(eval(str(r.headers).lower())['content-length'])
                sizes.append(size)
            else:
                content_length_found=False
                size=len(r.content)
                sizes.append(size)
            stop_time=time.time()
            dif=stop_time-start_time
            times.append(dif)
            # if content_length_found==True:
            #     print 'No:'+str(x+1)+' Tested_URL:'+test_site+' Download_Time:'+str(dif)+'[sec] Download_Size_(Based on: Content-Length):'+str(size/1024.0)+'[kb]'
            # if content_length_found==False:
            #     print 'No:'+str(x+1)+' Tested_URL:'+test_site+' Download_Time:'+str(dif)+'[sec] Download_Size_(Based on: Received data):'+str(size/1024.0)+'[kb]  '
            time.sleep(delay)
        stop_total_time=time.time()
        INSERT_TO_LOG(exceptions_file,str({'HTTP_GET_SITE_Exception':None}))
        if loops_number>1:
            return {'Average_Download_Time_[msec]':sum(times)/len(times)*1000,
                    'Total_Download_Size_[kb]':sum(sizes)/1024.0,
                    'Traffic_Execution_Time_[sec]':stop_total_time-start_total_time,
                    'Is_Content_Length_Size':str(content_length_found),
                    'Content':r.content,
                    'Final_URL':r.url}
        if loops_number==1:
            return {'Average_Download_Time_[msec]':sum(times)/len(times)*1000,
                    'Total_Download_Size_[kb]':sum(sizes)/1024.0,
                    'Traffic_Execution_Time_[sec]':stop_total_time-start_total_time,
                    'Is_Content_Length_Size':str(content_length_found),
                    'Response_Headers':r.headers,
                    'Status_Code':r.status_code,
                    'Content':r.content,
                    'Final_URL':r.url}
    except Exception,e:
        INSERT_TO_LOG(exceptions_file,str({'HTTP_GET_SITE_Exception':str(e)}))
        return {'HTTP_GET_SITE_Exception':str(e)}




    # Get Version #
    get_version=MC_APIS(ip=API_SERVER_DOMAIN,port=API_SERVER_PORT,user=AUTH_USER,password=AUTH_PASS,https=IS_HTTPS_SETUP,method='GET',url_path='shunra/api/configuration/version',
                         additional_headers={'Accept':'application/json'}, api_name='GET_VERSION')
    get_version_response=get_version.RUN_REQUEST()
    PRINT_DICT(get_version_response)
    SPEC_PRINT(['Check response content with JSON viewer'])

def CLOSE_ALL_BROWSERS():
    browsers=["chrome.exe","firefox.exe","iexplorer.exe","opera.exe"]
    for b in browsers:
        try:
            os.system("taskkill /f /im "+b)
        except:
            pass

def SIMPLE_HTTP_GET(url):
    a = urllib2.urlopen(url)
    return {'Status_Code':a.getcode(),'URL':url}

mode=CHOOSE_OPTION_FROM_LIST_1(['Prepare "GOOD URLs"','Record LR Script','Modify_LR_Script', 'Start_HTTP_Server'],"Choose mode:")

if mode=='Start_HTTP_Server':
    my_ip = urlopen('http://ip.42.pl/raw').read()
    self_port = int(raw_input('Please enter listening port:'))
    server_files_path=raw_input('Please enter full path to static HTML directory (/home/ubuntu/Ynet): ')
    web_dir = os.path.join(os.path.dirname(__file__), server_files_path)
    os.chdir(web_dir)
    index = open(os.path.join(web_dir,'index.html'), 'w')
    index.write('<html>')
    index.write('<body>')
    counter = 0
    for f in os.listdir(web_dir):
        counter+=1
        if self_port != 80:
            index.write('<a href=' + '"http://' + my_ip + ':' + str(self_port) + '/' + f + '"' + '>' + str(counter) + ') - ' + f + '</a>')
        else:
            index.write('<a href=' + '"http://' + my_ip + '/' + f + '"' + '>' + str(counter) + ') - ' + f + '</a>')
        index.write('<br>')
    index.write('</body>')
    index.write('</html>')
    index.close()
    PORT = self_port
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    print "Serving at port", my_ip, PORT
    httpd.serve_forever()

if mode=='Modify_LR_Script':
    print '1) All NV APIs will be removed'
    print '2) lr_think_time(1) will be added after each HTP request'
    print '3) Removes all "web_concurrent"'
    print '4) Remove all recorded "lr_think_time"'
    script_path=raw_input('Please paste LR full path here:')
    script_sections=open(script_path,'r').read().split('\n\n')
    filter_list = ['web_concurrent', '127.0.0.1:8182', 'lr_think_time']
    filtered_sections=[]
    for s in script_sections:
        to_add = True
        for item in filter_list:
            if item in s:
                to_add=False

                print '-'*50
                print item + ' was detected'
                print ''
                print s
                print ''
                print 'Will be deleted!!!'
                print '-'*50
                break
        if to_add==True:
            filtered_sections.append(s)
    script_name=open(script_path,'w')
    for s in filtered_sections:
        script_name.write('\n\n')
        script_name.write(s)
        if 'http' in s:
            script_name.write('\n\t\tlr_think_time(1);')
    script_name.close()
    input('Type ENTER to EXIT!!!')

if mode=='Prepare "GOOD URLs"':
    DELETE_LOG_CONTENT('Good_urls.txt')
    url=raw_input('Enter your static test site "IP:Port" (80 by default):')
    response=HTTP_GET_SITE('http://'+url+'/index.html',1)
    html=response['Content']
    final_url=response['Final_URL']
    links=[final_url]
    soup = BeautifulSoup.BeautifulSoup(html)
    for line in soup.findAll('a'):
        links.append(line.get('href'))
    links=list(set(links))
    http_links=[]
    for u in links:
        try:
            if 'http://' in str(u):
                http_links.append(u)
        except:
            pass
    number_of_requests = int(raw_input('Enter the number of "GOOD URLs" to send ' + '(0 - ' + str(len(http_links)) + '):'))
    # Filter out only http request that returned without Warnings (No ssl), proper status code #
    TEST_LINKS=[]
    start_index=0
    while len(TEST_LINKS)<number_of_requests:
        try:
            print 'Current number of "GOOD URLs" is: ',len(TEST_LINKS)
            result=SIMPLE_HTTP_GET(http_links[start_index])
            print result
            if result['Status_Code']==200:
                TEST_LINKS.append(http_links[start_index])
        except Exception,e:
            print e
        start_index+=1
    if len(TEST_LINKS)==0:
        print '*** ERRROR There is no links to send after filtering out "GOOD URLs"!!! ***'
        raw_input('Type ENTER to EXIT')
    print '='*80
    print 'The number of "GOOD URLs" is: '+str(len(TEST_LINKS))
    print '='*80
    for T in TEST_LINKS:
        INSERT_TO_LOG('Good_urls.txt',T)
    input('Type ENTER to EXIT!!!')


if mode=='Record LR Script':
    CLOSE_ALL_BROWSERS()
    # Get URLS from file #
    urls_to_record=open('Good_urls.txt','r').readlines()
    # Start LR (Special API for LR VUgen) #
    start_nv=MC_APIS(ip='127.0.0.1',port='8182',user='NVintegrator',password='Shunra_pwd1',https=False,method='POST',url_path='shunra/api/emulation/packetCaptureOnly',
                         additional_headers={'Accept':'application/json'}, api_name='Start_NV', request_payload={"testName" : "Record_LR_Script_While_NV_Emulation_"+str(time.time()).split('.')[0]})
    start_response=start_nv.RUN_REQUEST()
    PRINT_DICT(start_response)
    test_token=start_response['Content_As_Dict']['identifier']
    # Start traffic #
    SENT_URLS=[]
    for item in urls_to_record:
        result=SIMPLE_HTTP_GET(item)
        print result
        time.sleep(1)
        SENT_URLS.append(item)
    # Stop API#
    time.sleep(2)
    stop_put_data = '''{"testTokens": ["token"]}'''.replace('token', test_token)
    stop_obj_1 = MC_APIS(ip='127.0.0.1', port='8182', user='NVintegrator',password='Shunra_pwd1',https=False, method='PUT', url_path='shunra/api/emulation/stop',
                         additional_headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
                         request_payload=stop_put_data, body_type='STRING', api_name='STOP_API')
    stop_resp = stop_obj_1.RUN_REQUEST()
    PRINT_DICT(stop_resp)
    # Print traffic summary #
    print '\r\n'
    print '-'*100
    print 'Total number of sent HTTP requests is: '+str(len(SENT_URLS))
    for item in SENT_URLS:
        print SENT_URLS.index(item)+1,' - ',item.strip()
    input('Type ENTER to EXIT!!!')
