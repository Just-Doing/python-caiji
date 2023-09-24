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
		'link','Breadcrumb', 'Product type1','Product type2','cat','Product Name','applications','Product size','Concentration'
	]

def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, pInfo):
	print(str(len(products1))+"====="+url)
	sope = httpUtils.getHtmlFromUrl(url)
	nav = sope.find("nav", attrs={"id":"breadcrumbs"})
	pInfo["link"] = url
	pInfo["Breadcrumb"] = getNodeText(nav)

	labels = pInfo["Breadcrumb"].split('  ')
	if "Neurodegenerative disease" in labels:
		for inx,abel in enumerate(labels[labels.index("Neurodegenerative disease")+1:len(labels)]):
			labelTitle = "Classification lable"+str(inx)
			pInfo[labelTitle] = abel
			addHeader(headers1, labelTitle)


	# shippingInformation = sope.find("section", attrs={"id":"shipping-information"})
	# pInfo["Shipping info"] = getNodeText(shippingInformation)

	sizeSope = httpUtils.getJson("https://www.abcam.com/datasheetproperties/availability?abId="+pInfo["cat"].replace("ab", ""))
	sizeStr = ""
	sizes = sizeSope["size-information"]["Sizes"]
	for size in sizes:
		sizeTitle = size["Size"].replace("&micro;","µ")
		price = size["Price"]
		sizeStr += (sizeTitle + ":" + price+"|||")

	pInfo["Product size"] = sizeStr
			
	attributes = sope.find_all("li", attrs={"class":"attribute"})
	for attribute in attributes:
		title = getNodeText(attribute.find("h3", class_="name"))
		if title == "":
			title= getNodeText(attribute.find("div", class_="name"))
		value = getNodeText(attribute.find("div", class_="value"))
		if len(value) == 0:
			value = getNodeText(attribute)
		
		addHeader(headers1, title)
		pInfo[title] = value
	connStr = ""
	connectSope = httpUtils.getJson("https://www.abcam.com/datasheetproperties/concentrations?productId="+pInfo["cat"].replace("ab", ""))
	for conn in connectSope["Concentrations"]:
		connStr += conn+"\r\n"
	pInfo["Concentration"] = connStr

	application = sope.find("div", attrs={"id":"description_applications"})
	# applicationStr = ""
	# if application!=None:
	# 	appTds = application.find_all("td", class_="name")
	# 	for appTd in appTds:
	# 		applicationStr += getNodeText(appTd)+";"

	pInfo["applications"] = getNodeText(application)

	


	products1.append(pInfo.copy())


def getStr(size):
	return getNodeText(size).replace(".","").replace(" ","").replace(",","")



def getProductList(url, type1, type2):
	sope = httpUtils.getHtmlFromUrl(url)
	ps = sope.find_all("div", recursive=False)
	for p in ps:
		descs = p.find_all("div", attrs={"class":"pws_item"})
		h3=p.find("h3")
		pLink = h3.find("a")
		pInfo = {
			"Product type1": type1,
			"Product type2": type2,
			"Product Name": getNodeText(h3).replace(getNodeText(h3.find("span")), ''),
			"cat": p["data-productcode"],
		}
		for desc in descs:
			title = getNodeText(desc.find("div", class_="pws_label"))
			value = getNodeText(desc.find("div", class_="pws_value"))
			pInfo[title] = value
		
		getProductInfo("https://www.abcam.com"+pLink["href"], pInfo)
		
		

for pIndex in range(1,130):
	getProductList('https://www.abcam.com/products/loadmore?sortOptions=Relevance&selected.classification=Primary%20antibodies&selected.researchAreas=Neuroscience--Neurology%20process--Neurodegenerative%20disease&pagenumber='+str(pIndex),'Neurodegenerative disease','Primary antibodies')


for pIndex in range(1,27):
	getProductList('https://www.abcam.com/products/loadmore?sortOptions=Relevance&selected.classification=Proteins%20and%20Peptides&selected.researchAreas=Neuroscience--Neurology%20process--Neurodegenerative%20disease&pagenumber=2'+str(pIndex),'Neurodegenerative disease','Proteins and Peptides')


for pIndex in range(1,21):
	getProductList('https://www.abcam.com/products/loadmore?sortOptions=Relevance&selected.classification=ELISA%20and%20Matched%20Antibody%20Pair%20Kits&selected.researchAreas=Neuroscience--Neurology%20process--Neurodegenerative%20disease&pagenumber='+str(pIndex),'Neurodegenerative disease','ELISA and Matched Antibody Pair Kits')

for pIndex in range(1,15):
	getProductList('https://www.abcam.com/products/loadmore?sortOptions=Relevance&selected.classification=Cell%20lines%20and%20Lysates&selected.researchAreas=Neuroscience--Neurology%20process--Neurodegenerative%20disease&pagenumber='+str(pIndex),'Neurodegenerative disease','Cell lines and Lysates')

for pIndex in range(1,11):
	getProductList('https://www.abcam.com/products/loadmore?sortOptions=Relevance&selected.classification=Agonists%2C%20activators%2C%20antagonists%20and%20inhibitors&selected.researchAreas=Neuroscience--Neurology%20process--Neurodegenerative%20disease&pagenumber='+str(pIndex),'Neurodegenerative disease','Agonists, activators, antagonists and inhibitors')

# getProductInfo('https://www.abcam.com/products/primary-antibodies/nf-kb-p65-antibody-ab16502.html?productWallTab=ShowAll',{"cat":"ab255433"})
excelUtils.generateExcelMultipleSheet('abcam1.xlsx', [
	{
		"name": 'abcam1',
		"header": headers1 ,
		"data": products1
	}
])