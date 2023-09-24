from itertools import product
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import datetime
import json
import re
sys.path.append('../../..')
from lib import excelUtils
from lib import httpUtils
from lib import textUtil
from lib.htmlEleUtils import getNodeText
from lib.htmlEleUtils import getInnerHtml
import ssl
import math

products1 = []

headers1=['link','type1','type2','Product Name',
	  'Unit size1','Price1',
	  'Unit size2','Price2',
		'Unit size3','Price3',
		'Unit size4','Price4',
		'Unit size5','Price5',
		'Unit size6','Price6',
		'Unit size7','Price7',
		'Unit size8','Price8'
		]
global latestState
latestState=None
now = datetime.datetime.now()

# 将当前时间转换为指定格式的字符串
formatted_time = now.strftime("%Y-%m-%d %H%M%S")



def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, type, currentInfo):
	global latestState
	print(str(len(products1))+url)
	sope=httpUtils.getHtmlFromUrl(url)
	pInfo = {
		"link": url,
		"type1":type["t1"],
		"type2":type["t2"],
	}
	baseInfoAre=sope.find("div", attrs={"class":"product-images-inner"})
	baseTrs = baseInfoAre.find_all("tr")
	for baseTr in baseTrs:
		tds = baseTr.find_all("td")
		if len(tds) == 2:
			title = getNodeText(tds[0])
			value = getNodeText(tds[1])
			if len(title)>0:
				addHeader(headers1, title)
				pInfo[title] = value

	pName = sope.find("h1", attrs={"itemprop":"name"})
	pInfo["Product Name"] = getNodeText(pName)
	
	unitArea = sope.find("table", attrs={"class":"variations classy_list"})
	if unitArea !=None:
		tbody = unitArea.find("tbody")
		trs = tbody.find_all("tr")
		for inx,tr in enumerate(trs):
			tds = tr.find_all("td")
			pInfo["Unit size"+str(inx)] = getNodeText(tds[0])
			pInfo["Price"+str(inx)] = getNodeText(tds[1])

	products1.append(pInfo.copy())
	excelUtils.generateExcelMultipleSheet(formatted_time+'.xlsx', [
		{
			"name": 'axispharm',
			"header": headers1 ,
			"data": products1
		}
	])
	f = open('latestState.json','w')
	f.write( json.dumps(currentInfo))
	f.close()
	latestState=None

	

def getProductList(url, type, currentInfo):
	global latestState
	sope=httpUtils.getHtmlFromUrl(url)
	pListArea = sope.find("table", attrs={"class":"table text-center main-table product"})
	if pListArea != None:
		for tr in pListArea.find_all("tr"):
			tds = tr.find_all("td")
			if len(tds) > 2:
				pLink = tr.find("a")
				getProductInfo("https://axispharm.com"+pLink["href"], type, currentInfo)

	

def getProductPage(url, type, currentInfo):
	global latestState
	currentInfo["pageIndex"] = 1
	getProductList(url, type, currentInfo)


# with open('latestState.json','r') as file_to_read:
# 	content = file_to_read.read()
# 	latestState = json.loads(content)

with open('data.json','r') as file_to_read:
	content = file_to_read.read()
	types = json.loads(content)
	for inx, type in enumerate(types):
		if latestState == None or inx == latestState["typeIndex"]:
			getProductPage(type["url"], type, {"typeIndex": inx})

# getProductPage("https://axispharm.com/product-category/peg-linkers/peg-acid/",{"t1":"1","t2":"2"},{})

