from Params import *
from Mi_Functions import *

exceptions=[eval(item.strip()) for item in open(exceptions_file,'r').readlines()]
WRITE_DICTS_TO_CSV('Exceptions.csv',exceptions)


