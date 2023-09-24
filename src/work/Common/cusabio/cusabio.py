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

headers1=['link','Product Name','Target Names']
global latestState
latestState=None
now = datetime.datetime.now()

# 将当前时间转换为指定格式的字符串
formatted_time = now.strftime("%Y-%m-%d %H%M%S")



def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, currentInfo):
	global latestState
	print(str(len(products1))+url)
	sope=httpUtils.getHtmlFromUrl(url)
	pInfo = {
			"link": url,
		}
	divs = sope.find_all("div", attrs={"class":"item"})
	for div in divs:
		title = getNodeText(div.find("div", attrs={"class":"name"}))
		if "Target Names" in title:
			pInfo["Target Names"] = getNodeText(div.find("div", attrs={"class":"value"}))
	pName = getNodeText(sope.find("h1", attrs={"class":"margin-small-right"}))
	print(pName)
	pInfo["Product Name"] = pName
	products1.append(pInfo.copy())

	excelUtils.generateExcelMultipleSheet(formatted_time+'.xlsx', [
		{
			"name": 'cusabio',
			"header": headers1 ,
			"data": products1
		}
	])
	f = open('latestState.json','w')
	f.write( json.dumps(currentInfo))
	f.close()
	latestState=None

	

def getProductList(url, currentInfo):
	global latestState
	sope=httpUtils.getHtmlFromUrl(url)
	pArea = sope.find("div", attrs={"class":"table-responsive margin-big-top"})
	ps = pArea.find_all("tr")
	for inx, p in enumerate(ps):
		pLink = p.find("a")
		if latestState == None or inx >= latestState["proIndex"]:
			currentInfo["proIndex"] = inx
			if pLink != None:
				getProductInfo(pLink["href"], currentInfo)
	


with open('latestState.json','r') as file_to_read:
	content = file_to_read.read()
	latestState = json.loads(content)

for pIndex in range(1, 732):
	if latestState == None or pIndex >= latestState["pageIndex"]:
		getProductList("https://www.cusabio.com/catalog-54-"+str(pIndex)+".html", {"pageIndex": pIndex})



# getProductInfo("https://www.cusabio.com/Transmembrane-Protein/Recombinant-Mouse-Sialidase-4-Neu4--12927665.html", {"pageIndex": 1, "proIndex": 1})
