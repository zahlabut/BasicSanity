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
            tcp_stream=int(item['_source']['layers']['tcp']['tcp.stream'])
            tcp_source_port=item['_source']['layers']['tcp']['tcp.srcport']
            tcp_dst_port=item['_source']['layers']['tcp']['tcp.dstport']
            tcp_seq=item['_source']['layers']['tcp']['tcp.seq']
            tcp_ack=item['_source']['layers']['tcp']['tcp.ack']
            ip_src=item['_source']['layers']['ip']['ip.src']
            ip_dst=item['_source']['layers']['ip']['ip.dst']
            time_epoch=item['_source']['layers']['frame']['frame.time_epoch']

            tcp_reassembled_in=None
            if 'tcp.reassembled_in' in item['_source']['layers']['tcp']:
                tcp_reassembled_in = item['_source']['layers']['tcp']['tcp.reassembled_in']

            tcp_analysis=None
            if 'tcp.analysis' in item['_source']['layers']['tcp']:
                tcp_analysis = item['_source']['layers']['tcp']['tcp.analysis']
            http_data=None
            len_http_data=0
            tcp_len=int(item['_source']['layers']['tcp']['tcp.len'])
            tcp_hd_len = int(item['_source']['layers']['tcp']['tcp.hdr_len'])
            if 'http' in item['_source']['layers']:
                http_data=item['_source']['layers']['http']
                len_http_data=len(str(item['_source']['layers']['http']))
            dic={'Source_IP':ip_src,'Destination_IP':ip_dst,'Source_Port':tcp_source_port,'Destination_Port':tcp_dst_port,
                 'TCP_Seq':tcp_seq,'TCP_Ack':tcp_ack,'Time_Epoch':time_epoch,'TCP_Stream':tcp_stream, 'HTTP_Data':http_data,
                 'TCP_Len':tcp_len,'TCP_Header_Len':tcp_hd_len,'HTTP_Data_Len':len_http_data,'TCP_Analysis':tcp_analysis,'TCP_Reassembled_In':tcp_reassembled_in}
            #print dic
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

### Get only streams where you see your HTTP traffic ###
relevant_streams_contains = raw_input('Enter your test URL (http://52.20.143.142/index.html):')
relevant_streams={}
for k in streams.keys():
    if relevant_streams_contains in str(streams[k]):
        relevant_streams[k]=streams[k]

relevant_streams=sorted(relevant_streams.keys())
durations={}
all_durations=[]
for stream in relevant_streams:
    duration=float(streams[stream][-1]['Time_Epoch'])-float(streams[stream][0]['Time_Epoch'])
    durations[stream]=duration
    all_durations.append(duration)






### Calciulate trhroughput for all relevant streams ###
all_troughputs={}
for dur in durations.keys():
    src_ip=streams[dur][0]['Source_IP']
    dst_ip=streams[dur][0]['Destination_IP']
    upload_size=0
    download_size=0
    ignore_packets=['tcp.analysis.out_of_order','tcp.analysis.duplicate_ack','tcp.analysis.retransmission','tcp.analysis.keep_alive']
    for packet in streams[dur]:
        #print packet['TCP_Header_Len'],packet['TCP_Len']
        to_filter_out=[]
        if packet['Source_IP']==src_ip:
            for item in ignore_packets:
                if item in str(packet['TCP_Analysis']):
                    to_filter_out.append(True)
                    print 'Client to server --> '+item
            if True not in to_filter_out:
                upload_size+=packet['TCP_Len']
                upload_size+=packet['TCP_Header_Len']
        if packet['Source_IP']==dst_ip:
            for item in ignore_packets:
                if item in str(packet['TCP_Analysis']):
                    to_filter_out.append(True)
                    print 'Server to client --> '+item
            if True not in to_filter_out:
                download_size+=packet['TCP_Len']
                download_size+=packet['TCP_Header_Len']

    #print (upload_size/1024.0)/durations[dur],(download_size/1024.0)/durations[dur]
    #all_troughputs[dur]=((upload_size/1024.0)/durations[dur],(download_size/1024.0)/durations[dur])
    all_troughputs[dur]=((upload_size/1024.0),(download_size/1024.0)) #HTTP



SPEC_PRINT(['Stream_Number:Duration']+[str(item) for item in durations.iteritems()])
SPEC_PRINT(['Code ignores: retransmissions, duplictaes...']+['Stream_Number:Througput_Upload_Download']+[str(item) for item in all_troughputs.iteritems()])