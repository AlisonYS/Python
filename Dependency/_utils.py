from os import walk

def getFileListWithJava(path): 
	f = []
	for (dirpath, dirnames, filenames) in walk(path):
		for name in filenames:
			if name.endswith(".java") and (name is not "R.java"):
				f.append(name)
	return f