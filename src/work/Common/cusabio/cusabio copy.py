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

headers1=['link','type1','type2','type3','nav','Product Name','Size','price','source','Expression System']
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
		"type3":type["t3"],
	}
	nav = sope.find("ul", attrs={"class":"bread nav-bg"})
	pName = sope.find("h1", attrs={"class":"margin-small-right"})
	pInfo["nav"] = getNodeText(nav)
	pInfo["Product Name"] = getNodeText(pName)

	trs = sope.find_all("tr")
	for tr in trs:
		tds = tr.find_all("td")
		if len(tds) == 2:
			title = getNodeText(tds[0])
			value = getNodeText(tds[1])
			if title == "Size":
				sizeOptions = tds[1].find_all("option")
				if len(sizeOptions) > 0:
					value = ""
					price = ""
					for sizeOption in sizeOptions:
						value += getNodeText(sizeOption)+";"
						price += (sizeOption["price"] if sizeOption.has_attr("price") else "") +";"
					pInfo["price"] = price
			pInfo[title] = value
			addHeader(headers1, title)
	tabs = sope.find_all("div", attrs={"class":"tab-panel"})
	ExpressionSystemStr=""
	for tab in tabs:
		tabTrs = tab.find_all("tr")
		sourceStr = ""
		sizeStr = ""
		for tabTr in tabTrs:
			tabTds = tabTr.find_all("td")
			if len(tabTds) == 2:
				title = getNodeText(tabTds[0])
				value = getNodeText(tabTds[1])
				if title == "Size":
					sizeOptions = tabTds[1].find_all("option")
					if len(sizeOptions) > 0:
						for sizeOption in sizeOptions:
							sizeStr += getNodeText(sizeOption)+";"
				if title=="Source":
					sourceStr = value
		ExpressionSystemStr+=sourceStr+",size:"+sizeStr+"\r\n"
	pInfo["Expression System"] = ExpressionSystemStr

						
	items = sope.find_all("div", class_="item")
	for item in items:
		title = getNodeText(item.find("div", attrs={"class":"name"}))
		value = getNodeText(item.find("div", attrs={"class":"value"}))
		if len(title) > 0:
			pInfo[title] = value
			addHeader(headers1, title)
	pInfo["source"] = type["source"]
	products1.append(pInfo.copy())

	excelUtils.generateExcelMultipleSheet(formatted_time+'.xlsx', [
		{
			"name": 'cusabio',
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
	tye3s = sope.find_all("div", attrs={"class":"table-responsive margin-large-top"})
	for type3 in tye3s:
		type["t3"] = getNodeText(type3.find("h2"))
		type["source"] = ""
		ps = type3.find_all("tr")
		for inx,p in enumerate(ps):
			pLink = p.find("a")
			if latestState == None or inx == latestState["productIndex"]:
				currentInfo["productIndex"] = inx
				if pLink !=None:
					if "Proteins" in type["t3"]:
						type["source"] = getNodeText(p.find_all("td")[2])
					getProductInfo(pLink["href"], type, currentInfo)
	

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
# getProductInfo('https://www.cusabio.com/Polyclonal-Antibody/CALR-AntibodyHRP-conjugated-157641.html',{"t1":"1","t2":"2",'t3': '','source':''},{})

# getProductPage("https://www.cusabio.com/target/ANGPT2.html#a04",{"t1":"1","t2":"2"},{})

