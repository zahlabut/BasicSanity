import time
import timeit
import requests,subprocess,platform
import dns.resolver
import socket
import platform
from selenium import webdriver
from Mi_Functions import *
from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from Params import *
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

def OPEN_WEB_SITE_SELENIUM(url,proxy=None,timeout=5*60,delay=0):
    try:
        func_start_time=time.time()
        current_url='N/A'
        screenshoot_name='Empty_Screenshot.jpg'
        start_time=time.time()
        INSERT_TO_LOG(screenshoot_name,'')
        print '... Start browsing to: '+url
        if proxy!=None:
            PROXY = proxy
            webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
                "httpProxy":PROXY,
                "ftpProxy":PROXY,
                "sslProxy":PROXY,
                "noProxy":None,
                "proxyType":"MANUAL",
                "class":"org.openqa.selenium.Proxy",
                "autodetect":False
            }

            webdriver.DesiredCapabilities.CHROME['proxy'] = {
                "httpProxy":PROXY,
                "ftpProxy":PROXY,
                "sslProxy":PROXY,
                "noProxy":None,
                "proxyType":"MANUAL",
                "class":"org.openqa.selenium.Proxy",
                "autodetect":False
            }

        if 'windows' in platform.system().lower():
            driver = webdriver.Chrome()

        if 'linux' in platform.system().lower():
            display = Display(visible=0, size=(800, 600))
            print 'Start display result: ', display.start()
            driver = webdriver.Firefox()


            #profile=webdriver.FirefoxProfile
            #driver=webdriver.PhantomJS()



        # if 'chromedriver.exe' in os.listdir('.') and 'linux' not in platform.system().lower():
        #     print 'Chrome webdriver is used'
        #     driver = webdriver.Chrome(os.path.abspath('chromedriver.exe'))

        # if 'windows' in platform.system().lower():
        #     driver=webdriver.Firefox()


        driver.delete_all_cookies()
        driver.set_page_load_timeout(timeout)
        start_time=time.time()
        driver.get(url)
        current_url=driver.current_url
        stop_time=time.time()
        if SAVE_SCREENSHOT==True:
            print 'Save Screensot is True'
            screenshoot_name=str(time.time()).split('.')[0]+'_'+url.split('//')[-1].replace('.','_').replace('/','_')+'.jpg'
            driver.get_screenshot_as_file(screenshoot_name)
        if SAVE_SCREENSHOT==False:
            screenshoot_name=None
        time.sleep(delay)
        INSERT_TO_LOG(exceptions_file,str({'OPEN_WEB_SITE_SELENIUM_Exception':None}))
    except Exception, e:
        print e
        INSERT_TO_LOG(exceptions_file,str({'OPEN_WEB_SITE_SELENIUM_Exception':str(e)}))
    finally:
        try:
            driver.quit()
        except Exception, e:
            INSERT_TO_LOG(exceptions_file,str({'OPEN_WEB_SITE_SELENIUM_Exception':str(e)}))
            print e
        stop_time=time.time()
        if screenshoot_name in os.listdir('.'):
            return {'Page_Load_Time[sec]':stop_time-start_time,'Final_URL':current_url,'ScreenshootName':screenshoot_name}
        else:
            return {'Page_Load_Time[sec]':stop_time-func_start_time,'Final_URL':current_url,'ScreenshootName':'Empty_Screenshot.jpg'}

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
            if content_length_found==True:
                print 'No:'+str(x+1)+' Tested_URL:'+test_site+' Download_Time:'+str(dif)+'[sec] Download_Size_(Based on: Content-Length):'+str(size/1024.0)+'[kb]'
            if content_length_found==False:
                print 'No:'+str(x+1)+' Tested_URL:'+test_site+' Download_Time:'+str(dif)+'[sec] Download_Size_(Based on: Received data):'+str(size/1024.0)+'[kb]  '
            time.sleep(delay)
        stop_total_time=time.time()
        INSERT_TO_LOG(exceptions_file,str({'HTTP_GET_SITE_Exception':None}))
        if loops_number>1:
            return {'Function_Name':'HTTP_GET_SITE','Average_Download_Time_[msec]':sum(times)/len(times)*1000,'Total_Download_Size_[kb]':sum(sizes)/1024.0,
                    'Traffic_Execution_Time_[sec]':stop_total_time-start_total_time,'Is_Content_Length_Size':str(content_length_found)}
        if loops_number==1:
            return {'Function_Name':'HTTP_GET_SITE','Average_Download_Time_[msec]':sum(times)/len(times)*1000,'Total_Download_Size_[kb]':sum(sizes)/1024.0,
                    'Traffic_Execution_Time_[sec]':stop_total_time-start_total_time,'Is_Content_Length_Size':str(content_length_found),'Response_Headers':r.headers,'Status_Code':r.status_code}
    except Exception,e:
        INSERT_TO_LOG(exceptions_file,str({'HTTP_GET_SITE_Exception':str(e)}))
        return {'Function_Name':'HTTP_GET_SITE','HTTP_GET_SITE_Exception':str(e)}

def SEND_HTTP_GETS_ON_SAME_TCP_STREAM(url,number_of_gets, proxy=None):
    result_dict={}
    #try:

    if proxy==None:
        s = requests.Session()
        for x in range(0, number_of_gets):
            url=url+'?http_get_number='+str(x+1)
            start=time.time()
            #s.get(url)
            r = s.get(url)
            print url,r.status_code
            stop=time.time()
            result_dict[url]={'StatusCode':r.status_code,'Execution_Time':stop-start,'ResponseContentSize':len(r.content)}
            url=url.replace('?http_get_number='+str(x+1),'')

    if proxy!=None:
        s = requests.Session()
        for x in range(0,number_of_gets):
            url=url+'?http_get_number='+str(x+1)
            start=time.time()
            r=s.get(url,proxies=proxy,verify=False)
            print url,r.status_code
            stop=time.time()
            result_dict[url]={'StatusCode':r.status_code,'Execution_Time':stop-start,'ResponseContentSize':len(r.content)}
            url=url.replace('?http_get_number='+str(x+1),'')
    return result_dict
    #except Exception,e:
    #    return {'Function_Name':'SEND_HTTP_GETS_ON_SAME_TCP_STREAM','SEND_HTTP_GETS_ON_SAME_TCP_STREAM_Exception':str(e)}




# def SEND_HTTP_GETS_ON_SAME_TCP_STREAM(url):
#     s = requests.Session()
#     s.get(url)
#     r = s.get(url)
#     print(r.text)
#     r = s.get(url)
#     print(r.text)
#     r = s.get(url)
#     print(r.text)


# print SEND_HTTP_GETS_ON_SAME_TCP_STREAM('http://52.200.75.97/zababun.html?server_delay=100?body_size=66',10)



#print SEND_HTTP_GETS_ON_SAME_TCP_STREAM('http://ynet.co.il/lkjlkjljlk',3)


def DNS_QUERY(site,loop_number):
    try:
        myResolver = dns.resolver.Resolver()
        response=[]
        start_time=time.time()
        for x in range(0,loop_number):
            #time.sleep(2)
            try:
                myAnswers = myResolver.query(site, "A")
                response_to_print=''
                for rdata in myAnswers:
                    response.append(rdata)
                    response_to_print+=' '+str(rdata)
                print 'No:'+str(x+1)+' '+'DNS_Response:'+response_to_print
            except Exception, e:
                print str(e)
                response.append(None)
                print 'No:'+str(x+1)+' '+'DNS_Response:'+str(None)
        stop_time=time.time()
        INSERT_TO_LOG(exceptions_file,str({'DNS_QUERY_Exception':None}))
        return {'Failures':response.count('None'),'Sucess':loop_number-response.count('None'),'Average_Response_Time':(stop_time-start_time)/loop_number}
    except Exception, e:
        INSERT_TO_LOG(exceptions_file,str({'DNS_QUERY_Exception':str(e)}))
        return {'DNS_QUERY_Exception':str(e)}

def HTTP_GET_SOCKET(host,port,loop_number,request_trough_proxy=False,source_port=None, path_to_request=''):
    try:
        if request_trough_proxy==False:
            send_data=''
            send_data+='GET /'+path_to_request+' HTTP/1.1\r\n'
            send_data+='Host: www.'+host+'\r\n'
            send_data+='Connection: close\r\n'
            send_data+='Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n'
            send_data+='Upgrade-Insecure-Requests: 1\r\n'
            send_data+='User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36\r\n'
            #send_data+='Accept-Encoding: gzip, deflate, sdch\r\n'
            send_data+='Accept-Language: en-US,en;q=0.8\r\n'
            send_data+='\r\n'
            send_data+='\r\n'
            #print send_data

        if request_trough_proxy!=False:
            send_data=''
            send_data+='GET http://cnn.com/ HTTP/1.1\r\n'
            send_data+='Host: www.cnn.com\r\n'
            send_data+='Proxy-Connection: close\r\n'
            send_data+='Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n'
            send_data+='Upgrade-Insecure-Requests: 1\r\n'
            send_data+='User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36\r\n'
            #send_data+='Accept-Encoding: gzip, deflate, sdch\r\n'
            send_data+='Accept-Language: en-US,en;q=0.8\r\n'
            send_data+='\r\n'
            send_data+='\r\n'
            #print send_data

        total_size=0
        for x in range(0,loop_number):
            s = socket.socket()

            if source_port!=None:
                s.bind(('', source_port))


            start_connect=time.time()*1000
            s.connect((host,port))
            stop_connect=time.time()*1000
            start_send_data=time.time()*1000
            s.send(send_data)
            stop_send_data=time.time()*1000
            #response=s.recv(10000)
            start_wait_response=time.time()*1000
            response=''
            received_bytes_times=[]
            while True:
                data = s.recv(1)
                received_bytes_times.append(time.time()*1000)
                #print data
                if not data: break
                response+=data
            stop_wait_response=received_bytes_times[0]
            #print response
            s.close()
            total_size+=len(send_data)+len(response)
            print 'No:'+str(x+1)+' Host:'+host+' Request_size:'+str(len(send_data)/1024.0)+'[kb] Response_size:'+str(len(response)/1024.0)+'[kb]'

        response_data=response.split('\r\n\r\n')
        response_header_size=len(response_data[0])
        response_data_size=len(response_data[1])

        INSERT_TO_LOG(exceptions_file,str({'HTTP_GET_SOCKET_Exception':None}))
        return {'Total_TCP_size_[kb]':total_size/1024.0,
                'Connection_Establish_Time':stop_connect-start_connect,
                'Send_Data_Time':stop_send_data-start_send_data,
                'Sent_Data_Size':len(send_data),
                'Response_Headers_Size':response_header_size,
                'Response_Data_Size':response_data_size,
                'Response_Wait_Time':stop_wait_response-start_wait_response,
                'Response_Transmission_Time':received_bytes_times[-1]-received_bytes_times[0]}
    except Exception, e:
        INSERT_TO_LOG(exceptions_file,str({'HTTP_GET_SOCKET_Exception':str(e)}))
        return {'HTTP_GET_SOCKET_Exception':str(e)}

def SSH_QUERY_SOCKET(ip,port,msg,loop_number):
    total_sent_size=0
    for x in range(0,loop_number):
        time.sleep(1)
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (ip,port)
        total_sent_size+=len(msg)
        try:
            # Send data
            #print >>sys.stderr, 'sending "%s"' % msg
            sent = sock.sendto(msg, server_address)
            # Receive response
            #print >>sys.stderr, 'waiting to receive'
            data, server = sock.recvfrom(4096)
            #print >>sys.stderr, 'received "%s"' % data
        except Exception,e:
            print str(e)
            sock.close()
    return {"Total_Sent_Data[kb]":total_sent_size/1024.0}

def PING_HOST(host,loop_number,delay=1):
    try:
        start_time=time.time()
        times=[]
        for x in range(0,loop_number):
            time.sleep(delay)
            if 'windows' in platform.system().lower():
                ping = subprocess.Popen(["ping", "-n", "1",host],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
            if 'linux' in platform.system().lower():
                print '*** -U will be used, means you will see the sum of both directions in time field!!! ***'
                ping = subprocess.Popen(["ping","-U", "-c", "1",host],stdout = subprocess.PIPE,stderr = subprocess.PIPE)
            out, error = ping.communicate()
            out = out.strip()
            error = error.strip()
            print '-'*100
            print '\r\nNo:'+str(x+1)+' '+'PING_Response:\r\n'+str(out)#[0:20])+'...'+str(out[-20:-1])
            #print error
            Time=None
            if "timed out" in out.lower(): #Windows:
                times.append('timeout')
            if "100% packet loss" in out.lower(): #Linux
                times.append('timeout')
            else:
                for l in out.rsplit(','):
                    if 'Average' in l:#Windows
                        Time=l.split(' ')[-1].split('ms')[0]
                        print '-->',Time
                    if 'time=' in l.lower():
                        Time=l.split('=')[-1].split(' ms')[0]
                        print '-->',Time
            if Time!=None:
                times.append(float(Time))

        #Statistics
        total_time=0.0
        total_timeouts=0
        total_pass=0
        for item in times:
            if str(type(item))=="<type 'float'>":
                total_time+=item
                total_pass+=1
            else:
                total_timeouts+=1
        if list(set(times))!=['timeout']:
            average_time=total_time/total_pass
        else:
            average_time=None
        packets_lost=total_timeouts
        stop_time=time.time()
        INSERT_TO_LOG(exceptions_file,str({'PING_HOST_Exception':None}))
        return {'Function_Name':'PING_HOST','Average_Response_Time_[msec]':average_time,'Packet_Lost':packets_lost,'Execution_Time':stop_time-start_time}
    except Exception, e:
        INSERT_TO_LOG(exceptions_file,str({'PING_HOST_Exception':str(e)}))
        return {'Function_Name':'PING_HOST','PING_HOST_Exception':str(e)}

def HTTP_GET_SOCKET_TEST_RULES(host,port,accept_encoding,loop_number):
    try:
        send_data=''
        send_data+='GET / HTTP/1.1\r\n'
        send_data+='Host: www.'+host+'\r\n'
        send_data+='Connection: close\r\n'
        send_data+='Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n'
        send_data+='Upgrade-Insecure-Requests: 1\r\n'
        send_data+='User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36\r\n'
        send_data+='Accept-Encoding:'+accept_encoding+'\r\n'# gzip, deflate, sdch\r\n'
        send_data+='Accept-Language: en-US,en;q=0.8\r\n'
        send_data+='\r\n'
        send_data+='\r\n'
        #print send_data

        total_size=0
        for x in range(0,loop_number):
            s = socket.socket()
            s.connect((host,port))
            s.send(send_data)
            #response=s.recv(10000)
            response=''
            while True:
                data = s.recv(1)
                #print data
                if not data: break
                response+=data

            #print response
            s.close()
            total_size+=len(send_data)+len(response)
            print 'No:'+str(x+1)+' Host:'+host+' Request_size:'+str(len(send_data)/1024.0)+'[kb] Response_size:'+str(len(response)/1024.0)+'[kb]'
        INSERT_TO_LOG(exceptions_file,str({'HTTP_GET_SOCKET_TEST_RULES_Exception':None}))
        return {'Total_TCP_size_[kb]':total_size/1024.0}
    except Exception, e:
        INSERT_TO_LOG(exceptions_file,str({'HTTP_GET_SOCKET_TEST_RULES_Exception':str(e)}))
        return {'HTTP_GET_SOCKET_TEST_RULES_Exception':str(e)}

def OPEN_AND_CLOSE_TCP_SOCKET(domain, loop_number=1,server_port=80,delay=0):
    try:
        TCP_IP = socket.gethostbyname('www.'+domain)
        TCP_PORT = server_port
        BUFFER_SIZE = 1024
        connects=[]
        closes=[]
        sockets=[]
        for x in xrange(0,loop_number):
            #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s = socket.socket()
            start_connect=time.time()
            s.connect((TCP_IP, TCP_PORT))
            stop_connect=time.time()
            start_close=time.time()
            socket_info=s.getsockname()
            s.close()
            stop_close=time.time()
            connects.append(stop_connect-start_connect)
            closes.append(stop_close-start_close)
            sockets.append(socket_info)
            time.sleep(delay)
        return {'Function_Name':'OPEN_AND_CLOSE_TCP_SOCKET','Socket_Connect_Average_Time[msec]':sum(connects)/len(connects)*1000.0,
                'Socket_Close_Average_Time[msec]':sum(closes)/len(closes)*1000.0,'List_Of_Used_Sockets':sockets}
    except Exception,e:
        return {'Function_Name':'OPEN_AND_CLOSE_TCP_SOCKET','Exception':e}

def HLS_VLC(timeout=30, proxy=None):
    if 'linux' not in platform.system().lower():
        if proxy!=None:
            p = subprocess.Popen(["C:/Program Files (x86)/VideoLAN/VLC/vlc.exe","http://qthttp.apple.com.edgesuite.net/1010qwoeiuryfg/sl.m3u8","--http-proxy",HLS_PROXY])
        if proxy==None:
            p = subprocess.Popen(["C:/Program Files (x86)/VideoLAN/VLC/vlc.exe","http://qthttp.apple.com.edgesuite.net/1010qwoeiuryfg/sl.m3u8"])
    if 'linux' in platform.system().lower():
        if proxy==None:
            p = subprocess.Popen(["vlc-wrapper","http://qthttp.apple.com.edgesuite.net/1010qwoeiuryfg/sl.m3u8"])
        if proxy!=None:
            p = subprocess.Popen(["vlc-wrapper","http://qthttp.apple.com.edgesuite.net/1010qwoeiuryfg/sl.m3u8","--http-proxy",HLS_PROXY])
        #display = Display(visible=0, size=(800, 600))
    time.sleep(timeout)
    if p.poll() is None:
      p.kill()
      print 'Timed out'
    else:
      print p.communicate()
    # if 'linux' in platform.system().lower():
    #     display.stop()
    return {'HLS_Traffic_Execution_Time':timeout}



