import os 
import sys

def getName(line) :
    name = line.split('"')
    if len(name)>2:
        return name[3]
    else :
        return []
    
def getNameList() :
    fileObject = open("original.txt", "r")
    name_list = ["xuanmu"]            
    for line in fileObject.readlines():
        name = getName(line)
        if len(name)>0:
            name_list.append(name)
    return name_list

def writeFiles(str):
    filename = sys.argv[1]+ "/widget/res/values/public.xml"
    wr = open(filename, 'w')
    wr.write(str)
    wr.close()

try :
    f = open("save.txt")
    nameList = getNameList()
    finalStr = ""
    for line in f.readlines():
        saveName = getName(line)
        for n in nameList:
            if n == saveName:
                 finalStr += line
    print(finalStr)
except :
    print('Input Error!')