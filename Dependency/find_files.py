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
	select_sql = "select * from dependency.class where class_name = '" + fileName + "'";
	c = conn.cursor()
	a = c.execute(select_sql)
	info =  c.fetchmany(a)
	print info,select_sql
	c.close()
	return len(info)

if __name__=="__main__":
	cur = conn.cursor()
	try:
		path = sys.argv[1]
		bundleName = "android-phone-antui"
		for name in _utils.getFileListWithJava(path):
			if not checkKey(name) == 0:
				continue
			try:
				sql="insert into dependency.class(class_name,bundle_name) values('"+ name +"','"+ bundleName +"')"
				print sql
				cur.execute(sql)
				print("inset class")
			except Exception, e:
				print("class error : " + e)
			dependency = global_check_used(name, bundleName)
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
						sql="insert into dependency(class,"+_type+",bundle) values('"+ name +"','"+ key +"','"+ value+"')"
						cur.execute(sql)
						print("inset dependency")
					except Exception, e:
						print("dependency error : " + e)
	except Exception, e:
		print(e)
	else:
		print("else")
	finally:
		cur.close()
		conn.commit()
		conn.close()
		print("finally")
