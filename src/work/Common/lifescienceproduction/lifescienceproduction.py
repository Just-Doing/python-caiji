from itertools import product
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import datetime
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
import xlrd

products1 = []

headers1=['link','cat','Product Name','price','size','description','sku','Categories','FileTitle','FileName','Related Products','img']
global latestState
latestState=None
now = datetime.datetime.now()

# 将当前时间转换为指定格式的字符串
formatted_time = now.strftime("%Y-%m-%d %H%M%S")



def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, type):
	print(str(len(products1))+url)
	sope= httpUtils.getHtmlFromUrl(url)
	productName = sope.find("h2", attrs={"class":"single-post-title product_title entry-title"})
	if productName != None:
		pInfo = {
			"link": url,
			"cat": type,
			"Product Name":getNodeText(productName)
		}

		priceArea = sope.find("p",attrs={"class":"price"})
		if priceArea != None:
			priceVal = getNodeText(priceArea.find("span", attrs={"class":"woocommerce-Price-amount amount"}))
			size = getNodeText(priceArea.find("span", attrs={"class":"uom"}))
			pInfo["price"] = priceVal
			pInfo["size"] = size

		descArea = sope.find("div", attrs={"class":"woocommerce-product-details__short-description"})
		pInfo["description"] = getNodeText(descArea)

		sku = sope.find("span", attrs={"class":"sku_wrapper"})
		posted_in = sope.find("span", attrs={"class":"posted_in"})
		pInfo["sku"] = getNodeText(sku)
		pInfo["Categories"] = getNodeText(posted_in)

		attTable = sope.find("table", attrs={"class":"woocommerce-product-attributes shop_attributes"})
		if attTable != None:
			trs = attTable.find_all("tr")
			for tr in trs:
				ths = tr.find_all("th")
				tds = tr.find_all("td")
				if len(ths) == 1 and len(tds) == 1:
					title = getNodeText(ths[0])
					value = getNodeText(tds[0])
					pInfo[title] = value
					addHeader(headers1, title)
		
		fileArea = sope.find("div", attrs={"id":"tab-product-literature"})
		if fileArea != None:
			links = fileArea.find_all("a")
			fileNames = ""
			fileNames1 = ""
			for link in links:
				href = link["href"]
				fileName = getNodeText(link)+".pdf"
				if ".pdf" in href:
					try:
						httpUtils.urllib_download(href, fileName)
						fileNames+=fileName+"|||"
						fileNames1 += getNodeText(link)+"|||"
					except Exception as e:
						print(e)
			pInfo["FileTitle"] = fileNames1
			pInfo["FileName"] = fileNames

		relateProduct = sope.find("ul", attrs={"class":"products oceanwp-row clr grid infinite-scroll-wrap"})
		if relateProduct != None:
			relateTitles = relateProduct.find_all("li", attrs={"class":"title"})
			relTitle = ""
			for relateTitle in relateTitles:
				relTitle += getNodeText(relateTitle)+"|||"
			pInfo['Related Products'] = relTitle

		imgArea = sope.find("figure", attrs={"class":"woocommerce-product-gallery__wrapper"})
		if imgArea != None:
			img = imgArea.find("img")
			if img != None:
				imgName = type.replace("||","")+".png"
				httpUtils.urllib_download(img["src"], imgName)
				pInfo["img"] = imgName



		products1.append(pInfo.copy())
		excelUtils.generateExcelMultipleSheet('lifescienceproduction.xlsx', [
			{
				"name": 'lifescienceproduction',
				"header": headers1 ,
				"data": products1
			}
		])

	

def getProductList(url, type):
	print(url)
	sope=httpUtils.getHtmlFromUrl(url)
	pListArea = sope.find("div", attrs={"id":"content"})
	if pListArea != None:
		for tr in pListArea.find_all("article"):
			pLink = tr.find("a")
			getProductInfo(pLink["href"], type)
	else:
		products1.append({"cat": type})

	
with open('data.json','r') as file_to_read:
	content = file_to_read.read()
	types = json.loads(content)
	for inx, type in enumerate(types):
		getProductList("https://lifescienceproduction.co.uk/?s="+type["cat"].replace("||",""), type["cat"].replace("||",""))

# getProductInfo("https://usbiolab.com/tissue-array/product/adrenal-gland/EAG-2081a",'')

