import requests,time

test_site='http://'+raw_input('Enter your site, without http://:')
loop_number=int(raw_input('Enter loop number: '))
p_ip=raw_input('Enter Proxy IP: ')
p_port=raw_input('Enter Proxy PORT: ')
proxies = {"http": p_ip+':'+p_port}


def HTTP_GET_SITE(site_url,loops_number):
    times=[]
    sizes=[]
    for x in range(0,loops_number):
        size=None
        test_site=site_url
        start_time=time.time()
        r = requests.get(test_site,proxies=proxies)
        if 'content-length' in str(r.headers).lower():
            size=int(eval(str(r.headers).lower())['content-length'])
            sizes.append(size)
        else:
            sizes.append(size)
        stop_time=time.time()
        dif=stop_time-start_time
        times.append(dif)
        if size!=None:
            print 'No:'+str(x+1)+' Tested_URL:'+test_site+' Execution_Time:'+str(dif)+'[sec] Download_Size:'+str(size/1024)+'[kb]'+' Final_URL:'+r.url
        else:
            print 'No:'+str(x+1)+' Tested_URL:'+test_site+' Execution_Time:'+str(dif)+'[sec] Download_Size:'+'N/A'+' Final_URL:'+r.url
    if None not in sizes:
        return {'Average_download_time_[msec]':sum(times)/len(times)*1000,'Total_Download_Size_[kb]':sum(sizes)/1024}
    else:
        return {'Average_download_time_[msec]':sum(times)/len(times)*1000,'Total_Download_Size_[kb]':'N/A'}

r=HTTP_GET_SITE(test_site,loop_number)
print ''
print '------------'
for d in r.iteritems():
    print d


