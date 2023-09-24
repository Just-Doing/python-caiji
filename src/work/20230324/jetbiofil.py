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
	nav = sope.find("div", attrs={"class":"location auto"})

	pInfo = {
		"link": url,
		"type": type,
		"nav": getNodeText(nav)
	}
	
	specArea = sope.find("div", attrs={"class":"info mp"})
	pName = getNodeText(specArea.find("h1", attrs={"class":"f32 title"}))
	pInfo["Product Name"] = pName
	specText = getNodeText(specArea)
	spaces = specText.split("\n")
	for space in spaces:
		if ":" in space:
			infos = space.split(":")
			title = infos[0]
			value = infos[1]
			pInfo[title] = value
			addHeader(customerHeader, title)
			specText = specText.replace(space, "")

		if "：" in space:
			infos = space.split("：")
			title = infos[0]
			value = infos[1]
			pInfo[title] = value
			addHeader(customerHeader, title)
			specText = specText.replace(space, "")

	specText= specText.replace(pName, "")
	specText= specText.replace("Return to list", "")
	pInfo["introduce"] = specText

	detailAre = sope.find("div", attrs={"class":"product_details mp"})
	article = detailAre.find("div", attrs={"class":"article"})
	feature = article.find("div", attrs={"class":"info"})
	pInfo["Features"] = getNodeText(feature)

	catTb = sope.find("div", attrs={"class":"info table_box"})
	trs = catTb.find_all("tr")
	catStr = ""
	for inx, tr in enumerate(trs):
		if inx>0:
			tds = tr.find_all("td")
			catStr += getNodeText(tds[0])+";"
	pInfo["cat"] = catStr

	imgNames = ""
	imgArea = sope.find("div", attrs={"class":"big"})
	imgs = imgArea.find_all("li")
	for inx, img in enumerate(imgs):
		imgLink = "https://www.jetbiofil.com"+img["data-zoom-image"]
		imgName = pName+"-"+str(inx)+".jpg"
		httpUtils.urllib_download(imgLink, imgName)
		imgNames += imgName+";"
	pInfo["Img"]=imgNames
	products1.append(pInfo.copy())

def getProductList(url, type):
	sope = httpUtils.getHtmlFromUrl(url)
	ps = sope.find_all("li", attrs={"class":"zoomimg"})

	for p in ps:
		pLink = p.find("a")
		getProductInfo("https://www.jetbiofil.com" + pLink["href"], type)
			

headers=['link','type', 'nav', 'Product Name', 'introduce', 'Img','Features','cat']
getProductList("https://www.jetbiofil.com/en/Product/list_lcid_430.html", 'Bioprocess')
getProductList("https://www.jetbiofil.com/en/product/list_lcid_56_page_1.html", 'Cell Culture')
getProductList("https://www.jetbiofil.com/en/product/list_lcid_56_page_2.html", 'Cell Culture')
getProductList("https://www.jetbiofil.com/en/product/list_lcid_55_page_1.html", 'Liquid Handling and Storage')
getProductList("https://www.jetbiofil.com/en/product/list_lcid_55_page_2.html", 'Liquid Handling and Storage')
getProductList("https://www.jetbiofil.com/en/Product/list_lcid_51.html", 'Filtration')
getProductList("https://www.jetbiofil.com/en/Product/list_lcid_54.html", 'Molecular Biology')
getProductList("https://www.jetbiofil.com/en/Product/list_lcid_557.html", 'CellSafe™')
getProductList("https://www.jetbiofil.com/en/Product/list_lcid_517.html", 'Other')
getProductList("https://www.jetbiofil.com/en/Product/list_lcid_543.html", 'Medical Consumable')
getProductList("https://www.jetbiofil.com/en/Product/list_lcid_52.html", 'Biological Reagent')
getProductList("https://www.jetbiofil.com/en/Product/list_lcid_53_page_1.html", 'Laboratory Equipment')
getProductList("https://www.jetbiofil.com/en/Product/list_lcid_53_page_2.html", 'Laboratory Equipment')


# getProductInfo("https://www.jetbiofil.com/en/Product/info_itemid_1877_lcid_535.html")


excelUtils.generateExcelMultipleSheet('jetbiofil.xlsx', [
	{
		"name":"jetbiofil",
		"header": headers + customerHeader,
		"data": products1
	}
])