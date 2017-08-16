# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CodesearchPipeline(object):

	def __init__(self,dbpool):
        self.dbpool=dbpool

	@classmethod
	def from_settings(cls,settings):
		dbparams = dict(
				host=settings['MYSQL_HOST'],#读取settings中的配置
	            db=settings['MYSQL_DBNAME'],
	            user=settings['MYSQL_USER'],
	            passwd=settings['MYSQL_PASSWD'],
	            charset='utf8',#编码要加上，否则可能出现中文乱码问题
	            cursorclass=MySQLdb.cursors.DictCursor,
	            use_unicode=False,
			)
		dbpool=adbapi.ConnectionPool('MySQLdb',**dbparams)#**表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)#相当于dbpool付给了这个类，self中可以得到

    def process_item(self, item, spider):
        query=self.dbpool.runInteraction(self._conditional_insert,item)#调用插入的方法
        query.addErrback(self._handle_error,item,spider)#调用异常处理方法
        return item

    def _conditional_insert(self,tx,item):
        #print item['name']
        sql="insert into dependency(name,url) values(%s,%s)"
        params=(item["name"],item["url"])
        tx.execute(sql,params)