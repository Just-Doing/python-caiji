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
products2 = []
products3 = []
products4 = []
products5 = []
products6 = []

headers1=['link','Product Name','description']
headers2=['link',"Product Name",'SDS-PAGE-img',"SEC-MALS-img","Bioactivity-img"]
headers3=['link',"Product Name",'SDS-PAGE-img',"SEC-MALS-img","Bioactivity-img"]
headers4=['link',"Product Name",'SDS-PAGE-img',"SEC-MALS-img","Bioactivity-img"]
headers5=['link',"Product Name",'SDS-PAGE-img',"SEC-MALS-img","Bioactivity-img"]
headers6=['link',"Product Name",'SDS-PAGE-img',"SEC-MALS-img","Bioactivity-img"]


def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProduct1Info(url):
	print(str(len(products1))+url)
	sope=httpUtils.getHtmlFromUrl(url)
	pInfo = {
		"link": url,
	}
	pName = sope.find("h1", attrs={"class":"product_title entry-title"})
	pInfo["Product Name"] = getNodeText(pName)

	desc = sope.find("div", attrs={"class":"woocommerce-product-details__short-description"})
	pInfo["description"] = getNodeText(desc)
	specArea = sope.find("div", attrs={"id":"tab-description"})
	specs = specArea.find_all("strong")
	for spec in specs:
		title = getNodeText(spec)
		value = spec.nextSibling
		if len(title) > 0:
			pInfo[title] = value
			addHeader(headers1, title)

	products1.append(pInfo.copy())
	
def getProduct2Info(url, type):
	print(str(len(products2))+"-"+str(len(products3))+"-"+str(len(products4))+"-"+str(len(products5))+"-"+str(len(products6))+url)
	sope=httpUtils.getHtmlFromUrl(url)
	pInfo = {
		"link": url,
	}
	pName = sope.find("div", attrs={"class":"companyActivityTop"})
	pInfo["Product Name"] = getNodeText(pName)

	items = sope.find_all("div", attrs={"class":"item_name"})
	for item in items:
		title = getNodeText(item)
		values = item.find_next_siblings("div", attrs={"class":"item_value"})
		value = ""
		for v in values:
			value += getNodeText(v) + "/r/n"
		
		if title == "SDS-PAGE":
			value = getNodeText(item.parent)
			img = item.parent.find("img")
			if img != None:
				imgName =  "SDS-PAGE"+str(len(products2))+"-"+str(len(products3))+"-"+str(len(products4))+"-"+str(len(products5))+"-"+str(len(products6)) +".jpg"
				httpUtils.urllib_download("https://www.acrobiosystems.com"+img["src"],imgName)
				pInfo["SDS-PAGE-img"] = imgName
		
		if title == "SEC-MALS":
			value = getNodeText(item.parent)
			img = item.parent.find("img")
			if img != None:
				imgName = "SEC-MALS"+ str(len(products2))+"-"+str(len(products3))+"-"+str(len(products4))+"-"+str(len(products5))+"-"+str(len(products6)) +".jpg"
				httpUtils.urllib_download("https://www.acrobiosystems.com"+img["src"], imgName)
				pInfo["SEC-MALS-img"] = imgName
		
		if "Bioactivity" in title:
			value = getNodeText(item.parent)
			img = item.parent.find("img")
			if img != None:
				imgName = "Bioactivity"+ str(len(products2))+"-"+str(len(products3))+"-"+str(len(products4))+"-"+str(len(products5))+"-"+str(len(products6)) +".jpg"
				httpUtils.urllib_download("https://www.acrobiosystems.com"+img["src"], imgName)
				pInfo["Bioactivity-img"] = imgName

		if type =="Tyrosine kinase":
			addHeader(headers2, title)
		if type =="Receptor tyrosine kinase":
			addHeader(headers3, title)
		if type =="Receptor tyrosine kinase Serine/threonine-protein kinase":
			addHeader(headers4, title)
		if type =="Protease":
			addHeader(headers5, title)
		if type =="Alkaline phosphatase-like enzyme":
			addHeader(headers6, title)
		pInfo[title] = value

	if type =="Tyrosine kinase":
		products2.append(pInfo.copy())
	if type =="Receptor tyrosine kinase":
		products3.append(pInfo.copy())
	if type =="Receptor tyrosine kinase Serine/threonine-protein kinase":
		products4.append(pInfo.copy())
	if type =="Protease":
		products5.append(pInfo.copy())
	if type =="Alkaline phosphatase-like enzyme":
		products6.append(pInfo.copy())


def getProduct1List(url):
	sope=httpUtils.getHtmlFromUrl(url)
	tableArea = sope.find("ul", attrs={"class":"products columns-4"})
	if tableArea != None:
		ps = tableArea.find_all("li")
		for p in ps:
			pLink = p.find("a")
			getProduct1Info(pLink["href"])
	

def getProduct2List(url, type):
	sope=httpUtils.getHtmlFromUrl(url)
	tableArea = sope.find("table", attrs={"class":"layui-table productSearchTable"})
	if tableArea != None:
		ps = tableArea.find("tbody").find_all("tr")
		for p in ps:
			pLink = p.find("a")
			getProduct2Info("https://www.acrobiosystems.com"+pLink["href"], type)



# getProduct1Info("https://eaglebio.com/product/human-klk13-elisa-kit/")
# getProduct2Info("https://www.acrobiosystems.com/P3600-Human-PTK7--CCK4-Protein-His-Tag-%28MALS-verified%29.html",'Receptor tyrosine kinase Serine/threonine-protein kinase')

for pIndex in range(1,4):
	getProduct1List("https://eaglebio.com/product-category/all-products/assay-kits/cancer-biomarker-kits/page/"+str(pIndex)+"/")

#第二种
getProduct2Info("https://www.acrobiosystems.com/P3127-Human-JAK1-Protein-His-Tag.html", "Tyrosine kinase")
getProduct2List("https://www.acrobiosystems.com/L-1113-PTK7.html", 'Tyrosine kinase')

#第三种
getProduct2List("https://www.acrobiosystems.com/L-25-Axl.html","Receptor tyrosine kinase") 
getProduct2List("https://www.acrobiosystems.com/L-192-EGF%20R.html","Receptor tyrosine kinase") 
getProduct2List("https://www.acrobiosystems.com/L-968-EGFRvIII.html","Receptor tyrosine kinase") 
getProduct2List("https://www.acrobiosystems.com/L-999-EphA2.html","Receptor tyrosine kinase") 
getProduct2List("https://www.acrobiosystems.com/L-1000-EphA4.html","Receptor tyrosine kinase") 
getProduct2List("https://www.acrobiosystems.com/L-1482-EphA5.html","Receptor tyrosine kinase") 
getProduct2List("https://www.acrobiosystems.com/L-1470-EphA10.html","Receptor tyrosine kinase") 
getProduct2List("https://www.acrobiosystems.com/L-198-EphB4.html","Receptor tyrosine kinase") 
getProduct2List("https://www.acrobiosystems.com/L-223-FGF%20R1.html","Receptor tyrosine kinase") 
getProduct2List("https://www.acrobiosystems.com/L-1115-FGF%20R2%20(IIIb).html","Receptor tyrosine kinase") 
getProduct2List("https://www.acrobiosystems.com/L-1118-FGF%20R2%20(IIIc).html","Receptor tyrosine kinase") 
getProduct2List("https://www.acrobiosystems.com/L-1290-FGF%20R3%20(IIIb).html","Receptor tyrosine kinase") 
getProduct2List("https://www.acrobiosystems.com/L-224-FGF%20R4.html","Receptor tyrosine kinase") 
getProduct2List("https://www.acrobiosystems.com/L-963-Flt-3.html","Receptor tyrosine kinase") 
getProduct2List("https://www.acrobiosystems.com/L-266-Her2.html","Receptor tyrosine kinase") 
getProduct2List("https://www.acrobiosystems.com/L-550-PDGF%20R%20alpha.html","Receptor tyrosine kinase") 
getProduct2List("https://www.acrobiosystems.com/L-407-PDGF%20R%20beta.html","Receptor tyrosine kinase") 
getProduct2List("https://www.acrobiosystems.com/L-974-MERTK.html","Receptor tyrosine kinase") 
getProduct2List("https://www.acrobiosystems.com/L-929-TrkA.html","Receptor tyrosine kinase") 
getProduct2List("https://www.acrobiosystems.com/L-393-TrkB.html","Receptor tyrosine kinase") 
getProduct2List("https://www.acrobiosystems.com/L-517-TYRO3.html","Receptor tyrosine kinase") 

#第四种
getProduct2List("https://www.acrobiosystems.com/L-14-Akt1.html","Receptor tyrosine kinase Serine/threonine-protein kinase") 
getProduct2List("https://www.acrobiosystems.com/L-15-ALK-1.html","Receptor tyrosine kinase Serine/threonine-protein kinase") 
getProduct2List("https://www.acrobiosystems.com/L-994-ALK-7.html","Receptor tyrosine kinase Serine/threonine-protein kinase") 
getProduct2List("https://www.acrobiosystems.com/L-1117-MASP3.html","Receptor tyrosine kinase Serine/threonine-protein kinase") 

#第五种
getProduct2List("https://www.acrobiosystems.com/L-376-MMP-1.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-377-MMP-2.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-1469-MMP-3.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-655-MMP-7.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-1291-MMP-8.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-378-MMP-9.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-1611-MMP-10.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-60-EMMPRIN.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-168-Cathepsin%20S.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-164-Cathepsin%20B.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-167-Cathepsin%20L.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-1101-Coagulation%20Factor%20III.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-1168-Coagulation%20factor%20VII.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-1387-Coagulation%20factor%20IX.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-1386-Coagulation%20factor%20X.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-984-Coagulation%20factor%20XI.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-10-ADAM8.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-1267-ADAM9.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-9-ADAM17.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-31-BACE-1.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-845-CD28H.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-182-DPPIV.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-193-ENPP-2.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-1102-ENPP3.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-1055-FAP.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-430-RENIN.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-946-PSCA.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-229-PSMA.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-415-PLAU.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-375-Neprilysin.html","Protease") 
getProduct2List("https://www.acrobiosystems.com/L-832-LOXL2.html","Protease") 

#第六种
getProduct2List("https://www.acrobiosystems.com/L-1385-ALPG.html","Alkaline phosphatase-like enzyme") 
getProduct2List("https://www.acrobiosystems.com/L-1596-ALPI.html","Alkaline phosphatase-like enzyme") 
getProduct2List("https://www.acrobiosystems.com/L-1595-ALPL.html","Alkaline phosphatase-like enzyme") 
getProduct2List("https://www.acrobiosystems.com/L-1499-ALPP.html","Alkaline phosphatase-like enzyme") 


excelUtils.generateExcelMultipleSheet('0909.xlsx', [
	{
		"name": 'Cancer Biomarker Kits',
		"header": headers1 ,
		"data": products1
	},{
		"name": 'Tyrosine kinase',
		"header": headers2 ,
		"data": products2
	},{
		"name": 'Receptor tyrosine kinase',
		"header": headers3 ,
		"data": products3
	},{
		"name": 'Receptor tyrosine kinase Serine threonine-protein kinase',
		"header": headers4 ,
		"data": products4
	},{
		"name": 'Protease',
		"header": headers5 ,
		"data": products5
	},{
		"name": 'Alkaline phosphatase-like enzyme',
		"header": headers6 ,
		"data": products6
	}
])