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
products1 = []
headers1=['link', 'Product type','Product Name','cat','Storage','Figures']


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
	specs = sope.find_all("div", attrs={"class":"pdp-pod-card__item"})
	for spec in specs:
		title = getNodeText(spec.find("div", attrs={"class":"pdp-specifications__name"}))
		value = getNodeText(spec.find("div", attrs={"class":"pdp-specifications__value"}))
		if len(title) >0:
			pInfo[title] = value
			addHeader(headers1, title)
	storage = sope.find("div", attrs={"class":"pdp-contents-and-storage"})
	if storage != None:
		pInfo["Storage"] = getNodeText(storage.find("div", attrs={"class":"c-card__description"}))

	figures = sope.find("div", attrs={"class":"pdp-figures__content"})
	if figures != None:
		imgs = figures.find_all("div", attrs={"class":"pdp-figures__image"})
		imgStr = ""
		for img in imgs:
			imgEn = img.find("img")
			imgName = imgEn["src"].split("/")[-1]
			httpUtils.urllib_download("https://www.thermofisher.cn"+imgEn["src"], imgName)
			imgStr += imgName+"|||"
		pInfo["Figures"] = imgStr



	products1.append(pInfo.copy())
	

def getProductList(url, type1):
	sope = httpUtils.getHtmlFromUrl(url)

	ps = sope.find_all("div", attrs={"class":"result catalog search-card active-prod-card OneLinkNoTx result-card catalog-card"})
	for p in ps:
			pLink = p.find("a")
			getProductInfo(pLink["href"], type1)
			


#thermofisher
# for pIndex in range(1,7):
# 	getProductList('https://www.thermofisher.cn/search/browse/category/cn/zh/90222235?viewtype=tableview&query=*%3A*&resultPage='+str(pIndex)+'&resultsPerPage=60','蛋白标记试剂')

# for pIndex in range(1,3):
# 	getProductList('https://www.thermofisher.cn/search/browse/category/cn/zh/90222233?viewtype=tableview&query=*%3A*&resultPage='+str(pIndex)+'&resultsPerPage=60','交联试剂')

# getProductList('https://www.thermofisher.cn/search/browse/category/cn/zh/90222237?viewtype=tableview&query=*%3A*&resultPage=1&resultsPerPage=60','蛋白修饰试剂')
# getProductList('https://www.thermofisher.cn/search/browse/category/cn/zh/90332038?viewtype=tableview&query=*%3A*&resultPage=1&resultsPerPage=60','蛋白质和抗体标记试剂盒')
# getProductList('https://www.thermofisher.cn/search/browse/category/cn/zh/90227192?viewtype=tableview&query=*%3A*&resultPage=1&resultsPerPage=60','Tandem Mass Tag 试剂')
getProductInfo("https://www.thermofisher.cn/order/catalog/product/A20100?SID=srch-srp-A20100", "ss")




excelUtils.generateExcelMultipleSheet('thermofisher.xlsx', [
	{
		"name":"thermofisher",
		"header": headers1,
		"data": products1
	}
])