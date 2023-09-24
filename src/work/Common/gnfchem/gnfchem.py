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

ssl._create_default_https_context = ssl._create_unverified_context

products1 = []

headers1=['link', 'nav','Product type','Product Name','img','CAS NO.']


def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, type1):
	print(str(len(products1))+url)
	sope = httpUtils.getHtmlFromUrl(url)
	nav = sope.find("ul", attrs={"class":"path-nav"})
	pInfo = {
		"link": url,
		"Product type": type1,
		"nav":getNodeText(nav)
	}
	pName = getNodeText(sope.find("h1", attrs={"class":"product-title"}))
	pInfo["Product Name"] = pName
	summary = sope.find("section", attrs={"class":"product-summary"})
	lis = summary.find_all("li")
	for li in lis:
		title = getNodeText(li.find("em"))
		value = getNodeText(li).replace(title,"")
		title = title.replace(":", "")
		addHeader(headers1, title)
		pInfo[title] = value

	tabContent = sope.find("section", attrs={"class":"tab-panel-content"})
	ps = tabContent.find_all("p")
	for p in ps:
		strongList = p.find_all("strong")
		if len(strongList) == 1:
			title = getNodeText(strongList[0])
			addHeader(headers1, title)
			if title == "Specification":
				specStr = ""
				trs=[]
				if p.nextSibling != None and p.nextSibling.nextSibling != None:
					trs = p.nextSibling.nextSibling.find_all("tr")
				else:
					trs = tabContent.find_all("tr")
				for tr in trs:
					tds = tr.find_all("td")
					for inx,td in enumerate(tds):
						specStr += getNodeText(td)+(":" if inx < len(tds)-1 else "")
					specStr+=";\r\n"
				pInfo["Specification"] = specStr
			else:
				if p.nextSibling !=None:
					pInfo[title] = getNodeText(p.nextSibling.nextSibling)
	
	imgArea = sope.find("div", attrs={"class":"image-additional"})
	imgs = imgArea.find_all("li")
	imgNames = ""
	for inx,img in enumerate(imgs):
		imgLink = img.find("a")
		if imgLink != None:
			imgName = pInfo["Product Name"].replace(".", "").replace("/", "").replace("%", "").replace("(", "").replace(")", "").replace("|"0000, "")+str(inx)+".jpg"
			httpUtils.urllib_download(imgLink["href"], imgName)
			imgNames += imgName+","
	pInfo["img"] = imgNames

	casArea1 = sope.find_all("p")
	casArea2 = sope.find_all("tr")
	casArea3 = sope.find_all("span")

	for casArea in (casArea1+casArea2+casArea3):
		title = getNodeText(casArea)
		if "cas" in title.lower():
			pInfo["CAS NO."] = title.replace("CAS NO.:","").replace("CAS No.","")



	products1.append(pInfo.copy())
	



def getProductList(url, type1):
	sope = httpUtils.getHtmlFromUrl(url)
	ps = sope.find_all("div", attrs={"class":"product-item"})
	for p in ps:
		plink = p.find("a")
		if plink != None:
			getProductInfo(plink["href"], type1)


# getProductInfo('https://www.gnfchem.com/trisodium-citrate.html', 'aa')

getProductList('https://www.gnfchem.com/products/food-additives-food-additives-2-3/','Acidulants')
getProductList('https://www.gnfchem.com/products/amino-acids/','Amino Acids')
getProductList('https://www.gnfchem.com/products/amino-acids/page/2/','Amino Acids')

getProductList('https://www.gnfchem.com/products/food-additives-food-additives-2-2/','Antioxidants')
getProductList('https://www.gnfchem.com/products/food-additives-food-additives-2-8/','Cocoa Series')
getProductList('https://www.gnfchem.com/products/food-ingredientes/','Dehydrated Vegetables')
getProductList('https://www.gnfchem.com/products/food-additives-food-additives-2-9/','Emulsifiers')
getProductList('https://www.gnfchem.com/products/food-additives-food-additives-2-5/','Flavorings')
getProductList('https://www.gnfchem.com/products/food-additives-food-additives-2-6/','Phosphates')
getProductList('https://www.gnfchem.com/products/food-additives-food-additives-2-10/','Plant Extracts')
getProductList('https://www.gnfchem.com/products/food-additives/','Preservatives')
getProductList('https://www.gnfchem.com/products/food-additives-food-additives-2-7/','Proteins')

getProductList('https://www.gnfchem.com/products/food-additives-food-additives-2-4/','Sweeteners')
getProductList('https://www.gnfchem.com/products/food-additives-food-additives-2-4/page/2/','Sweeteners')

getProductList('https://www.gnfchem.com/products/food-additives-food-additives-2/','Thickeners')

getProductList('https://www.gnfchem.com/products/vitamins/','Vitamins')
getProductList('https://www.gnfchem.com/products/vitamins/page/2/','Vitamins')

getProductList('https://www.gnfchem.com/products/enzyme/','Enzyme')



excelUtils.generateExcelMultipleSheet('gnfchem.xlsx', [
	{
		"name": 'gnfchem',
		"header": headers1 ,
		"data": products1
	}
])