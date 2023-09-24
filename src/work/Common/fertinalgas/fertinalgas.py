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

headers1=['link','nav', 'CATEGORIES', 'product name','Product Description','Application'
	]
customerHeader=[]
def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, type1):
	print(str(len(products1))+"====="+url)
	sope = httpUtils.getHtmlFromUrl(url)
	nav = sope.find("ul", attrs={"class":"breadcrumb"})
	pInfo={
		"link": url,
		"CATEGORIES": type1
	}
	pName = sope.find("h2", attrs={"class":"product_title entry-title show-product-nav"})
	pInfo["product name"]  = getNodeText(pName)
	pInfo["Application"] = ""
	pInfo["Product Description"] = ""
	descs = sope.find_all("div", attrs={"class":"editor-component-row editor-component-row-relative"})
	for desc in descs:
		title = getNodeText(desc)
		if title == "Product Description":
			pInfo["Product Description"] = getNodeText(desc.findNextSibling("div"))
		if "Application" in title:
			pInfo["Application"] = getNodeText(desc.findNextSibling("div"))
	
	#如果没取到
	if len(pInfo["Application"]) == 0:
		h3s = sope.find_all("h3")
		for h3 in h3s:
			title = getNodeText(h3)
			if  'Applications' in title:
				pInfo["Application"] = getNodeText(h3.findNextSibling("ul"))
		




	tab = sope.find("div", attrs={"id":"tab-description"})
	if tab != None:
		specArea = tab.find("table")
		if specArea != None:
			trs = specArea.find_all("tr")
			itemIndex = -1
			for inx,tr in enumerate(trs):
				tds = tr.find_all("td")
				if inx == 0:
					for tdInx, td in enumerate(tds):
						if getNodeText(td).lower() == "item" or getNodeText(td).lower() == "items":
							itemIndex = tdInx
				else:
					if itemIndex>-1:
						title = getNodeText(tds[itemIndex])
						value = ""
						for tdInx,td in enumerate(tds):
							if tdInx>itemIndex:
								value += getNodeText(tds[tdInx]) + "|||"
						pInfo[title] = value
						addHeader(headers1, title)

	pInfo["nav"] = getNodeText(nav)


	products1.append(pInfo.copy())


def getProductList(url, type1):
	sope = httpUtils.getHtmlFromUrl(url)
	ps = sope.find("ul", attrs={"class":"products"}).find_all("li")
	for p in ps:
		pLink = p.find("a")
		getProductInfo(pLink["href"], type1)
		
		
getProductList('https://www.fertinalgas.com/product-category/biostimulant-seaweed-extract/seaweed-extract-flakes/','seaweed extract flakes')
getProductList('https://www.fertinalgas.com/product-category/biostimulant-seaweed-extract/seaweed-extract-gel/','seaweed extract gel')
getProductList('https://www.fertinalgas.com/product-category/biostimulant-seaweed-extract/seaweed-extract-liquid/','seaweed extract liquid')
getProductList('https://www.fertinalgas.com/product-category/biostimulant-seaweed-extract/seaweed-fertilizer-crystal-seaweed-compound-fertilizer/','seaweed fertilizer crystal')
getProductList('https://www.fertinalgas.com/product-category/biostimulant-seaweed-extract/seaweed-fertilizer-powder/','seaweed fertilizer powder')


# getProductInfo('https://www.fertinalgas.com/product/bio-fertilizer-manufacturers-seaweed-extract-from-ascophyllum-nodosum/', 'a')


excelUtils.generateExcelMultipleSheet('fertinalgas.xlsx', [
	{
		"name": 'fertinalgas',
		"header": headers1 + customerHeader,
		"data": products1
	}
])