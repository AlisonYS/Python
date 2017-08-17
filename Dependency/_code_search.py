import httplib2
import urllib
from bs4 import BeautifulSoup

def global_check_used(class_name, bundle_name):
	max = 0	
	de = {}
	global_search_url = 'http://codesearch.alipay.net/source/search?project=Android_wallet_master&q=%s&n=%s&start=0'
	h = httplib2.Http()
	__str = global_search_url % (urllib.quote(class_name), "")
	print __str
	resp, content = h.request(__str, "GET")
	soup = BeautifulSoup(content, "html.parser")
	results = soup.find(id="results")
	if not results:
		print('check size not result')
		return de
	sizeSet = results.find_all('p', class_="pagetitle")
	if sizeSet is None or len(sizeSet) is 0:
		print('none result when global search size' + class_name + "--" + bundle_name)
	else:
		for result in sizeSet:
			bold = result.find_all('b')
			if len(bold) > 2:
				max = int(bold[2].text)

	if max is 0:
		dependencySet = results.find_all('td', class_="f")
		if dependencySet is None or len(dependencySet) is 0:
			print('none result when global search ' + class_name + "--" + bundle_name)
		else:
			for dependency in dependencySet:
				a_link = dependency.a
				href = a_link.get('href').split('/')
				if href[4]!= bundle_name:
					de[a_link.get_text()] = href[4]
		return de

	else:
		resp, content = h.request(global_search_url % (urllib.quote(class_name), str(max)), "GET")
		soup = BeautifulSoup(content, "html.parser")
		totalResults = soup.find(id="results")
		if not totalResults:
			print('check maxLine not totalResults')
		totalSet = totalResults.find_all('td', class_="f")
		if totalSet is None or len(totalSet) is 0:
			print('none result when global search ' + class_name + "--" + bundle_name)
		else:
			for single in totalSet:
				a_link = single.a
				href = a_link.get('href').split('/')
				if href[4] is not bundle_name:
					de[a_link.get_text()] = href[4]
		return de
	return de

