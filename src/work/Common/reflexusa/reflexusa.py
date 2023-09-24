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

headers1=['link','nav','type1','type2','Product Name','Cat. No.','price','imgName','Product Description','Accessories']


def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, type, type2):
	print(str(len(products1))+url)
	sope=httpUtils.getHtmlFromUrl(url)
	pInfo = {
		"link": url,
		"type1":type,
		"type2":type2
	}
	nav = sope.find("div", attrs={"class":"breadcrumbs"})
	pInfo["nav"] = getNodeText(nav)
	pName = sope.find("h1", attrs={"id":"item-contenttitle"})
	if pName == None:
		pName = sope.find("h1", attrs={"class":"contenttitle-center"})
	pInfo["Product Name"] = getNodeText(pName)
	formArea = sope.find("div", attrs={"class":"itemform productInfo"})
	if formArea == None:
		formArea=sope.find("div", attrs={"class":"itemform"})
	if formArea!=None:
		cate = formArea.find("div", attrs={"class":"code"})
		pInfo["Cat. No."] = getNodeText(cate)
		price = formArea.find("div", attrs={"class":"price-bold"})
		if price == None:
			price=formArea.find("div", attrs={"class":"sale-price-bold"})
		pInfo["price"] = getNodeText(price)

		multiOption = formArea.find_all("span", attrs={"class":"multiLineOption"})
		for multi in multiOption:
			title = getNodeText(multi.find("span", attrs={"class":"itemoption"}))
			values = ""
			options = multi.find_all("option")
			for option in options:
				values += getNodeText(option) + ";"
			addHeader(headers1, title)
			pInfo[title] = values
	
	itemarea = sope.find("div", attrs={"id":"itemarea"})
	if itemarea == None:
		itemarea = sope.find("div", attrs={"id":"contentarea"})
	if itemarea!=None:
		img = itemarea.find("img")
		if img != None:
			imgName = pInfo["Product Name"].replace('"',"").replace('.',"").replace('%',"") +".jpg"
			pInfo["imgName"] = imgName
			# httpUtils.urllib_download(img["src"],imgName)

	caption = sope.find("div", attrs={"id":"caption"})
	pInfo["Product Description"] = getNodeText(caption)
	AccessoriesStr = ""
	Accessories = sope.find("h2", attrs={"id":"accessorytitle"})
	if Accessories != None:
		contents = sope.find("div", attrs={"id":"contents"})
		if contents !=None:
			tds = contents.find_all("td")
			for td in tds:
				aName = getNodeText(td.find("div", class_="name"))
				aPrice = getNodeText(td.find("div", attrs={"class":"price-bold"}))
				aDescrption=""
				divs = td.find_all("div")
				if len(divs)>1:
					aDescrption = getNodeText(divs[1])
				aForm = td.find("form")
				huohao = getNodeText(aForm)
				AccessoriesStr=aName+"|"+aDescrption+"|"+aPrice+"|"+huohao+";\r\n"
			pInfo["Accessories"] = AccessoriesStr





	products1.append(pInfo.copy())
	

def getProductList(url, type,type2):
	print(url)
	sope=httpUtils.getHtmlFromUrl(url)
	Accessories = sope.find("h2", attrs={"id":"accessorytitle"})
	productArea = sope.find("div", attrs={"id":"itemarea"})
	if Accessories != None or productArea != None:
		getProductInfo(url, type, '')
	else:
		tableArea = sope.find("table", attrs={"id":"contents-table"})
		if tableArea != None:
			ps = tableArea.find_all("td")
			for p in ps:
				pLink = p.find("a")
				getProductInfo("https://www.reflexusa.com/"+pLink["href"], type, type2)
	

def getProductType(url, type):
	print(url)
	sope=httpUtils.getHtmlFromUrl(url)
	typeArea = sope.find("table", attrs={"id":"contents-table"})
	if typeArea != None:
		tds = typeArea.find_all("td")
		for td in tds:
			typeLink = td.find("a")
			link = typeLink["href"]
			if "https://" not in link:
				link = "https://www.reflexusa.com/"+link
			type2 = getNodeText(td.find("div", attrs={"class":"name"}))
			getProductList(link, type, type2)


# getProductList("https://www.reflexusa.com/windowslenses.html",'1','2')

getProductType('https://www.reflexusa.com/noname.html','Optics Lenses Prisms Polarizers')
getProductType('https://www.reflexusa.com/cuvettes-uv-vis-nir.html','UV-Vis-NIR Cells Cuvettes')
getProductType('https://www.reflexusa.com/delatula.html','Deuterium and Tungsten Lamps')
getProductType('https://www.reflexusa.com/d2holcatlam1.html','AA Lamps Graphite Tubes')
getProductType('https://www.reflexusa.com/d2holcatlam.html','Dies Mills Press Equipment')
getProductType('https://www.reflexusa.com/trancel.html','Liquid Solid Gas Analysis Cells')
getProductType('https://www.reflexusa.com/opatrprisrod.html','Variable Temp High Pressure Analysis Cells')
getProductType('https://www.reflexusa.com/section1.html','Reflectance Accessories and Fiber Optic Process Flow Cells')
getProductType('https://www.reflexusa.com/pidlapumelah.html','PID Lamps Pulsed Xenon Mercury Lamps Hg Xenon Lamps')

excelUtils.generateExcelMultipleSheet('chemsrc.xlsx', [
	{
		"name": 'reflexusa',
		"header": headers1 ,
		"data": products1
	}
])