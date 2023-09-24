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


def getProductInfo(url, type):
	print(str(len(products1)) + "==" + url)
	sope = httpUtils.getHtmlFromUrl(url)

	pInfo = {
		"link": url,
		"type":type
	}
	specArea = sope.find("table", attrs={"id":"product-attribute-specs-table"})
	specs = specArea.find_all("tr")
	imgs=[]
	pdfs=[]
	for spec in specs:
		title = getNodeText(spec.find("th"))
		value = getNodeText(spec.find("td"))
		img = spec.find("td").find("img")
		pdf = spec.find("td").find("a")
		if pdf != None and pdf["href"].endswith(".pdf"):
			pdfs.append(spec)
		else:
			if img != None:
				imgs.append(spec)
			else:
				pInfo[title] = value
				addHeader(headers, title)


	archiveName = pInfo["CAS Number"] if "CAS Number" in pInfo else pInfo["Product Name"]
	for img in imgs:
		title = getNodeText(img.find("th"))
		imgSrc = img.find("td").find("img")
		pInfo[title] = archiveName+".png"
		httpUtils.urllib_download(imgSrc["src"], archiveName+".png")
		addHeader(headers, title)
	
	for pdf in pdfs:
		title = getNodeText(pdf.find("th"))
		pdfSrc = pdf.find("td").find("a")
		pInfo[title] = archiveName+".pdf"
		httpUtils.urllib_download(pdfSrc["href"], archiveName+".pdf")
		addHeader(headers, title)
	products1.append(pInfo.copy())

def getProductList(url, type):
	sope = httpUtils.getHtmlFromUrl(url)
	pListArea = sope.find("ol", attrs={"id": "products-list"})
	ps = pListArea.find_all("li")

	for p in ps:
		pLink = p.find("a")
		href= pLink["href"]
		if len(href) > 5:
			getProductInfo(pLink["href"], type)
			

headers=['link', 'type']


for pIndex in range(1, 8):
	getProductList("https://www.cdnisotopes.com/nf/products/categories/environmental-standards?limit=50&p="+str(pIndex),'Environmental Standards')
for pIndex in range(1, 6):
	getProductList("https://www.cdnisotopes.com/nf/products/categories/medical-research-products?limit=50&p="+str(pIndex),'Medical Research Products')


# getProductInfo("https://www.cdnisotopes.com/nf/d-8179","ttt")


excelUtils.generateExcelMultipleSheet('cdnisotopes.xlsx', [
	{
		"name":"cdnisotopes",
		"header": headers ,
		"data": products1
	}
])