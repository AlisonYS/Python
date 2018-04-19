from os import walk
import re

def getFileListWithJava(path): 
	for (dirpath, dirnames, filenames) in walk(path):
		for name in filenames:
			if name.endswith(".java") and (name is not "R.java"):
				myfile = open(dirpath +"/"+ name) 
				content = myfile.readlines()
				for line in content:
					if line.startswith('package '):		
						_str = line[line.find('package ') + len('package '):-2]
						package_name = '"' + _str + '.' + name[0:-5] +'"'
				lines = len(content) 
				print name,lines,package_name
				yield name,lines,package_name


# "@com.alipay.mobile.ui:drawable/announcement_close_normal"
# "com.alipay.mobile.ui.R.drawable.qr_default"

def getPubliceResource(filepath): 
	myfile = open(filepath) 
	content = myfile.readlines()
	xml_name = '@com.alipay.mobile.ui:%s/%s'
	java_name = 'com.alipay.mobile.ui.R.%s.%s'
	for line in content:
		typeArray = re.findall('type="(.*?)"',line)
		nameArray = re.findall('name="(.*?)"',line)
		if len(typeArray) != 0:
			r_type = typeArray[0]
			r_name = nameArray[0]
			if (r_type != 'attr'):
				xml = '"' + xml_name % (r_type, r_name) + '"'
				java = '"' + java_name % (r_type, r_name) + '"'
				yield r_name, xml, java
	

if __name__ == '__main__':
	for resourc, xml,java, in getPubliceResource("/Users/xuanmu/work/mpaas-ui/ui/widget/res/values/public.xml"):
		print resourc, xml, java

