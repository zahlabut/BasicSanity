###Exceptions log file ###
exceptions_file='Exceptions.log'
### API Log File ###
api_log_file='API_Results.csv'


### Number of API failures ###
#Script will exit if this number is reached!
global number_of_api_failures
number_of_api_failures=5

### Save test results in zip file ###
SAVE_ZIP=True

### Common parameters ###
SAVE_CAPTURE=False

### For OptMyApp Sanity ###
USE_SELENIUM=True
#global USE_TRANSACTIONS
USE_TRANSACTIONS=False
SAVE_SCREENSHOT=True
USE_ALEXA_SITES=False
USE_HTTPS_SITES=False
USE_HLS_SITES=False
SITES_RANGE=(0, 1)
REPORT_TIMEOUT=60*10
STOP_START_DELAY=5
REPORT_SAMPLE_DELAY=5



# OPT_MY_APP_DOMAIN= 'test.hpenv.com'
# USER_EMAIL='dm2@hpe.com'
# DEVICE_ID="05e854d0065c863cbdce527531544b0b"
# USER_ID="3af77ef5-8bb8-4560-8bad-dda901f57cfd"
# USER_PASSWORD='Dm123456'
# USER_DEVICE={"device":"Python_Chrome_AddOn_Simulator"}


OPT_MY_APP_DOMAIN= 'test.hpenv.com'
USER_EMAIL='arkady.shtempler@hpe.com'
DEVICE_ID="d4cd04b0d237385877d840d500bd3f31"
USER_ID="0689c729-8e42-42de-9dc2-c859fd8ba161"
USER_PASSWORD='Admin1234'
USER_DEVICE={"device":"Arkady_Monitoring_User"}
