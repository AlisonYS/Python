from os import walk
import sys
import MySQLdb
import os 
import json

def TableToJson(): 
    # try:
	conn = MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='mysql1103',db ='dependency')
	cur = conn.cursor()
	sql = "SELECT pc.class_name AS name,pc.lineCount AS lineCount FROM dependency.class pc WHERE pc.description is not NULL"
	cur.execute(sql)
	data = cur.fetchall()
	cur.close()
	conn.close()
	jsonData = []
	for row in data:  
		result = {} 
		result['controlName'] = row[0].split('.')[0]  
		result['totalCodeLines'] = row[1]
		result['appstoreSize'] = ""
		result['binarySize'] = str(59.63*1024*float(row[1])/float(2385636))
		jsonData.append(result)
	return jsonData
	# except Exception, e:
	# 	print 'MySQL connect fail...'  
	# else:
	# 	jsondatar=json.dumps(jsonData,ensure_ascii=False)
	# 	return jsondatar[1:len(jsondatar)-1]
  
if __name__ == '__main__':  
	jsonData = TableToJson() 
	with open('getdata.js','w') as f:
		print jsonData
		json.dump(jsonData, f)