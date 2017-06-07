import os 
import sys

def dealArray(array):
    temp_str = "<public type=\""+ array[0]+"\"       name=\""+ array[1] +"\"             id=\""+ array[2]+"\"/>"
    return temp_str;

def writeFiles(str):
    filename = "public_after.xml"
    wr = open(filename, 'w')
    wr.write(str)
    wr.close()

try :
    f = open("public_reduce.xml")
    public_list = "<resources>" + '\n'
    try :
        for line in f.readlines():
            temp = line.split('"')
            if len(temp)>2:
                fileObject = open("public.xml", "r")
                for nameLine in fileObject.readlines():
                    name = nameLine.split('"')
                    if len(name)>2 and temp[3]==name[3]:
                        name_id = name[5]
                        break
                public_array = [temp[1], temp[3], name_id]    
                public_list += "  "+ dealArray(public_array) + '\n'
    finally :
        public_list += "</resources>"
        writeFiles(public_list)
        print('Done Success!')
except :
    print('Input Error!')