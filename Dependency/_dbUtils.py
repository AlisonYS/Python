import MySQLdb
conn = MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='mysql1103',db ='dependency')
dbcur = conn.cursor()

def closeCursor():
	dbcur.close()
	conn.commit()
	conn.close()

def creatResourceTable(re_tablename):
    creat = "CREATE TABLE if not exists dependency.%s (resouceName VARCHAR(45) NOT NULL, resouceXmlName VARCHAR(100) NOT NULL, resouceJavaName VARCHAR(100) NOT NULL,PRIMARY KEY (resouceName))";   
    dbcur.execute(creat % re_tablename)


def updateResourceTable(re_tablename, resouceName, resouceXmlName, resouceJavaName):
    sql = "update dependency.%s SET resouceJavaName = '%s', resouceXmlName = '%s' WHERE resouceName = '%s'"
    dbcur.execute(sql % (re_tablename, resouceJavaName, resouceXmlName, resouceName))


def insertResourceTable(re_tablename, resouceName, resouceXmlName, resouceJavaName):
    sql="insert into dependency.%s(resouceName,resouceXmlName,resouceJavaName) values ('%s','%s','%s')"
    dbcur.execute(sql % (re_tablename, resouceName, resouceXmlName, resouceJavaName))


def creatDependencyTable(de_tablename):
    creat = "CREATE TABLE if not exists dependency.%s (id INT, resouceName VARCHAR(100) NOT NULL, xml VARCHAR(100) NULL, java VARCHAR(100) NULL, other VARCHAR(100) NULL, bundle VARCHAR(100) NOT NULL, PRIMARY KEY (id))";   
    dbcur.execute(creat % de_tablename)


def checkKey(tablename, resouceName):
	c = conn.cursor()
	select_sql = "select * from dependency.%s where resouceName = '%s'"
	a = c.execute(select_sql % (tablename, resouceName))
	info =  c.fetchmany(a)
	c.close()
	print resouceName, len(info),'>>>>>>>>>>>>>>>>>'
	return len(info)


def checkDependencyBundleNull(de_tablename, resouceName):
	select_sql = "select * from dependency.%s where resouceName = '%s' and bundle ='null'"
	a = dbcur.execute(select_sql % (de_tablename, resouceName))
	info =  dbcur.fetchmany(a)
	print resouceName, len(info),'>>>>>>>>>>>>>>>>>'
	return len(info)

def insertDependencyTable(de_tablename, resouceName, de_type, de_key ,de_bundles):
	if checkKey(de_tablename, resouceName) == 0:
		sql="insert into dependency.%s(resouceName, %s, bundle) values('%s','%s','%s')"
		dbcur.execute(sql % (de_tablename, de_type, resouceName, de_key, de_bundles))
		print("inset dependency : " + resouceName)
	else:
		if checkDependencyBundleNull(de_tablename, resouceName) != 0:
			sql="update dependency.%s SET %s = '%s', bundle = '%s' WHERE resouceName = '%s' and bundle ='null'"
			dbcur.execute(sql % (de_tablename, de_type, de_key, de_bundles, resouceName))
			print("update dependency : " + resouceName)
		elif de_bundles != 'null':
			sql="insert into dependency.%s(resouceName, %s, bundle) values('%s','%s','%s')"
			dbcur.execute(sql % (de_tablename, de_type, resouceName, de_key, de_bundles))
			print("inset dependency : " + resouceName)





if __name__ == '__main__':
	checkTableExists('checkTableExists')
