# encoding: utf-8  

from os import walk
import sys
import os 
import re


FILE_NAME = "/android/%s.md"
INTER_CONT = "接口说明\n\n```\n%s\n```\n\n#"
DEMO_CONT = "示例\n\n```\n%s\n```"
DEMO_ACTIVITY_KEY = '%s start \*\*/(.*[\s\S]*?)/\*\* %s end'
DEMO_XML_KEY = '%s start -->(.*[\s\S]*?)<!-- %s end'

def writeFile(fileName, content):
    wr = open(fileName, 'w')
    wr.write(content)
    wr.close()


def readFile(fileName):
    demeFile = open(fileName)
    content = demeFile.read()
    return content


def findFirstPattern(pattern, content):
	find = re.findall(pattern, str(content))
	if len(find) != 0:
		return find[0]
	return ""

def replaceFile(fileName, inter, demo):
	interfacePattern = '接口[\s\S]*?\#'
	demoPattern = '示例[\s\S]*```'
	currentContent = readFile(fileName)

	# 替换接口
	strinfo = re.compile(interfacePattern)
	currentContent = strinfo.sub( INTER_CONT % inter, currentContent)

	# 替换demo
	strinfo2 = re.compile(demoPattern)
	currentContent = strinfo2.sub( DEMO_CONT % demo, currentContent)

	writeFile(fileName, currentContent)



def getFileListWithJava(path): 
	activityPattern = '@activity : (.*)'
	xmlPattern = '@xml : (.*)'
	desPattern = '@name : (.*)'
	outputPattern = '@output : (.*)'
	interfacePattern = '@interface[\s\S]*?\)'

	for (dirpath, dirnames, filenames) in walk(path):
		for name in filenames:
			if name.endswith(".java") and (name is not "R.java"):
				myfile = open(dirpath +"/"+ name) 
				content = myfile.read()
				isoutput = findFirstPattern(outputPattern, content)
				if isoutput == 'true':
					des = findFirstPattern(desPattern, content)
					demoActivity = findFirstPattern(activityPattern, content)
					demoXml = findFirstPattern(xmlPattern, content)
					interfaceArray = re.findall(interfacePattern, str(content))
					yield name.split('.')[0], des, interfaceArray, demoXml, demoActivity


def getActivityDemoInfo(srcDir, mdName, demoActivity):
	if demoActivity == "":
		return ""
	key = DEMO_ACTIVITY_KEY % (mdName, mdName)
	print demoActivity
	demoActivity = demoActivity + ".java"

	for (dirpath, dirnames, filenames) in walk(srcDir + '/antui/test/src'):
		for name in filenames:
			if name == demoActivity:
				myfile = open(dirpath +"/"+ name) 
				content = myfile.read()
				demoArray = re.findall(key, str(content))
				if len(demoArray) != 0:
					alldemo = ""
					for demo in demoArray:
						alldemo += demo + '\n'
					return alldemo
				else:
					break

	return ""


def getXmlDemoInfo(srcDir, mdName, demoXml):
	if demoXml == "":
		return ""
	key = DEMO_XML_KEY % (mdName, mdName)
	print demoXml
	demoXml = demoXml + ".xml"

	for (dirpath, dirnames, filenames) in walk(srcDir + '/antui/test/res'):
		for name in filenames:
			if name == demoXml:
				myfile = open(dirpath +"/"+ name) 
				content = myfile.read()
				demoArray = re.findall(key, str(content))
				if len(demoArray) != 0:
					alldemo = ""
					for demo in demoArray:
						alldemo += demo + '\n'
					return alldemo
			break

	return ""


def writeAutoDoc(docDir, srcDir):
	demoStr = readFile("demo.md")
	order = 1
	for (mdName, nameDes, interfaceArray, demoXml, demoActivity) in getFileListWithJava(srcDir + '/antui/api/src'):
		print mdName, nameDes
		allinter = ""
		for interface in interfaceArray:
			allinter += '    /**\n     * ' + interface + '\n\n'

		demo = getXmlDemoInfo(srcDir, mdName, demoXml)
		demo = demo + '\n'
		demo = demo + getActivityDemoInfo(srcDir, mdName, demoActivity)
		
		fileName = docDir + FILE_NAME % mdName.lower()
		if os.path.exists(fileName):
			replaceFile(fileName, allinter, demo)
		else:
			writeStr = demoStr % (order, mdName, nameDes, allinter, demo)
			writeFile(fileName, writeStr)

		order += 1


if __name__=="__main__":
	docDir = '/Users/xuanmu/work/antui-client-docs'
	srcDir = '/Users/xuanmu/work/android-phone-antui'
	writeAutoDoc(docDir, srcDir)
	
	