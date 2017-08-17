import subprocess
import sys
import os
import time

for scriptInstance in xrange(0,10):
    print scriptInstance
    #sys.stdout=open('result%s.txt' % scriptInstance,'w')
    subprocess.Popen(['python','TM_Sanity.py'],stdout=sys.stdout, stderr=subprocess.STDOUT)
    #print os.system('python TM_Sanity.py')
    time.sleep(5)
