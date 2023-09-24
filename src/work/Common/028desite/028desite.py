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
import ssl
import math

ssl._create_default_https_context = ssl._create_unverified_context

products1 = []

headers1=['link','type','Product Name','img']


def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, type):
	print(str(len(products1))+url)
	sope = httpUtils.getHtmlFromUrl(url)
	pInfo = {
		"link": url,
		"type":type,
	}
	
	specArea = sope.find("div", attrs={"class":"pro-show-ms fl"})
	if specArea != None:
		spans = specArea.find_all("span")
		for span in spans:
			title = getNodeText(span).replace("：","")
			# value = getNodeText(span.nextSibling)
			pInfo[title] = span.nextSibling.strip()
			addHeader(headers1, title)
	
	infoArea = sope.find("div", attrs={"class":"pro-show-nr"})
	infoStrs = infoArea.prettify().replace('<div class="pro-show-nr">',"").replace('</div>',"").replace('<br>',"").replace('</br>',"").split("<br/>")
	for infoStr in infoStrs:
		infoPart = infoStr.strip().split("：")
		if len(infoPart) == 2:
			title = infoPart[0].replace("：","")
			value = infoPart[1]
			pInfo[title] = value
			addHeader(headers1, title)
	
	imgArea = sope.find("div", attrs={"class":"pro-show-img fl"})
	img = imgArea.find("img")
	if img != None:
		imgName = (pInfo["CAS NO"] if len(pInfo["CAS NO"])>0 else pInfo["分子式"]).replace("|","").replace(".","") + ".jpg"
		if img["src"].startswith("/"):
			httpUtils.urllib_download("http://m.028desite.com"+img["src"], imgName)
		else:
			httpUtils.urllib_download("http://m.028desite.com/"+img["src"], imgName)
		pInfo["img"]=imgName

	products1.append(pInfo.copy())
	

def getProductList(url, type):
	sope = httpUtils.getHtmlFromUrl(url)
	ps = sope.find("ul", attrs={"class":"list-pro cl"}).find_all("li")
	for p in ps:
		pLink = p.find("a")
		getProductInfo("http://m.028desite.com"+pLink["href"], type)
	


for pIndex in range(1, 465):
	getProductList("http://m.028desite.com/list-6-"+str(pIndex)+".html", '中药标准品')
	
for pIndex in range(1, 4):
	getProductList("http://m.028desite.com/list-9-"+str(pIndex)+".html", '高纯度提取物')

# getProductInfo("http://m.028desite.com/show-6-2444-1.html","a")

excelUtils.generateExcelMultipleSheet('028desite.xlsx', [
	{
		"name": '028desite',
		"header": headers1 ,
		"data": products1
	}
])