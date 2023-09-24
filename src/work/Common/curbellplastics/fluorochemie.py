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

headers1=['link','nav','type1','Product Name','Description','Features','Application','Packing','Transportation & Storage','Shelf life']


def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, type):
	print(str(len(products1)) + url)
	sope=httpUtils.getHtmlFromUrl(url)
	pInfo = {
		"link": url,
		"type1": type,
	}
	nav = sope.find("ol", attrs={"class":"breadcrumbs text-small"})
	pInfo["nav"] = getNodeText(nav)
	
	pInfo["Product Name"] = getNodeText(sope.find("h1", attrs={"class":"h3-size entry-title"}))

	specArea = sope.find("div", attrs={"class":"wpb_column vc_column_container vc_col-sm-12"})
	if specArea != None:
		pAreas = specArea.find_all("p")
		for pArea in pAreas:
			title = getNodeText(pArea.find("strong"))
			if "Description" in title:
				for p in pArea.next_siblings:
					value = getNodeText(p)
					if ":" in value:
						title = value.split(":")[0]
						pInfo[title] = value.split(":")[1]
						addHeader(headers1, title)

				valueStr = ""
				for p in pArea.next_siblings:
					value = getNodeText(p)
					if ":" not in value:
						valueStr = value
						break;
				pInfo["Description"]=valueStr

			if "Features" in title:
				pInfo["Features"]=getNodeText(pArea.findNextSibling("ul"))


			if "Application" in title:
				valueStr = ""
				for p in pArea.next_siblings:
					strong = p.find("strong")
					if strong != None:
						break;
					valueStr += getNodeText(p)+"\r\n"
				pInfo["Application"]=valueStr

			if "Packing" in title:
				valueStr = ""
				for p in pArea.next_siblings:
					strong = p.find("strong")
					if strong != None:
						break;
					valueStr += getNodeText(p)+"\r\n"
				pInfo["Packing"]=valueStr

			if "Transportation & Storage" in title:
				valueStr = ""
				for p in pArea.next_siblings:
					strong = p.find("strong")
					if strong != None:
						break;
					valueStr += getNodeText(p)+"\r\n"
				pInfo["Transportation & Storage"]=valueStr
			if "Shelf life" in title:
				valueStr = ""
				for p in pArea.next_siblings:
					strong = p.find("strong")
					if strong != None:
						break;
					valueStr += getNodeText(p)+"\r\n"
				pInfo["Shelf life"]=valueStr


		specTable = specArea.find("table")
		if specTable != None:
			specTrs = specTable.find_all("tr")
			for specTr in specTrs:
				tds = specTr.find_all("td")
				if len(tds) > 0:
					title = getNodeText(tds[0])
					valuesTr = ""
					for td in tds[1:]:
						valuesTr += getNodeText(td)+"/"
					pInfo[title] = valuesTr
					addHeader(headers1, title)

		products1.append(pInfo.copy())
	

def getProductList(url, type):
	sope=httpUtils.getHtmlFromUrl(url)

	tables = sope.find_all("table", attrs={"class":"tablepress"})
	for table in tables:
		thead = table.find("thead")
		tbody = table.find("tbody")
		trs = tbody.find_all("tr")
		if len(trs)>0:
			for tr in trs:
				tds = tr.find_all("td")
				pLink = tds[0].find("a")
				if pLink != None:
					typeIndex = -1
					if thead != None:
						ths = thead.find_all("th")
						for inx,th in enumerate(ths):
							if getNodeText(th) == "Type":
								typeIndex = inx

					if typeIndex > -1:
						tds = tr.find_all("td")
						getProductInfo(pLink['href'], getNodeText(tds[typeIndex]))
					else:
						getProductInfo(pLink['href'], '')
	



# getProductInfo('https://www.fluorochemie.com/product/perfluorocycloether-fc-77', '')

# getProductInfo('https://www.fluorochemie.com/product/general-purpose-fluorosilicone-rubber-compound-fs-r8700', '')


getProductList('https://www.fluorochemie.com/products#1559727450643-40042ed4-2c19','')



excelUtils.generateExcelMultipleSheet('fluorochemie.xlsx', [
	{
		"name": 'fluorochemie',
		"header": headers1 ,
		"data": products1
	}
])