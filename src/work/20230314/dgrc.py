from itertools import product
import sys
from bs4 import BeautifulSoup
import bs4
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
notes = []
notesHeader = ['Product Name']
sizeHeader=[]


def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url):
	print(str(len(products1)) + "==" + url)
	sope = httpUtils.getHtmlFromSafeUrl(url)
	nav = sope.find("div", attrs={"id":"page-breadcrumb"})

	pName = sope.find("th", attrs={"class":"cell full"})
	pInfo = {
		"link": url,
		"Product Name": getNodeText(pName),
		"nav": getNodeText(nav)
	}

	fullTables = sope.find_all("table", attrs={"class":"full"})
	if len(fullTables) > 1:
		contentTab = fullTables[1]
		contentTr = contentTab.find("tr")
		contentTds = contentTr.find_all("td")
		bs = contentTds[0].find_all("b")
		strongs = contentTds[0].find_all("strong")
		for b in bs+strongs:
			title = getNodeText(b)
			value = b.nextSibling
			if type(value)==bs4.element.NavigableString and len(value) > 1:
				pInfo[title] = value
				addHeader(headers, title)
			else:
				if b.nextSibling != None:
					value = b.nextSibling.nextSibling
					if type(value)==bs4.element.Tag:
						pInfo[title] = getNodeText(value)
						addHeader(headers, title)
				else:
					value = b.parent.findNextSibling("ul")
					pInfo[title] = getNodeText(value)
					addHeader(headers, title)


	trs = sope.find_all("tr")
	for tr in trs:
		ths = tr.find_all("th")
		tds = tr.find_all("td")
		if len(ths) == 1 and len(tds) == 1:
			title = getNodeText(ths[0])
			value = getNodeText(tds[0])
			pInfo[title] = value
			addHeader(headers, title)

	note = {
		"Product Name": pInfo["Product Name"]
	}
	lis = sope.find_all("li")
	for li in lis:
		liLink = li.find("a")
		if liLink != None:
			title = getNodeText(liLink)
			if "Notes (" in title:
				notesUrl = "https://dgrc.bio.indiana.edu"+liLink["href"]
				notesSope = httpUtils.getHtmlFromSafeUrl(notesUrl)
				lists = notesSope.find_all("div", attrs={"class":"resource-title-list"})

				for list in lists:
					title = getNodeText(list)
					value = list.findNextSibling("div", attrs={"class":"resource-body-list"})
					
					note[title] = getNodeText(value)
					addHeader(notesHeader, title)
	notes.append(note.copy())

	notices = sope.find_all("span", attrs={"class":"alert"})
	sizeStr = ""
	for notice in notices:
		title = getNodeText(notice)
		if title == "Notice:":
			pInfo["Notice"] = getNodeText(notice.parent)
		if title.startswith("$"):
			if len(sizeStr) > 0:
				sizeStr+="+"
			sizeStr += title
	pInfo["price"] = sizeStr

	products1.append(pInfo.copy())

def getProductList(url):
	sope = httpUtils.getHtmlFromSafeUrl(url)
	tableArea = sope.find("table",attrs={"class":"list sortable"})
	ps = tableArea.find("tbody").find_all("tr")

	for p in ps:
		pLink = p.find("a")
		getProductInfo("https://dgrc.bio.indiana.edu" + pLink["href"])
			

headers=['link', 'Product Name','Notice','price']

getProductList("https://dgrc.bio.indiana.edu/cells/Catalog")

# getProductList("https://www.novusbio.com/search?keywords=Drosophila&species=Drosophila&category=Primary%20Antibodies&page="+str(2))
# getProductInfo("https://dgrc.bio.indiana.edu/product/View?product=210")


excelUtils.generateExcelMultipleSheet('dgrc.xlsx', [
	{
		"name":"dgrc",
		"header": headers + sizeHeader,
		"data": products1
	},{
		"name":"notes",
		"header": notesHeader,
		"data": notes
	}
])