import httplib2
from bs4 import BeautifulSoup

def global_check_used(class_name, bundle_name):
	global_search_url = 'http://codesearch.alipay.net/search?project=Android_wallet_repo&q=' + class_name
	h = httplib2.Http()
	resp, content = h.request(global_search_url, "GET")
	soup = BeautifulSoup(content, "html.parser")
	results = soup.find(id="results")
	de = {}
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
				de[a_link.get_text()] = href[3]
	return de
