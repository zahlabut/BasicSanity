import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from HP_Functions import *
from datetime import datetime
import uuid
from NV_JSON_Report_Parser import *


########################################## Parameters ##############################################
def CONVERT_INI_TO_VARIABLES(ini_file_name):
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
CONVERT_INI_TO_VARIABLES('BasicReportSanity.ini')
####################################################################################################



### Start Report Content Validation Scenario ###
ports_parameters='?ports=8888,65000,80,443,8080,8090'
NV_MODE=['AS_PROXY','LOCAL_NV']





Tests=['HTTP_WATERFALL']#,'Resource_Analysis','Recomendations']



traffic_results=[]
for test in Tests:

    # Set NV IP and client Source IP
    if is_proxy=='True':
        IS_PROXY='true' #For start API
        NV_IP=ip
        src_ip=GET_MY_PUBLIC_IP()
        WGET_PROXIES = {'http': 'http://' + NV_IP + ':' + str(proxy_port), 'https': 'https://' + NV_IP + ':' + str(proxy_port)}
        SELENIUM_PROXY=NV_IP+':'+str(proxy_port)
    if is_proxy=='False':
        NV_IP='127.0.0.1'
        IS_PROXY='false'
        src_ip=GET_PHYSICAL_INTERFACE_IP()
        WGET_PROXIES =None
        SELENIUM_PROXY=None
    ### Kill all running emulations on NV (FORCE STOP API)###
    kill_all=MC_APIS(ip=NV_IP,port=port,user=user,password=password,https=is_https,method='PUT',url_path='shunra/api/emulation/resetall',
                         additional_headers={'Accept':'application/json'}, api_name='FORCE_STOP')
    kill_alls_response=kill_all.RUN_REQUEST()
    PRINT_DICT(kill_alls_response)

    ### Shunra API get profiles ###
    get_profiles=MC_APIS(ip=NV_IP,port=port,user=user,password=password,https=is_https,method='GET',url_path='shunra/api/profile',
                         additional_headers={'Accept':'application/json'}, api_name='GET_PROFILES')
    get_profiles_response=get_profiles.RUN_REQUEST()
    PRINT_DICT(get_profiles_response)
    all_profiles=get_profiles_response['Content_As_Dict']['profiles']
    print all_profiles
    for prof in all_profiles:
        if prof['name']=="Network disconnection":
            all_profiles.remove(prof)

    ### Start API #
    prof=random.choice(all_profiles)
    profile_id=prof['id']
    network_scenario=prof['name']
    test_name=test+'_'+prof['name'].replace(' ','_')+'_'+str(time.time())
    device_id='zababun_device_id_123'
    flow_id='zababun_flow_id_123'
    pl_id='zababun_pl_id_123'
    test_description='NV_Report_Validation_Of_'+test_name
    start_post_data={"deviceId": device_id,
                     "flows":[{"flowId": flow_id, "srcIp": src_ip, "profileId": profile_id, "isCaptureClientPL": True}],
                     "testMetadata": {"testName":test_name, "description": test_description, "networkScenario": network_scenario}}
    start_obj=MC_APIS(ip=NV_IP,port=port,user=user,password=password,https=is_https,method='POST',url_path='shunra/api/emulation/custom',
                      additional_headers={'Accept':'application/json','Content-Type':'application/json'},params={'mode':'MULTI_USER','useProxy':IS_PROXY},request_payload=start_post_data, api_name='START_API')
    start_resp=start_obj.RUN_REQUEST()
    PRINT_DICT(start_resp)
    test_token=start_resp['Content_As_Dict']['testToken']

    ### Send Trafic ###
    if test=='HTTP_WATERFALL':
        traffic_results.append(HTTP_GET_SITE(http_url,1,WGET_PROXIES,request_headers={'Accept-Encoding':'None','Arkady_Request_ID':str(uuid.uuid4())}))
        traffic_results.append(HTTP_GET_SITE(https_url,1,WGET_PROXIES,request_headers={'Accept-Encoding':'None','Arkady_Request_ID':str(uuid.uuid4())}))

    ### Stop API ###
    time.sleep(2)
    stop_put_data='''{"testTokens": ["token"]}'''.replace('token',test_token)
    stop_obj=MC_APIS(ip=NV_IP,port=port,user=user,password=password,https=is_https,method='PUT',url_path='shunra/api/emulation/stop',
                    additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload=stop_put_data, body_type='STRING', api_name='STOP_API')
    stop_resp=stop_obj.RUN_REQUEST()
    PRINT_DICT(stop_resp)

    ### Analyze test ###
    analyze_obj=MC_APIS(ip=NV_IP,port=port,user=user,password=password,https=is_https,method='PUT',url_path='shunra/api/analysisreport/analyze/'+test_token+ports_parameters,
                    additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload={}, body_type='JSON', api_name='ANALYZE_API')
    analyze_resp=analyze_obj.RUN_REQUEST()
    PRINT_DICT(analyze_resp)


    ### Get JSON Report ###
    json_report_obj=MC_APIS(ip=NV_IP,port=port,user=user,password=password,https=is_https,method='GET',url_path='shunra/api/analysisreport/'+test_token+'?zipResult=false',
                    additional_headers={'Accept':'application/json','Content-Type':'application/json'},request_payload={}, body_type='JSON', api_name='GET_JSON_REPORT')
    json_report_resp=json_report_obj.RUN_REQUEST()
    PRINT_DICT(json_report_resp)
    file_to_save_nv_json='NV_JSON.json'
    DELETE_LOG_CONTENT(file_to_save_nv_json)
    INSERT_TO_LOG(file_to_save_nv_json, json_report_resp['Content'])
    #print json_report_resp['Content_As_Dict']


    ### Make PASS/FAIL decision ###
    if test=='HTTP_WATERFALL':
        parsed_json_obj=PARSE_JSON_REPORT(os.path.abspath(file_to_save_nv_json))
        print parsed_json_obj.HTTP_WATERFALL_TEST_VALIDATION(traffic_results,threshold_percentage)





#
# # Get JSON report and export all needed values for testing #
# # Needed values are:
# # 1) "usingProxy": false,
# # 2) "type": "ServerTime",
# # 3) "start": 1500970262267,
# # 4) "end": 1500970262275
#
# if print_json=='True':
#     print '-'*80
#     print 'NV JSON Report'
#     print json_report_resp['Content']
#     print '-'*80
# exported_values={}
#
# for data in json_report_content_as_dict['reports']['waterfall']['subTransactions']:
#     start='N/A'
#     end='N/A'
#     for typ in data['components']:
#         if typ['type']=='ServerTime':
#             start=typ['start']
#             end=typ['end']
#     try:
#         delta_start_end=end-start
#     except:
#         delta_start_end='N/A'
#
#
#     exported_values[data['attributes']['URI']]={'Start':start,'End':end,'UsingProxy':data['attributes']['usingProxy'],'CalculatedDelay':str(delta_start_end)}
#     if TEST=='Real traffic to WEB site with Selenium':
#         exported_values_as_list.append(
#             {
#                 'URL':data['attributes']['URI'],
#                 'Start':start,
#                 'End':end,
#                 'UsingProxy':data['attributes']['usingProxy'],
#                 'CalculatedDelay':str(delta_start_end),
#                 'WgetYnetResult':str(ynet_result),
#                 'Profile_Name':prof['name']
#             })
#     else:
#         if end=='N/A' or start=='N/A':
#             exported_values_as_list.append(
#                 {
#                     'URL':data['attributes']['URI'],
#                     'Start':start,
#                     'End':end,
#                     'UsingProxy':data['attributes']['usingProxy'],
#                     'CalculatedDelay':'N/A',
#                     'Profile_Name':prof['name']
#                 })
#         else:
#             exported_values_as_list.append(
#                 {
#                     'URL':data['attributes']['URI'],
#                     'Start':start,
#                     'End':end,
#                     'UsingProxy':data['attributes']['usingProxy'],
#                     'CalculatedDelay':str(end-start),
#                     'Profile_Name':prof['name']
#                 })
#
# # Compare between Traffic Result and Results exported from NV JSON Report
# result_file_name='Estimated_Server_Time_Result.csv'
# for k in sent_urls.keys():
#     if k in exported_values.keys():
#         if exported_values[k]['CalculatedDelay']!='N/A':
#             result_dic_list.append({'TestMode':mode,
#                                     'TestName':test_name,
#                                     'TestedURL':k,
#                                     'UsingProxy':exported_values[k]['UsingProxy'],
#                                     'ConfiguredServerDelay':sent_urls[k]['ServerDelay'],
#                                     'CalculatedServerTimeDelay':exported_values[k]['CalculatedDelay'],
#                                     'VarianceCalculation':abs(float(sent_urls[k]['ServerDelay'])-float(exported_values[k]['CalculatedDelay']))})
#         else:
#             result_dic_list.append({'TestMode':mode,
#                                     'TestName':test_name,
#                                     'TestedURL':k,
#                                     'UsingProxy':exported_values[k]['UsingProxy'],
#                                     'ConfiguredServerDelay':sent_urls[k]['ServerDelay'],
#                                     'CalculatedServerTimeDelay':exported_values[k]['CalculatedDelay'],
#                                     'VarianceCalculation':'N/A'})
#
#
#     else:
#         print 'Warning - '+k+ ' was not found in NV Json Report!!!'
#         result_dic_list.append({'TestMode':mode,
#                                 'TestName':test_name,
#                                 'TestedURL':k,
#                                 'UsingProxy':'N/A',
#                                 'ConfiguredServerDelay':sent_urls[k]['ServerDelay'],
#                                 'CalculatedServerTimeDelay':'N/A',
#                                 'VarianceCalculation':'N/A'})
#
# if ask_to_continue_after_each_profile=='True':
#     ### For debug  to test single profile ###
#     WRITE_DICTS_TO_CSV(result_file_name,result_dic_list)
#     WRITE_DICTS_TO_CSV('AllExportedValuseFromJSON.csv',exported_values_as_list)
#     CONTINUE('Continue to the next profile?')
#
#
# WRITE_DICTS_TO_CSV(result_file_name,result_dic_list)
# WRITE_DICTS_TO_CSV('AllExportedValuseFromJSON.csv',exported_values_as_list)
#
