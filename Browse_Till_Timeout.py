import time, platform,sys,os
from selenium import webdriver

def OPEN_WEB_SITE_SELENIUM(url,proxy=None,timeout=5*60,delay=0):
    try:
        func_start_time=time.time()
        current_url='N/A'
        start_time=time.time()
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

        driver.delete_all_cookies()
        driver.set_page_load_timeout(timeout)
        start_time=time.time()
        driver.get(url)
        stop_time=time.time()
        current_url=driver.current_url
        time.sleep(delay)
    except Exception, e:
        print e
    finally:
        try:
            driver.quit()
        except Exception, e:
            print e
        stop_time=time.time()
        return {'Page_Load_Time[sec]':stop_time-func_start_time,'Final_URL':current_url}



url=raw_input('Please enter your test URL (Full URL): ')
timeout=int(raw_input('Please ENTER timeout in seconds (minimum 30): '))
proxy=raw_input('Enter proxy as "IP:Port" or "No" if no proxy is needed: ')

proxy_mode=None
if ':' in proxy:
    proxy_mode=True
    selenium_proxy=proxy
if "no" in proxy.lower():
    proxy_mode=False

if proxy_mode==None:
    print '*** ACHTUNG !!!! ***'
    print 'Something went wrong while entering proxy, your input was: '+proxy+' please rerun!!!'



start_time=time.time()
loop_number=0
all_results=[]
while(time.time() < start_time+timeout-25):
    loop_number+=1
    if proxy_mode==False:
        result=OPEN_WEB_SITE_SELENIUM(url,proxy=None,timeout=25)
    if proxy_mode==True:
        result=OPEN_WEB_SITE_SELENIUM(url,proxy=selenium_proxy,timeout=25)
    print result
    all_results.append(result)
end_time=time.time()

print '\r\n'*5
print '='*80
print "Browsing time was ~"+str(end_time-start_time)
print 'Your test site was requested for: '+str(loop_number)+' times!!!'
print 'Statistics:'
for item in all_results:
    print item
print '='*80
raw_input('Type ENTER to Exit!')

