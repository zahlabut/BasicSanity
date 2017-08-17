### Copy and paste MonitoringOptMyApp.py content ###
import os,sys,unittest,shutil
import subprocess
from Mi_Functions import *
from TrafficTypes import *
cur_path=os.path.abspath('.')
sys.path.append(cur_path)
from boto import ec2
from Params import *


ADV_REPORT_EXECUTION_TIME_THRESHOLD=60
REPLAY_REPORT_EXECUTION_TIME_THRESHOLD=60*10
API_EXECUTION_TIME_THRESHOLD=30
ENVIRONMENT_AWS_NAME_STRING=sys.argv[1]



if 'linux' in platform.system().lower() and SAVE_CAPTURE==True:
    os.system('sudo python Cleaner.py')
else:
    os.system('python Cleaner.py')


class OptMyAppMonitoring(unittest.TestCase):

    def test___1_Run_Advanced_Mode_Scenario___(self):
        FNULL = open(os.devnull, 'w')
        # Advanced Mode Single loop with Wget #
        shutil.copy2(os.path.join('ParamFiles','Params_Adv_Wget.py'), 'Params.py')
        #params=[line.strip() for line in open('Params.py','r').readlines() if line.startswith('#')==False]
        #SPEC_PRINT(['---- BasicSanityTool V 1.0 --------','Designed to test TM/OptMyAPP by: Arkady Shtempler','','Script parameters:']+params+['*** Goodbye World !!! ***'])
        status=subprocess.call(['python','OptMyAppSanity.py'],stdout=FNULL, stderr=subprocess.STDOUT)
        FNULL.close()
        self.assertEqual(status,0,'ACHTUNG !!! - '+str(status))
        #self.assertIn('OptMyAppSanity.py END',output,'ACHTUNG !!! - Scenario failed to run, check OptMyAppSanity.py output:\r\n'+output)




    def test___2_Run_Replay_Mode_Scenario___(self):
        FNULL = open(os.devnull, 'w')
        # Replay Mode Single loop with Wget #
        shutil.copy2(os.path.join('ParamFiles','Params_Replay_Wget.py'), 'Params.py')
        #params=[line.strip() for line in open('Params.py','r').readlines() if line.startswith('#')==False]
        #SPEC_PRINT(['---- BasicSanityTool V 1.0 --------','Designed to test TM/OptMyAPP by: Arkady Shtempler','','Script parameters:']+params+['*** Goodbye World !!! ***'])
        status=subprocess.call(['python','OptMyAppSanity.py'],stdout=FNULL, stderr=subprocess.STDOUT)
        FNULL.close()
        self.assertEqual(status,0,'ACHTUNG !!! - '+str(status))
        #self.assertIn('OptMyAppSanity.py END',output,'ACHTUNG !!! - Scenario failed to run, check OptMyAppSanity.py output:\r\n'+output)

    def test___NV_Report_Created___(self):
        directories=[d for d in os.listdir('.') if os.path.isdir(d)==True and d.startswith('.')==False and ('replay' in d.lower() or 'advanced' in d.lower())]
        self.assertNotEqual([],directories,'ACHTUNG !!! - Result directory was not found')
        for d in directories:
            self.assertNotEqual([],directories,'ACHTUNG !!! - Result directory was not found')
            htmls=[f for f in os.listdir(d) if f.endswith('.html')==True]
            self.assertEqual(len(htmls),1,'ACHTUNG !!! - NV report HTML does not exist!!!')

    def test___NV_Report_Contains_User_HTTP_Traffic___(self):
        directories=[d for d in os.listdir('.') if os.path.isdir(d)==True and d.startswith('.')==False and ('replay' in d.lower() or 'advanced' in d.lower())]
        self.assertNotEqual([],directories,'ACHTUNG !!! - Result directory was not found')
        for d in directories:
            self.assertNotEqual([],directories,'ACHTUNG !!! - Result directory was not found')
            test_result_csv=[f for f in os.listdir(d) if 'TestResult_' in f and f.endswith('.csv')==True]
            self.assertNotEqual([],test_result_csv,'ACHTUNG !!! - TestResult file not found')
            html=[f for f in os.listdir(d) if f.endswith('.html')==True]
            self.assertNotEqual([],html,'ACHTUNG !!! - NV report HTML does not exist!!!')
            html=html[0]
            csv_file_data=READ_CSV_AS_NESTED_LIST(os.path.join(d,test_result_csv[0]))
            csv_file_fields=csv_file_data[0]
            option='Tested_URL'
            field_index=csv_file_fields.index(option)
            tested_url=[item[field_index] for item in csv_file_data[1:]][0]
            nv_report_data=open(os.path.join(d,html),'r').read()
            self.assertIn(tested_url,nv_report_data,'ACHTUNG !!! - '+tested_url+' was not found in NV Report')

    def test___NV_Report_Contains_Transactions___(self):
        directories=[d for d in os.listdir('.') if os.path.isdir(d)==True and d.startswith('.')==False and ('replay' in d.lower() or 'advanced' in d.lower())]
        self.assertNotEqual([],directories,'ACHTUNG !!! - Result directory was not found')
        for d in directories:
            self.assertNotEqual([],directories,'ACHTUNG !!! - Result directory was not found')
            if 'advanced' in d.lower():
                html=[f for f in os.listdir(d) if f.endswith('.html')==True]
                self.assertNotEqual([],html,'ACHTUNG !!! - NV report HTML does not exist!!!')
                html=html[0]
                nv_report_data=open(os.path.join(d,html),'r').read()
                transactions=['Transaction_baseline','Transaction_good3G','Transaction_busy3G']
                for n in transactions:
                    self.assertIn(n,nv_report_data,'ACHTUNG !!! - '+n+' was not found in NV Report')

    def test___NV_Report_Generation_Time_Advanced_Mode___(self):
        directories=[d for d in os.listdir('.') if os.path.isdir(d)==True and d.startswith('.')==False and ('replay' in d.lower() or 'advanced' in d.lower())]
        self.assertNotEqual([],directories,'ACHTUNG !!! - Result directory was not found')
        for d in directories:
            self.assertNotEqual([],directories,'ACHTUNG !!! - Result directory was not found')
            if 'advanced' in d.lower():
                test_result_csv=[f for f in os.listdir(d) if 'TestResult_' in f and f.endswith('.csv')==True]
                self.assertNotEqual([],test_result_csv,'ACHTUNG !!! - NV report HTML does not exist!!!')
                csv_file_data=READ_CSV_AS_NESTED_LIST(os.path.join(d,test_result_csv[0]))
                csv_file_fields=csv_file_data[0]
                option='Report_Execution_Time'
                self.assertIn(option,csv_file_fields,'ACHTUNG !!! - "'+option+'" does not exist in *csv file column names!!!')
                field_index=csv_file_fields.index(option)
                report_execution_time=float([item[field_index] for item in csv_file_data[1:]][0])
                self.assertGreater(ADV_REPORT_EXECUTION_TIME_THRESHOLD,report_execution_time,'ACHTUNG !!! - NV report generation time is: '+str(report_execution_time)+'!!!')

    def test___NV_Report_Generation_Time_Replay_Mode___(self):
        directories=[d for d in os.listdir('.') if os.path.isdir(d)==True and d.startswith('.')==False and ('replay' in d.lower() or 'advanced' in d.lower())]
        self.assertNotEqual([],directories,'ACHTUNG !!! - Result directory was not found')
        for d in directories:
            self.assertNotEqual([],directories,'ACHTUNG !!! - Result directory was not found')
            if 'replay' in d.lower():
                test_result_csv=[f for f in os.listdir(d) if 'TestResult_' in f and f.endswith('.csv')==True]
                self.assertNotEqual([],test_result_csv,'ACHTUNG !!! - TestResult file not found')
                csv_file_data=READ_CSV_AS_NESTED_LIST(os.path.join(d,test_result_csv[0]))
                csv_file_fields=csv_file_data[0]
                option='Report_Execution_Time'
                self.assertIn(option,csv_file_fields,'ACHTUNG !!! - "'+option+'" does not exist in *csv file column names!!!')
                field_index=csv_file_fields.index(option)
                report_execution_time=float([item[field_index] for item in csv_file_data[1:]][0])
                self.assertGreater(REPLAY_REPORT_EXECUTION_TIME_THRESHOLD,report_execution_time,'ACHTUNG !!! - NV report generation time is: '+str(report_execution_time)+'!!!')


    def test___API_Failures_Advanced_Mode___(self):
        directories=[d for d in os.listdir('.') if os.path.isdir(d)==True and d.startswith('.')==False and ('replay' in d.lower() or 'advanced' in d.lower())]
        self.assertNotEqual([],directories,'ACHTUNG !!! - Result directory was not found')
        for d in directories:
            self.assertNotEqual([],directories,'ACHTUNG !!! - Result directory was not found')
            if 'advanced' in d.lower():
                api_result_csv=[f for f in os.listdir(d) if 'API_Results' in f and f.endswith('.csv')==True]
                self.assertNotEqual([],api_result_csv,'ACHTUNG !!! - API_Results file not found')
                csv_file_data=READ_CSV_AS_NESTED_LIST(os.path.join(d,api_result_csv[0]))
                csv_file_fields=csv_file_data[0]
                option='ErrorCode'
                field_index=csv_file_fields.index(option)
                for lis in csv_file_data[1:]:
                    self.assertNotIn('-',lis[field_index],'ACHTUNG !!! - Received API ErrorCode is: '+lis[field_index]+' !!!\r\n'+str(lis))


    def test___API_Failures_Replay_Mode___(self):
        directories=[d for d in os.listdir('.') if os.path.isdir(d)==True and d.startswith('.')==False and ('replay' in d.lower() or 'advanced' in d.lower())]
        self.assertNotEqual([],directories,'ACHTUNG !!! - Result directory was not found')
        for d in directories:
            self.assertNotEqual([],directories,'ACHTUNG !!! - Result directory was not found')
            if 'replay' in d.lower():
                api_result_csv=[f for f in os.listdir(d) if 'API_Results' in f and f.endswith('.csv')==True]
                self.assertNotEqual([],api_result_csv,'ACHTUNG !!! - API_Results file not found')
                csv_file_data=READ_CSV_AS_NESTED_LIST(os.path.join(d,api_result_csv[0]))
                csv_file_fields=csv_file_data[0]
                option='ErrorCode'
                field_index=csv_file_fields.index(option)
                for lis in csv_file_data[1:]:
                    self.assertNotIn('-',lis[field_index],'ACHTUNG !!! - Received API ErrorCode is: '+lis[field_index]+' !!!\r\n'+str(lis))


    def test___API_Response_Time_Advanced_Mode___(self):
        directories=[d for d in os.listdir('.') if os.path.isdir(d)==True and d.startswith('.')==False and ('replay' in d.lower() or 'advanced' in d.lower())]
        self.assertNotEqual([],directories,'ACHTUNG !!! - Result directory was not found')
        for d in directories:
            self.assertNotEqual([],directories,'ACHTUNG !!! - Result directory was not found')
            if 'advanced' in d.lower():
                api_result_csv=[f for f in os.listdir(d) if 'API_Results' in f and f.endswith('.csv')==True]
                self.assertNotEqual([],api_result_csv,'ACHTUNG !!! - API_Results file not found')
                csv_file_data=READ_CSV_AS_NESTED_LIST(os.path.join(d,api_result_csv[0]))
                csv_file_fields=csv_file_data[0]
                option='ExecutionTime'
                field_index=csv_file_fields.index(option)
                for lis in csv_file_data[1:]:
                    self.assertGreater(API_EXECUTION_TIME_THRESHOLD,float(lis[field_index]),'ACHTUNG !!! - API Response time is: '+lis[field_index]+' !!!\r\n'+str(lis))


    def test___API_Response_Time_Replay_Mode__(self):
        directories=[d for d in os.listdir('.') if os.path.isdir(d)==True and d.startswith('.')==False and ('replay' in d.lower() or 'advanced' in d.lower())]
        self.assertNotEqual([],directories,'ACHTUNG !!! - Result directory was not found')
        for d in directories:
            self.assertNotEqual([],directories,'ACHTUNG !!! - Result directory was not found')
            if 'replay' in d.lower():
                api_result_csv=[f for f in os.listdir(d) if 'API_Results' in f and f.endswith('.csv')==True]
                self.assertNotEqual([],api_result_csv,'ACHTUNG !!! - API_Results file not found')
                csv_file_data=READ_CSV_AS_NESTED_LIST(os.path.join(d,api_result_csv[0]))
                csv_file_fields=csv_file_data[0]
                option='ExecutionTime'
                field_index=csv_file_fields.index(option)
                for lis in csv_file_data[1:]:
                    self.assertGreater(API_EXECUTION_TIME_THRESHOLD,float(lis[field_index]),'ACHTUNG !!! - API Response time is: '+lis[field_index]+' !!!\r\n'+str(lis))


    def test___Traffic_Execution_Time_Matchs_Emulated_Network__(self):
        directories=[d for d in os.listdir('.') if os.path.isdir(d)==True and d.startswith('.')==False and ('replay' in d.lower() or 'advanced' in d.lower())]
        self.assertNotEqual([],directories,'ACHTUNG !!! - Result directory was not found')
        for d in directories:
            self.assertNotEqual([],directories,'ACHTUNG !!! - Result directory was not found')
            if 'advanced' in d.lower():
                transaction_file=[f for f in os.listdir(d) if 'Transactions' in f and f.endswith('.csv')==True]
                self.assertNotEqual([],transaction_file,'ACHTUNG !!! - Transaction file does not exist!!!')
                csv_file_data=READ_CSV_AS_NESTED_LIST(os.path.join(d,transaction_file[0]))
                csv_file_fields=csv_file_data[0]
                option='Traffic_Execution_Time_[sec]'
                field_index=csv_file_fields.index(option)
                execution_time=[]
                execution_time_print_string=[]
                for lis in csv_file_data[1:]:
                    if 'baseline' in str(lis):
                        self.assertNotEqual('',lis[field_index],'ACHTUNG !!! No execution time found for "baseline" '+str(lis))
                        execution_time.append(float(lis[field_index]))
                        execution_time_print_string.append('baseline --> '+lis[field_index])
                    if 'good3G' in str(lis):
                        self.assertNotEqual('',lis[field_index],'ACHTUNG !!! No execution time found for "good3G" '+str(lis))
                        execution_time.append(float(lis[field_index]))
                        execution_time_print_string.append('good3G --> '+lis[field_index])
                    if 'busy3G' in str(lis):
                        self.assertNotEqual('',lis[field_index],'ACHTUNG !!! No execution time found for "busy3G" '+str(lis))
                        execution_time.append(float(lis[field_index]))
                        execution_time_print_string.append('busy3G --> '+lis[field_index])
                self.assertListEqual(execution_time,sorted(execution_time),'ACHTUNG !!! - Traffic Execution times does not make sense'+'\r\n'+str(execution_time_print_string))


    def test___Average_Download_Time_Matchs_Emulated_Network___(self):
        directories=[d for d in os.listdir('.') if os.path.isdir(d)==True and d.startswith('.')==False and ('replay' in d.lower() or 'advanced' in d.lower())]
        self.assertNotEqual([],directories,'ACHTUNG !!! - Result directory was not found')
        for d in directories:
            self.assertNotEqual([],directories,'ACHTUNG !!! - Result directory was not found')
            if 'advanced' in d.lower():
                transaction_file=[f for f in os.listdir(d) if 'Transactions' in f and f.endswith('.csv')==True]
                self.assertNotEqual([],transaction_file,'ACHTUNG !!! - Transaction file does not exist!!!')
                csv_file_data=READ_CSV_AS_NESTED_LIST(os.path.join(d,transaction_file[0]))
                csv_file_fields=csv_file_data[0]
                option='Average_Download_Time_[msec]'
                field_index=csv_file_fields.index(option)
                execution_time=[]
                execution_time_print_string=[]
                nets=['baseline','good3G','busy3G']
                for n in nets:
                    for lis in csv_file_data[1:]:
                        if n in str(lis):
                            self.assertNotEqual('',lis[field_index],'ACHTUNG !!! No execution time found for "'+n+'" network'+str(lis))
                            execution_time.append(float(lis[field_index]))
                            execution_time_print_string.append(n+' --> '+lis[field_index])
                self.assertListEqual(execution_time,sorted(execution_time),'ACHTUNG !!! - Average traffic execution times does not make sense'+'\r\n'+str(execution_time_print_string))


    def test___Data_Was_Received_By_User_Per_Emulated_Network__(self):
        directories=[d for d in os.listdir('.') if os.path.isdir(d)==True and d.startswith('.')==False and ('replay' in d.lower() or 'advanced' in d.lower())]
        self.assertNotEqual([],directories,'ACHTUNG !!! - Result directory was not found')
        for d in directories:
            self.assertNotEqual([],directories,'ACHTUNG !!! - Result directory was not found')
            if 'advanced' in d.lower():
                transaction_file=[f for f in os.listdir(d) if 'Transactions' in f and f.endswith('.csv')==True]
                self.assertNotEqual([],transaction_file,'ACHTUNG !!! - Transaction file does not exist!!!')
                csv_file_data=READ_CSV_AS_NESTED_LIST(os.path.join(d,transaction_file[0]))
                csv_file_fields=csv_file_data[0]
                option='Total_Download_Size_[kb]'
                field_index=csv_file_fields.index(option)
                nets=['baseline','good3G','busy3G']
                for n in nets:
                    for lis in csv_file_data[1:]:
                        if n in str(lis):
                            self.assertNotEqual('',lis[field_index],'ACHTUNG !!! No execution time found for "'+n+'" network'+str(lis))
                            self.assertGreater(float(lis[field_index]),0,'ACHTUNG !!! - Received data is Zero! '+n+' --> '+lis[field_index])

    # def test___Static_HTML_Is_Available__(self):
    #     if 'linux' in platform.system().lower():
    #         display = Display(visible=0, size=(800, 600))
    #         display.start()
    #     url='http://hpenv.com'
    #     result=OPEN_WEB_SITE_SELENIUM(url)
    #     self.assertNotIn('OPEN_WEB_SITE_SELENIUM_Exception',result.keys(),'ACHTUNG !!! - Failed to load: '+url+' '+str(result)+' !!!')
    #     self.assertEqual(result['Final_URL'],'http://hpenv.com/','ACHTUNG !!! - Final URL:'+result['Final_URL']+' is not as expected: "http://hpenv.com/" !!!')
    #     self.assertGreater(30,result['Page_Load_Time[sec]'],'ACHTUNG !!! - Page load time is greater than 30 seconds !!!')
    #     os.remove(result['ScreenshootName'])
    #     if 'linux' in platform.system().lower():
    #         display.stop()


    # def test___AWS_Instances_Status__(self):
    #     ec2conn = ec2.connection.EC2Connection(AWS_SEC_ID,AWS_SEC_KEY)
    #     reservations = ec2conn.get_all_instances()
    #     instances = [i for r in reservations for i in r.instances]
    #     for i in instances:
    #         i=i.__dict__
    #         if ENVIRONMENT_NAME_STRING.lower() in i['tags']['Name'].lower() and i['tags']['Name']!='NVCloud-prod-website':
    #             #print i['tags']['Name'], i['_state'], i['public_dns_name']
    #             status=str(i['_state'])
    #             self.assertIn('running',status, 'ACHTUNG !!! - '+str(i['tags']['Name'])+' is down !!!')
    #     ec2conn.close()


if __name__ == '__main__':
    unittest.main()
# suite = unittest.TestLoader().loadTestsFromTestCase(OptMyAppMonitoring)
# unittest.TextTestRunner(verbosity=1).run(suite)


