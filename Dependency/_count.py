import MySQLdb

conn = MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='mysql1103',db ='dependency')

if __name__=="__main__":
	cur = conn.cursor()
	try:
		cur.execute('select * from dependency.class')
		classes=cur.fetchall()
		for _className in classes:
			sql = "select * from dependency.dependency where class = '%s'" % _className[0]
			count = cur.execute(sql)
			print _className[0], count
	except Exception, e:
		print(e)
	finally:
		cur.close()
		conn.commit()
		conn.close()
		print("finally")