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
		'link','cat','price', 'Description','pdf'
	]

def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, pInfo):
	print(str(len(products1))+"====="+url)
	sope = httpUtils.getRenderdHtmlFromUrl(url)
	description = sope.find("div", attrs={"itemprop":"name"})
	descriptionStr = getNodeText(description).replace(getNodeText(description.find("b")), "")
	
	pInfo["Description"] = descriptionStr
	specArea = sope.find("table", attrs={"class":"table table-bordered table-striped attribute"})
	specs = specArea.find("tbody").find_all("tr")
	for tr in specs:
		tds = tr.find_all("td")
		if len(tds) > 1:
			title = getNodeText(tds[0])
			value = getNodeText(tds[1])
			if len(title) > 0:
				pInfo[title] = value
				addHeader(headers1, title)
	if "Microarray Panel" in pInfo:
		pInfo["Description"] += "\r\n" + pInfo["Microarray Panel"]

	sheetArea = sope.find("div", attrs={"class":"wishlist-compare"})
	if sheetArea != None:
		links = sheetArea.find_all("a")
		for link in links:
			linkName = getNodeText(link)
			if "Convert Specs to Excel" in linkName :
				href = link["onclick"].replace("javascript:window.open('", "").replace("', '_blank');","")
				pInfo["pdf"] = pInfo["cat"]+" specs.xlsx"
				httpUtils.urllib_download("https://www.tissuearray.com/"+href, pInfo["pdf"])

	products1.append(pInfo.copy())
	excelUtils.generateExcelMultipleSheet('tissuearray.xlsx', [
	{
		"name": 'tissuearray',
		"header": headers1 ,
		"data": products1
	}
])



def getProductList(url):
	sope = httpUtils.getHtmlFromUrl(url)
	ps = sope.find("table", attrs={"class":"table table-bordered table-striped table-hover list"}).find("tbody").find_all("tr")
	print(str(len(ps)))
	for p in ps:
		tds = p.find_all("td")
		pLink = tds[5].find("a")
		if pLink["title"] == 'In Stock':
			pInfo = {
				"link":url,
				"cat": getNodeText(tds[1]),
				"price": getNodeText(tds[5])
			}
			getProductInfo(pLink["href"], pInfo)
		


# getProductList('https://www.tissuearray.com/tissue-arrays?limit=%3E100')

getProductList('https://www.tissuearray.com/Dog_Arrays')

getProductList('https://www.tissuearray.com/Monkey-Arrays')


getProductList('https://www.tissuearray.com/Mouse-Arrays')
getProductList('https://www.tissuearray.com/Rat-Arrays')
# for pIndex in range(1, 15):
# 	getProductList('https://www.tissuearray.com/tissue-arrays?page='+str(pIndex))


# getProductInfo('https://www.tissuearray.com/tissue-arrays/Adrenal_Gland/AD2081a',{"cat":"ab255433"})
excelUtils.generateExcelMultipleSheet('tissuearray.xlsx', [
	{
		"name": 'tissuearray',
		"header": headers1 ,
		"data": products1
	}
])