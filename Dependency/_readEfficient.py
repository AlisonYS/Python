import json
import time
import MySQLdb


def store(data):
    with open('jsonEfficientAndroid.json', 'w') as json_file:
        json_file.write(json.dumps(data))

def load():
    with open('jsonEfficientAndroid.json') as json_file:
        fileJson = json.load(json_file)
        return fileJson

if __name__ == "__main__":
    result = load()
    conn = MySQLdb.connect(host='localhost',port = 3306,user='root',passwd='mysql1103',db ='dependency')
    cur = conn.cursor()

    for fileJson in result:
        uedDevTimeConsume = "'" + fileJson["uedDevTimeConsume"] + "'" 
        developTimeConsume = "'" + fileJson["developTimeConsume"]+ "'" 
        testTimeConsume = "'" + fileJson["testTimeConsume"]+ "'" 
        name = "'" + fileJson["controlName"]+ ".java'" 
        uedCheckUponTimeConsume = "'" + fileJson["uedCheckUponTimeConsume"]+ "'" 
        pdTimeConsume = "'" + fileJson["pdTimeConsume"]+ "'" 
        sql = "UPDATE class SET uedDevTimeConsume = " + uedDevTimeConsume + ", developTimeConsume = " + developTimeConsume+ ", testTimeConsume = " + testTimeConsume + ", uedCheckUponTimeConsume = " + uedCheckUponTimeConsume+ ", pdTimeConsume = " + pdTimeConsume+ " where class_name = " + name
        cur.execute(sql)
        print sql

