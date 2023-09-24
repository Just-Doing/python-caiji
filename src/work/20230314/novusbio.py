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
customerHeader = []
sizeHeader=[]


def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url):
	print(str(len(products1)) + "==" + url)
	sope = httpUtils.getHtmlFromSafeUrl(url)
	nav = sope.find("div", attrs={"id":"page-breadcrumb"})

	pName = sope.find("div", attrs={"class":"main grid_16"})
	pInfo = {
		"link": url,
		"Product Name": getNodeText(pName),
		"nav": getNodeText(nav)
	}
	tables = sope.find_all("table", attrs={"class":"ds_list"})
	for table in tables:
		trs = table.find_all("tr")
		for tr in trs:
			tds = tr.find_all("td", recursive=False)
			if len(tds) == 2:
				title = getNodeText(tds[0])
				value = getNodeText(tds[1])
				pInfo[title] = value
				addHeader(headers, title)

	sizeTb = sope.find("table", attrs={"class":"sticky-enabled"})
	sizeTrs = sizeTb.find("tbody").find_all("tr")
	sizeIndex = 0
	for tr in sizeTrs:
		tds = tr.find_all("td")
		if len(tds) > 1:
			sizeIndex += 1
			size = getNodeText(tds[0].find("div", attrs={"class":"atc_size"}))
			cat = getNodeText(tds[0].find("div", attrs={"class":"atc_catnum"}))
			sizeTitle = "Size/Catalog No.-"+str(sizeIndex)
			pInfo[sizeTitle] = size+"/"+cat
			addHeader(sizeHeader, sizeTitle)
	greyHead2s = sope.find_all("h2", attrs={"class":"greyHead2"})
	for greyHead2 in greyHead2s:
		title = getNodeText(greyHead2)
		if title == "Notes":
			pInfo["Notes"] = getNodeText(greyHead2.findNextSibling("div"))
		if title == "Background":
			pInfo["Background"] = getNodeText(greyHead2.findNextSibling("div"))
		if title == "Limitations":
			pInfo["Limitations"] = getNodeText(greyHead2.findNextSibling("div"))
		if "Alternate Names for " in title:
			pInfo["Alternate Names for"] = getNodeText(greyHead2.findNextSibling("div"))
		

	products1.append(pInfo.copy())

def getProductList(url):
	sope = httpUtils.getHtmlFromSafeUrl(url)
	ps = sope.find_all("div", attrs={"class":"new-search-result search-result-wrapper"})

	for p in ps:
		pLink = p.find("a")
		getProductInfo("https://www.novusbio.com" + pLink["href"])
			

headers=['link', 'nav', 'Product Name','Notes','Background','Limitations','Alternate Names for']
for pIndex in range(1, 20):
	getProductList("https://www.novusbio.com/search?keywords=Drosophila&species=Drosophila&category=Primary%20Antibodies&page="+str(pIndex))

# getProductList("https://www.novusbio.com/search?keywords=Drosophila&species=Drosophila&category=Primary%20Antibodies&page="+str(2))
# getProductInfo("https://www.novusbio.com/products/fat1-antibody-fat-1-3d7-1_nb100-2693")



excelUtils.generateExcelMultipleSheet('novusbio.xlsx', [
	{
		"name":"novusbio",
		"header": headers + sizeHeader,
		"data": products1
	}
])