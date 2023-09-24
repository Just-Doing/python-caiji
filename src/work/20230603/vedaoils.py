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
import math
products1 = []
products2 = []
products3 = []
products4 = []
products5 = []

headers1=['link', 'Product type1','Product type2','Product Name','size','price']
headers2=['link', 'Product type1','Product type2','Product Name','size','price']
headers3=['link', 'Product type1','Product type2','Product Name','size','price']
headers4=['link', 'Product type1','Product type2','Product Name','size','price']
headers5=['link', 'Product type1','Product type2','Product Name','size','price']


def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, type1, type2, typeIndex):
	print(typeIndex)
	if typeIndex ==0:
		print(str(len(products1)) + "=1==" + url)
	if typeIndex ==1:
		print(str(len(products2)) + "=2==" + url)
	if typeIndex ==2:
		print(str(len(products3)) + "=3==" + url)
	if typeIndex ==3:
		print(str(len(products4)) + "=4==" + url)
	if typeIndex ==4:
		print(str(len(products5)) + "=5==" + url)

	sope = httpUtils.getHtmlFromUrl(url)
	pNameArea = sope.find("div", attrs={"class":"IndividualProductContent"})
	if pNameArea == None:
		pNameArea = sope.find("div", attrs={"class":"product-single__meta"})
	pName = getNodeText(pNameArea.find("h1"))

	pInfo = {
		"link": url,
		"Product type1": type1,
		"Product type2": type2,
		"Product Name": pName,
	}
	sizeStr = ""
	sizeAreas = sope.find_all("div", attrs={"class":"nm-easywholesale-name-and-price-only"})
	if len(sizeAreas) == 0:
		sizeArea = sope.find("span", attrs={"id":"ProductPrice-product-template"})
		sizeStr = getNodeText(sizeArea)
	else:
		for sizeArea in sizeAreas:
			size = getNodeText(sizeArea.find("div", attrs={"class":"nm-easywholesale-name"}))
			price = getNodeText(sizeArea.find("div", attrs={"class":"nm-easywholesale-price"}))
			sizeStr += size + ":" + price + ";"
	pInfo["size"] = sizeStr

	trs = sope.find_all("tr")
	for tr in trs:
		tds = tr.find_all("td")
		if len(tds) == 2:
			title = getNodeText(tds[0])
			value = getNodeText(tds[1])
			pInfo[title] = value
			if typeIndex ==0:
				addHeader(headers1, title)
			if typeIndex ==1:
				addHeader(headers2, title)
			if typeIndex ==2:
				addHeader(headers3, title)
			if typeIndex ==3:
				addHeader(headers4, title)
			if typeIndex ==4:
				addHeader(headers5, title)

	if typeIndex ==0:
		products1.append(pInfo.copy())
	if typeIndex ==1:
		products2.append(pInfo.copy())
	if typeIndex ==2:
		products3.append(pInfo.copy())
	if typeIndex ==3:
		products4.append(pInfo.copy())
	if typeIndex ==4:
		products5.append(pInfo.copy())
	print(pInfo)

def getStr(size):
	return getNodeText(size).replace(".","").replace(" ","").replace(",","")



def getProductList(url, type1, type2, typeIndex):
	sope = httpUtils.getHtmlFromUrl(url)
	productArea = sope.find("div", attrs={"id":"AjaxinateContainer"})
	ps = productArea.find_all("div", attrs={"class":"mx-box-sec item-relative grid-view-item"})
	for p in ps:
		pLink = p.find("a")
		getProductInfo("https://www.vedaoils.com"+pLink["href"], type1, type2, typeIndex)
		
		

def getProductPage(url, type1, type2, typeIndex):
	print(url)
	sope = httpUtils.getHtmlFromUrl(url)
  #页数 =  总数/40 
	totalCountArea = sope.find("span", attrs={"class":"filters-toolbar__product-count"})
	totalStr = getNodeText(totalCountArea).replace(" products","").replace(" product","")
	if totalStr != "":
		totalCount = math.ceil( int(totalStr)/40)
		for pIndex in range(1, totalCount+1):
				getProductList(url+"?page="+str(pIndex), type1, type2, typeIndex)

type1s=[]
def getProductType():
	htmlStr='<ul class="site-nav list--inline " id="SiteNav"><li class="site-nav--has-dropdown" aria-has-popup="true" aria-controls="SiteNavLabel-natural-oils"><a href="/collections/bulk-natural-oils" class="site-nav__link site-nav__link--main">  Natural Oils  <svg aria-hidden="true" focusable="false" role="presentation" class="icon icon--wide icon-chevron-down" viewBox="0 0 498.98 284.49"><defs><style>.cls-1{fill:#231f20}</style></defs><path class="cls-1" d="M80.93 271.76A35 35 0 0 1 140.68 247l189.74 189.75L520.16 247a35 35 0 1 1 49.5 49.5L355.17 511a35 35 0 0 1-49.5 0L91.18 296.5a34.89 34.89 0 0 1-10.25-24.74z" transform="translate(-80.93 -236.76)"></path></svg>  <span class="visually-hidden">expand</span></a><div class="site-nav__dropdown" id="SiteNavLabel-natural-oils" aria-expanded="false">  <ul>  <li>  <a href="https://www.vedaoils.com/collections/essential-oils" class="site-nav__link site-nav__child-link">Essentials Oils</a></li>  <li>  <a href="/collections/carrier-oils" class="site-nav__link site-nav__child-link">Carrier Oils</a></li>  <li>  <a href="/collections/spa-oils" class="site-nav__link site-nav__child-link">Spa Oils</a></li>  <li>  <a href="/collections/body-massage-oils" class="site-nav__link site-nav__child-link">Massage Oils</a></li>  <li>  <a href="/collections/diffuser-oils" class="site-nav__link site-nav__child-link">Diffuser Oils</a></li>  <li>  <a href="/collections/absolute-oils" class="site-nav__link site-nav__child-link">Absolute Oils</a></li>  <li>  <a href="/collections/essential-oils-blends" class="site-nav__link site-nav__child-link site-nav__link--last">Essential Oils Blends</a></li>  </ul>  </div>  </li><li class="site-nav--has-dropdown" aria-has-popup="true" aria-controls="SiteNavLabel-raw-ingredients"><a href="#" class="site-nav__link site-nav__link--main">  Raw Ingredients   <svg aria-hidden="true" focusable="false" role="presentation" class="icon icon--wide icon-chevron-down" viewBox="0 0 498.98 284.49"><defs><style>.cls-1{fill:#231f20}</style></defs><path class="cls-1" d="M80.93 271.76A35 35 0 0 1 140.68 247l189.74 189.75L520.16 247a35 35 0 1 1 49.5 49.5L355.17 511a35 35 0 0 1-49.5 0L91.18 296.5a34.89 34.89 0 0 1-10.25-24.74z" transform="translate(-80.93 -236.76)"></path></svg>  <span class="visually-hidden">expand</span></a><div class="site-nav__dropdown" id="SiteNavLabel-raw-ingredients" aria-expanded="false">  <ul>  <li>  <a href="https://www.vedaoils.com/collections/food-flavour-oils" class="site-nav__link site-nav__child-link">Flavour Oils</a></li>  <li>  <a href="/collections/liquid-bases" class="site-nav__link site-nav__child-link">Liquid Bases</a></li>  <li>  <a href="/collections/body-butters" class="site-nav__link site-nav__child-link">Body Butters</a></li>  <li>  <a href="/collections/floral-waters" class="site-nav__link site-nav__child-link">Floral Waters</a></li>  <li>  <a href="/collections/natural-clays" class="site-nav__link site-nav__child-link">Clay Powders</a></li>  <li>  <a href="/collections/dried-flowers" class="site-nav__link site-nav__child-link">Dried Flowers</a></li>  <li>  <a href="https://www.vedaoils.com/collections/Surfactants" class="site-nav__link site-nav__child-link">Surfactants</a></li>  <li>  <a href="/collections/herbal-powders" class="site-nav__link site-nav__child-link">Herbal Powders</a></li>  <li>  <a href="https://www.vedaoils.com/collections/additives-lye" class="site-nav__link site-nav__child-link">Additives &amp; Lyes</a></li>  <li>  <a href="https://www.vedaoils.com/collections/mica-powder" class="site-nav__link site-nav__child-link">Pigment Powders</a></li>  <li>  <a href="/collections/lip-balm-flavor-oils" class="site-nav__link site-nav__child-link">Lip Balm Flavor Oils</a></li>  <li>  <a href="https://www.vedaoils.com/collections/herbal-liquid-extract" class="site-nav__link site-nav__child-link">Herbal Liquid Extracts</a></li>  <li>  <a href="/collections/cosmetic-raw-materials" class="site-nav__link site-nav__child-link">Cosmetic Raw Materials</a></li>  <li>  <a href="https://www.vedaoils.com/collections/tools-and-equipments" class="site-nav__link site-nav__child-link">Tools &amp; Equipments</a></li>  <li>  <a href="https://www.vedaoils.com/collections/preservatives-stabilizers" class="site-nav__link site-nav__child-link">Preservatives &amp; Stabilizers</a></li>  <li>  <a href="/collections/oleoresins" class="site-nav__link site-nav__child-link site-nav__link--last">Oleoresins</a></li>  </ul>  </div>  </li><li class="site-nav--has-dropdown" aria-has-popup="true" aria-controls="SiteNavLabel-soap-supplies"><a href="/collections/soap-making-supplies" class="site-nav__link site-nav__link--main">  Soap Supplies  <svg aria-hidden="true" focusable="false" role="presentation" class="icon icon--wide icon-chevron-down" viewBox="0 0 498.98 284.49"><defs><style>.cls-1{fill:#231f20}</style></defs><path class="cls-1" d="M80.93 271.76A35 35 0 0 1 140.68 247l189.74 189.75L520.16 247a35 35 0 1 1 49.5 49.5L355.17 511a35 35 0 0 1-49.5 0L91.18 296.5a34.89 34.89 0 0 1-10.25-24.74z" transform="translate(-80.93 -236.76)"></path></svg>  <span class="visually-hidden">expand</span></a><div class="site-nav__dropdown" id="SiteNavLabel-soap-supplies" aria-expanded="false">  <ul>  <li>  <a href="/collections/melt-and-pour-soap-base" class="site-nav__link site-nav__child-link">Soap Bases</a></li>  <li>  <a href="https://www.vedaoils.com/collections/soap-molds" class="site-nav__link site-nav__child-link">Soap Molds</a></li>  <li>  <a href="/collections/soap-making-kits" class="site-nav__link site-nav__child-link">Soap Making Kits</a></li>  <li>  <a href="/collections/soap-making-colors" class="site-nav__link site-nav__child-link site-nav__link--last">Soap Making Colors</a></li>  </ul>  </div>  </li><li class="site-nav--has-dropdown" aria-has-popup="true" aria-controls="SiteNavLabel-candle-supplies"><a href="https://www.vedaoils.com/collections/candle-making-supplies-wholesale" class="site-nav__link site-nav__link--main">  Candle Supplies  <svg aria-hidden="true" focusable="false" role="presentation" class="icon icon--wide icon-chevron-down" viewBox="0 0 498.98 284.49"><defs><style>.cls-1{fill:#231f20}</style></defs><path class="cls-1" d="M80.93 271.76A35 35 0 0 1 140.68 247l189.74 189.75L520.16 247a35 35 0 1 1 49.5 49.5L355.17 511a35 35 0 0 1-49.5 0L91.18 296.5a34.89 34.89 0 0 1-10.25-24.74z" transform="translate(-80.93 -236.76)"></path></svg>  <span class="visually-hidden">expand</span></a><div class="site-nav__dropdown" id="SiteNavLabel-candle-supplies" aria-expanded="false">  <ul>  <li>  <a href="/collections/waxes" class="site-nav__link site-nav__child-link">Waxes</a></li>  <li>  <a href="/collections/candle-jars" class="site-nav__link site-nav__child-link">Candle Jars</a></li>  <li>  <a href="https://www.vedaoils.com/collections/candle-wick" class="site-nav__link site-nav__child-link">Candle Wicks</a></li>  <li>  <a href="https://www.vedaoils.com/collections/candle-molds" class="site-nav__link site-nav__child-link">Candle Molds</a></li>  <li class="site-nav--active">  <a href="/collections/candle-colours-dyes" class="site-nav__link site-nav__child-link">Candle Colors</a></li>  <li>  <a href="https://www.vedaoils.com/collections/diy-kits/products/diy-candle-making-kit" class="site-nav__link site-nav__child-link">Candle Making Kit</a></li>  <li>  <a href="https://www.vedaoils.com/collections/candle-wick-holder" class="site-nav__link site-nav__child-link site-nav__link--last">Candle Wick Holder</a></li>  </ul>  </div>  </li><li><a href="https://www.vedaoils.com/collections/fragrance-oils" class="site-nav__link site-nav__link--main">Fragrance Oils</a>  </li>  </ul>'
	sope = BeautifulSoup(htmlStr,  "html.parser", from_encoding="utf-8").find("ul")
	ps = sope.find_all("li", recursive=False)
	for inx, p in enumerate(ps):
		pLink = p.find("a")
		type1 = getNodeText(pLink).strip().replace("expand","")
		type1s.append(type1)
		if pLink != None:
			if type1 == "Fragrance Oils":
				getProductPage("https://www.vedaoils.com/collections/fragrance-oils", type1, '', inx)
			else:
				type2s = p.find_all("li")
				for type2 in type2s:
					pLink = type2.find("a")
					type2Str = getNodeText(pLink).strip().replace("expand","")
					# print(type1+"==="+type2Str)
					url = "" if "https://" in pLink["href"] else "https://www.vedaoils.com"
					getProductPage(url+pLink["href"], type1, type2Str, inx)
# type1s=['1','2','3','4','5']
# getProductInfo('https://www.vedaoils.com/collections/essential-oils/products/lavender-essential-oils','', '',0)
# getProductInfo('https://www.vedaoils.com/collections/food-flavour-oils/products/vanilla-flavour-oil','', '',1)
# getProductInfo('https://www.vedaoils.com/collections/melt-and-pour-soap-base/products/aloe-vera-melt-and-pour-soap-base','', '',2)
# getProductInfo('https://www.vedaoils.com/collections/waxes/products/white-beeswax-pellets','', '',3)
# getProductInfo('https://www.vedaoils.com/collections/fragrance-oils/products/oceanic-mist-fragrance-oil','', '',4)

getProductType()




excelUtils.generateExcelMultipleSheet('vedaoils.xlsx', [
	{
		"name": type1s[0],
		"header": headers1 ,
		"data": products1
	},{
		"name": type1s[1],
		"header": headers2 ,
		"data": products2
	},{
		"name": type1s[2],
		"header": headers3 ,
		"data": products3
	},{
		"name": type1s[3],
		"header": headers4 ,
		"data": products4
	},{
		"name": type1s[4],
		"header": headers5 ,
		"data": products5
	},
])