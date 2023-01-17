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
header=['link','type', 'Product Name','E No:','CAS No..','Application','Description','Available Grade of','Quality Control','Storage','Handling Precaution']

def addHeader(title):
  if title not in header and len(title) > 0:
    header.append(title)

def getProductInfo(url, type):
  print(str(len(products)) + ":" + url)
  sope = httpUtils.getRenderdHtmlFromUrl(url)
  specArea = sope.find("div", attrs={"id":"p_right"})
  pName = specArea.find("h1")
  email = specArea.find("span", attrs={"class":"h1email"})
  pInfo = {}
  pInfo["link"] = url
  pInfo["type"] = type
  pInfo["Product Name"] = getNodeText(pName).replace(getNodeText(email),"")
  info1 = specArea.find("div", attrs={"id":"fpl"})
  info2 = specArea.find("div", attrs={"id":"d1"})
  trs = info1.find_all("tr")
  Application = ""
  Description = ""
  for tr in trs:
    tds = tr.find_all("td")
    if len(tds) == 2:
      title = getNodeText(tds[0])
      value = getNodeText(tds[1])
      pInfo[title] = value
    if len(tds) == 1:
      html = tr.find("div").prettify()
      html = html.replace("<hr/>", "</div><div>")
      htmlSope = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
      divs = htmlSope.find_all("div")
      if len(divs) == 1:
          Application = getNodeText(divs[0])
      if len(divs) > 1:
        pInfo["Description"] = getNodeText(divs[0])
        Application = getNodeText(divs[1])
  if info2 != None:
    trs = info2.find_all("tr")
    for tr in trs:
      tds = tr.find_all("td")
      if len(tds) == 2:
        title = getNodeText(tds[0])
        value = getNodeText(tds[1])
        pInfo[title] = value
        addHeader(title)
  
  h3s = sope.find_all("h3")
  for h3 in h3s:
    title = getNodeText(h3)
    if title.find("Available Grade") > -1:
      pInfo["Available Grade of"] = getNodeText(h3.findNextSibling("li"))
    if title.find("Quality Control") > -1:
      pInfo["Quality Control"] = getNodeText(h3.findNextSibling("p"))
    if title.find("Storage&Handling Precaution") > -1:
      value = getNodeText(h3.findNextSibling("p"))
      vp = value.split("Handling Precaution")
      pInfo["Storage"] = vp[0]
      if len(vp) > 1:
        pInfo["Handling Precaution"] = vp[1]
    if title.find("Application and Uses") > -1:
      Application = Application +"\r\n"+ getNodeText(h3.findNextSibling("p"))
  
  pInfo["Application"] = Application
  print(pInfo)
  products.append(pInfo.copy())


def getProductList(url, type):
  sope = httpUtils.getHtmlFromUrl(url)
  lis = sope.find_all("div", attrs={"id":"p_table"})
  for li in lis:
    pLink = li.find("a")
    if pLink!=None:
      src = pLink["href"]
      getProductInfo(src, type)

for pIndex in range(1, 3):
  getProductList("https://www.foodchemadditives.com/products/food-thickener_"+str(pIndex)+"/", 'Thickeners')

getProductList("https://www.foodchemadditives.com/products/antioxidant/", 'Antioxidants')

for pIndex in range(1, 3):
  getProductList("https://www.foodchemadditives.com/products/preservative_"+str(pIndex)+"/", 'Preservatives')

for pIndex in range(1, 3):
  getProductList("https://www.foodchemadditives.com/products/acidulant_"+str(pIndex)+"/", 'Acidulants')
for pIndex in range(1, 3):
  getProductList("https://www.foodchemadditives.com/products/protein-powder_"+str(pIndex)+"/", 'Proteins')
for pIndex in range(1, 3):
  getProductList("https://www.foodchemadditives.com/products/vitamin-powder_"+str(pIndex)+"/", 'Vitamins')
for pIndex in range(1, 10):
  getProductList("https://www.foodchemadditives.com/products/plant-extract_"+str(pIndex)+"/", 'Plant Extracts')
for pIndex in range(1, 3):
  getProductList("https://www.foodchemadditives.com/products/food-emulsifiers_"+str(pIndex)+"/", 'Emulsifiers')

# getProductInfo("https://www.foodchemadditives.com/products/Hydrolyzed-Animal-Protein-Beef",'ss')

excelUtils.generateExcel('foodchemadditives.xlsx', products, header)