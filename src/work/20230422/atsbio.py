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


def getProductInfo(url):
	print(str(len(products1)) + "==" + url)
	sope = httpUtils.getHtmlFromUrl(url)

	pInfo = {
		"link": url,
	}
	
	pName = getNodeText(sope.find("h1", attrs={"class":"product_title entry-title"}))
	pInfo["Product Name"] = pName

	subTitle = getNodeText(sope.find("div", attrs={"class":"woocommerce-product-details__short-description"}))
	pInfo["sub title"] = subTitle

	sku = getNodeText(sope.find("div", attrs={"class":"product_meta"}))
	pInfo["sku"] = sku

	desc = getNodeText(sope.find("div", attrs={"class":"woocommerce-Tabs-panel woocommerce-Tabs-panel--description panel entry-content wc-tab"}))
	pInfo["description"] = desc
	
	cate = url.split("/")[-2]+".pdf"
	dataSheet = "https://www.atsbio.com/catalog/data/"+cate
	print(dataSheet)
	pInfo["data sheet"] = cate

	httpUtils.urllib_download(dataSheet, cate)
	products1.append(pInfo.copy())

def getProductList(url):
	sope = httpUtils.getHtmlFromUrl(url)
	ps = sope.find_all("div", attrs={"class":"astra-shop-summary-wrap"})

	for p in ps:
		pLink = p.find("a")
		print(pLink["href"])
		getProductInfo(pLink["href"])
			

headers=['link', 'Product Name', 'sub title', 'sku','description','data sheet']
# getProductInfo("https://atsbio.com/products/it27/")
# getProductList("https://atsbio.com/products/page/1/")
for pIndex in range(1, 34):
	getProductList("https://atsbio.com/products/page/"+str(pIndex)+"/")


# getProductInfo("https://www.jetbiofil.com/en/Product/info_itemid_1877_lcid_535.html")


excelUtils.generateExcelMultipleSheet('jetbiofil.xlsx', [
	{
		"name":"atsbio",
		"header": headers + customerHeader,
		"data": products1
	}
])