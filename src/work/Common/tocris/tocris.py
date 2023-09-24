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
		'link','cat','img','Product Name','price','Biological Activity'
	]

def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, pInfo):
	print(str(len(products1))+"====="+url)
	sope = httpUtils.getRenderdHtmlFromUrl(url)
	pNameArea = sope.find("div", attrs={"id":"content_column"})
	if pNameArea != None:
		pInfo["Product Name"] = getNodeText(pNameArea.find("h1"))
	price = sope.find("tr", attrs={"class":"et_atc_product"})
	if price != None:
		pInfo["price"] = getNodeText(price.find("td"))
	product_infos = sope.find_all("div", attrs={"class":"product_info"})
	for product_info in product_infos:
		title = getNodeText(product_info.find("span"))
		value = getNodeText(product_info).replace(title, "")
		if len(title) > 0:
			pInfo[title] = value
			addHeader(headers1, title)
			
	ds_biological = sope.find("div", attrs={"id":"ds_biological_activity"})
	if ds_biological != None:
		pInfo["Biological Activity"] = getNodeText(ds_biological)

	ds_solubility = sope.find("div", attrs={"id":"ds_solubility"})
	ds_solubility_trs = []
	technical_trs = []
	if ds_solubility != None:
		ds_solubility_trs = ds_solubility.find_all("tr")
	ds_technical_data = sope.find("div", attrs={"id":"ds_technical_data"})
	if ds_technical_data != None:
		technical_trs = ds_technical_data.find_all("tr")

	for tr in ds_solubility_trs + technical_trs:
		tds = tr.find_all("td")
		if len(tds) == 2:
			title = getNodeText(tds[0])
			value = getNodeText(tds[1])
			if len(title) > 0:
				pInfo[title] = value
				addHeader(headers1, title)

	imgArea = sope.find("div", attrs={"id":"tocris_product_images"})
	if imgArea != None:
		img = imgArea.find("img")
		if img != None:
			imgName = pInfo["cat"]+".png"
			httpUtils.cutImgFromUrl(img["src"], imgName)
			pInfo["img"] = imgName


	products1.append(pInfo.copy())
	excelUtils.generateExcelMultipleSheet('tocris.xlsx', [
	{
		"name": 'tocris',
		"header": headers1 ,
		"data": products1
	}
])



def getProductList(url):
	print(url)
	sope = httpUtils.getRenderdHtmlFromUrl(url)
	ps = sope.find("table", attrs={"class":"pharm_prod_table table table-condensed"}).find("tbody").find_all("tr")
	for p in ps:
		tds = p.find_all("td")
		if len(tds)> 1:
			pLink = p.find("a")
			if pLink != None:
				pInfo = {
					"link":url,
					"cat": getNodeText(tds[0])
				}
				if "https://www.tocris.com" in pLink["href"]:
					getProductInfo(pLink["href"], pInfo)
				else:
					getProductInfo("https://www.tocris.com"+pLink["href"], pInfo)
			


# getProductList('https://www.tocris.com/cn/product-type/near-infrared-nir-fluorescent-dyes')
# getProductList('https://www.tocris.com/cn/product-type/click-reactive-fluorescent-dyes')
# getProductList('https://www.tocris.com/cn/product-type/cyanine-dyes')
# getProductList('https://www.tocris.com/cn/product-type/standard-fluorescein-coumarin-and-rhodamine-based-dyes')


# getProductList('https://www.tocris.com/cn/product-type/cell-viability-stains-and-dyes')
# getProductList('https://www.tocris.com/cn/product-type/enzyme-probes-and-enzyme-substrates')
# getProductList('https://www.tocris.com/cn/product-type/fluorescent-actin-probes')
# getProductList('https://www.tocris.com/cn/product-type/fluorescent-amyloid-beta-probes')
# getProductList('https://www.tocris.com/cn/product-type/fluorescent-cell-indicators-and-sensors')
# getProductList('https://www.tocris.com/cn/product-type/fluorescent-lipid-probes-and-cell-membrane-stains')
# getProductList('https://www.tocris.com/cn/product-type/fluorescent-lysosome-probes')
# getProductList('https://www.tocris.com/cn/product-type/fluorescent-receptor-probes')
# getProductList('https://www.tocris.com/cn/product-type/fluorescent-rna-probes')
# getProductList('https://www.tocris.com/cn/product-type/fluorescent-transporter-probes')
# getProductList('https://www.tocris.com/cn/product-type/histology-stains')
getProductList('https://www.tocris.com/cn/product-type/microtubules-probes')


getProductList('https://www.tocris.com/cn/product-type/fluorescent-cholesterol-probes')
getProductList('https://www.tocris.com/cn/product-type/dna-fluorescent-stains')
getProductList('https://www.tocris.com/cn/product-type/fluorescent-integrin-probes')
getProductList('https://www.tocris.com/cn/product-type/fluorescent-ion-indicators')


getProductList('https://www.tocris.com/cn/product-type/neuron-and-astrocyte-probes')
getProductList('https://www.tocris.com/cn/product-type/other-fluorescent-probes')

# for pIndex in range(1, 15):
# 	getProductList('https://www.tissuearray.com/tissue-arrays?page='+str(pIndex))


# getProductInfo('https://www.tissuearray.com/tissue-arrays/Adrenal_Gland/AD2081a',{"cat":"ab255433"})
excelUtils.generateExcelMultipleSheet('tocris.xlsx', [
	{
		"name": 'tocris',
		"header": headers1 ,
		"data": products1
	}
])