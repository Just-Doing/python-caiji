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
customerHeader = []
sizeHeader=[]

def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, type1, type2, size):
	print(str(len(products1)) + "==" + url)
	sope = httpUtils.getHtmlFromUrl(url)
	sizeArea = sope.find("span", attrs={"itemprop":"priceSpecification"})
	if sizeArea == None:
		sizeArea = sope.find("strong", attrs={"class":"price"})

	pInfo = {
		"link": url,
		"Product type1": type1,
		"Product type2": type2,
		"Product Name": getNodeText(sope.find("h1", attrs={"class":"fn product-title"})),
		"size": size,
		"price": getNodeText(sizeArea),
	}

	ps = sope.find_all("p")
	for p in ps:
		title = getNodeText(p)
		if "INCI:" in title or "INCI Name:" in title:
			pInfo["INCI"] = title.replace("INCI:","").replace("INCI Name:","")
	
	
	descArea = sope.find("div", attrs={"class":"desc"})
	pInfo["DESCRIPTION"] = getNodeText(descArea)
	if descArea != None:
		descs = descArea.find_all("strong")
		for desc in descs:
			titleStr = getNodeText(desc)
			if ":" in titleStr:
				titles = titleStr.split(":")
				title = titles[0]
				value = titleStr.replace(title+":", "")
				if type1 =="Pigments":
					addHeader(headers1, title)
				if type1 =="Equipment and bottles":
					addHeader(headers2, title)
				if type1 =="Mineral Make-up":
					addHeader(headers3, title)
				if type1 =="Brushes":
					addHeader(headers4, title)
				if type1 =="Soapmaking":
					addHeader(headers5, title)
				
				pInfo[title] = value

	table = sope.find("table", class_="table")
	if table!=None:
		trs = table.find_all("tr")
		for tr in trs:
			tds = tr.find_all("td")
			if len(tds) == 2:
				title = getNodeText(tds[0])
				value = getNodeText(tds[1])
				if type1 =="Pigments":
					addHeader(headers1, title)
				if type1 =="Equipment and bottles":
					addHeader(headers2, title)
				if type1 =="Mineral Make-up":
					addHeader(headers3, title)
				if type1 =="Brushes":
					addHeader(headers4, title)
				if type1 =="Soapmaking":
					addHeader(headers5, title)
				pInfo[title] = value

	if type1 =="Pigments":
		products1.append(pInfo.copy())
	if type1 =="Equipment and bottles":
		products2.append(pInfo.copy())
	if type1 =="Mineral Make-up":
		products3.append(pInfo.copy())
	if type1 =="Brushes":
		products4.append(pInfo.copy())
	if type1 =="Soapmaking":
		products5.append(pInfo.copy())
	

def getStr(size):
	return getNodeText(size).replace(".","").replace(" ","").replace(",","")

def getProductSize(url, type1, type2):
	sope = httpUtils.getHtmlFromUrl(url)
	pName = sope.find("div", attrs={"class":"product-headline"})
	if pName != None:
		sizes = sope.find_all("span", attrs={"class":"label-variation"})
		if len(sizes) > 0:
			for size in sizes:
				if "Pigment-weiss-Titandioxid" in url:
					getProductInfo("https://www.alexmo-cosmetics.de/Pigment-weiss-"+getStr(size)+"-Titandioxid", type1, type2, getNodeText(size))
				else:
					if "Arrowroot-organic-ground-Pfeilwurzel-organic-gemahlen" in url:
						getProductInfo("https://www.alexmo-cosmetics.de/Arrowroot-organic-ground-"+getStr(size)+"-Pfeilwurzel-organic-gemahlen-"+getStr(size), type1, type2, getNodeText(size))
					else:
						if "Pigment-green-10g" in url:
							getProductInfo("https://www.alexmo-cosmetics.de/Pigment-green-"+getStr(size), type1, type2, getNodeText(size))
						else:
							if "Pigment-MiAmore-10g" in url:
								getProductInfo("https://www.alexmo-cosmetics.de/Pigment-MiAmore-"+getStr(size), type1, type2, getNodeText(size))
							else:
								if "Iron-Oxide-Red-Pigment-rot" in url:
									getProductInfo("https://www.alexmo-cosmetics.de/Iron-Oxide-Red-"+getStr(size)+"-Pigment-rot", type1, type2, getNodeText(size))
								else:
									if "iron-oxides-redbrown-30g" in url:
										if getStr(size)=="1000g":
											getProductInfo("https://www.alexmo-cosmetics.de/Iron-oxides-redbrown-1000g-Pigrment-rotbraun-1000g", type1, type2, getNodeText(size))
										else:
											getProductInfo("https://www.alexmo-cosmetics.de/Iron-oxides-redbrown-"+getStr(size)+"-Pigment-rotbraun-"+getStr(size), type1, type2, getNodeText(size))
									else:
										if "Iron-Oxide-Black-Pigment-schwarz" in url:
											getProductInfo("https://www.alexmo-cosmetics.de/Iron-Oxide-Black-"+getStr(size)+"-Pigment-schwarz", type1, type2, getNodeText(size))
										else:
											if "Flaming-Lights-10g_3" in url:
												getProductInfo("https://www.alexmo-cosmetics.de/Flaming-Lights-"+getStr(size)+"_1", type1, type2, getNodeText(size))
											else:
												if "Indian-Summer-10g_3" in url:
													getProductInfo("https://www.alexmo-cosmetics.de/Indian-Summer-"+getStr(size)+"_1", type1, type2, getNodeText(size))
												else:
													if "Le-Rouge-10g" in url:
														getProductInfo("https://www.alexmo-cosmetics.de/Le-Rouge-"+getStr(size)+"_1", type1, type2, getNodeText(size))
													else:
														if "Beige_3" in url:
															getProductInfo("https://www.alexmo-cosmetics.de/Beige-"+getStr(size)+"_1", type1, type2, getNodeText(size))
														else:
															if "blue-bottles-Blauglasflasche" in url:
																getProductInfo("https://www.alexmo-cosmetics.de/blue-bottles-"+getStr(size)+"-Blauglasflasche-"+getStr(size), type1, type2, getNodeText(size))
															else:
																if "Glass-pipette-Glaspipette-mit-weissem-Sauger" in url:
																	getProductInfo("https://www.alexmo-cosmetics.de/Glass-pipette-"+getStr(size)+"-Glaspipette-mit-weissem-Sauger-"+getStr(size), type1, type2, getNodeText(size))
																else:
																	if "Glass-jar-with-bamboo-screw-cap-Glastiegel-mit-Bambus-Schraubverschluss" in url:
																		if getStr(size) == "5ml":
																			getProductInfo("https://www.alexmo-cosmetics.de/Glass-jar-with-bamboo-screw-cap-Glastiegel-mit-Bambus-Schraubverschluss-5ml", type1, type2, getNodeText(size))
																		else:
																			getProductInfo("https://www.alexmo-cosmetics.de/Glass-jar-with-bamboo-screw-cap-"+getStr(size)+"-Glastiegel-mit-Bambus-Schraubverschluss-"+getStr(size), type1, type2, getNodeText(size))
																	else:
																		if "Pipette-bottle-black-20ml-Pipettenflasche-schwarz-20ml" in url:
																			if getStr(size) == "1piece":
																				getProductInfo("https://www.alexmo-cosmetics.de/Pipette-bottle-black-20ml-1-piece-Pipettenflasche-schwarz-20ml-1Stueck", type1, type2, getNodeText(size))
																			else:
																				getProductInfo("https://www.alexmo-cosmetics.de/Pipette-bottle-black-20ml-"+getNodeText(size).replace(" piece","")+"-piece-Pipettenflasche-schwarz-20ml-"+getNodeText(size).replace(" piece","")+"-Stueck", type1, type2, getNodeText(size))
																		else:
																			if "Rollrandglas" in url:
																				getProductInfo("https://www.alexmo-cosmetics.de/Rolled-rim-bottles-"+getStr(size)+"-Rollrandglas-"+getNodeText(size).replace(" ml","")+"-ml", type1, type2, getNodeText(size))
																			else:
																				if "blue-bottles-Blauglasflasche" in url:
																					getProductInfo("https://www.alexmo-cosmetics.de/blue-bottles-"+getStr(size)+"-Blauglasflasche-"+getStr(size), type1, type2, getNodeText(size))
																				else:
																					if "Glass-pipette-Glaspipette-mit-weissem-Sauger" in url:
																						getProductInfo("https://www.alexmo-cosmetics.de/Glass-pipette-"+getStr(size)+"-Glaspipette-mit-weissem-Sauger-"+getStr(size), type1, type2, getNodeText(size))
																					else:
																						if "Glass-jar-with-bamboo-screw-cap-Glastiegel-mit-Bambus-Schraubverschluss" in url:
																							getProductInfo("https://www.alexmo-cosmetics.de/Glass-jar-with-bamboo-screw-cap-"+getStr(size)+"-Glastiegel-mit-Bambus-Schraubverschluss-"+getStr(size), type1, type2, getNodeText(size))
																						else:
																							if "Pipette-bottle-black-20ml-Pipettenflasche-schwarz-20ml" in url:
																								getProductInfo("https://www.alexmo-cosmetics.de/Pipette-bottle-black-20ml-"+getNodeText(size).replace(" piece","")+"-piece-Pipettenflasche-schwarz-20ml-"+getNodeText(size).replace(" piece","")+"-Stueck", type1, type2, getNodeText(size))
																							else:
																								if "Mineral-Foundation-Jar-with-sifter-Powder-or-Rouge" in url:
																									getProductInfo("https://www.alexmo-cosmetics.de/Jar-with-sifter-"+getStr(size)+"-Dose-fuer-Mineral-Foundation-Puder-oder-Rouge-"+getNodeText(size).replace(" ml","")+"-ml", type1, type2, getNodeText(size))
																								else:
																									if "Pasteur-pipettes" in url:
																										getProductInfo("https://www.alexmo-cosmetics.de/Pasteur-pipettes"+("_1" if getStr(size)=="25piece" else ""), type1, type2, getNodeText(size))
																									else:
																										if "Colorbox" in url:
																											units = getNodeText(size).split(" ")
																											getProductInfo("https://www.alexmo-cosmetics.de/Colorbox-"+units[0]+"-Stueck", type1, type2, getNodeText(size))
																										else:
																											if "Cream-jar-Green-PE-nature-Cremedose-Green-PE-natur" in url:
																												getProductInfo("https://www.alexmo-cosmetics.de/Cream-jar-Green-PE-nature-"+getStr(size)+"-Cremedose-Green-PE-natur-"+getStr(size), type1, type2, getNodeText(size))
																											else:
																												if "Deostick-Papertube" in url:
																													units = getNodeText(size).split(" ")
																													getProductInfo("https://www.alexmo-cosmetics.de/Deostick-Papertube-"+units[0]+"-Stueck", type1, type2, getNodeText(size))
																												else:
																													if "DIY-Liner-fuer-Lip-und-Eyeliner-aus-Cellulose" in url:
																														units = getNodeText(size).split(" ")
																														getProductInfo("https://www.alexmo-cosmetics.de/DIY-Liner-fuer-Lip-und-Eyeliner-aus-Cellulose-"+units[0]+"-Stueck", type1, type2, getNodeText(size))
																													else:
																														if "Lipbalm-Papertube-Colour" in url:
																															units = getNodeText(size).split(" ")
																															getProductInfo("https://www.alexmo-cosmetics.de/Lipbalm-Papertube-Colour-"+units[0]+"-Stueck", type1, type2, getNodeText(size))
																														else:
																															if "Lipbalm-Papertube-Nature" in url:
																																getProductInfo("https://www.alexmo-cosmetics.de/Lipbalm-Papertube-Nature-"+getStr(size).replace("piece","")+"-piece", type1, type2, getNodeText(size))
																															else:
																																if "Luffa-Peeling-Pad" in url:
																																	units = getNodeText(size).split(" ")
																																	getProductInfo("https://www.alexmo-cosmetics.de/Luffa-Peeling-Pad-"+units[0]+"-Stueck", type1, type2, getNodeText(size))
																																else:
																																	if "Loofah-disc-Luffa-Scheibe" in url:
																																		getProductInfo("https://www.alexmo-cosmetics.de/Loofah-disc-"+getStr(size).replace("piece","")+"-piece-Luffa-Scheibe-"+getStr(size).replace("piece","")+"-Stueck", type1, type2, getNodeText(size))
																																	else:
																																		if "Powderbox" in url:
																																			units = getNodeText(size).split(" ")
																																			getProductInfo("https://www.alexmo-cosmetics.de/Powderbox-"+units[0]+"-Stueck", type1, type2, getNodeText(size))
																																		else:
																																			if "Becherglas-high-form-hohe-Form" in url:
																																				getProductInfo("https://www.alexmo-cosmetics.de/Beaker-glass-high-form-"+getStr(size)+"-Becherglas-hohe-Form-"+getStr(size), type1, type2, getNodeText(size))
																																			else:
																																				if "Beaker-low-form-Becherglas-niedrige-Form" in url:
																																					getProductInfo("https://www.alexmo-cosmetics.de/Beaker-glass-low-form-"+getStr(size)+"-Becherglas-niedrige-Form-"+getStr(size), type1, type2, getNodeText(size))
																																				else:
																																					if "Magic-Towel" in url:
																																						units = getNodeText(size).split(" ")
																																						getProductInfo("https://www.alexmo-cosmetics.de/Magic-Towel-"+units[0]+"-Stueck", type1, type2, getNodeText(size))
																																					else:
																																						if "Aprikosenkernoel-kaltgepresst-organic" in url and getStr(size)=="2500ml":
																																							getProductInfo("https://www.alexmo-cosmetics.de/Aprikosenkernoel-kaltgepresst-organic", type1, type2, getNodeText(size))
																																						else:
																																							if "Acocadooel-gruen-organic" in url:
																																								getProductInfo("https://www.alexmo-cosmetics.de/Avocadooel-gruen-organic-"+getStr(size), type1, type2, getNodeText(size))
																																							else:
																																								if "Mangobutter-organic" in url:
																																									if getStr(size)=="2500ml":
																																										getProductInfo("https://www.alexmo-cosmetics.de/Mangobutter-organic-2500ml", type1, type2, getNodeText(size))
																																									else:
																																										if getStr(size)=="5000ml":
																																											getProductInfo("https://www.alexmo-cosmetics.de/Mangobutter-organic-5000ml", type1, type2, getNodeText(size))
																																										else:
																																											getProductInfo("https://www.alexmo-cosmetics.de/Mangobutter-kbA-"+getStr(size)+"_1", type1, type2, getNodeText(size))
																																								else:
																																									if "Rizinusoil-cp-organic" in url:
																																										if getStr(size)=="100ml" or getStr(size)=="1000ml" or getStr(size)=="2500ml":
																																											getProductInfo("https://www.alexmo-cosmetics.de/Rizinusoil-cp-organic"+getStr(size), type1, type2, getNodeText(size))
																																										else:
																																											getProductInfo(url.replace("_1", "").replace("_2", "").replace("-20g", "")+"-"+getStr(size), type1, type2, getNodeText(size))
																																									else:
																																										if "Shea-Butter-refined-organic" in url:
																																											getProductInfo("https://www.alexmo-cosmetics.de/Sheabutter-raff-organic-"+getStr(size), type1, type2, getNodeText(size))
																																										else:
																																											if "Softlanae-649vegan-Lanolin-substitute" in url and getStr(size) != "2500ml" and getStr(size) != "5000ml":
																																												getProductInfo("https://www.alexmo-cosmetics.de/Softlanae-649-veganer-Lanolin-Ersatz-"+getStr(size)+"_1", type1, type2, getNodeText(size))
																																											else:
																																												if "Activated-Charcoal-Aktivkohle" in url:
																																													getProductInfo("https://www.alexmo-cosmetics.de/Activated-Charcoal-"+getStr(size)+"-Aktivkohle", type1, type2, getNodeText(size))
																																												else:
																																													if "Magermilchpulver-Lebensmittelqualitaet" in url:
																																														getProductInfo("https://www.alexmo-cosmetics.de/Magermilchpulver-"+getStr(size)+"-Lebensmittelqualitaet", type1, type2, getNodeText(size))
																																													else:
																																														if "Rose-flower-blossoms-ground-red-Rosenbluetenblaetter-rot-gemahlen" in url and (getStr(size) == "20g" or getStr(size) == "50g"):
																																															getProductInfo("https://www.alexmo-cosmetics.de/Rose-flower-blossoms-ground-red-"+getStr(size)+"-Rosenbluetenblaetter-rot-gemahlen", type1, type2, getNodeText(size))
																																														else:
																																															if "Shikakai-Pulver_3" in url:
																																																if getStr(size) == "5000g":
																																																	getProductInfo("https://www.alexmo-cosmetics.de/Shikakai-Pulver_1", type1, type2, getNodeText(size))
																																																else:
																																																	if getStr(size) == "5000g":
																																																		getProductInfo("https://www.alexmo-cosmetics.de/Shikakai-Pulver", type1, type2, getNodeText(size))
																																																	else:
																																																		getProductInfo("https://www.alexmo-cosmetics.de/Shikakai-Pulver-"+getStr(size)+"_1", type1, type2, getNodeText(size))
																																															else:
																																																if "Clay-purple-Tonerde-purple" in url:
																																																	getProductInfo("https://www.alexmo-cosmetics.de/Tonerde-purple-"+getStr(size)+"_1", type1, type2, getNodeText(size))
																																																else:
																																																	getProductInfo(url.replace("_1", "").replace("_2", "").replace("-20g", "")+"-"+getStr(size), type1, type2, getNodeText(size))
		else:
			getProductInfo(url, type1, type2, '')


def getProductList(url, type1, type2):
	sope = httpUtils.getHtmlFromUrl(url)

	ps = sope.find_all("div", attrs={"class":"product-wrapper"})
	for p in ps:
			pLink = p.find("a")
			getProductSize(pLink["href"], type1, type2)
			

headers1=['link', 'Product type1','Product type2','Product Name','INCI','DESCRIPTION','size','price']
headers2=['link', 'Product type1','Product type2','Product Name','INCI','DESCRIPTION','size','price']
headers3=['link', 'Product type1','Product type2','Product Name','INCI','DESCRIPTION','size','price']
headers4=['link', 'Product type1','Product type2','Product Name','INCI','DESCRIPTION','size','price']
headers5=['link', 'Product type1','Product type2','Product Name','INCI','DESCRIPTION','size','price']


# getProductInfo('https://www.alexmo-cosmetics.de/Balance-Blue_1','Pigments', 'White pigments and Fillers','20g')
#Pigments
for pIndex in range(1,3):
	getProductList('https://www.alexmo-cosmetics.de/White-pigments-and-Fillers_s'+str(pIndex),'Pigments', 'White pigments and Fillers')
getProductList('https://www.alexmo-cosmetics.de/Iron-Oxides','Pigments', 'Iron Oxides')
getProductList('https://www.alexmo-cosmetics.de/Pearl-effect-pigments','Pigments', 'Pearl-effect-pigments')
getProductList('https://www.alexmo-cosmetics.de/colored-micas','Pigments', 'colored micas')
getProductList('https://www.alexmo-cosmetics.de/Pure-pigment-mixtures','Pigments', 'Pure pigment mixtures')
#Equipment and bottles
getProductList('https://www.alexmo-cosmetics.de/Aluminium','Equipment and bottles', 'Aluminium')
for pIndex in range(1,3):
	getProductList('https://www.alexmo-cosmetics.de/Glass_s'+str(pIndex),'Equipment and bottles', 'Glass')
for pIndex in range(1,3):
	getProductList('https://www.alexmo-cosmetics.de/Plastics_s'+str(pIndex),'Equipment and bottles', 'Plastics')
for pIndex in range(1,3):
	getProductList('https://www.alexmo-cosmetics.de/Sustainable-packaging_s'+str(pIndex),'Equipment and bottles', 'Sustainable packaging')
for pIndex in range(1,3):
	getProductList('https://www.alexmo-cosmetics.de/Equipment-for-mixing_s'+str(pIndex),'Equipment and bottles', 'Equipment for mixing')
getProductList('https://www.alexmo-cosmetics.de/Starter-Kits','Equipment and bottles', 'Starter Kits')


#Mineral Make-up
getProductList('https://www.alexmo-cosmetics.de/Mineral-Foundation_1','Mineral Make-up', 'Mineral Foundation')
getProductList('https://www.alexmo-cosmetics.de/Rouge_2','Mineral Make-up', 'Rouge')
getProductList('https://www.alexmo-cosmetics.de/Mineral-Corrector_2','Mineral Make-up', 'Mineral Corrector')

#Brushes
getProductList('https://www.alexmo-cosmetics.de/Brushes','Brushes', '')

#Soapmaking
getProductList('https://www.alexmo-cosmetics.de/Soap-Oils-Fats-Waxes','Soapmaking', 'Soap Oils, Fats, Waxes')
for pIndex in range(1,3):
	getProductList('https://www.alexmo-cosmetics.de/Soap-Ingredients_s'+str(pIndex), 'Soapmaking', 'Soap Ingredients')
for pIndex in range(1,3):
	getProductList('https://www.alexmo-cosmetics.de/Soap-Pigments-and-fragrance_s'+str(pIndex), 'Soapmaking', 'Soap Pigments and fragrance')





excelUtils.generateExcelMultipleSheet('alexmo.xlsx', [
	{
		"name":"Pigments",
		"header": headers1 ,
		"data": products1
	},{
		"name":"Equipment and bottles",
		"header": headers2 ,
		"data": products2
	},{
		"name":"Mineral Make-up",
		"header": headers3 ,
		"data": products3
	},{
		"name":"Brushes",
		"header": headers4 ,
		"data": products4
	},{
		"name":"Soapmaking",
		"header": headers5 ,
		"data": products5
	},
])