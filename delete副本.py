import os
import sys
try :
    f = open("dupRes.txt")
    finalStr = ""
    for line in f.readlines():
        os.popen("rm -f " + line)
except :
    print('Input Error!')
