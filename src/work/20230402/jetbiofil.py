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

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("window-size=1024,768")
chrome_options.add_argument("--proxy-server=http://127.0.0.1:33210")

# chrome_options.add_argument("--no-sandbox")
browser = webdriver.Chrome(chrome_options=chrome_options)
def getProductInfo(url):
	print(str(len(products1)) + "==" + url)
	browser.get(url)
	sope= BeautifulSoup(browser.page_source, "html.parser")

	pInfo = {
		"link": url,
	}
	pNameArea = sope.find("h1", attrs={"class":"product_title entry-title"})
	pName = getNodeText(pNameArea)
	pInfo["Product Name"] = pName
	cate = pNameArea.next_sibling
	pInfo["Catalog Number"] = cate.replace("Catalog Number:","")

	skuArea = sope.find("table", attrs={"class":"wc-product-table woocommerce dataTable no-footer dtr-inline"})
	if skuArea!= None:
		skus = skuArea.find("tbody").find_all("tr")
		skuStr = ""
		for sku in skus:
			tds = sku.find_all("td")
			if len(tds) > 2:
				skuStr += getNodeText(tds[0])+":"+getNodeText(tds[1])+"|||"
		pInfo["sku"] = skuStr


	imgArea = sope.find("div", attrs={"class":"woocommerce-product-gallery__image--placeholder"})
	if imgArea != None:
		img = imgArea.find("img")
		imgLink = img["src"]
		imgName = ""
		if "Catalog Number" in pInfo:
			imgName = pInfo["Catalog Number"]+".jpg"
		else:
			if "Product Name" in pInfo:
				imgName = pInfo["Product Name"]+".jpg"
		pInfo["img"] = imgName
		httpUtils.urllib_download(imgLink, imgName)
	archives = sope.find_all("a", attrs={"style":"position: relative; overflow: hidden;"})
	for archive in archives:
		archiveLink = archive["href"]
		if ".pdf" in archiveLink:
			pdfName = ""
			if "Catalog Number" in pInfo:
				pdfName = pInfo["Catalog Number"]+".pdf"
			else:
				if "Product Name" in pInfo:
					pdfName = pInfo["Product Name"]+".pdf"
			pInfo["pdf"] = pdfName
			httpUtils.urllib_download(archiveLink, pdfName)
		else:
			pInfo["PumbMed"] = archiveLink
	
	descArea = sope.find("div", attrs={"class":"desciption_box"})
	sescSope = BeautifulSoup(descArea.prettify().replace("Description","").replace("<br/>","sepator"), "html.parser", from_encoding="utf-8")
	specs = getNodeText(sescSope).split("sepator")
	specs = list(filter(lambda o: len(o.strip())>1, specs))
	for inx,item in enumerate(specs):
		specStr = item.strip().replace("\r","").replace("\n","")
		if len(specStr) >0:
			if "GENE NAME      (BOLD)    / SYNONYMS:" in specStr:
				pInfo["GENE NAME (BOLD) / SYNONYMS"] = specs[inx+1]
			if "SPECIES:" in specStr:
				pInfo["SPECIES"] = specs[inx+1]
			if "ENCODED PROTEIN NAME:" in specStr:
				pInfo["ENCODED PROTEIN NAME"] = specs[inx+1]
			if "Function:" in specStr:
				pInfo["Function"] = specs[inx+1]
			if "Sequence (" in specStr:
				pInfo["Sequence-Title"] = specStr
				pInfo["Sequence"] = specs[inx+1]

	products1.append(pInfo.copy())

def getProductList(url):
	sope = httpUtils.getHtmlFromUrl(url)
	ps = sope.find_all("tr")

	for p in ps:
		pLink = p.find("a")
		if pLink!= None:
			src = pLink["href"]
			if "www.pharna.com/product/" in src:
				getProductInfo(src)

			

headers=['link','Product Name', 'Catalog Number', 'sku','GENE NAME (BOLD) / SYNONYMS','SPECIES',
	 'ENCODED PROTEIN NAME','Function','Sequence-Title','Sequence','img','pdf','PumbMed']
getProductList("https://www.pharna.com/synthetic-mrna-products-2/")


# getProductInfo("https://www.pharna.com/product/1003201/")


excelUtils.generateExcelMultipleSheet('jetbiofil.xlsx', [
	{
		"name":"jetbiofil",
		"header": headers + customerHeader,
		"data": products1
	}
])