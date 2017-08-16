import scrapy

class CodeSearchSpider(scrapy.Spider):
	name="CodeSearch"
	start_urls = ['http://codesearch.alipay.net/source/search?project=Android_wallet_master&q=%s&n=%s&start=0',]

	def start_request(self):
		for url in start_urls:
			
	def parse(self,response):
