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
		'link','Breadcrumb', 'Product type1','Product type2','Product Name'
	]

def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, pInfo):
	print(str(len(products1))+"====="+url)
	sope = httpUtils.getHtmlFromUrl(url)
	nav = sope.find("ol", attrs={"class":"breadcrumb margin-bottom-1rem margin-top-1rem"})
	pInfo["link"] = url
	pInfo["Breadcrumb"] = getNodeText(nav)

	baseArea = sope.find("div", attrs={"class":"col-md-6 col-xs-12 padding-top-1rem"})
	if baseArea != None:
		baseInfos = baseArea.find_all("div", attrs={"class":"row"})
		for info in baseInfos:
			title = getNodeText(info.find("div", attrs={"class":"col-md-3 col-xs-12"}))
			value = getNodeText(info.find("div", attrs={"class":"col-md-9 col-xs-12"}))
			pInfo[title] = value
			addHeader(headers1, title)

		attrAreas = sope.find_all("div", attrs={"class":"gene-detail flex-item"})
		for attrArea in attrAreas:
			attrs = attrArea.find_all("div", attrs={"class":"row"})
			for attr in attrs:
				title = getNodeText(attr.find("div", attrs={"class":"col-md-4 col-xs-12"}))
				if len(title) == 0:
					title = getNodeText(attr.find("div", attrs={"class":"col-md-4 col-xs-12 refer-height"}))
				value = getNodeText(attr.find("div", attrs={"class":"col-md-8 col-xs-12"}))
				pInfo[title] = value
				addHeader(headers1, title)
		print(pInfo)
	products1.append(pInfo.copy())



def getProductList(url, type1, type2):
	sope = httpUtils.getHtmlFromUrl(url)
	ps = sope.find_all("div", attrs={"class":"group-item flex-box"})
	for p in ps:
		pLink = p.find("a")
		pInfo = {
			"Product type1": type1,
			"Product type2": type2,
			"Product Name": getNodeText(pLink)
		}
		getProductInfo("http://www.modelorg.us"+pLink["href"], pInfo)
		
		


getProductList('http://www.modelorg.us/portal/search/index.html?keyword=Alzheimer%27s+Disease&post_type=3&verify_data=&list_rows=100',"Alzheimer's Disease",'Mice')
getProductList('http://www.modelorg.us/portal/search/index.html?keyword=Parkinson%27s+Disease&post_type=3&verify_data=&list_rows=100',"Parkinson's Disease",'Mice')
getProductList('http://www.modelorg.us/portal/search/index.html?keyword=Huntington+Disease&post_type=3&verify_data=&list_rows=100','Huntington Disease','Mice')
getProductList('http://www.modelorg.us/portal/search/index.html?keyword=Amyotrophic+lateral+sclerosis&post_type=3&verify_data=&list_rows=100','Amyotrophic lateral sclerosis','Mice')
getProductList('http://www.modelorg.us/portal/search/index.html?keyword=Multiple+Sclerosis&post_type=3&verify_data=&list_rows=100','Multiple Sclerosis','Mice')


# getProductInfo('http://www.modelorg.us/portal/article/index/id/43653/post_type/3.html',{"cat":"ab255433"})
excelUtils.generateExcelMultipleSheet('modelorg.xlsx', [
	{
		"name": 'modelorg',
		"header": headers1 ,
		"data": products1
	}
])