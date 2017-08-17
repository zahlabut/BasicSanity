import socket,time

def HTTP_GET_SOCKET(host,port,loop_number,delay=1):
    try:
        total_sent=0
        total_received=0
        send_data=''
        send_data+='GET / HTTP/1.1\r\n'
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
            s_ip_port=s.getpeername()
            c_ip_port=s.getsockname()
            s.close()
            total_size+=len(send_data)+len(response)
            total_sent+=round(len(send_data)/1024.0,2)
            total_received+=round(len(response)/1024.0,2)
            print str(c_ip_port)+' --> '+str(s_ip_port)+str(round(len(send_data)/1024.0,2))+'[kb] Response_size:'+str(round(len(response)/1024.0,2))+'[kb]' +' Total sent:'+str(total_sent)+'[kb]' +' Total received:'+str(total_received)+'[kb]'+' Loop No:'+str(x+1)
            time.sleep(delay)

        return {'Total_TCP_size_[kb]':total_size/1024.0}
    except Exception, e:
        return str(e)



host=raw_input('Please enter HOST, "ynet.co.il" for example: ')
delay=input('Enter delay between HTTP GETs:')
loops=input('Enter Loop Number:')
print HTTP_GET_SOCKET(host,80,loops,delay)