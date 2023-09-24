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

headers1=['link','type','nav','Product Name','Core Type','Available Array Type']
global latestState
latestState=None
now = datetime.datetime.now()

# 将当前时间转换为指定格式的字符串
formatted_time = now.strftime("%Y-%m-%d %H%M%S")



def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, type):
	print(str(len(products1))+url)
	sope= httpUtils.getHtmlFromUrl(url)
	nav = sope.find("ol", attrs={"class":"breadcrumb"})
	productName = sope.find("div", attrs={"id":"block-pagetitle"})
	pInfo = {
		"link": url,
		"type":type["name"],
		"nav": getNodeText(nav),
		"Product Name":getNodeText(productName)
	}

	specArea = sope.find("div", attrs={"id":"block-usbiolab-content"})
	container = specArea.find("div", attrs={"class":"container"})
	pInfo["Core Type"] = ""
	ps = container.find_all("p")
	if len(ps)>1:
		pInfo["Core Type"] += getNodeText(ps[0])+"\r\n"
		pInfo["Core Type"] += getNodeText(ps[1])
	if len(ps)==1:
		pInfo["Core Type"] += getNodeText(ps[0])
	arrType = sope.find("select", attrs={"class":"form-select required"})
	if arrType != None:
		arrTypeStr = ""
		arrTypeOpts = arrType.find_all("option")
		for arrTypeOpt in arrTypeOpts:
			arrTypeStr += getNodeText(arrTypeOpt) + ";"
		pInfo["Available Array Type"] = arrTypeStr

	infoTable = sope.find("table", attrs={"class":"table table-bordered product-detail-table"})
	if infoTable != None:
		trs = infoTable.find_all("tr")
		for tr in trs:
			tds = tr.find_all("td")
			if len(tds) == 2:
				title = getNodeText(tds[0])
				value = getNodeText(tds[1])
				if len(title) > 0:
					pInfo[title] = value
					addHeader(headers1, title)

	products1.append(pInfo.copy())
	excelUtils.generateExcelMultipleSheet('usbiolab.xlsx', [
		{
			"name": 'usbiolab',
			"header": headers1 ,
			"data": products1
		}
	])

	

def getProductList(url, type):
	sope=httpUtils.getHtmlFromUrl(url)
	pListArea = sope.find("table", attrs={"class":"views-table views-view-table cols-6 responsive-enabled"})
	if pListArea != None:
		for tr in pListArea.find("tbody").find_all("tr"):
			pLink = tr.find("a")
			getProductInfo("https://usbiolab.com"+pLink["href"], type)

	

with open('data.json','r') as file_to_read:
	content = file_to_read.read()
	types = json.loads(content)
	for inx, type in enumerate(types):
		getProductList(type["url"], type)

# getProductInfo("https://usbiolab.com/tissue-array/product/adrenal-gland/EAG-2081a",'')

