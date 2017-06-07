import os 
import sys

def dealline(line) :
    resource = line.split('resource ')
    if len(resource)>1:
        xx = resource[1].split()
        info = xx[1].split(':')[1]
        style = info.split('/')
        push_array = [style[0], style[1], xx[0]]
        return push_array
    else :
        return []

def dealArray(array):
    temp_str = "<public type=\""+ array[0]+"\"       name=\""+ array[1] +"\"             id=\""+ array[2]+"\"/>"
    return temp_str;
    
def getfile() :
    query = "~xuanmu/TOOL/boost_gradle_home/aapt/aapt d resources " + sys.argv[1] + "/build/build/outputs/apk/antui-build-debug.apk"
    return os.popen(query)

def writeFiles(str):
    filename = sys.argv[1]+ "/api/res/values/public.xml"
    wr = open(filename, 'w')
    wr.write(str)
    wr.close()

try :
    f = getfile()
    public_list = "<resources>" + '\n'
    duplicate_id = ["test"]
    try :
        for line in f.readlines():
            public_array = dealline(line)
            if (len(public_array)>0 and public_array[0] != "id"):
                isduplicate = 0
                for public_id in duplicate_id:
                    if public_id == public_array[2]:
                        isduplicate = 1
                if isduplicate == 0:
                    duplicate_id.append(public_array[2])
                    public_list += "  "+dealArray(public_array) + '\n'
    finally :
        public_list += "</resources>"
        writeFiles(public_list)
        print('Done Success!')
except :
    print('Input Error!')
