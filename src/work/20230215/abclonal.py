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
products2 = []
products3 = []
customerHeader = []

def addCustomerHeader(title):
  if title not in customerHeader and len(title) > 0:
    customerHeader.append(title)

def getProductInfo(url, type):
	print(str(len(products1))+"-"+str(len(products2))+"-"+str(len(products3)) + "==" + url)
	sope = httpUtils.getHtmlFromUrl(url)
	nav = sope.find("h3", attrs={"itemscope":"breadcrumb"})
	pName = sope.find("h1", attrs={"itemprop":"name"})
	pInfo = {
		"link": url,
		"nav": getNodeText(nav),
		"Product Name": getNodeText(pName)
	}
	spans = sope.find_all("span")
	for span in spans:
		span_b_title = getNodeText(span.find("b"))
		if span_b_title =="Tested applications:":
			TestedApplications = span.find_all("a", attrs={"data-label": re.compile('^(?!none$).*$')})
			if len(TestedApplications):
				pInfo["Tested applications"]=""
				for o in TestedApplications: pInfo["Tested applications"]+=getNodeText(o)+";"

		if span_b_title =="Reactivity:":
			pInfo["Reactivity"] = getNodeText(span).replace("Reactivity:","")

	trs = sope.find_all("tr")
	for tr in trs:
		tds = tr.find_all("td")
		ths = tr.find_all("th")
		if len(tds)==1 and len(ths)==1:
			title = getNodeText(ths[0])
			value = getNodeText(tds[0])
			if len(title) > 0:
				pInfo[title] = value
				addCustomerHeader(title)

	back = sope.find("div", attrs={"id":"collapse2"})
	pInfo["Background"] = getNodeText(back)

	imgArea=sope.find("div", "slider1")
	if imgArea != None:
		imgs = imgArea.find_all("div", attrs={"class": "slide"})
		imgIndex = 0
		for img in imgs:
			classStr = img["class"]
			if classStr[0] == "slide":
				imgEl = img.find("img")
				imgIndex+=1
				imgName = pInfo["Catalog No."]+"-"+str(imgIndex)+".png"
				imgTitle = "Figures-"+str(imgIndex)
				imgDescTitle = "Figures-"+str(imgIndex)+"-description"
				httpUtils.urllib_download("https://abclonal.com"+imgEl["src"], imgName)
				pInfo[imgTitle] = imgName
				pInfo[imgDescTitle] = getNodeText(img.find("p"))

	pInfo["Research Area"]=getNodeText(sope.find("div", attrs={"id":"collapse6"}))
	sizeArea = sope.find("select", attrs={"class":"selectsize form-control"})
	if sizeArea != None:
		opts = sizeArea.find_all("option")
		if len(opts):
			sizeIndex = 0
			for opt in opts:
				sizeIndex += 1
				sizeTitle = "size-"+str(sizeIndex)
				pInfo[sizeTitle]=getNodeText(opt)

	print(pInfo)
	if type == "1":
		products1.append(pInfo.copy())
	if type == "2":
		products2.append(pInfo.copy())
	if type == "2":
		products3.append(pInfo.copy())

def getProductList(url, type):
	sope = httpUtils.getHtmlFromUrl(url)
	ps = sope.find_all("div", attrs={"class":"products-box clearfix"})
	for p in ps:
		pLink = p.find("a")
		getProductInfo("https://abclonal.com"+pLink["href"], type)
			

for pIndex in range(1, 12):
	getProductList("https://abclonal.com/index.php?m=Search&a=index&keyword=Ferroptosis&catid=129&rmab=0&p="+str(pIndex), '1')
getProductList("https://abclonal.com/search/index?keyword=Ferroptosis&catid=72", '2')
getProductList("https://abclonal.com/search/index?keyword=Ferroptosis&catid=1109", '2')
# getProductInfo("https://abclonal.com/catalog-antibodies/AcetylHMGB1K29RabbitpAb/A16002", "1")

headers1=[
	'link','nav','Product Name','Background','Research Area',
	'Figures-1','Figures-1-description',
	'Figures-2','Figures-2-description',
	'Figures-3','Figures-3-description',
	'Figures-4','Figures-4-description',
	'Figures-5','Figures-5-description',
	'size-1','size-2','size-3',
	'size-4','size-5',
	'size-6','size-7'
]




excelUtils.generateExcelMultipleSheet('abclonal.xlsx', [
	{
		"name":"Ferroptosis-Antibody",
		"header": headers1 + ['Tested applications','Reactivity','Catalog No.','Host species','Purification method','Isotype','Immunogen','Sequence','Gene ID','Swiss prot','Synonyms','Calculated MW','Observed MW','Recommended','dilution','Storage buffer','Application key','Positive samples','Cellular location','Customer validation','Research Area'],
		"data": products1
	},
	{
		"name":"Ferroptosis-proteins",
		"header": headers1 + ['Description','Bio-Activity','Purity','Endotoxin','Formulation','Species','Background','Synonym','Expressed Host','Tag','Swiss-Prot','Gene ID','Storage','Reconstitution'],
		"data": products2
	},
	{
		"name":"Ferroptosis-assay kits",
		"header": headers1 + ['Sample','Instrument','Detection','Assay Time','Conjugate','Assay Type','Sample type','Cross reacts with','Product overview','Intended use','Storage instructions','Sensitivity','Standard curve range','Components','Safety notes'],
		"data": products3
	}
])