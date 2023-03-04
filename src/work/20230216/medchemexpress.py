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
	sope = httpUtils.getRenderdHtmlFromUrl(url)
	nav = sope.find("div", attrs={"id":"bread"})
	pNameArea = sope.find("div", attrs={"id":"pro_detail_hd"})
	pNameH1 = pNameArea.find("h1")
	pName = pNameH1.find("strong")
	Synonyms = pNameH1.find("span")
	listNav = "Signaling Pathways > Apoptosis > Ferroptosis > Ferroptosis Inhibitor"
	if type == "2":
		listNav = "SignalingPathways > Apoptosis > Ferroptosis > Ferroptosis Activator"
	if listNav == "3":
		listNav = "Signaling Pathways > Apoptosis > Ferroptosis > Ferroptosis Inducer"

	dt = pNameArea.find("dt")
	dtSpans = dt.find_all("span")
	cat = ""
	Purity = ""
	for span in dtSpans:
		value = getNodeText(span)
		if "Cat. No.:" in value:
			cat = value.replace("Cat. No.:","")
		if "Purity:" in value:
			Purity = value.replace("Purity:","")


	pInfo = {
		"link": url,
		"listNav": listNav,
		"nav": getNodeText(nav),
		"Product Name": getNodeText(pName),
		"Synonyms": getNodeText(Synonyms).replace("Synonyms:",""),
		"Cat. No": cat,
		"Purity": Purity
	}

	sizeTable = sope.find(id="con_one_1")
	sizeTrs = sizeTable.find_all("tr")
	haveSolid=0
	Solid = ""
	for tr in sizeTrs:
		if getNodeText(tr) == "Solid":
			haveSolid=1
		trId = tr.get('id')
		if trId != None:
			if trId == "tr_dw_1":
				pInfo["Solution"] = getNodeText(tr.find("td"))
			if trId == "tr_dw_2":
				pInfo["Solid + Solvent"] = getNodeText(tr.find("td"))
			if "tr_mg_" in trId:
				Solid += getNodeText(tr.find("td"))+";"
		if "Get quote" in getNodeText(tr):
			Solid += getNodeText(tr.find("td"))+";"
	if haveSolid==1:
		pInfo["Solid"] = Solid
	pInfo["Size"] = Solid

	trs = sope.find_all("tr")
	for tr in trs:
		tds = tr.find_all("td", recursive=False)
		ths = tr.find_all("th", recursive=False)
		if len(tds) == 1 and len(ths) == 1:
			title = getNodeText(ths[0])
			value = getNodeText(tds[0])
			pInfo[title] = value
			addCustomerHeader(title)
	imgArea = sope.find("div", attrs={"class":"struct-img-wrapper"})
	if imgArea != None:
		img = imgArea.find("img")
		imgName = (pInfo["Cat. No"] if len(pInfo["Cat. No"]) > 0 else pInfo["CAS No."])+".png"
		httpUtils.urllib_download("https:"+img["src"], imgName)
		pInfo["imgName"]=imgName 


	print(pInfo)
	if type == "1":
		products1.append(pInfo.copy())
	if type == "2":
		products2.append(pInfo.copy())
	if type == "3":
		products3.append(pInfo.copy())

def getProductList(url, type):
	sope = httpUtils.getHtmlFromUrl(url)
	ps = sope.find("ul", attrs={"class":"sub_ctg_list_con"}).find_all("li")
	for p in ps:
		pLink = p.find("a")
		getProductInfo("https://www.medchemexpress.com"+pLink["href"], type)
			

for pIndex in range(1, 6):
	getProductList("https://www.medchemexpress.com/Targets/Ferroptosis/effect/inhibitor.html?page="+str(pIndex), '1')

for pIndex in range(1, 6):
	getProductList("https://www.medchemexpress.com/Targets/Ferroptosis/effect/activator.html?page="+str(pIndex), '2')

getProductList("https://www.medchemexpress.com/Targets/Ferroptosis/effect/inducer.html", '3')

# getProductInfo("https://www.medchemexpress.com/Ferrostatin-1.html", '1')

headers1=[
	'link','listNav','nav','Product Name','Synonyms','Cat. No','imgName','Solution','Solid + Solvent','Solid','CAS No.','Description','IC50 & Target','In Vitro','In Vivo',
	'Molecular Weight','Appearance','Formula','SMILES','Shipping','Storage','Solvent & Solubility','Purity'
]

headers2=[
	'link','listNav','nav','Product Name','Synonyms','Cat. No','imgName','Size','CAS No.','Description','In Vitro','In Vivo','Molecular Weight','Appearance','Formula','SMILES','Shipping','Storage','Solvent & Solubility','Purity'
]

headers3=[
	'link','listNav','nav','Product Name','Synonyms','Cat. No','imgName','Solution','Solid + Solvent','Solid','CAS No.','Description','IC50 & Target','In Vitro','In Vivo',
	'Molecular Weight','Appearance','Formula','SMILES','Shipping','Storage','Solvent & Solubility','Purity'
]


excelUtils.generateExcelMultipleSheet('medchemexpress.xlsx', [
	{
		"name":"Ferroptosis-Antibody",
		"header": headers1 ,
		"data": products1
	},
	{
		"name":"Ferroptosis-proteins",
		"header": headers2,
		"data": products2
	},
	{
		"name":"Ferroptosis-assay kits",
		"header": headers3,
		"data": products3
	}
])