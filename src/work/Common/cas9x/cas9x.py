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
		'link','产品货号：', '产品价格：'
	]

def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, pInfo):
	print(str(len(products1))+"====="+url)
	sope = httpUtils.getHtmlFromUrl(url)
	pAreas = sope.find_all("p")
	spans = sope.find_all("span")
	for span in spans+pAreas:
		strongs = span.find_all("strong")
		if len(strongs) == 2:
			title = getNodeText(strongs[0])
			value = getNodeText(strongs[1])
			if "产品价格：" in title:
				pInfo["产品价格："] = value.replace("产品价格：","")
			else:
				pInfo[title] = value
		if len(strongs) == 1:
			title = getNodeText(strongs[0])
			if "产品价格：" in title:
				pInfo["产品价格："] = title.replace("产品价格：","")

	infos = sope.find("div", attrs={"class":"info-content"}).find_all("p")
	for info in infos:
		title=getNodeText(info.find("strong"))
		if len(title) >0:
			value = getNodeText(info).replace(title, "")
			if len(value) >0:
				pInfo[title] = value
				addHeader(headers1, title)
	products1.append(pInfo.copy())



def getProductList(url):
	sope = httpUtils.getHtmlFromUrl(url)
	ps = sope.find("div", attrs={"class":"bdxbpro-nei"}).find_all("li")
	for p in ps:
		pLink = p.find("a")
		pInfo = {
			"Product Name": getNodeText(pLink)
		}
		getProductInfo(pLink["href"], pInfo)
		
		
for pIndex in range(1, 21):
	getProductList('http://www.cas9x.com/bdxb/jybjxbzxh?page='+str(pIndex))


# getProductInfo('http://www.modelorg.us/portal/article/index/id/43653/post_type/3.html',{"cat":"ab255433"})
excelUtils.generateExcelMultipleSheet('cas9x.xlsx', [
	{
		"name": 'cas9x',
		"header": headers1 ,
		"data": products1
	}
])