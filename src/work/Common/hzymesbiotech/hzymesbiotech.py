#coding：utf-8
from itertools import product
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import json
from urllib.parse import quote_plus
sys.path.append('../../..')
from lib import excelUtils
from lib import httpUtils
from lib import textUtil
from lib.htmlEleUtils import getNodeText
from lib.htmlEleUtils import getInnerHtml


products1 = []

headers1=['link','nav', 'Product type1','Product type2','Product Name','cat/Size','img','pdf','Description','Application'
	]
customerHeader=[]
def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, pInfo):
	print(str(len(products1))+"====="+url)
	sope = httpUtils.getRenderdHtmlFromUrl(url)


	pName = sope.find("h1", attrs={"class":"elementor-heading-title elementor-size-default"})
	pInfo["link"] = url
	pInfo["Product Name"] = getNodeText(pName)

	catalogStr = ""
	catalog = sope.find("div", attrs={"class":"elementor-shortcode"})
	if catalog != None:
		tbody = catalog.find("tbody")
		if tbody != None:
			trs = tbody.find_all("tr")
			for tr in trs:
				tds = tr.find_all("td")
				if len(tds) == 3:
					catalogStr += getNodeText(tds[1]) + ":" + getNodeText(tds[2]) + "|||"
	pInfo["cat/Size"] = catalogStr

	sections = sope.find_all("section", attrs={"class":"elementor-section"})
	if len(sections)>1:
		productInfoArea = sections[1]
		img = productInfoArea.find("img")
		if img != None:
			imgName = pInfo["Product Name"].replace("(","-").replace(")","").replace(" ","").replace("#","").replace("（","").replace("）","") +".jpg"
			pattern=re.compile("[\u4e00-\u9fa5]+")
			src = img["src"]
			for match in pattern.findall(src):
				src = src.replace(match, quote_plus(match))
			src=src.replace('（','%EF%BC%88').replace('）','%EF%BC%89')
			httpUtils.urllib_download(src, imgName)
			pInfo["img"] = imgName

 #PDF
	pdfArea = sope.find("div", attrs={"class":"elementor-button-wrapper"})
	if pdfArea!=None:
		pdfLink = pdfArea.find("a")
		if pdfLink !=None:
			pattern=re.compile("[\u4e00-\u9fa5]+")
			src = pdfLink["href"]
			for match in pattern.findall(src):
				src = src.replace(match, quote_plus(match))
			src=src.replace('（','%EF%BC%88').replace('）','%EF%BC%89')
			pdfName = pInfo["Product Name"].replace("(","-").replace(")","").replace(" ","").replace("#","").replace("（","").replace("）","") +".pdf"
			if src != "#":
				httpUtils.urllib_download(src, pdfName)
				pInfo["pdf"] = pdfName
	trs = sope.find_all("tr")
	for tr in trs:
		tds = tr.find_all("td")
		if len(tds) == 2 or len(tds)==3:
			title = getNodeText(tds[0])
			value = getNodeText(tds[1])
			pInfo[title] = value
			addHeader(headers1, title)
	
	tabArea = sope.find("div", attrs={"class":"elementor-tabs-content-wrapper"})
	if tabArea!=None:
		tabTitles = tabArea.find_all("div", attrs={"class":"elementor-tab-title"})
		for tabTitle in tabTitles:
			tabTitleStr = getNodeText(tabTitle)
			if tabTitleStr =="Description":
				pInfo["Description"] = getNodeText(tabTitle.nextSibling.nextSibling)
			if tabTitleStr =="Application":
				pInfo["Application"] = getNodeText(tabTitle.nextSibling.nextSibling)
			if tabTitleStr =="Specification":
				h3 = tabTitle.nextSibling.nextSibling.find_all("h3")
				h2 = tabTitle.nextSibling.nextSibling.find_all("h2")
				for h in h3 + h2:
					title = getNodeText(h)
					value = ""
					for sib in h.next_siblings:
						if sib.name != "p" and sib.name != "ol":
							break
						value += "\r\n"+ getNodeText(sib)
					pInfo[title] = value
					addHeader(headers1, title)

	products1.append(pInfo.copy())



def getProductList(url, type1, type2):
	sope = httpUtils.getHtmlFromUrl(url)
	ps = sope.find_all("div", attrs={"class":"elementor-button-wrapper"})
	for p in ps:
		pLink = p.find("a")
		pInfo = {
			"Product type1": type1
		}
		if pLink.has_attr("href"):
			url = pLink["href"]
			if url != "#":
				getProductInfo(pLink["href"], pInfo)
		
		

getProductList('https://hzymesbiotech.com/molecular-diagnosis/','Molecular diagnosis','')
getProductList('https://hzymesbiotech.com/immunodiagnosis/','Immunodiagnosis','')
getProductList('https://hzymesbiotech.com/biochemical-diagnostics/','Biochemical diagnostics','')
getProductList('https://hzymesbiotech.com/biopharma/','Biopharma','')


# getProductInfo('https://hzymesbiotech.com/dutp%ef%bc%88100mm%ef%bc%89/',{})
# getProductInfo('https://hzymesbiotech.com/proteinase-k-ngs/',{})
# getProductInfo('https://hzymesbiotech.com/proteinase-k-liquid/#',{})




excelUtils.generateExcelMultipleSheet('hzymesbiotech.xlsx', [
	{
		"name": 'hzymesbiotech',
		"header": headers1 + customerHeader,
		"data": products1
	}
])