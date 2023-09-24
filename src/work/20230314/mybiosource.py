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
	sope = httpUtils.getHtmlFromUrl(url)
	nav = sope.find_all("ul", attrs={"class":"uk-breadcrumb uk-margin-remove"})

	pName = sope.find("h1", attrs={"class":"uk-text-bold uk-margin-bottom uk-margin-remove-top uk-display-block uk-heading-line uk-h3"})
	pInfo = {
		"link": url,
		"Product Name": getNodeText(pName),
		"nav": getNodeText(nav[1])
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
			strongName = spec.find("strong")
			if strongName == None:
				strongName = divs[0].find("a")

			if len(title) >0:
				title = title.replace(getNodeText(strongName), "").strip()
				pInfo[title] = value
				addHeader(customerHeader, title)
	products1.append(pInfo.copy())

def getProductList(url):
	sope = httpUtils.getHtmlFromUrl(url)
	ps = sope.find_all("div", attrs={"class":"uk-width-expand@m product-details"})

	for p in ps:
		pLink = p.find("a")
		getProductInfo("https://www.mybiosource.com" + pLink["href"])
			

for pIndex in range(1, 22):
	getProductList("https://www.mybiosource.com/search/Caenorhabditis+Elegans?type=Antibody&size=200&page="+str(pIndex))

# getProductList("https://www.mybiosource.com/search/Caenorhabditis+Elegans?type=Antibody&size=200&page="+str(1))
# getProductInfo("https://www.mybiosource.com/polyclonal-human-antibody/apoa1/9403317")

headers=['link', 'nav', 'Product Name', 'Catalog #','Full Product Name','Product Synonym Names','Product Gene Name','3D Structure','Clonality','Isotype'
	 ,'Clone Number','Host','Species Reactivity','Form/Format'
	 ,'Concentration','Conjugate','Storage Buffer','Preparation and Storage','Other Notes','Related Product Information for',
	 'Product Categories/Family for','Applications Tested/Suitable for','Application Notes for','NCBI GeneID','Molecular Weight','NCBI Official Symbol',
	 'Protein Family']


excelUtils.generateExcelMultipleSheet('mybiosource.xlsx', [
	{
		"name":"mybiosource",
		"header": headers + sizeHeader,
		"data": products1
	}
])