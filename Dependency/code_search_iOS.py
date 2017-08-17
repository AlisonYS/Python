from os import walk
import sys
import MySQLdb
import os 
import logging
from _code_search import global_check_used
import _utils
import json

conn = MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='mysql1103',db ='dependency')

def checkKey(fileName):
	select_sql = "select * from dependency.class where class_name = '" + fileName + "'";
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
				if key.endswith(".m"):
					_type = 'm'
				elif key.endswith(".h"):
					_type = 'h'
				else:
					_type = 'other'
				sql="insert into ios_dependency(class,"+_type+",bundle) values('"+ class_name +"','"+ key +"','"+ value+"')"
				print sql
				cur.execute(sql)
				print("inset dependency")
			except Exception, e:
				print("dependency error : " + e)
	else:
		print("global_check is None")


if __name__=="__main__":
	cur = conn.cursor()
	bundleName = "ios-phone-antui"

	ios_file = open("jsonControlList.txt")
	lines = ios_file.readlines()
	# for line in lines:
	# 	insertDependency(line,line,bundleName)


	
	jsonData = []
	for line in lines: 
		result = {} 
		name = line
		dependency_sql = "select * from dependency.ios_dependency where class = '%s' and bundle != 'ios-phone-antuidemo' and other is NULL" % name 
		print dependency_sql
		count = cur.execute(dependency_sql)
		result['controlName'] = name.split('"')[1]
		result['alipayDependency'] = str(count)
		jsonData.append(result)

	with open('jsonDependency.txt','w') as f:
		print jsonData 
		json.dump(jsonData, f)

	
	cur.close()
	conn.commit()
	conn.close()