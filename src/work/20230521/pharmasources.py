from itertools import product
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
import re
sys.path.append('../..')
from lib import excelUtils
from lib import httpUtils
from lib import textUtil
from lib.htmlEleUtils import getNodeText
from lib.htmlEleUtils import getInnerHtml
products1 = []
customerHeader = []
sizeHeader=[]

def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, type):
	print(str(len(products1)) + "==" + url)
	sope = httpUtils.getHtmlFromUrl(url)

	pInfo = {
		"link": url,
		"type":type
	}
	ps = sope.find_all("p", class_="t6")
	for p in ps:
		title = getNodeText(p)
		if title == "EC Number":
			pInfo["EC Number"] =  getNodeText(p.nextSibling)
	lis = sope.find_all("li")
	for li in lis:
		title = getNodeText(li)
		titles = title.split(":")
		if len(titles) > 3:
			t1 = titles[0]
			v1 = titles[1]
			t2 = titles[2]
			v2 = titles[3]
			pInfo[t1] = v1
			pInfo[t2] = v2
			addHeader( headers, t1)
			addHeader(headers, t2)
		else:
			if len(titles) > 1:
				t1 = titles[0]
				v1 = titles[1]
				pInfo[t1] = v1
				addHeader( headers, t1)
		


	products1.append(pInfo.copy())

def getProductList(url, type):
	sope = httpUtils.getJson(url)
	data = json.loads(sope)

	for p in data["posts"]:
		href= "https://sekisuidiagnostics.com/products/"+p["post_name"]
		if len(p["post_name"]) > 0:
			getProductInfo(href, type)
			

headers=['link', 'type']


# for pIndex in range(1, 10):
# 	getProductList("https://sekisuidiagnostics.com/wp-json/post-filters-archive/get-posts?post_type=sek_product&posts_per_page=12&paged="+str(pIndex)+"&tax[product_category]=19&orderby=title&order=ASC",'Pharmaceutical Intermediates')

with open("G:\git\python-caiji\src\work\test\tes.json") as f: 

	print(f["posts"])
# getProductInfo("https://sekisuidiagnostics.com/product/12a-hydroxysteroid-dehydrogenase/","ttt")


excelUtils.generateExcelMultipleSheet('sekisuidiagnostics.xlsx', [
	{
		"name":"sekisuidiagnostics",
		"header": headers ,
		"data": products1
	}
])