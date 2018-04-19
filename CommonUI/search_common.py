from os import walk
import sys
import os 
import re


def isXmlContainsUse(filepath):
	xmlKey = '(@com.alipay.mobile.ui:.*?)"'
	myfile = open(filepath) 
	content = myfile.read()
	valueArray = re.findall(xmlKey,str(content))
	return valueArray



def isJaveContainsUse(filepath):
	javeKey = '(com.alipay.mobile.ui.R..*?)[);]'
	myfile = open(filepath) 
	content = myfile.read()
	valueArray = re.findall(javeKey,str(content))
	return valueArray



def getCommonuiUsed(dirpath): 

	xmlArray = []
	for (dirpath, dirnames, filenames) in os.walk(dirpath):  
		for fileName in filenames:  
			fullpath = dirpath + "/" + fileName

			if fileName.endswith(".xml"):
				value1 = isXmlContainsUse(fullpath)
				if len(value1) != 0:
					print fullpath, value1
			elif fileName.endswith(".java"): 
				value2 = isJaveContainsUse(fullpath)
				if len(value2) != 0:
					print fullpath, value2


if __name__=="__main__":
	# try:
	getCommonuiUsed('/Users/xuanmu/work/android-phone-fortunehome/tabmanager')
