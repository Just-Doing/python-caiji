from itertools import product
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
import re
sys.path.append('../../..')
from lib import excelUtils
from lib import httpUtils
from lib import textUtil
from lib.htmlEleUtils import getNodeText
from lib.htmlEleUtils import getInnerHtml
import math
products1 = []

headers1=[
		'link','Breadcrumb','Product Name','size/price','Category'
	]

def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url):
	print(str(len(products1))+"====="+url)
	sope = httpUtils.getHtmlFromUrl(url)
	nav = sope.find("div", attrs={"class":"breadcrumbs"})
	pInfo={
		"link":url
	}
	pInfo["Breadcrumb"] = getNodeText(nav)

	
	pInfo["Product Name"] = getNodeText(sope.find("h1", attrs={"class":"page-title"}))
	attrs = sope.find_all("div", attrs={"class":"product attribute sku"})
	for attr in attrs:
		title = getNodeText(attr.find("strong"))
		value = getNodeText(attr.find("div", attrs={"class":"value"}))
		pInfo[title] = value
		addHeader(headers1, title)

	sizes = sope.find_all("div", attrs={"class":"field choice admin__field admin__field-option required"})
	sizeStr = ""
	for size in sizes:
		option = size.find("input")
		sizeStr += getNodeText(size.find("label")) + "-" + option["price"]+","
	pInfo["size/price"] = sizeStr

	category = sope.find("div", attrs={"class":"product category"})
	pInfo["Category"] = getNodeText(category.find("div", attrs={"class":"value"}))

	trs = sope.find_all("tr")
	for tr in trs:
		tds = tr.find_all("td")
		ths = tr.find_all("th")
		if len(tds) == 1 and len(ths) == 1:
			title = getNodeText(ths[0])
			value = getNodeText(tds[0])
			pInfo[title] = value
			addHeader(headers1, title)



	products1.append(pInfo.copy())



def getProductList(url):
	sope = httpUtils.getHtmlFromUrl(url)
	ps = sope.find_all("li", attrs={"class":"item product product-item"})
	for p in ps:
		pLink = p.find("a")
		getProductInfo(pLink["href"])
		
		

for pIndex in range(1, 9):
	getProductList('https://www.arp1.com/catalogsearch/result/index/?p='+str(pIndex)+'&product_list_limit=100&q=autoimmune')


# getProductInfo('https://www.arp1.com/aire-antibody-csb-pa001502ha01hu.html')
excelUtils.generateExcelMultipleSheet('arp1.xlsx', [
	{
		"name": 'arp1',
		"header": headers1 ,
		"data": products1
	}
])