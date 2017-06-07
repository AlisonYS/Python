import os 
import sys
try :
    f = open("emotion.txt")
    finalStr = ""
    for line in f.readlines():
        filename = line.split('"')
        if len(filename)>3 :
            print(filename[0])
except :
    print('Input Error!')
