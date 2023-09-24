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
products2 = []
products3 = []
products4 = []
products5 = []
products6 = []
products7 = []
products8 = []
products9 = []
products10 = []
products11 = []
products12 = []
products13 = []
products14 = []
products15 = []
products16 = []
products17 = []
products18 = []
products19 = []
products20 = []
products21 = []

headers1=['link', 'Product type1','Product type2','Product Name','size','price']
headers2=['link', 'Product type1','Product type2','Product Name','size','price']
headers3=['link', 'Product type1','Product type2','Product Name','size','price']
headers4=['link', 'Product type1','Product type2','Product Name','size','price']
headers5=['link', 'Product type1','Product type2','Product Name','size','price']
headers6=['link', 'Product type1','Product type2','Product Name','size','price']
headers7=['link', 'Product type1','Product type2','Product Name','size','price']
headers8=['link', 'Product type1','Product type2','Product Name','size','price']
headers9=['link', 'Product type1','Product type2','Product Name','size','price']
headers10=['link', 'Product type1','Product type2','Product Name','size','price']
headers11=['link', 'Product type1','Product type2','Product Name','size','price']
headers12=['link', 'Product type1','Product type2','Product Name','size','price']
headers13=['link', 'Product type1','Product type2','Product Name','size','price']
headers14=['link', 'Product type1','Product type2','Product Name','size','price']
headers15=['link', 'Product type1','Product type2','Product Name','size','price']
headers16=['link', 'Product type1','Product type2','Product Name','size','price']
headers17=['link', 'Product type1','Product type2','Product Name','size','price']
headers18=['link', 'Product type1','Product type2','Product Name','size','price']
headers19=['link', 'Product type1','Product type2','Product Name','size','price']
headers20=['link', 'Product type1','Product type2','Product Name','size','price']
headers21=['link', 'Product type1','Product type2','Product Name','size','price']
type1s=[]

def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, type1, typeIndex):
	print(url)
	print(typeIndex)
	sope = httpUtils.getHtmlFromUrl(url)
	pNameArea = sope.find("h1", attrs={"class":"product-name hidden-sm-down"})
	pName = getNodeText(pNameArea)


	pInfo = {
		"link": url,
		"Product type1": type1,
		"Product Name": pName,
	}

	decss = sope.find_all("div", attrs={"class":"descr"})
	decss1 = sope.find_all("div", attrs={"class":"detail"})
	for decs in decss + decss1:
		divs = decs.find_all("div", recursive=False)
		if len(divs) == 2:
			title = getNodeText(divs[0])
			value = getNodeText(divs[1])
			if len(title) > 0:
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
				if typeIndex ==5:
					addHeader(headers6, title)
				if typeIndex ==6:
					addHeader(headers7, title)
				if typeIndex ==7:
					addHeader(headers8, title)
				if typeIndex ==8:
					addHeader(headers9, title)
				if typeIndex ==9:
					addHeader(headers10, title)
				if typeIndex ==10:
					addHeader(headers11, title)
				if typeIndex ==11:
					addHeader(headers12, title)
				if typeIndex ==12:
					addHeader(headers13, title)
				if typeIndex ==13:
					addHeader(headers14, title)
				if typeIndex ==14:
					addHeader(headers15, title)
				if typeIndex ==15:
					addHeader(headers16, title)
				if typeIndex ==16:
					addHeader(headers17, title)
				if typeIndex ==17:
					addHeader(headers18, title)
				if typeIndex ==18:
					addHeader(headers19, title)
				if typeIndex ==19:
					addHeader(headers20, title)
				if typeIndex ==20:
					addHeader(headers21, title)

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
	if typeIndex ==5:
		products6.append(pInfo.copy())
	if typeIndex ==6:
		products7.append(pInfo.copy())
	if typeIndex ==7:
		products8.append(pInfo.copy())
	if typeIndex ==8:
		products9.append(pInfo.copy())
	if typeIndex ==9:
		products10.append(pInfo.copy())
	if typeIndex ==10:
		products11.append(pInfo.copy())
	if typeIndex ==11:
		products12.append(pInfo.copy())
	if typeIndex ==12:
		products13.append(pInfo.copy())
	if typeIndex ==13:
		products14.append(pInfo.copy())
	if typeIndex ==14:
		products15.append(pInfo.copy())
	if typeIndex ==15:
		products16.append(pInfo.copy())
	if typeIndex ==16:
		products17.append(pInfo.copy())
	if typeIndex ==17:
		products18.append(pInfo.copy())
	if typeIndex ==18:
		products19.append(pInfo.copy())
	if typeIndex ==19:
		products20.append(pInfo.copy())
	if typeIndex ==20:
		products21.append(pInfo.copy())




def getProductList(url, type1, typeIndex):
	addHeader(type1s, type1)
	sope = httpUtils.getHtmlFromUrl(url)

	ps = sope.find_all("div", attrs={"class":"product"})
	for p in ps:
		pLink = p.find("a")
		getProductInfo("https://www.makingcosmetics.com"+pLink["href"], type1, typeIndex)
		


for pIndex in range(0, 10):
  getProductList('https://www.makingcosmetics.com/on/demandware.store/Sites-makingcosmetics-Site/en_US/Search-UpdateGrid?cgid=Active-Ingredients&start='+str(pIndex*12)+'&sz=12&selectedUrl=https%3A%2F%2Fwww.makingcosmetics.com%2Fon%2Fdemandware.store%2FSites-makingcosmetics-Site%2Fen_US%2FSearch-UpdateGrid%3Fcgid%3DActive-Ingredients%26start%3D36%26sz%3D12','Cosmeceuticals',0 )
for pIndex in range(0, 7):
  getProductList('https://www.makingcosmetics.com/on/demandware.store/Sites-makingcosmetics-Site/en_US/Search-UpdateGrid?cgid=Active-Ingredients-2&start='+str(pIndex*12)+'&sz=12&selectedUrl=https%3A%2F%2Fwww.makingcosmetics.com%2Fon%2Fdemandware.store%2FSites-makingcosmetics-Site%2Fen_US%2FSearch-UpdateGrid%3Fcgid%3DActive-Ingredients-2%26start%3D12%26sz%3D12','Sensitive Skin Actives', 1 )
for pIndex in range(0, 4):
  getProductList('https://www.makingcosmetics.com/on/demandware.store/Sites-makingcosmetics-Site/en_US/Search-UpdateGrid?cgid=Active-Ingredients-3&start='+str(pIndex*12)+'&sz=12&selectedUrl=https%3A%2F%2Fwww.makingcosmetics.com%2Fon%2Fdemandware.store%2FSites-makingcosmetics-Site%2Fen_US%2FSearch-UpdateGrid%3Fcgid%3DActive-Ingredients-3%26start%3D12%26sz%3D12','Skin Tone Actives',2)
for pIndex in range(0, 11):
  getProductList('https://www.makingcosmetics.com/on/demandware.store/Sites-makingcosmetics-Site/en_US/Search-UpdateGrid?cgid=Botanical-Ingredients&start='+str(pIndex*12)+'&sz=12&selectedUrl=https%3A%2F%2Fwww.makingcosmetics.com%2Fon%2Fdemandware.store%2FSites-makingcosmetics-Site%2Fen_US%2FSearch-UpdateGrid%3Fcgid%3DBotanical-Ingredients%26start%3D12%26sz%3D12','Botanical Ingredients',3)
for pIndex in range(0, 7):
  getProductList('https://www.makingcosmetics.com/on/demandware.store/Sites-makingcosmetics-Site/en_US/Search-UpdateGrid?cgid=Colors-Color-Blends&start='+str(pIndex*12)+'&sz=12&selectedUrl=https%3A%2F%2Fwww.makingcosmetics.com%2Fon%2Fdemandware.store%2FSites-makingcosmetics-Site%2Fen_US%2FSearch-UpdateGrid%3Fcgid%3DColors-Color-Blends%26start%3D12%26sz%3D12','Colors & Color Blends',4)
for pIndex in range(0, 4):
  getProductList('https://www.makingcosmetics.com/on/demandware.store/Sites-makingcosmetics-Site/en_US/Search-UpdateGrid?cgid=Conditioners&start='+str(pIndex*12)+'&sz=12&selectedUrl=https%3A%2F%2Fwww.makingcosmetics.com%2Fon%2Fdemandware.store%2FSites-makingcosmetics-Site%2Fen_US%2FSearch-UpdateGrid%3Fcgid%3DConditioners%26start%3D12%26sz%3D12','Conditioners' ,5)
for pIndex in range(0, 9):
  getProductList('https://www.makingcosmetics.com/on/demandware.store/Sites-makingcosmetics-Site/en_US/Search-UpdateGrid?cgid=Emollients&start='+str(pIndex*12)+'&sz=12&selectedUrl=https%3A%2F%2Fwww.makingcosmetics.com%2Fon%2Fdemandware.store%2FSites-makingcosmetics-Site%2Fen_US%2FSearch-UpdateGrid%3Fcgid%3DEmollients%26start%3D12%26sz%3D12','Emollients' ,6)
for pIndex in range(0, 6):
  getProductList('https://www.makingcosmetics.com/on/demandware.store/Sites-makingcosmetics-Site/en_US/Search-UpdateGrid?cgid=Emulsifiers&start='+str(pIndex*12)+'&sz=12&selectedUrl=https%3A%2F%2Fwww.makingcosmetics.com%2Fon%2Fdemandware.store%2FSites-makingcosmetics-Site%2Fen_US%2FSearch-UpdateGrid%3Fcgid%3DEmulsifiers%26start%3D12%26sz%3D12','Emulsifiers',7)
for pIndex in range(0, 4):
  getProductList('https://www.makingcosmetics.com/on/demandware.store/Sites-makingcosmetics-Site/en_US/Search-UpdateGrid?cgid=Flavors-Fragrances&start='+str(pIndex*12)+'&sz=12&selectedUrl=https%3A%2F%2Fwww.makingcosmetics.com%2Fon%2Fdemandware.store%2FSites-makingcosmetics-Site%2Fen_US%2FSearch-UpdateGrid%3Fcgid%3DFlavors-Fragrances%26start%3D12%26sz%3D12','Flavors & Fragrances' ,8)
for pIndex in range(0, 7):
  getProductList('https://www.makingcosmetics.com/on/demandware.store/Sites-makingcosmetics-Site/en_US/Search-UpdateGrid?cgid=Humectants&start='+str(pIndex*12)+'&sz=12&selectedUrl=https%3A%2F%2Fwww.makingcosmetics.com%2Fon%2Fdemandware.store%2FSites-makingcosmetics-Site%2Fen_US%2FSearch-UpdateGrid%3Fcgid%3DHumectants%26start%3D12%26sz%3D12','Humectants & Proteins',9)
for pIndex in range(0, 3):
  getProductList('https://www.makingcosmetics.com/on/demandware.store/Sites-makingcosmetics-Site/en_US/Search-UpdateGrid?cgid=Hair-Style&start='+str(pIndex*12)+'&sz=12&selectedUrl=https%3A%2F%2Fwww.makingcosmetics.com%2Fon%2Fdemandware.store%2FSites-makingcosmetics-Site%2Fen_US%2FSearch-UpdateGrid%3Fcgid%3DHair-Style%26start%3D12%26sz%3D12','Hair Styling',10 )
getProductList('https://www.makingcosmetics.com/on/demandware.store/Sites-makingcosmetics-Site/en_US/Search-UpdateGrid?cgid=Deodorants-Odor-Neutralizers&start=0&sz=12','Deodorants & Odor Neutralizers' ,11)

for pIndex in range(0, 4):
  getProductList('https://www.makingcosmetics.com/on/demandware.store/Sites-makingcosmetics-Site/en_US/Search-UpdateGrid?cgid=OTC-Active-Ingredients&start='+str(pIndex*12)+'&sz=12&selectedUrl=https%3A%2F%2Fwww.makingcosmetics.com%2Fon%2Fdemandware.store%2FSites-makingcosmetics-Site%2Fen_US%2FSearch-UpdateGrid%3Fcgid%3DOTC-Active-Ingredients%26start%3D12%26sz%3D12','OTC Actives & Sunscreens' ,12)
for pIndex in range(0, 3):
  getProductList('https://www.makingcosmetics.com/on/demandware.store/Sites-makingcosmetics-Site/en_US/Search-UpdateGrid?cgid=Preservatives-Stabilizers&start='+str(pIndex*12)+'&sz=12&selectedUrl=https%3A%2F%2Fwww.makingcosmetics.com%2Fon%2Fdemandware.store%2FSites-makingcosmetics-Site%2Fen_US%2FSearch-UpdateGrid%3Fcgid%3DPreservatives-Stabilizers%26start%3D12%26sz%3D12','Preservatives & Stabilizers',13)
for pIndex in range(0, 7):
  getProductList('https://www.makingcosmetics.com/on/demandware.store/Sites-makingcosmetics-Site/en_US/Search-UpdateGrid?cgid=Surfactants-Exfoliants&start='+str(pIndex*12)+'&sz=12&selectedUrl=https%3A%2F%2Fwww.makingcosmetics.com%2Fon%2Fdemandware.store%2FSites-makingcosmetics-Site%2Fen_US%2FSearch-UpdateGrid%3Fcgid%3DSurfactants-Exfoliants%26start%3D12%26sz%3D12','Surfactants & Exfoliants' ,14)
for pIndex in range(0, 4):
  getProductList('https://www.makingcosmetics.com/on/demandware.store/Sites-makingcosmetics-Site/en_US/Search-UpdateGrid?cgid=Texturizers-Fillers&start='+str(pIndex*12)+'&sz=12&selectedUrl=https%3A%2F%2Fwww.makingcosmetics.com%2Fon%2Fdemandware.store%2FSites-makingcosmetics-Site%2Fen_US%2FSearch-UpdateGrid%3Fcgid%3DTexturizers-Fillers%26start%3D12%26sz%3D12','Texturizers & Fillers',15)
for pIndex in range(0, 7):
  getProductList('https://www.makingcosmetics.com/on/demandware.store/Sites-makingcosmetics-Site/en_US/Search-UpdateGrid?cgid=Thickeners&start='+str(pIndex*12)+'&sz=12&selectedUrl=https%3A%2F%2Fwww.makingcosmetics.com%2Fon%2Fdemandware.store%2FSites-makingcosmetics-Site%2Fen_US%2FSearch-UpdateGrid%3Fcgid%3DThickeners%26start%3D12%26sz%3D12','Thickeners' ,16)
getProductList('https://www.makingcosmetics.com/on/demandware.store/Sites-makingcosmetics-Site/en_US/Search-UpdateGrid?cgid=Liquid-Sunscreens&start=0&sz=12','Liquid Sunscreens',17)
getProductList('https://www.makingcosmetics.com/on/demandware.store/Sites-makingcosmetics-Site/en_US/Search-UpdateGrid?cgid=Solid-Sunscreens&start=0&sz=12','Solid Sunscreens',18)

getProductList('https://www.makingcosmetics.com/on/demandware.store/Sites-makingcosmetics-Site/en_US/Search-UpdateGrid?cgid=UVA-Filters&start=0&sz=12','UVA Filters',19)
for pIndex in range(0, 2):
  getProductList('https://www.makingcosmetics.com/on/demandware.store/Sites-makingcosmetics-Site/en_US/Search-UpdateGrid?cgid=UVB-Filters&start='+str(pIndex*12)+'&sz=12&selectedUrl=https%3A%2F%2Fwww.makingcosmetics.com%2Fon%2Fdemandware.store%2FSites-makingcosmetics-Site%2Fen_US%2FSearch-UpdateGrid%3Fcgid%3DUVB-Filters%26start%3D12%26sz%3D12','UVB Filters',20)

# getProductInfo('https://www.makingcosmetics.com/SCR-AVOB-01.html?lang=en_US','Pigments',1)



excelUtils.generateExcelMultipleSheet('newdirections.xlsx', [
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
	},{
		"name": type1s[5],
		"header": headers6 ,
		"data": products6
	},{
		"name": type1s[6],
		"header": headers7 ,
		"data": products7
	},{
		"name": type1s[7],
		"header": headers8 ,
		"data": products8
	},{
		"name": type1s[8],
		"header": headers9 ,
		"data": products9
	},{
		"name": type1s[9],
		"header": headers10 ,
		"data": products10
	},{
		"name": type1s[10],
		"header": headers11 ,
		"data": products11
	},{
		"name": type1s[11],
		"header": headers12 ,
		"data": products12
	},{
		"name": type1s[12],
		"header": headers13 ,
		"data": products13
	},{
		"name": type1s[13],
		"header": headers14 ,
		"data": products14
	},{
		"name": type1s[14],
		"header": headers15 ,
		"data": products15
	},{
		"name": type1s[15],
		"header": headers16 ,
		"data": products16
	},{
		"name": type1s[16],
		"header": headers17 ,
		"data": products17
	},{
		"name": type1s[17],
		"header": headers18 ,
		"data": products18
	},{
		"name": type1s[18],
		"header": headers19 ,
		"data": products19
	},{
		"name": type1s[19],
		"header": headers20 ,
		"data": products20
	},{
		"name": type1s[20],
		"header": headers21 ,
		"data": products21
	}
])