# BasicSanity
TM and OptMyApp sanity test

Configuration is done using Params.py
1) OptMyApp parameters
    USE_SELENIUM=False
    USE_TRANSACTIONS=False
    SAVE_SCREENSHOT=False
    USE_ALEXA_SITES=False
    USE_HTTPS_SITES=True
    USE_HLS_SITES=False
    SITES_RANGE=(0, 1)
    REPORT_TIMEOUT=60*5
    WGET_MODE_LOOPS=1
    SLEEP_DELAY=2 #Delay after each HTTP GET
    STOP_START_DELAY=5
    REPLAY_MODE={'Enabled':True,'URL':'https://apps.facebook.com','LoopNumber':100}
    ADVANCED_MODE_BASELINE={'Enabled':True,'URL':'http://google.com','LoopNumber':1} #Used if USE_TRANSACTIONS is TRUE
    ADVANCED_MODE_3G_GOOD={'Enabled':True,'URL':'https://accounts.youtube.com','LoopNumber':50}
    ADVANCED_MODE_3G_BUSY={'Enabled':True,'URL':'https://cscentral.amazon.com','LoopNumber':25}
    OPT_MY_APP_DOMAIN= 'test.hpenv.com'

    Combination of "USE_SELENIUM + USE_TRANSACTIONS"
    1) True True   --> Only Advanced mode will be activated using: transactions and Selenium
    2) False True  --> Only Advanced mode will be activated using: transactions and WGETs
       Note: configuration for this test case will be taken from ADVANCED_MODE_BASELINE
    3) True False  --> Replay mode and all network types in Advanced mode will be activated using Selenium
    4) False False --> Replay mode and all network types in Advanced mode will be activated using WGETs

