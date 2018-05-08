from os import walk
import sys
import os 
import re

# ARRAY_FILE = os.path.join(webpage.settings.BASE_DIR,'front','biz','iconfont','arrays.xml')
ARRAY_FILE = "arrays.xml"
EXCHANGE_FILE = "ui2antui.txt"



ICONFONT = "AUIconDrawable iconDrawable = new AUIconDrawable(context, new IconPaintBuilder(0xff%s, size, com.alipay.mobile.antui.R.string.%s"
TITLEICON = "%s(this, com.alipay.mobile.antui.R.string.%s)"


def get_codeDict():
    code_to_res_dict = dict()
    with open(ARRAY_FILE, 'r') as f:
        for line in f.readlines():
            if line.strip().startswith('<string name='):
                name = line.split('\"')[1]
                code = line.split('&#x')[1].split(";")[0].upper()
                code_to_res_dict[code] = name
    return code_to_res_dict

CODE2RESOURCE = get_codeDict()


def get_exchangeDict():
	ui2antuiDict = {}
	with open(EXCHANGE_FILE, 'r') as f:
		for line in f.readlines():
			dictArray = line.split('|')
			des = dictArray[1]
			if des.startswith("E") :
				code = des.split('#')
				des = ICONFONT % (code[2], CODE2RESOURCE[code[0].upper().strip()])
			elif des.startswith("IconUtils"):
				code = des.split('#')
				if len(code) == 2:
					des = TITLEICON % (code[0], CODE2RESOURCE[code[1].upper().strip()])
			ui2antuiDict[dictArray[0]] = des	
	return ui2antuiDict

UI2ANTUIDICT = get_exchangeDict()


def isXmlContainsUse(filepath):
	xmlKey = '(@com.alipay.mobile.ui:.*?)"'
	myfile = open(filepath) 
	content = myfile.read()
	valueArray = re.findall(xmlKey,str(content))
	valueDict = dict()
	if len(valueArray) != 0:
		for value in valueArray:
			valueDict[value] = UI2ANTUIDICT[value.split('/')[-1]]
	
	return valueDict



def isJaveContainsUse(filepath):
	javeKey = '(com.alipay.mobile.ui.R..*?)[);]'
	myfile = open(filepath) 
	content = myfile.read()
	valueArray = re.findall(javeKey,str(content))
	valueDict = dict()
	if len(valueArray) != 0:
		for value in valueArray:
			valueDict[value] = UI2ANTUIDICT[value.split('.')[-1]]
	
	return valueDict



def getCommonuiUsed(dirpath): 
	for (dirp, dirnames, filenames) in os.walk(dirpath):  
		for fileName in filenames:  
			fullpath = dirp + "/" + fileName
			outpath = dirp.replace(dirpath, '') + "/" + fileName

			if fileName.endswith(".xml"):
				value1 = isXmlContainsUse(fullpath)
				if len(value1) != 0:
					yield outpath, value1
			elif fileName.endswith(".java"): 
				value2 = isJaveContainsUse(fullpath)
				if len(value2) != 0:
					yield outpath, value2


def getUsedDic(dirpath):
	useDict = dict()
	for (fileName, sourceArray) in getCommonuiUsed(dirpath):
		useDict[fileName] = sourceArray
	return useDict

if __name__=="__main__":
	# # try:
	for (fileName, sourceDict) in getCommonuiUsed('/Users/xuanmu/work/android-phone-fortunehome'):
		print fileName
		if sourceDict :
			for k,v in sourceDict.items():
				print k, v
	# print getUsedDic['/Users/xuanmu/work/android-phone-fortunehome'].keys()



	