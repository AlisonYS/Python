import os 
import sys
import httplib2
from bs4 import BeautifulSoup

def global_check_used(class_name,bundle_name):
    global_search_url = 'http://codesearch.alipay.net/search?project=Android_wallet_repo&q=' + class_name
    h = httplib2.Http()
    resp, content = h.request(global_search_url, "GET")
    soup = BeautifulSoup(content, "html.parser")
    results = soup.find(id="results")
    if not results:
        print('not result')
    resultSet = results.find_all('td', class_="f")
    if resultSet == None or len(resultSet) == 0:
        print('none result when global search ' + class_name + "--" + bundle_name)
    else:
        for result in resultSet:
            a_link = result.a
            href = a_link.get('href').split('/')
            if href[3]!= bundle_name:
                print(href[3] + " " + a_link.get_text())

def get_bundle_onwer(bundle_name):
    owner_url = 'https://huoban.alipay.com/module/index.htm?productName=wallet&toPage=1&searchKeyword=' + bundle_name
    h = httplib2.Http()
    resp, content = h.request(owner_url, "GET")
    print(resp)
    soup = BeautifulSoup(content, "html.parser")
    results = soup.find(id="results")

try :
    global_check_used("com.alipay.mobile.antui.dialog.AUListDialog","android-phone-antui")
except :
    print('Input Error!')

import MySQLdb

conn= MySQLdb.connect(
                      host='localhost',
                      port = 3306,
                      user='root',
                      passwd='123456',
                      db ='test',
                      )
cur = conn.cursor()

#创建数据表
#cur.execute("create table student(id int ,name varchar(20),class varchar(30),age varchar(10))")

#插入一条数据
#cur.execute("insert into student values('2','Tom','3 year 2 class','9')")


#修改查询条件的数据
#cur.execute("update student set class='3 year 1 class' where name = 'Tom'")

#删除查询条件的数据
#cur.execute("delete from student where age='9'")

cur.close()
conn.commit()
conn.close()
