from os import walk
import sys
import MySQLdb
import os 
import logging
from _code_search import global_check_used
import _utils
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')

conn = MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='mysql1103',db ='dependency')

def checkKey(fileName):
	select_sql = "select * from dependency.ui_class where class_name = '" + fileName + "'";
	c = conn.cursor()
	a = c.execute(select_sql)
	info =  c.fetchmany(a)
	c.close()
	print len(info),'>>>>>>>>>>>>>>>>>'
	return len(info)

def insertDependency(class_name, package_name, bundle_name):
	dependency = global_check_used(package_name, bundle_name)
	if dependency is not None:
		for key, value in dependency.items():
			print(key + ":" + value)
			try:
				if key.endswith(".xml"):
					_type = 'xml'
				elif key.endswith(".java"):
					_type = 'java'
				else:
					_type = 'other'
				sql="insert into ui_dependency(class,"+_type+",bundle) values('"+ class_name +"','"+ key +"','"+ value+"')"
				print sql
				cur.execute(sql)
				print("inset dependency")
			except Exception, e:
				print("dependency error : " + e)
	else:
		print("global_check is None")


if __name__=="__main__":
	cur = conn.cursor()
	# try:
	path = sys.argv[1]
	bundleName = "mpaas-ui"
	for name,lineCount,packageName in _utils.getFileListWithJava(path):
		if checkKey(name) is not 0:
			sql="UPDATE dependency.ui_class SET packageName = '%s', lineCount = '%s' WHERE class_name ='%s'"
			cur.execute(sql % (packageName,lineCount,name))
			continue
		try:
			sql="INSERT into dependency.ui_class(class_name,bundle_name,lineCount) values ('%s','%s','%s')"
			print sql % (name,bundleName,lineCount)
			cur.execute(sql % (name,bundleName,lineCount))
			print("inset class")
		except Exception, e:
			print("class error : " + e)

	
	sql = "SELECT pc.class_name, pc.packageName FROM dependency.ui_class pc"
	cur.execute(sql)
	data = cur.fetchall()
	for row in data:  
		insertDependency(row[0],row[1],bundleName)

	
	cur.close()
	conn.commit()
	conn.close()
