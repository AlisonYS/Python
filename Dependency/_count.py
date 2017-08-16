import MySQLdb

conn = MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='mysql1103',db ='dependency')

if __name__=="__main__":
	cur = conn.cursor()
	try:
		cur.execute("select * from dependency.class where bundle_name = 'mpaas-ui'")
		classes=cur.fetchall()
		for _className in classes:
			sql = "select * from dependency.dependency where class = '%s'" % _className[0]
			count = cur.execute(sql)
			dependencys = cur.fetchall()
			dependency_str = ""
			for _dependency in dependencys:
				dependency_str += _dependency[7] + ","
			print _className[0], count, dependency_str
	except Exception, e:
		print(e)
	finally:
		cur.close()
		conn.commit()
		conn.close()
		print("finally")