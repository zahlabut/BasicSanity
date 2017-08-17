##########################
PORT_NUMBER=80
IS_HTTPS_SERVER=False
##########################

import time,ssl,socket,random
from urllib2 import urlopen
import urlparse
from urlparse import urlparse
import BaseHTTPServer, SimpleHTTPServer

AWS_INT_IP=socket.gethostbyname(socket.gethostname())
AWS_EXT_IP=urlopen('http://ip.42.pl/raw').read()
HOST_NAME=AWS_EXT_IP


#class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        """Respond to a GET request."""
        print s.path
        url_values={}
        parsed_url=urlparse(s.path)
        url_values['Requested_Server_Object']=parsed_url.path
        url_values['URL_Query']=parsed_url.query
        url_values['URL_Parameters']={'body_size': '1', 'server_delay': '0'}
        if len(url_values['URL_Query'])>0:
            params=parsed_url.query.split('?')
            params_as_dic=url_values['URL_Parameters']
            for p in params:
                k=p.split('=')[0]
                v=p.split('=')[1]
                params_as_dic[k]=v
            url_values['URL_Parameters']=params_as_dic
        print '-->',url_values
        # Generate data
        start_data=time.time()
        data=''
        data+="<html><head><title>Python Server - for testing 'Sever Delay' feature!!! </title></head>"
        mult_character='#'*(int(url_values['URL_Parameters']['body_size']))
        data+="<body><p>"+mult_character+"</p>"
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        data+="<p>You accessed path: %s</p>" % s.path
        data+="</body></html>"
        stop_data=time.time()
        data_creation_took=stop_data-start_data
        content_length=len(data)
        print '--> Created data size is: '+str(content_length/1024.0)+'[kb]'
        if 'max_delay' in url_values['URL_Parameters'].keys():
            delay_time=float(random.choice(xrange(0, int(url_values['URL_Parameters']['max_delay']), 1)))/1000-data_creation_took
        else:
            delay_time=float(url_values['URL_Parameters']['server_delay'])/1000-data_creation_took
        if delay_time<0:
            pass
        else:
            time.sleep(delay_time)
        # Delay Response
        s.protocol_version='HTTP/1.1'
        s.send_response(200)
        s.send_header("Connection", "keep-alive")
        s.send_header("Content-Type", "text/html")
        s.send_header("Content-Length", content_length)
        s.send_header("Generating-Data",data_creation_took)
        s.send_header("Sleep-Time-In-Sec",delay_time)
        s.end_headers()
        s.wfile.write(data)


if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    #httpd = server_class(("", PORT_NUMBER), MyHandler)

    httpd = BaseHTTPServer.HTTPServer(("", PORT_NUMBER), MyHandler)
    # taken from http://www.piware.de/2011/01/creating-an-https-server-in-python/
    # generate server.xml with the following command:
    #    openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
    # run as follows:
    #    python simple-https-server.py
    # then in your browser, visit:
    #    https://localhost:4443
    if IS_HTTPS_SERVER==True:
        print "Your server configured as HTTPS!!!"
        httpd.socket = ssl.wrap_socket (httpd.socket, certfile='./server.pem', server_side=True)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)




# if mode=='Start_HTTP_Server':
#     my_ip = urlopen('http://ip.42.pl/raw').read()
#     self_port = int(raw_input('Please enter listening port:'))
#     server_files_path=raw_input('Please enter full path to static HTML directory (/home/ubuntu/Ynet): ')
#     web_dir = os.path.join(os.path.dirname(__file__), server_files_path)
#     os.chdir(web_dir)
#     index = open(os.path.join(web_dir,'index.html'), 'w')
#     index.write('<html>')
#     index.write('<body>')
#     counter = 0
#     for f in os.listdir(web_dir):
#         counter+=1
#         if self_port != 80:
#             index.write('<a href=' + '"http://' + my_ip + ':' + str(self_port) + '/' + f + '"' + '>' + str(counter) + ') - ' + f + '</a>')
#         else:
#             index.write('<a href=' + '"http://' + my_ip + '/' + f + '"' + '>' + str(counter) + ') - ' + f + '</a>')
#         index.write('<br>')
#     index.write('</body>')
#     index.write('</html>')
#     index.close()
#     PORT = self_port
#     Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
#     httpd = SocketServer.TCPServer(("", PORT), Handler)
#     print "Serving at port", my_ip, PORT
#     httpd.serve_forever()







