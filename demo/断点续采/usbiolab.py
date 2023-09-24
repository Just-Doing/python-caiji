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

products1 = []

headers1=['link','type1','Product Name','Brackish Medium','PH', 'MEDIA VOLUME', 'price','Description','Component']
global latestState
latestState=None
now = datetime.datetime.now()

# 将当前时间转换为指定格式的字符串
formatted_time = now.strftime("%Y-%m-%d %H%M%S")



def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, type, currentInfo):
	global latestState
	print(str(len(products1))+url)
	chrome_options = webdriver.ChromeOptions()
	# chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument("window-size=1024,768")

	# chrome_options.add_argument("--no-sandbox")
	browser = webdriver.Chrome(chrome_options=chrome_options)
	browser.get(url)
	sope= BeautifulSoup(browser.page_source, "html.parser")

	pInfo = {
		"link": url,
		"type1":type["t1"],
	}
	pName = sope.find("h2", attrs={"class":"product_name culture-media"})
	pInfo["Product Name"] = getNodeText(pName)
	brack = sope.find("a", attrs={"id": "media-waterType"})
	brackStr = getNodeText(brack).split("|")
	if len(brackStr) > 1:
		pInfo["Brackish Medium"] = brackStr[0]
		pInfo["PH"] = brackStr[1]
	
	sizeStr = ""
	price = "" 
	sizes = browser.find_elements_by_xpath("//div[@class='selector-wrapper']//option")
	for sizeInx in range(0, len(sizes)):
		sizeOpt = sizes[sizeInx]
		sizeOpt.click()
		sizeSope= BeautifulSoup(browser.page_source, "html.parser")
		sizeStr += sizeOpt.text+"|||"
		price += getNodeText(sizeSope.find("span", attrs={"class":"current_price"}))+"|||"
	pInfo["MEDIA VOLUME"] = sizeStr
	pInfo["price"] = price
	details = sope.find_all("h3", attrs={"class":"details-heading"})

	for detail in details:
		title = getNodeText(detail)
		if "Medium" in title:
			pInfo["Description"] = getNodeText(detail.findNextSibling("p"))
	componentArea = sope.find("table", attrs={"id":"responsive-table"})
	componentStr = ""
	if componentArea != None:
		trs = componentArea.find_all("tr")
		for inx,tr in enumerate(trs):
			if inx >0:
				tds = tr.find_all("td")
				componentStr += getNodeText(tds[1])+";"
	pInfo["Component"] = componentStr

	products1.append(pInfo.copy())
	excelUtils.generateExcelMultipleSheet(formatted_time+'.xlsx', [
		{
			"name": 'axispharm',
			"header": headers1 ,
			"data": products1
		}
	])
	f = open('latestState.json','w')
	f.write( json.dumps(currentInfo))
	f.close()
	latestState=None

	

def getProductList(url, type, currentInfo):
	global latestState
	sope=httpUtils.getHtmlFromUrl(url)
	pListArea = sope.find("table", attrs={"class":"table text-center main-table product"})
	if pListArea != None:
		for tr in pListArea.find_all("tr"):
			tds = tr.find_all("td")
			if len(tds) > 2:
				pLink = tr.find("a")
				getProductInfo("https://axispharm.com"+pLink["href"], type, currentInfo)

	

def getProductPage(url, type, currentInfo):
	global latestState
	currentInfo["pageIndex"] = 1
	getProductList(url, type, currentInfo)


# with open('latestState.json','r') as file_to_read:
# 	content = file_to_read.read()
# 	latestState = json.loads(content)

with open('data.json','r') as file_to_read:
	content = file_to_read.read()
	types = json.loads(content)
	for inx, type in enumerate(types):
		getProductInfo("https://utex.org"+type["url"], type, {"typeIndex": inx})

# getProductInfo("https://utex.org/products/modified-bold-3n-medium?variant=30991514763354",{"t1":"1"},{})

