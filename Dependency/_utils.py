from os import walk

def getFileListWithJava(path): 
	for (dirpath, dirnames, filenames) in walk(path):
		for name in filenames:
			if name.endswith(".java") and (name is not "R.java"):
				myfile = open(dirpath +"/"+ name) 
				content = myfile.readlines()
				for line in content:
					if line.startswith('package '):		
						_str = line[line.find('package ') + len('package '):-2]
						package_name = _str + '.' + name[0:-5]
				lines = len(content) 
				print name,lines,package_name
				yield name,lines,package_name
	

if __name__ == '__main__':
	for name,lines,pkg_name in getFileListWithJava("/Users/xuanmu/work/android-phone-antui/antui/api/src"):
		print name,lines,pkg_name
