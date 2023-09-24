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

ssl._create_default_https_context = ssl._create_unverified_context

products1 = []

headers1=['link', 'nav','Product type','Product Name','Cat. No.','Purity','Description']


def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, type1):
	print(str(len(products1))+url)
	sope = httpUtils.getHtmlFromUrl(url)
	pInfo = {
		"link": url,
	}
	trs = sope.find_all("tr")
	for tr in trs:
		tds = tr.find_all("td")
		ths = tr.find_all("th")
		if len(tds) == 1 and len(ths) == 1 :
			title = getNodeText(ths[0])
			value = getNodeText(tds[0])
			pInfo[title] = value
			addHeader(headers1, title)

	pNameArea = sope.find("div", attrs={"class":"detail_hd"})
	pInfo["Product Name"] = getNodeText(pNameArea.find("h1"))
	dt = pNameArea.find("dt")
	spans = dt.find_all("span")
	for span in spans:
		title = getNodeText(span)
		if "Cat. No." in title:
			pInfo["Cat. No."] = title.replace("Cat. No.:","")
		if "Purity" in title:
			pInfo["Purity"] = title.replace("Purity:","")

	desc = sope.find("p", attrs={"id":"product_syn"})
	pInfo["Description"] = getNodeText(desc)
	# imgArea = sope.find("div", attrs={"class":"struct-img-wrapper"})
	# img = imgArea.find("img", attrs={"class":"data-img"})
	# #保存图片
	# if img != None:
	# 	imgName = pInfo["Cat. No."] + ".jpg"
	# 	pInfo["img"]=imgName
	# 	httpUtils.urllib_download("https:"+img["src"], imgName)
	
	products1.append(pInfo.copy())
	



def getProductList(url, type1):
	sope = httpUtils.getHtmlFromUrl(url)
	ps = sope.find("ul", attrs={"class":"sub_ctg_list_con"}).find_all("li")
	for p in ps:
		plink = p.find("a")
		if plink != None:
			getProductInfo("https://www.medchemexpress.com"+plink["href"], type1)


# getProductInfo('https://www.gnfchem.com/trisodium-citrate.html', 'aa')

for pIndex in range(1, 33):
	getProductList('https://www.medchemexpress.com/click-chemistry/azide.html?page='+str(pIndex), 'Acidulants')

# getProductList('https://www.medchemexpress.com/click-chemistry/azide.html', 'Acidulants')

excelUtils.generateExcelMultipleSheet('medchemexpress.xlsx', [
	{
		"name": 'medchemexpress',
		"header": headers1 ,
		"data": products1
	}
])