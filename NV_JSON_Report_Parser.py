import json
class PARSE_JSON_REPORT():
    def __init__(self, json_file_path):
        self.json_file_path=json_file_path
        self.dict=json.loads(open(self.json_file_path,'r').read())
        #self.ark_id=ark_id

    def GET_ALL_KEYS(self):
        return self.dict.keys()

    def JSON_AS_STRING(self):
        return open(self.json_file_path,'r').read()

    def CHECK_IF_STRING_IS_IN(self,some_string):
        if some_string.lower() in str(self.dict).lower():
            return True
        else:
            return False

    def HTTP_WATERFALL_TEST_VALIDATION(self,traffic_results,threshold_percentage):
        print traffic_results
        print threshold_percentage
        for item in traffic_results:
            if self.CHECK_IF_STRING_IS_IN(item['Request_Headers']['Arkady_Request_ID'])==False:
                return {'TestResult':'Failed','ErrorMessage':'Arkady_Request_ID:'+item['Request_Headers']['Arkady_Request_ID']+' was not found in NV Json Report!!!'}

        # If all IDs are in NV JSON Report, continue to size and time validation with threshold value
        # Exporting size and time from NV Json report #
        self.waterfall_requests=[]
        for item in self.dict['transactionReports'][0]['reports']['waterfall']['subTransactions']:
            self.dic={}
            self.dic['URL']=url=item['attributes']['URI']
            self.dic['Time']=item['end']-item['start']
            self.dic['Response_Code']=item['attributes']['StatusCode']
            self.dic['Content_Size']=item['attributes']['ResponseContentSize']
            self.waterfall_requests.append(self.dic)

        # Compare between expected and actual values #
        self.waterfall_requests=[item for item in self.waterfall_requests if item['Response_Code']==200]
        print '-------------------'
        print self.waterfall_requests
        print traffic_results
        print '--------------------------- compare bla'


#
#
# obj=PARSE_JSON_REPORT('C:\Users\Administrator\PycharmProjects\BasicSanity\TempScripts\NV_JSON.json')#,'')
# dict=obj.dict
# print obj.GET_ALL_KEYS()
# print obj.JSON_AS_STRING()
# print obj.CHECK_IF_ARKADY_ID_IS_IN('a9f1714e-c0ef-4b57-8f27-385d640a68b9')
# print obj.EXPORT_REQUETS_FROM_WATERFALL()
#
#

