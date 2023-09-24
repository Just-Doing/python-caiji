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
products2 = []

headers1=['link', 'category0', 'category1', 'category2', 'category3','Product Name','price','Description','packaging','Manufacturer Code','Manufacturer Name','Primary Market','Use','Brand','Size/Color','Sizing','Material','Fabrication']
headers2=['link', 'category0', 'category1', 'category2', 'category3','Product Name','price','Description','packaging','Manufacturer Code','Manufacturer Name','Primary Market','Use','Brand','Size/Color','Sizing','Material','Fabrication']
type1s=[]

def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, type1, data):
	print(str(len(products1))+url)
	pData = httpUtils.getJson(url)
	pInfo = {
		"link": "https://www.net32.com"+data["url"],
		"Product Name": data["name"],
		"price": data["price"],
		"Description": pData["description"],
		"packaging": data["packaging"],
		"Manufacturer Code": pData["manufacturerCode"] if "manufacturerCode" in pData else "",
		"Manufacturer Name": pData["manufacturerName"] if "manufacturerName" in pData else "",
		"Brand": pData["brandName"] if "brandName" in pData else "",
	}
	types = type1.split("---")
	for inx, typeStr in enumerate(types):
		if len(typeStr)>0:
			pInfo["category"+str(inx)] = typeStr
	npdAttributes= pData["npdAttributes"]
	for key in npdAttributes:
		pInfo[key] = npdAttributes[key]
		if types[0] == "牙髓":
			addHeader(headers1, key)
		else:
			if types[0] =="一次性产品":
				addHeader(headers2, key)

	if types[0] == "牙髓":
		products1.append(pInfo.copy())
	else:
		if types[0] =="一次性产品":
			products2.append(pInfo.copy())



def getProductList(url, data, type1):
	datas = httpUtils.postJson(url, data)
	if "facets" in datas:
		typeDatas = list(filter(lambda o: o["field"] == "category", datas["facets"]))
		if len(typeDatas)>0:
			typeData = typeDatas[0]
			typeList = typeData["values"]
			if len(typeList)>0:
				for type in typeList:
					para = data.copy()
					para["filters"][1]["value"] = type["value"]
					getProductList(url, para, type1+"---"+type["label"])
			else:
				for p in datas["productDetails"]:
					getProductInfo("https://www.net32.com/rest/neo/pdp/"+str(p["mp_id"]), type1, p)
				if datas["pagination"]["nextPage"] > 0:
					para = data.copy()
					para["page"] = datas["pagination"]["nextPage"]
					getProductList(url, para, type1)




getProductList('https://www.net32.com/rest/neo/search/get-search-results',{
	"searchParam": "",
	"page": 1,
	"resultsPerPage": 60,
	"isUgrIdRequired": False,
	"isBuyGetPage": False,
	"filters": [
		{
			"field": "availability",
			"value": "in stock"
		}, {
			"field": "category",
			"value":"Endodontic products"
		}
	],
	"sorting": [
		{
			"field": "priority",
			"direction": "desc"
		}
	],
	"tag": ""
},'牙髓' )


getProductList('https://www.net32.com/rest/neo/search/get-search-results',{
	"searchParam":"",
	"page":1,
	"resultsPerPage":60,
	"isUgrIdRequired":False,"isBuyGetPage":False,
	"filters":[{"field":"availability","value":"in stock"},
			{"field":"category","value":"Disposables"}],
			"sorting":[{"field":"priority","direction":"desc"}],"tag":""}, '一次性产品' )
  
# getProductList('https://www.net32.com/rest/neo/search/get-search-results','a')


type1s=['牙髓','一次性产品']

excelUtils.generateExcelMultipleSheet('net32.xlsx', [
	{
		"name": type1s[0],
		"header": headers1 ,
		"data": products1
	},{
		"name": type1s[1],
		"header": headers2,
		"data": products2
	}
])