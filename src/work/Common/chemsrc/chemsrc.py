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

headers1=['link','type1','type2','type3','type4','type5','Product Name']
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
		"type1":type["parent1"],
		"type2":type["parent2"],
		"type3":type["parent3"],
		"type4":type["parent4"],
		"type5":type["tile"]
	}
	pName = sope.find("div", attrs={"class":"h1title"})
	pInfo["Product Name"] = getNodeText(pName)

	
	trs = sope.find_all("tr")
	for tr in trs:
		ths = tr.find_all("th")
		tds = tr.find_all("td")
		if len(ths) ==1 and len(tds)==1:
			title = getNodeText(ths[0])
			value = getNodeText(tds[0])
			pInfo[title] = value
			addHeader(headers1, title)

	baseTb = sope.find("table", attrs={"id":"baseTbl"})
	if baseTb != None:
		baseTrs = baseTb.find_all("tr")
		for tr in baseTrs:
			ths = tr.find_all("th")
			for th in ths:
				title = getNodeText(th)
				value = getNodeText(th.findNextSibling("td"))
				pInfo[title] = value
				addHeader(headers1, title)

	products1.append(pInfo.copy())
	excelUtils.generateExcelMultipleSheet(formatted_time+'.xlsx', [
		{
			"name": 'chemsrc',
			"header": headers1 ,
			"data": products1
		}
	])
	f = open('latestState.json','w')
	print(currentInfo)
	f.write( json.dumps(currentInfo))
	f.close()
	latestState=None

	

def getProductList(url, type, currentInfo):
	global latestState
	sope=httpUtils.getHtmlFromUrl(url)
	ps = sope.find_all("div", attrs={"class":"media search-media"})
	for inx,p in enumerate(ps):
		pLink = p.find("a")
		if latestState == None or inx == latestState["productIndex"]:
			currentInfo["productIndex"] = inx
			getProductInfo("https://www.chemsrc.com"+pLink["href"], type, currentInfo)
			time.sleep(43)
	

def getProductPage(url, type, currentInfo):
	global latestState
	sope=httpUtils.getHtmlFromUrl(url)
	pageArea = sope.find("div", attrs={"class":"page-header"})
	if pageArea != None:
		totalPage = int(getNodeText(pageArea.find("span", attrs={"class":"pull-right"}).find("i")))
		for pIndex in range(1, math.ceil(totalPage/30)+1):
			if latestState == None or pIndex == latestState["pageIndex"]:
				currentInfo["pageIndex"] = pIndex
				getProductList(url+"?page="+str(pIndex), type, currentInfo)


with open('latestState.json','r') as file_to_read:
	content = file_to_read.read()
	latestState = json.loads(content)

with open('data.json','r') as file_to_read:
	content = file_to_read.read()
	types = json.loads(content)
	for inx, type in enumerate(types):
		if latestState == None or inx == latestState["typeIndex"]:
			getProductPage("https://www.chemsrc.com"+type["href"], type, {"typeIndex": inx})


