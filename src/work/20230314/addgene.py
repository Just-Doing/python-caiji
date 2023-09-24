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

def addCustomerHeader(title):
  if title not in customerHeader and len(title) > 0:
    customerHeader.append(title)

def getProductInfo(url, pid):
	print(str(len(products1)) + "==" + url)
	productId = pid.replace("/","")
	sope = httpUtils.getHtmlFromUrl(url)
	nav = sope.select("div.breadcrumbs")
	pName = sope.find("div", attrs={"class":"panel-heading"})
	desc = sope.find("span", attrs={"id":"format-details-"+productId})
	pInfo = {
		"link": url,
		"nav": getNodeText(nav[0]).replace("\n"," ").replace("  "," "),
		"Product Name": getNodeText(pName.find("span", attrs={"class":"material-name"})),
		"Description": getNodeText(desc),

	}

	sections = sope.find_all("li", attrs={"class":"field"})
	for section in sections:
		titleEl = section.find("div", attrs={"class":"field-label"})
		if titleEl != None:
			titleEl = section.find("span", attrs={"class":"field-label"})
			if titleEl != None:
				title = getNodeText(titleEl)
				value = getNodeText(section).replace(title, "")
				pInfo[title] = value
				addCustomerHeader(title)


	imgArea = sope.find("div", attrs={"id":"plasmid-sequence-maps"})
	if imgArea != None:
		imgName = productId+".png"
		pInfo["Picture"] = imgName
		img = imgArea.find("img")
		if img!=None:
			httpUtils.urllib_download(img["src"], imgName)
	
	sequencesSope = httpUtils.getHtmlFromUrl(url+"sequences/")
	seqSections = sequencesSope.find_all("section")
	for section in seqSections:
		h2s = section.find_all("h2")
		if len(h2s) == 1:
			title = getNodeText(h2s[0])
			if title != "Ordering":
				value = getNodeText(section.find("textarea"))
				pInfo[title] = value
				addCustomerHeader(title)

	# print(pInfo)
	products1.append(pInfo.copy())


def getProductList(url):
	sope = httpUtils.getHtmlFromUrl(url)
	ps = sope.find("ol", attrs={"class":"list-group"}).find_all("li")
	for p in ps:
		pLink = p.find("a")
		getProductInfo("https://www.addgene.org"+pLink["href"], pLink["href"])
			
			
for pIndex in range(1, 29):
	getProductList("https://www.addgene.org/search/catalog/plasmids/?q=C.+elegans&page_number="+str(pIndex)+"&page_size=50")

# getProductInfo("https://www.addgene.org/21896/", "/21896/")

headers1=[
	'link','nav','Product Name','Description'
]



excelUtils.generateExcelMultipleSheet('addgene.xlsx', [
	{
		"name":"addgene",
		"header": headers1 + customerHeader,
		"data": products1
	}
])