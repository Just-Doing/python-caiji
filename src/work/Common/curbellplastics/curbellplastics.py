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

headers1=['link','nav','type1','Product Name']


def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, type):
	print(str(len(products1))+url)
	sope=httpUtils.getHtmlFromUrl(url)
	pInfo = {
		"link": url,
		"type1":type,
	}
	nav = sope.find("div", attrs={"class":"breadcrumbs text-center lg:text-left min-w-0 flex-1"})
	pInfo["nav"] = getNodeText(nav)
	
	pInfo["Product Name"] = getNodeText(sope.find("h1", attrs={"class":"text-28 leading-tight text-primary font-heading font-black"}))

	specAreas = sope.find_all("div", attrs={"class":"space-y-8"})
	for specArea in specAreas:
		specs = specArea.find_all("div", recursive=False)
		for spec in specs:
			title = getNodeText(spec.find("div", attrs={"class":"w-1/4"}))
			value = getNodeText(spec.find("div", attrs={"class":"flex-1"}))
			if len(title)>0:
				pInfo[title] = value
				addHeader(headers1, title)

	products1.append(pInfo.copy())
	

def getProductList(url, type):
	sope=httpUtils.getHtmlFromUrl(url)

	tableArea = sope.find("div", attrs={"class":"clear-both products grid group/products lg:grid-cols-2 xl:grid-cols-3 lg:gap-4 2xl:gap-8"})
	if tableArea != None:
		ps = tableArea.find_all("div", attrs={"class":"group border-b-3 py-5 flex lg:group-[.grid]/products:flex-col lg:group-[.grid]/products:border-3 lg:group-[.grid]/products:p-0"})
		for p in ps:
			pLink = p.find("a")
			getProductInfo(pLink["href"], type)
	



# getProductList('https://www.curbellplastics.com/product-category/material/fep/','fep')
# getProductInfo('https://www.curbellplastics.com/product/w01-03970/', '')

for pIndex in range(1, 5):
	getProductList('https://www.curbellplastics.com/product-category/material/ptfe/page/'+str(pIndex)+'/','ptfe')
getProductList('https://www.curbellplastics.com/product-category/material/pvdf/','pvdf')

for pIndex in range(1, 6):
	getProductList('https://www.curbellplastics.com/product-category/material/peek/page/'+str(pIndex)+'/','peek')
for pIndex in range(1, 3):
	getProductList('https://www.curbellplastics.com/product-category/material/pctfe/page/'+str(pIndex)+'/','pctfe')
getProductList('https://www.curbellplastics.com/product-category/material/fep/','fep')

excelUtils.generateExcelMultipleSheet('curbellplastics.xlsx', [
	{
		"name": 'curbellplastics',
		"header": headers1 ,
		"data": products1
	}
])