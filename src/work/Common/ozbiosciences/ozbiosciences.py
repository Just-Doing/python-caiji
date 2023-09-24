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

headers1=['link','nav','Product Name',
	  'CatNo1','Unit size1','Price1',
	  'CatNo2','Unit size2','Price2',
	  'CatNo3','Unit size3','Price3',
	  'CatNo4','Unit size4','Price4',
	  'CatNo5','Unit size5','Price5',
	  'CatNo6','Unit size6','Price6',
	  'CatNo7','Unit size7','Price7',
	  'CatNo8','Unit size8','Price8',
	  'CatNo9','Unit size9','Price9',
	  'CatNo10','Unit size10','Price10',
	  'CatNo11','Unit size11','Price11',
	  'CatNo12','Unit size12','Price12'
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
	}
	nav = sope.find("nav", class_="breadcrumb")
	pInfo["nav"] = getNodeText(nav)
	pName = sope.find("h1", class_="h1")
	pInfo["Product Name"] = getNodeText(pName)

	unitArea = sope.find("table", attrs={"id":"wk-combination-block-view"})
	if unitArea != None:
		tbody = unitArea.find("tbody")
		trs = tbody.find_all("tr")
		for inx,tr in enumerate(trs):
			tds = tr.find_all("td")
			catNo = getNodeText(tds[0])
			unit = getNodeText(tds[1])
			price = getNodeText(tds[2])
			pInfo["Unit size"+str(inx)] = unit
			pInfo["Price"+str(inx)] = price
			pInfo["CatNo"+str(inx)] = catNo



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
	for tr in sope.find_all("div", attrs={"class":"js-product product col-xs-6 col-xl-4"}):
		pLink = tr.find("a")
		getProductInfo(pLink["href"], type, currentInfo)

	

def getProductPage(url, type, currentInfo):
	global latestState
	currentInfo["pageIndex"] = 1
	sope=httpUtils.getHtmlFromUrl(url)
	types = sope.find_all("li", attrs={"class":"subcategory level-0"})
	if len(types) == 0:
		getProductList(url, type, currentInfo)
	else:
		for type in types:
			typeLink = type.find("a")
			getProductPage(typeLink["href"], type, currentInfo)


getProductPage("https://ozbiosciences.com/83-products", {}, {})


