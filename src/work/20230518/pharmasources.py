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
	specs = sope.find("div",class_="d1_2_1").find_all("b")
	for spec in specs:
		title = getNodeText(spec)
		if len(title) > 0:
			value = spec.next_sibling
			pInfo[title] = value

	specs2 = sope.find("ul", class_="pros_lb1").find_all("b")
	for spec2 in specs2:
		title = getNodeText(spec2)
		titles = title.split(":")
		value= ""
		if len(titles)>1 and len(titles[1])>0:
			title = titles[0]
			value = titles[1]
		else:
			value = spec2.next_sibling
		pInfo[title] = value


	pros_lb2 = sope.find("ul", class_="pros_lb2")
	if pros_lb2 != None:
		specs3 = pros_lb2.find_all(["p","li"])
		latestTypeIsDesc = True
		for spec3 in specs3:
			title = getNodeText(spec3)
			titles = title.split(":")
			if latestTypeIsDesc==True:
				latestTypeIsDesc = len(titles)==1
			if len(titles)>5:
				title1 = titles[0]
				value1 = titles[1]
				title2 = titles[2]
				value2= titles[3]
				title3 = titles[4]
				value3= titles[5]
				pInfo[title1] = value1
				pInfo[title2] = value2
				pInfo[title3] = value3
			else:
				if len(titles)>3:
					title1 = titles[0]
					value1 = titles[1]
					title2 = titles[2]
					value2= titles[3]
					pInfo[title1] = value1
					pInfo[title2] = value2
				else:
					if len(titles)>1:
						title1 = titles[0]
						value1 = titles[1]
						pInfo[title1] = value1
	
		functionOrPrescription = pros_lb2.find("strong")
		if functionOrPrescription !=None:
			title = getNodeText(functionOrPrescription)
			if title.lower() =="function" or title.lower()=="prescription":
				value = getNodeText(pros_lb2).replace(title, "")
				pInfo[title.lower()] = value

		if latestTypeIsDesc == True:
			pInfo["Product Description"] = getNodeText(pros_lb2)
	
	imgArea = sope.find("div", class_="d1_1")
	if imgArea != None:
		img = imgArea.find("img")
		if img != None:
			imgName = (pInfo["CAS No.:"] if "CAS No.:" in pInfo else pInfo["Product Name:"]) +".png"
			pInfo["Picture"] = imgName
			httpUtils.urllib_download(img["src"],imgName)
	products1.append(pInfo.copy())

def getProductList(url, type):
	sope = httpUtils.getHtmlFromUrl(url)
	pListArea = sope.find("ul", attrs={"class": "pro_lb1 center_img"})
	ps = pListArea.find_all("li")

	for p in ps:
		pLink = p.find("a")
		if pLink != None:
			href= pLink["href"]
			if len(href) > 5:
				getProductInfo(pLink["href"], type)
			

headers=['link', 'type','Picture','Category:','Product Name:','CAS No.:','Standard:','Grade:','Grade','Monthly Production Capacity:','Delivery Lead Time:','Factory Location:',
	 'Contract Manufacturing:','Sample Provided:','Main Sales Markets:','Packaging Information:','Payment Terms:','Melting point:','Purity:',
	 'Color:','Store:','Form:','Density:','Use:',
	 'Storage','Validity','Characters','Molecular Weight','Appearance','Molecular Formula','Specification','Properties',
	 'Storage:','Validity:','Characters:','Molecular Weight:','Appearance:','Molecular Formula:','Specification:','Properties:',
	 'Product Description','function','prescription']


# for pIndex in range(1, 335):
# 	getProductList("https://www.pharmasources.com/products/catid/pharmaceutical-intermediates-524-countall-n-page-"+str(pIndex),'Pharmaceutical Intermediates')
# for pIndex in range(1, 335):
# 	getProductList("https://www.pharmasources.com/products/catid/active-pharmaceutical-ingredients-4-countall-n-page-"+str(pIndex),'Active Pharmaceutical Ingredients')
with open("G:\git\python-caiji\src\work\20230521\tes.json") as f: 

	print(f["posts"])

# getProductInfo("https://www.pharmasources.com/products/abamectin-309262.html","ttt")


excelUtils.generateExcelMultipleSheet('pharmasources1.xlsx', [
	{
		"name":"cdnisotopes",
		"header": headers ,
		"data": products1
	}
])