import os, sys, json,socket
import os.path
my_path=os.path.abspath('.')
import numpy as np
import matplotlib.pyplot as plt

up_dir_path=os.path.abspath(os.path.join(my_path, os.pardir))
sys.path.append(up_dir_path)

from APIs import *
from TrafficTypes import *

### Convert file content to python directory ###
pcap_json_file=CHOOSE_OPTION_FROM_LIST_1([f for f in os.listdir('.') if f.endswith('.json')],'Choose your pcap JSON file')
json_data=open(pcap_json_file,'r').read().decode('utf-8','ignore')
data=json.loads(json_data)
print type(data)


### Get all TCP streams as dictionary where values are lists ###
streams={}
raw_data_list_of_dics=[]
for item in data:
    if 'tcp' in item['_source']['layers'] and 'ip' in item['_source']['layers']:
        if item['_source']['layers']['ip']['ip.version']=='4':
            tcp_stream=item['_source']['layers']['tcp']['tcp.stream']
            tcp_source_port=item['_source']['layers']['tcp']['tcp.srcport']
            tcp_dst_port=item['_source']['layers']['tcp']['tcp.dstport']
            tcp_seq=item['_source']['layers']['tcp']['tcp.seq']
            tcp_ack=item['_source']['layers']['tcp']['tcp.ack']
            ip_src=item['_source']['layers']['ip']['ip.src']
            ip_dst=item['_source']['layers']['ip']['ip.dst']
            time_epoch=item['_source']['layers']['frame']['frame.time_epoch']
            dic={'Source_IP':ip_src,'Destination_IP':ip_dst,'Source_Port':tcp_source_port,'Destination_Port':tcp_dst_port,
                 'TCP_Seq':tcp_seq,'TCP_Ack':tcp_ack,'Time_Epoch':time_epoch,'TCP_Stream':tcp_stream}
            if 'tcp.analysis' in item['_source']['layers']['tcp']:
                dic['TCP_Analysis']=item['_source']['layers']['tcp']['tcp.analysis']
                for k in item['_source']['layers']['tcp']['tcp.analysis']:
                    if 'rtt' in k:
                        dic[k]=item['_source']['layers']['tcp']['tcp.analysis'][k]
            if tcp_stream not in streams.keys():
                streams[tcp_stream]=[dic]
            else:
                streams[tcp_stream].append(dic)
    else:
        continue
    raw_data_list_of_dics.append(dic)

### Write all data (row data) to csv ###
save_csv=CHOOSE_OPTION_FROM_LIST_1(['Yes','No'],'Would you like to save all graph data into CSV file?')
if save_csv=='Yes':
    WRITE_DICTS_TO_CSV('Raw_Data.csv',raw_data_list_of_dics)

### ---------------------------------------Plot graphs -----------------------------------------------------------------------###
x1,x2,x3,x4,y1,y2,y3,y4=[],[],[],[],[],[],[],[]
ld1,ld2,ld3,ld4=[],[],[],[]



relevant_ports=raw_input('Enter your servers ports separated by coma (81,82,83...)')
relevant_ports=[str(p) for p in relevant_ports.split(',')]
print relevant_ports


ip_mode=CHOOSE_OPTION_FROM_LIST_1(['Use server IP','Use IP provided by user'],'Please choose your option:')
if ip_mode=='Use server IP':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    machine_ip=s.getsockname()[0]
    s.close()
    SPEC_PRINT(['This script will use your machine IP (only outgoing traffic) to plot latency graph','Your server IP is: '+machine_ip])
if ip_mode=='Use IP provided by user':
    machine_ip=raw_input('Please enter your test machine source IP (172.31.57.247):')
graph_names=['Initial_RTT','Ack_RTT','TCP_Handshake_Per_Stream','TCP_Duration_Per_Stream']

# Prepare data for tcp.analysis.initial_rtt and tcp.analysis.ack_rtt #
for d in raw_data_list_of_dics:
    if d['Source_IP']==machine_ip and 'tcp.analysis.initial_rtt' in d.keys() and (d['Destination_Port'] in relevant_ports or d['Source_Port'] in relevant_ports):
        x1.append(d['Time_Epoch'])
        y1.append(d['tcp.analysis.initial_rtt'])
        ld1.append(d)
    if d['Source_IP']==machine_ip and 'tcp.analysis.ack_rtt' in d.keys() and (d['Destination_Port'] in relevant_ports or d['Source_Port'] in relevant_ports):
        x2.append(d['Time_Epoch'])
        y2.append(d['tcp.analysis.ack_rtt'])
        ld2.append(d)

# Calculate TCP handshakee per stream, save to CSV file and add to plot graph #
csv_file_name='TCP_Handshake.csv'
for st in streams.keys():
    if streams[st][0]['Source_IP']==machine_ip and (streams[st][0]['Destination_Port'] in relevant_ports or streams[st][0]['Source_Port'] in relevant_ports) and len(streams[st])>=3:
        handshake_time=float(streams[st][2]['Time_Epoch'])-float(streams[st][0]['Time_Epoch'])
        x3.append(st)
        y3.append(handshake_time)
        ld3.append({'Stream_Number':st,'Handshake_Time':handshake_time})


# Calculate TCP session duration per stream and plot on graph #
for st in streams.keys():
    if streams[st][0]['Source_IP']==machine_ip and (streams[st][0]['Destination_Port'] in relevant_ports or streams[st][0]['Source_Port'] in relevant_ports):
        session_duration=float(streams[st][-1]['Time_Epoch'])-float(streams[st][0]['Time_Epoch'])
        x4.append(st)
        y4.append(session_duration)
        ld4.append({'Stream_Number': st, 'Session_Duration_Time': session_duration})





plt.figure(1)
plt.subplot(221)
plt.title(graph_names[0])
plt.xlabel('Time_Epoch')
plt.ylabel('tcp.analysis.initial_rtt')
plt.scatter(x1, y1)
if save_csv=='Yes':
    DELETE_LOG_CONTENT(graph_names[0]+'.csv')
    WRITE_DICTS_TO_CSV(graph_names[0]+'.csv',ld1)

plt.subplot(222)
plt.title(graph_names[1])
plt.xlabel('Time_Epoch')
plt.ylabel('tcp.analysis.ack_rtt')
plt.scatter(x2, y2)
if save_csv=='Yes':
    DELETE_LOG_CONTENT(graph_names[1]+'.csv')
    WRITE_DICTS_TO_CSV(graph_names[1]+'.csv',ld2)

plt.subplot(223)
plt.title(graph_names[2])
plt.xlabel('TCP_Stream_Number')
plt.ylabel('TCP_Handshake_Time')
plt.scatter(x3, y3)
if save_csv=='Yes':
    DELETE_LOG_CONTENT(graph_names[2]+'.csv')
    WRITE_DICTS_TO_CSV(graph_names[2]+'.csv',ld3)

plt.subplot(224)
plt.title(graph_names[3])
plt.xlabel('TCP_Stream_Number')
plt.ylabel('TCP_Duration_Time')
plt.scatter(x4, y4)
if save_csv=='Yes':
    DELETE_LOG_CONTENT(graph_names[3]+'.csv')
    WRITE_DICTS_TO_CSV(graph_names[3]+'.csv',ld4)

plt.show()


