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
		'link','cat','Product Name', 'Size','Description','img'
	]

def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, pInfo):
	print(str(len(products1))+"====="+url)
	sope = httpUtils.getRenderdHtmlFromUrl(url)
	pNameArea = sope.find("h1", attrs={"class":"pr_name"})
	pInfo["Product Name"] = getNodeText(pNameArea)
	imgArea = sope.find("div", attrs={"class":"image_inside"})
	if imgArea != None:
		imgName = pInfo["cat"]+".png"
		imgSrc = imgArea.find("img")["src"]
		httpUtils.urllib_download(imgSrc, imgName)
		pInfo["img"] = imgName
	sizeOption = sope.find("div", attrs={"class":"option col-md-12"})
	sizeLabels = sizeOption.find_all("label")
	sizeStr = ""
	for label in sizeLabels:
		sizeStr += getNodeText(label) + ";"
	pInfo["Size"] = sizeStr

	DescriptionArea = sope.find("div", attrs={"id":"tab-description"})
	pInfo["Description"] = getNodeText(DescriptionArea)
	specTable = sope.find("table", attrs={"class":"table table-bordered table-responsive table-striped"})
	trs = specTable.find_all("tr")
	for tr in trs:
		tds = tr.find_all("td")
		if len(tds) == 2:
			title = getNodeText(tds[0])
			value = getNodeText(tds[1])
			pInfo[title] = value
			addHeader(headers1, title)

	
	products1.append(pInfo.copy())



def getProductList(url):
	sope = httpUtils.getRenderdHtmlFromUrl(url)
	ps = sope.find_all("div", attrs={"id":"clickablediv"})
	for p in ps:
		cat = p.find("span", attrs={"style":"font-size:12px;"})
		pLink = p.find("a")
		pInfo = {
			"Product Name": getNodeText(pLink),
			"link":url,
			"cat": getNodeText(cat)
		}
		getProductInfo(pLink["href"], pInfo)
		


# getProductList('https://www.abbexa.com/index.php?route=product/search&module_id=81&search=breast+cancer&category_id=60;61&page=1')
for pIndex in range(1, 3):
	getProductList('https://www.abbexa.com/index.php?route=product/search&module_id=81&search=breast&category_id=65&page='+str(pIndex))

getProductList('https://www.abbexa.com/index.php?route=product/search&module_id=81&category_id=154;198;188&search=breast')

# getProductInfo('http://www.modelorg.us/portal/article/index/id/43653/post_type/3.html',{"cat":"ab255433"})
excelUtils.generateExcelMultipleSheet('abbexa.xlsx', [
	{
		"name": 'Antibodies for Breast Cancer.',
		"header": headers1 ,
		"data": products1
	}
])