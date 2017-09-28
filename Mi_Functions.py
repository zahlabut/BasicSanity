__author__ = 'Arkady'
import ConfigParser
from BeautifulSoup import BeautifulSoup
from fuzzywuzzy import fuzz
from time import gmtime, strftime
import json,shutil,os,time,csv
import csv,codecs,cStringIO,os,urllib2,sys,shutil,xlsxwriter,time,string #psycopg2
from collections import Counter
from string import Template
import re,random
from fuzzywuzzy import fuzz
#from BeautifulSoup import BeautifulSoup
import BeautifulSoup
from time import gmtime, strftime
csv.field_size_limit(999999999)
import pyscreenshot as ImageGrab
import string
import random
import zipfile
import ssl
import platform



import sys
from PIL import Image
import socket

def CONVERT_INI_TO_VARIABLES(ini_file_name):
    print ini_file_name
    try:
        config = ConfigParser.ConfigParser()
        config.read(ini_file_name)

        dictionary = {}
        for section in config.sections():
            dictionary[section] = {}
            for option in config.options(section):
                dictionary[section][option] = config.get(section, option)

        sections=config.sections()
        for section in sections:
            data=dictionary[section]
            globals().update(data)
    except Exception, e:
        print '*** CONVERT_INI_TO_VARIABLES!!! ***', e
        EXIT("**************** FATAL ERROR, CANNOT CONTINUE EXECUTION !!!   ******************")
        sys.exit(1)

def IS_JSON(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError, e:
        return False
    return True
def GET_PHYSICAL_INTERFACE_IP():
    return socket.gethostbyname(socket.gethostname())
def MERGE_IMAGES(images_list):
    images = map(Image.open, images_list)
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
      new_im.paste(im, (x_offset,0))
      x_offset += im.size[0]

    new_im.save('Merged.jpg')
    return 'Merged.jpg'
class MyOutput():
    def __init__(self, logfile):
        self.stdout = sys.stdout
        self.log = open(logfile, 'w')
    def write(self, text):
        self.stdout.write(text)
        self.log.write(text)
        self.log.flush()
    def close(self):
        self.stdout.close()
        self.log.close()
def DELETE_LOG_CONTENT(log_file_name):
    f = open(log_file_name, 'w')
    f.write('')


def UNZIP_ZIPPED_NV_REPORT(binary_content):
    DELETE_LOG_CONTENT('content.zip')
    INSERT_TO_LOG('content.zip',binary_content)
    zip = zipfile.ZipFile('content.zip')
    html=zip.read('EmbeddedReport.html')
    shutil.rmtree(os.path.abspath('content.zip'),ignore_errors=True)
    return html

def CLEANER():
    deleted_files=[]
    use_path=[os.path.abspath('.'),os.path.join(os.path.abspath('.'),'TempScripts'),os.path.join(os.path.abspath('.'),'ParsePcapJsonFile'),os.path.join(os.path.abspath('.'))]
    for path in use_path:
        lo_lagaat=['HLS_Links.csv','HTTPS_Sites_Top_100.csv','HLS_Links.csv','AlexaTopMilion.csv','ParamFiles','hpenv.cer','NV_Certigficate.cer','ThresholdKaro.txt']
        to_delete=['.jpg','.log','.cap','Test_Result','HARs_','.jpg','.html','.zip','.out','.txt','.har','test___'] +[fil for fil in os.listdir(path) if (fil.endswith('.csv') and fil not in lo_lagaat)]
        for fil in os.listdir(path):
            for k in to_delete:
                if k in fil:
                    try:
                        os.remove(os.path.join(path,fil))
                        deleted_files.append(fil)
                    except Exception,e:
                        shutil.rmtree(os.path.join(path,fil), ignore_errors=True)
                        if os.path.isdir(os.path.join(path,fil))==True and 'linux' in platform.system().lower():
                            os.system('sudo rm -rf '+os.path.join(path,fil))
    SPEC_PRINT(['Cleaner --> Completed'])
    return deleted_files

def SPEC_PRINT(string_list):
    len_list=[]
    for item in string_list:
        len_list.append(len('### '+item.strip()+' ###'))
    max_len=max(len_list)
    if max_len<150:
        print ''
        print"#"*max_len
        for item in string_list:
            print "### "+item.strip()+" "*(max_len-len("### "+item.strip())-4)+" ###"
        print"#"*max_len+'\n'
    else:
        print '\r\n'+'#'*120
        for item in string_list:
            print item
        print '#'*120


def GET_MY_PUBLIC_IP():
    if 'linux' in platform.system().lower():
        return urllib2.urlopen('http://enabledns.com/ip').read()
    else:
        ssl._create_default_https_context = ssl._create_unverified_context
        return urllib2.urlopen('http://enabledns.com/ip').read()

def GET_ALL_REQUEST_URLS_FROM_HAR(har_file, har_is_ziped=False):
    ret_dict={}
    ret_dict['Har_File_Name']=os.path.basename(har_file)
    if har_is_ziped==False:
        data=open(har_file,'r').read().decode('utf-8','ignore')
    if har_is_ziped==True:
        zip_ref = zipfile.ZipFile(har_file, 'r')
        zip_ref.extract('NV.har') #In case when file name will be changed by Sharon this line will fail :(
        data=open('NV.har','r').read().decode('utf-8','ignore')
    data = json.loads(data)
    entries=data['log']['entries']
    urls=[]
    for item in entries:
        urls.append(item['request']['url'])
    ret_dict['URLs']=urls
    ret_dict['Number_Of_URLs']=len(urls)
    return ret_dict



#print GET_ALL_REQUEST_URLS_FROM_HAR('Async_Har_CC0169F6-414B-4E21-86BE-386C9B8A171A.har', har_is_ziped=True)


def DELAY(wait_time):
    time.sleep(wait_time)


def PRINT_DICT(dic,limit=True):
    print '='*45+' PRINT_DICT '+'='*45
    last_line_len=len('='*45+' PRINT_DICT '+'='*45)
    if limit==True:
        for k in dic.keys():
            if len(str(dic[k]))<1000:
                print k+' --> '+str(dic[k])
            else:
                print k+' --> '+str(dic[k])[0:50].strip()+'...........'+str(dic[k])[-50:-1].strip()
    if limit==False:
        for k in dic.keys():
            print k+' --> '+str(dic[k])
    print '/'*last_line_len
def INSERT_TO_LOG(log_file, msg, time_flag=0):
    log_file = open(log_file, 'ab')
    if time_flag==0:
        string=msg
    if time_flag==1:
        string=time.strftime("%Y-%m-%d %H:%M:%S")+' '+msg
    log_file.write(string+'\n')
    log_file.close()
def PIL_SAVE_SCREENSHOT(dst_path,file_name):
    time.sleep(2)
    ImageGrab.grab_to_file(os.path.join(dst_path,file_name+'.png'))
    time.sleep(2)
def GET_LINKS_FROM_HTML(html_or_url,request_the_url=False):
    links=[]
    if request_the_url==False:
        soup = BeautifulSoup.BeautifulSoup(html_or_url)
        for line in soup.findAll('a'):
            links.append(line.get('href'))
        return links
    if request_the_url==True:
        response = urllib2.urlopen(html_or_url)
        html = response.read()
        soup = BeautifulSoup.BeautifulSoup(html)
        for line in soup.findAll('a'):
            links.append(line.get('href'))
        return links


def EXIT(string):
    stam=raw_input(string)
    sys.exit(1)
def CONTINUE (message=''):
    print message
    cont=raw_input('Continue? y/n  ')
    if (cont=='y'):
        print "Your choose is: '"+cont+"' continue execution!"
        print ''
    elif (cont=='n'):
        print "Your choose is: '"+cont+"' execution will be stopped!"
        sys.exit(1)
    else:
        print "No such option: '"+cont+"'"
        CONTINUE ()
def CHOOSE_OPTION_FROM_LIST_1(lis, msg):
    print ''
    list_object=[item for item in lis]
    list_object.sort(key=str.lower)
    if 'Exit' in list_object:
        list_object.remove('Exit')
        list_object.sort(key=str.lower)
        list_object.append('Exit')
    try:
        if (len(list_object)<1):
            print "Nothing to choose :( "
            print "Execution will stop!"
            time.sleep(5)
            EXIT("**************** FATAL ERROR, CANNOT CONTINUE EXECUTION !!!   ******************")
            sys.exit(1)

        print msg
        counter=1
        for item in list_object:
            print str(counter)+') - '+item
            counter=counter+1

        choosed_option=raw_input("Choose option by entering the suitable number! ")
        while (int(choosed_option)<0 or int(choosed_option)> len(list_object)):
            print "No such option - ", choosed_option
            choosed_option=raw_input("Choose option by entering the suitable number! ")

        print "Chosen option is : '"+list_object[int(choosed_option)-1]+"'\r\n"
        return list_object[int(choosed_option)-1]

    except Exception, e:
        print '*** No such option!!!***', e
        #print 'Execution will stop! '
        #time.sleep(5)
        #EXIT("**************** FATAL ERROR, CANNOT CONTINUE EXECUTION !!!   ******************")
        #sys.exit(1)
        CHOOSE_OPTION_FROM_LIST_1(list_object, msg)
def DELETE_LOG_CONTENT(log_file_name):
    f = open(log_file_name, 'w')
    f.write('')
    f.close()
def DELETE_LOG_CONTENT_PATH(path):
    f = open(os.path.join(path), 'w')
    f.write('')
    f.close()
def ADD_LIST_AS_LINE_TO_CSV_FILE(csv_file_name,lis):
    try:
        f = open(csv_file_name, 'ab')
        writer = csv.writer(f)
        writer.writerow(lis)
        f.close()
    except Exception, e:
        print '*** ADD_LIST_AS_LINE_TO_CSV_FILE!!! ***', e
def ADD_LIST_AS_LINE_TO_CSV_FILE_PATH(csv_file_path,file_name,lis):
    try:
        f = open(os.path.join(csv_file_path,file_name), 'ab')
        writer = csv.writer(f)
        writer.writerow(lis)
        f.close()
    except Exception, e:
        print '*** ADD_LIST_AS_LINE_TO_CSV_FILE!!! ***', e
def READ_CSV_AS_NESTED_LIST(file_name):
    try:
        nested=[]
        with open(file_name, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                nested.append(row)
        return nested

    except Exception, e:
        print '*** READ_CSV_AS_NESTED_LIST!!! ***', e
def RUN_SQL_TO_FILE(dbname,user,host,password,sql,result_file,db_port,single_sql=True):
    try:
        DELETE_LOG_CONTENT(result_file)
        conn_string = "host="+host+" dbname="+dbname+" user="+user+" password="+password+" port="+db_port
        cursor = psycopg2.connect(conn_string).cursor()

        if single_sql==True:
            cursor.execute(sql)
            data = cursor.fetchall()
            a = cursor.description
            headers=[a[0] for a in cursor.description]
            data=[list(item) for item in data]
            data.insert(0, headers)
            for lis in data:
                print lis
                ADD_LIST_AS_LINE_TO_CSV_FILE(result_file,lis)

        if single_sql==False:
            count=0
            total_sqls=len(sql)
            all_data=[]
            for item in sql:
                count+=1
                cursor.execute(item)
                data = cursor.fetchall()
                a = cursor.description
                headers=[a[0] for a in cursor.description]
                if len(data)!=0:
                    data=[list(item) for item in data][0]
                    all_data.append(data)
                    percentage_done=count*100.0/total_sqls
                    sys.stdout.write('Completed SQL quaries:'+str(round(percentage_done,2))+'%\r\n')
                    #sys.stdout.flush()
                    #print round(percentage_done,2)
            all_data.insert(0, headers)

            for lis in all_data:
                ADD_LIST_AS_LINE_TO_CSV_FILE(result_file,lis)
        return True
    except Exception, e:
        print str(e)
        return False
def RUN_SQL(dbname,user,host,password,db_port,sql):
    try:
        conn_string = "host="+host+" dbname="+dbname+" user="+user+" password="+password+" port="+db_port
        cursor = psycopg2.connect(conn_string).cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        a = cursor.description
        headers=[a[0] for a in cursor.description]
        data=[list(item) for item in data]
        all_dic=[]
        for d in data:
            keys=headers
            values=d
            dictionary=dict(zip(keys, values))
            all_dic.append(dictionary)
        return [True,all_dic]
    except Exception, e:
        return [False,str(e)]
def RUN_SQL_SAMPLE_DB(dbname,user,host,password,db_port,sql,timeout=100):
    start_time=time.time()
    end_time=start_time+timeout
    sample_time=time.time()
    all_dic=[]
    while all_dic==[] and sample_time<end_time:
        time.sleep(30)
        sample_time=time.time()
        print 'Sampling Condition is True!','Time rest:' +str(end_time-sample_time),'SQL result: '+str(all_dic)
        try:
            conn_string = "host="+host+" dbname="+dbname+" user="+user+" password="+password+" port="+db_port
            cursor = psycopg2.connect(conn_string).cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            a=cursor.description
            headers=[a[0] for a in cursor.description]
            data=[list(item) for item in data]
            for d in data:
                keys=headers
                values=d
                dictionary=dict(zip(keys, values))
                all_dic.append(dictionary)
        except Exception, e:
            print str(e)
            all_dic=[]
            #pass
            continue
    return all_dic
def SQL_QUERY_GET_KEYS(sql_string):
    keys=re.findall('\{(.*?)\}', sql_string)
    keys=[item.lower() for item in keys]
    return keys
def SQL_QUERY_SET_VALUES_BY_KEYS(sql_query, dic):
    for k in dic:
        sql_query=sql_query.replace('{'+k+'}',dic[k])
    return sql_query
def CREATE_EXCEL_SHEETS(file_name,sheet_dict):
    #Create an new Excel file and add a worksheet.
    try:
        workbook = xlsxwriter.Workbook(file_name)
        for d in sheet_dict.keys():
            worksheet = workbook.add_worksheet(d[0:30])#Sheet name should be less 31
            bold = workbook.add_format({'bold': 1})
            nes_lis_data=sheet_dict[d]
            row=0
            for lis in nes_lis_data:
                col=0
                for item in lis:
                    #item=item.decode("utf8")
                    #print item
                    worksheet.write(row, col, str(item).decode('utf8', 'ignore'))
                    col+=1
                row+=1
        workbook.close()
        return True
    except Exception, e:
        print '*** CREATE_EXCEL_SHEETS!!! ***', e
def FIX_SELENIUM_LINUX():
    os.system('Xvfb :99 -ac &')
    os.system('export DISPLAY=:99')
    os.system('firefox &')
def WRITE_DICTS_TO_CSV(csv_name,Dict_List):
    ### Get all unique keys ###
    DELETE_LOG_CONTENT(csv_name)
    all_keys=[]
    for item in Dict_List:
        for key in item.keys():
            if key not in all_keys:
                all_keys.append(key)
    csv_headers=all_keys
    ADD_LIST_AS_LINE_TO_CSV_FILE(csv_name,csv_headers)
    for item in Dict_List:
        list_to_write=['' for k in csv_headers]
        for key in item.keys():
            if key in csv_headers:
                list_to_write[csv_headers.index(key)]=item[key]
        ADD_LIST_AS_LINE_TO_CSV_FILE(csv_name,list_to_write)
def WRITE_DICT_TO_CSV(dict,csv_name):
    headers=dict.keys()
    DELETE_LOG_CONTENT(csv_name)
    ADD_LIST_AS_LINE_TO_CSV_FILE(csv_name,headers)
    list_to_add=[]
    for h in headers:
        list_to_add.append(dict[h])
    ADD_LIST_AS_LINE_TO_CSV_FILE(csv_name,list_to_add)
def MY_LIS_COMPARE(lis1,lis2):
    lis1=[item.lower().strip().replace(' ','') for item in lis1]
    lis2=[item.lower().strip().replace(' ','') for item in lis2]
    ### Change for Storm to LPP result comparison
    #replace_strings=['good','error','warning']
    replace_strings=[]
    for string in replace_strings:
        if string in lis1[-1].lower():
            lis1[-1]=string

    for string in replace_strings:
        if string in lis2[-1].lower():
            lis2[-1]=string

    indexes=[]
    if lis1==lis2:
        res=True

    else:
        res=False
        for x in range(0,len(lis1)):
            if str(lis1[x]).lower()!=str(lis2[x]).lower():
                indexes.append(x)
    return [res,indexes]
def id_generator(size=20, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))