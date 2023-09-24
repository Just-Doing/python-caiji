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
import math
products1 = []

headers1=['link','nav', 'Product type1','Product type2','cat','Product Name','Description:','Application:','Tag:','Reactivity:','Conjugate:','image','Product size',
	  'Key features and details','applications','Cellular localization','Cellular localization-link','Shipping info'
	]

def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, pInfo):
	print(str(len(products1))+"====="+url)
	sope = httpUtils.getHtmlFromUrl(url)
	nav = sope.find("nav", attrs={"id":"breadcrumbs"})
	pInfo["link"] = url
	pInfo["nav"] = getNodeText(nav)

	shippingInformation = sope.find("section", attrs={"id":"shipping-information"})
	pInfo["Shipping info"] = getNodeText(shippingInformation)

	sizeSope = httpUtils.getJson("https://www.abcam.com/datasheetproperties/availability?abId="+pInfo["cat"].replace("ab", ""))
	sizeStr = ""
	sizes = sizeSope["size-information"]["Sizes"]
	for size in sizes:
		sizeTitle = size["Size"].replace("&micro;","µ")
		price = size["Price"]
		sizeStr += (sizeTitle + ":" + price+";")

	pInfo["Product size"] = sizeStr

	keyFeature = sope.find("section", attrs={"id":"key-features"})
	keyFeatureStr = ""
	if keyFeature != None:
		keyFeatureLis = keyFeature.find_all("li")
		for li in keyFeatureLis:
			keyFeatureStr += getNodeText(li)
	attributes = sope.find_all("li", attrs={"class":"attribute"})
	for attribute in attributes:
		title = getNodeText(attribute.find("h3", class_="name"))
		value = getNodeText(attribute.find("div", class_="value"))
		if title == "Cellular localization":
			linkArea = attribute.findNextSibling("li", attrs={"class":"citation clearfix"})
			if linkArea != None:
				link = linkArea.find("a", attrs={"rel":"nofollow noopener noreferrer"})
				pInfo["Cellular localization"] = value + getNodeText(linkArea)
				if link != None:
					pInfo["Cellular localization-link"] = link["href"]
		else:
			if title == "Database links":
				links = attribute.find_all("a")
				linkStr = ""
				for link in links:
					linkStr += link["href"]
				pInfo["Database links"] = linkStr
			else:
				addHeader(headers1, title)
				pInfo[title] = value
	application = sope.find("div", attrs={"id":"description_applications"})
	applicationStr = ""
	if application!=None:
		appTds = application.find_all("td", class_="name")
		for appTd in appTds:
			applicationStr += getNodeText(appTd)+";"

	pInfo["applications"] = applicationStr

	pInfo["Key features and details"] = keyFeatureStr
	

	imageArea = sope.find("ul", attrs={"class":"thumbnail-list"})
	imageStr = ""
	if imageArea != None:
		lis = imageArea.find_all("li")
		for inx, li in enumerate(lis):
			img = li.find("a")
			if img != None:
				imgName = pInfo["cat"]+"-"+str(inx)+".jpg"
				httpUtils.urllib_download(img["href"], imgName)
				imageStr += imgName+";"

	pInfo["image"] = imageStr
	products1.append(pInfo.copy())


def getStr(size):
	return getNodeText(size).replace(".","").replace(" ","").replace(",","")



def getProductList(url, type1, type2):
	sope = httpUtils.getHtmlFromUrl(url)
	ps = sope.find_all("div", recursive=False)
	for p in ps:
		descs = p.find_all("div", attrs={"class":"pws_item"})
		pLink = p.find("h3").find("a")
		pInfo = {
			"Product type1": type1,
			"Product type2": type2,
			"Product Name": getNodeText(p.find("h3")),
			"cat": p["data-productcode"],
		}
		for desc in descs:
			title = getNodeText(desc.find("div", class_="pws_label"))
			value = getNodeText(desc.find("div", class_="pws_value"))
			pInfo[title] = value
		
		getProductInfo("https://www.abcam.com"+pLink["href"], pInfo)
		
		

for pIndex in range(1,18):
	getProductList('https://www.abcam.com/products/loadmore?selected.classification=Cell+and+tissue+imaging+tools&pagenumber='+str(pIndex),'Cell and tissue imaging tools','')


# getProductList('https://www.abcam.com/products/loadmore?sortOptions=Relevance&selected.classification=Primary%20antibodies&selected.researchAreas=Immunology--Innate%20Immunity--Macrophage%20%2F%20Inflamm.&pagenumber=1','Primary antibodies','Fc Receptors')




excelUtils.generateExcelMultipleSheet('abcam3.xlsx', [
	{
		"name": 'abcam3',
		"header": headers1 ,
		"data": products1
	}
])