from itertools import product
import sys
from bs4 import BeautifulSoup

sys.path.append('../..')
from lib import excelUtils
from lib import httpUtils
from lib import textUtil
from lib.htmlEleUtils import getNodeText
from lib.htmlEleUtils import getInnerHtml
products = []
header=['link','type', 'Product Name','PRODUCT USE','PRODUCT FEATURES','SOURCE','APPLICATION','SUGGESTED USE','SUITABLE FOR','FUNCTION','MANUFACTURING']

def addHeader(title):
  if title not in header and len(title) > 0:
    header.append(title)

def getProductInfo(url, type):
  print(str(len(products)) + ":" + url)
  sope = httpUtils.getRenderdHtmlFromUrl(url)
  pName = sope.find("h1", attrs={"class":"proddetail-style-slider-name this-description-name"})
  pInfo = {}
  pInfo["link"] = url
  pInfo["type"] = type
  pInfo["Product Name"] = getNodeText(pName)
  trs = sope.find_all("tr")
  for tr in trs:
    tds = tr.find_all("td")
    if len(tds) == 1:
      attrStr = getNodeText(tds[0]).split(":")
      if len(attrStr) == 2:
        title = attrStr[0]
        value = attrStr[1]
        addHeader(title)
        pInfo[title] = value
    if len(tds) == 2:
      title = getNodeText(tds[0])
      value =getNodeText(tds[1])
      addHeader(title)
      pInfo[title] = value
  tables = sope.find_all("table")
  for table in tables:
    firstTr = table.find("tr", attrs={"class":"firstRow"})
    if firstTr!=None:
      title = getNodeText(firstTr)
      if title=="PRODUCT USE":
        pInfo["PRODUCT USE"] = getNodeText(table).replace("PRODUCT USE","")
      if title=="PRODUCT FEATURES":
        pInfo["PRODUCT FEATURES"] = getNodeText(table).replace("PRODUCT FEATURES","")
  others = sope.find_all("p")
  for other in others:
    value = getNodeText(other)
    if value.find("SOURCE：") > -1:
      pInfo["SOURCE"] = value.replace("SOURCE：","")
    if value.find("APPLICATION:") > -1:
      ps = other.find_next_siblings("p")
      app = ""
      for p in ps:
        v = getNodeText(p)
        if len(v) == 0:
          break;
        app = app + v + "\r\n"
      pInfo["APPLICATION"] = app

    if value.find("SUGGESTED USE：") > -1:
      pInfo["SUGGESTED USE"] = value.replace("SUGGESTED USE：","")
    if value.find("SUITABLE FOR：") > -1:
      pInfo["SUITABLE FOR"] = value.replace("SUITABLE FOR：","")
    if value.find("FUNCTION：") > -1:
      pInfo["FUNCTION"] = value.replace("FUNCTION：","")
    if value.find("MANUFACTURING：") > -1:
      pInfo["MANUFACTURING"] = value.replace("MANUFACTURING：","")

  products.append(pInfo.copy())


def getProductList(url, type):
  sope = httpUtils.getRenderdHtmlFromUrl(url)
  lis = sope.find_all("li", attrs={"class":"sitewidget-prodlist-noborder"})
  for li in lis:
    pLink = li.find("a")
    if pLink!=None:
      src = pLink["href"]
      getProductInfo("https://www.megafoodsh.com"+src, type)

for pIndex in range(1, 7):
  getProductList("https://www.megafoodsh.com/Food-Coating-Agent-pl3319303-p"+str(pIndex)+".html", 'Food Coating Agent')

for pIndex in range(1, 3):
  getProductList("https://www.megafoodsh.com/Probiotics-Strain-pl3609303-p"+str(pIndex)+".html", 'Probiotics Strain')
# getProductInfo("https://www.megafoodsh.com/Food-Grade-Single-Probiorics-Bifidobacterium-Breve-Powder-pd46527595.html",'ss')

excelUtils.generateExcel('megafoodsh.xlsx', products, header)