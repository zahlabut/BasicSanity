from Mi_Functions import *
from tabulate import tabulate
from APIs import *
shutil.copy2(os.path.join('ParamFiles','Registration_Params.py'), 'Params.py')
import Params
reload(Params)
from Params import *



### Main ###
SPEC_PRINT([OPT_MY_APP_DOMAIN,pg_db_name])
opt_my_app_url='https://' + OPT_MY_APP_DOMAIN + '/hp/nvcloud?hf=myLittlePony'
emails_start_index=input('Enter email start index: ')
email_end_index=input('Enter email end index: ')

data_to_print=[]
data_to_print.append(['Email','Password','DeviceID','FirstName','LastName','Company','Country','RegisterEC','UserDetailsEC','Passcode','ActivateEC','UserID','DeviceInfo'])
for i in xrange(emails_start_index,email_end_index+1):
    print '='*100
    data=[]
    email=user_base_email.split('@')[0]+'+'+str(i)+'@'+user_base_email.split('@')[1]
    deviceid=device_id+str(i)
    firstName=First_Name+str(i)
    lastName=Last_Name+str(i)
    data.append(email)
    data.append(user_password)
    data.append(deviceid)
    data.append(firstName)
    data.append(lastName)
    data.append(company)
    data.append(country)
    ### New User Register
    print '... New user registers '
    register_response=OPT_MY_APP_API(opt_my_app_url, requestType='registerUser',
                                     deviceId=deviceid,
                                     email=email,
                                     password=user_password,
                                     deviceInfo=deviceinfo)
    print register_response
    data.append(register_response['errorCode'])



    ### New User fills forms
    print '... New fills forms '
    fill_forms_response=OPT_MY_APP_API(opt_my_app_url,requestType='userDetails',
                                  deviceId=deviceid,
                                  email=email,
                                  firstName=firstName,
                                  lastName=lastName,
                                  company=company,
                                  country=country)

    print fill_forms_response
    data.append(fill_forms_response['errorCode'])


    ### Get Passcode from DB
    passcode=RUN_SQL(pg_db_name,pg_user,pg_ip,pg_pwd,pg_port,"select passcode from users where email="+"'"+email+"'")
    print passcode
    passcode=passcode[1][0]['passcode']
    data.append(passcode)


    ### User enters passcode
    print '... New user enters passcode '
    passcode_result=OPT_MY_APP_API(opt_my_app_url,requestType='activate',
                                  deviceId=device_id+str(i),
                                  email=email,
                                  passcode=passcode)
    print passcode_result
    data.append(passcode_result['errorCode'])
    data.append(passcode_result['userId'])
    data.append(str(deviceinfo))
    data_to_print.append(data)

print '='*100
print tabulate(data_to_print,tablefmt='plain')



