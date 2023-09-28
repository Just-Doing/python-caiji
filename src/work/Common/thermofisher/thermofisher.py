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
headers1=['link', 'Product type','Product Name','cat']


def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, type1):
	print(str(len(products1)) + "==" + url)
	sope = httpUtils.getHtmlFromUrl(url)

	pInfo = {
		"link": url,
		"Product type": type1,
		"Product Name": getNodeText(sope.find("div", attrs={"class":"pdp-product-summary__product-title"})),
		"cat": getNodeText(sope.find("div", attrs={"class":"pdp-product-summary__catalog-number"})),
	}

	products1.append(pInfo.copy())
	

def getProductList(url, type1):
	sope = httpUtils.getHtmlFromUrl(url)

	ps = sope.find_all("div", attrs={"class":"result catalog search-card active-prod-card OneLinkNoTx result-card catalog-card"})
	for p in ps:
			pLink = p.find("a")
			getProductInfo(pLink["href"], type1)
			


#thermofisher
for pIndex in range(1,7):
	getProductList('https://www.thermofisher.cn/search/browse/category/cn/zh/90222235?viewtype=tableview&query=*%3A*&resultPage='+str(pIndex)+'&resultsPerPage=60','蛋白标记试剂')

for pIndex in range(1,3):
	getProductList('https://www.thermofisher.cn/search/browse/category/cn/zh/90222233?viewtype=tableview&query=*%3A*&resultPage='+str(pIndex)+'&resultsPerPage=60','交联试剂')

getProductList('https://www.thermofisher.cn/search/browse/category/cn/zh/90222237?viewtype=tableview&query=*%3A*&resultPage=1&resultsPerPage=60','蛋白修饰试剂')
getProductList('https://www.thermofisher.cn/search/browse/category/cn/zh/90332038?viewtype=tableview&query=*%3A*&resultPage=1&resultsPerPage=60','蛋白质和抗体标记试剂盒')
getProductList('https://www.thermofisher.cn/search/browse/category/cn/zh/90227192?viewtype=tableview&query=*%3A*&resultPage=1&resultsPerPage=60','Tandem Mass Tag 试剂')





excelUtils.generateExcelMultipleSheet('thermofisher.xlsx', [
	{
		"name":"thermofisher",
		"header": headers1,
		"data": products1
	}
])