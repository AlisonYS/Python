from os import walk
import sys
import os 
import logging
from _code_search import global_check_used
import _utils
import _dbUtils
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')


def insertDependency(de_tableName, resouceName, searchName, bundleName):
	dependency = global_check_used(searchName, bundleName) 
	if dependency is not None:
		for key, value in dependency.items():
			if key.endswith(".xml"):
				_type = 'xml'
			elif key.endswith(".java"):
				_type = 'java'
			else:
				_type = 'other'
			_dbUtils.insertDependencyTable(de_tableName, resouceName, _type, key, value)
	else:
		_dbUtils.insertDependencyTable(de_tableName, resouceName, 'other', '', 'null')


if __name__=="__main__":
	# try:
	path = sys.argv[1]
	bundleName = "mpaas-ui"
	resouce_tableName = "mpaasUi_resouce"
	dependency_tableName = "mpaasUi_resouce_dependency"

	_dbUtils.creatResourceTable(resouce_tableName)
	_dbUtils.creatDependencyTable(dependency_tableName)


	# insertDependency(dependency_tableName, 'text_green_16', '@com.alipay.mobile.ui:style/text_green_16', bundleName)

	for name,xmlName,javaName in _utils.getPubliceResource(path):
		if _dbUtils.checkKey(resouce_tableName, name) is not 0:
			_dbUtils.updateResourceTable(resouce_tableName, name, xmlName, javaName)
			insertDependency(dependency_tableName, name, xmlName, bundleName)
			insertDependency(dependency_tableName, name, javaName, bundleName)
			continue
		try:
			_dbUtils.insertResourceTable(resouce_tableName, name, xmlName, javaName)
			insertDependency(dependency_tableName, name, xmlName, bundleName)
			insertDependency(dependency_tableName, name, javaName, bundleName)
		except Exception, e:
			print("class error : " + e)


	_dbUtils.closeCursor()
