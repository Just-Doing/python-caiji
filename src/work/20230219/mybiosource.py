from itertools import product
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
import re
sys.path.append('../..')
from lib import excelUtils
from lib import httpUtils
from lib import textUtil
from lib.htmlEleUtils import getNodeText
from lib.htmlEleUtils import getInnerHtml
products1 = []
products2 = []
products3 = []
products4 = []
customerHeader = []
sizeHeader=[]

def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, type):
	print(str(len(products1))+"-"+str(len(products2))+"-"+str(len(products3)) + "==" + url)
	sope = httpUtils.getHtmlFromUrl(url)
	pName = sope.find("h1", attrs={"class":"uk-text-bold uk-margin-bottom uk-margin-remove-top uk-display-block uk-heading-line uk-h3"})
	pInfo = {
		"link": url,
		"Product Name": getNodeText(pName),
	}
	trs = sope.find_all("tr")
	for tr in trs:
		tds = tr.find_all("td", recursive=False)
		if len(tds) == 2:
			title = getNodeText(tds[0])
			value =  getNodeText(tds[1])
			if title == "Catalog #":
				pInfo["Catalog #"] = value
	sizes = sope.find_all("input", attrs={"class":"uk-radio"})
	for inx,size in enumerate(sizes):
		sizeStr = size.nextSibling
		sizeTitle = "Unit/Price-"+str(inx)
		pInfo[sizeTitle] = sizeStr
		addHeader(sizeHeader, sizeTitle)

	specs = sope.find_all("div", attrs={"class":"uk-grid uk-grid-small uk-margin-small-top"})
	for spec in specs:
		divs = spec.find_all("div", recursive=False)
		if len(divs) == 2:
			title = getNodeText(divs[0])
			value = getNodeText(divs[1])
			if len(title) >0:
				pInfo[title] = value
				addHeader(customerHeader, title)
	if type == "1":
		products1.append(pInfo.copy())
	if type == "2":
		products2.append(pInfo.copy())
	if type == "3":
		products3.append(pInfo.copy())
	if type == "4":
		products4.append(pInfo.copy())

def getProductList(url, type):
	sope = httpUtils.getHtmlFromUrl(url)
	ps = sope.find_all("div", attrs={"class":"product-listing uk-grid uk-grid-small uk-margin-remove uk-padding-small"})
	for p in ps:
		pLink = p.find("a")
		getProductInfo("https://www.mybiosource.com"+pLink["href"], type)
			

# getProductList("https://www.mybiosource.com/pathway/736188", '1')

# for pIndex in range(1, 5):
# 	getProductList("https://www.mybiosource.com/pathway/198312?name=198312&page="+str(pIndex), '2')

# getProductList("https://www.mybiosource.com/pathway/139776", '3')


# for pIndex in range(1, 52):
# 	getProductList("https://www.mybiosource.com/pathway/187191&page="+str(pIndex), '4')

getProductInfo("https://www.mybiosource.com/human-elisa-kits/neutrophil-gelatinase-associated-lipocalin-ngal/2021888", '1')

headers=['link','Product Name','Catalog #']


excelUtils.generateExcelMultipleSheet('mybiosource.xlsx', [
	{
		"name":"Iron Complex Transport System Pathwayy",
		"header": headers + sizeHeader + customerHeader,
		"data": products1
	},
	{
		"name":"Iron Homeostasis Pathway",
		"header": headers + sizeHeader + customerHeader,
		"data": products2
	},
	{
		"name":"Iron Reduction And Absorption Pathway",
		"header": headers + sizeHeader + customerHeader,
		"data": products3
	},
	{
		"name":"Iron Uptake And Transport Pathway",
		"header": headers + sizeHeader + customerHeader,
		"data": products4
	}
])