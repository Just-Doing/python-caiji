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
		'link','Product Name','sku', 'size','price','img',"Product Information","introduce","Publications","Publications-Link",'Downloads-File-Title','Downloads-File-Name'
	]

def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url):
	print(str(len(products1))+"====="+url)
	sope = httpUtils.getRenderdHtmlFromUrl(url)
	pName = sope.find("h1", attrs={"class":"title"})
	pInfo = {
		"link":url,
		"Product Name": getNodeText(pName)
	}
	pArea = sope.find("div", attrs={"class":"productWrapper"})
	sku = pArea.find("div", attrs={"class":"smallTitle"})
	pInfo["sku"] = getNodeText(sku)

	sizeArea = sope.find("select", attrs={"class":"customSelect customVariantSelect"})
	if sizeArea != None:
		sizes = sizeArea.find_all("option")
		sizeStr = ""
		for size in  sizes:
			sizeStr += getNodeText(size) + ";"
		pInfo["size"] = sizeStr

	prices = sope.find_all("div", attrs={"class":"price col"})
	priceStr = ""
	for price in prices:
		if len(priceStr) > 0:
			break;
		if price.has_attr("data-price"):
			priceStr = price["data-price"]
	pInfo["price"] = priceStr
	imgArea = sope.find("div", attrs={"class":"image"})
	if imgArea !=None:
		img = imgArea.find("img")
		if img != None:
			src = img["src"]
			imgNamePart = src.split("/")[-1]
			httpUtils.urllib_download("https://www.nimagen.com"+src, imgNamePart)
			pInfo["img"] = imgNamePart
	
	proInformation = sope.find("section", attrs={"class":"productDescriptionBlock"})
	if proInformation != None:
		pInfo["Product Information"] = getNodeText(proInformation.find("h2"))
	
		pInfo["introduce"] = getNodeText(proInformation.find("div", attrs={"class":"subCols"}))

	Publications = sope.find("section", attrs={"class":"productTextBlock"})
	if Publications != None:
		text = getNodeText(Publications.find("div", attrs={"class":"text"}))
		pInfo["Publications"] = text
		link = Publications.find("a")
		if link != None:
			pInfo["Publications-Link"] =  link["href"]
	tabs = sope.find_all("div", attrs={"class":"tab"})
	for tab in tabs:
		title = getNodeText(tab.find("div", attrs={"class":"tabTitle"}))
		if len(title) >0:
			if title == "Premium features":
				pInfo["Premium features"] = getNodeText(tab.find("div", attrs={"class":"tabContent"}))
			if title == "Downloads":
				links = tab.find_all("a")
				linkNames = ""
				fileNames = ""
				for link in links:
					linkNames += getNodeText(link)+"|||"
					href = link["href"]
					fileName = href.split("/")[-1]
					print("https://www.nimagen.com" + href)
					print(fileName)
					httpUtils.urllib_download("https://www.nimagen.com" + href, fileName)
					fileNames += fileName +"|||"

				pInfo["Downloads-File-Title"] = linkNames
				pInfo["Downloads-File-Name"] = fileNames



	products1.append(pInfo.copy())
	excelUtils.generateExcelMultipleSheet('nimagen.xlsx', [
		{
			"name": 'nimagen',
			"header": headers1 ,
			"data": products1
		}
	])


# getProductInfo("https://www.nimagen.com/shop/products/ap-500/ampliclean-cleanup-kit-magnetic-beads-500-ml")

fileName="data.json"
with open(fileName,'rb') as file_to_read:
	content=file_to_read.read()
	urls = json.loads(content)
	for url in urls:
		getProductInfo(url)
