from itertools import product
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


sys.path.append('../..')
from lib import excelUtils
from lib import httpUtils
from lib import textUtil
from lib.htmlEleUtils import getNodeText
from lib.htmlEleUtils import getInnerHtml
products = []
header=['link','type1','type2', 'Product Name1', 'Product Name2','Description','Unit Size']
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("window-size=1024,768")
chrome_options.add_argument("--proxy-server=http://127.0.0.1:33210")

# chrome_options.add_argument("--no-sandbox")
browser = webdriver.Chrome(chrome_options=chrome_options)

def svg_to_png(svgSrc, pngSrc):
  pic = svg2rlg(svgSrc)
  renderPM.drawToFile(pic, pngSrc)

def addHeader(title):
  if title not in header and len(title) > 0:
    header.append(title)

def getProductInfo(url, type1, type2):
  print(str(len(products)) + ":" + url)
  pInfo = {
    "type1": type1,
    "type2": type2
  }
  pInfo["link"] = url
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  pName1 = sope.find("h1", attrs={"class":"brand-h2 product-name"})
  pName2 = pName1.find("span")
  pInfo["Product Name2"] = getNodeText(pName2)
  pInfo["Product Name1"] = getNodeText(pName1).replace(pInfo["Product Name2"], "")
  desc = sope.find("div", attrs={"class":"description-and-detail col-12"})
  sizeArea = sope.find("ul", attrs={"class":"sizecode-swatches sizecode-attribute d-flex pt-sm-1 flex-wrap"})
  if sizeArea !=None:
    sizes = sizeArea.find_all("li")
    sizeStr = ""
    for size in sizes:
      sizeTitle = getNodeText(size.find("div", attrs={"class":"attribute-display attribute-availability product-availability"})).replace("\n","").replace("In Stock","")
      price = getNodeText(size.find("div", attrs={"class":"attribute-price"}))
      sizeStr+="("+sizeTitle+"/"+price+");"
    pInfo["Unit Size"] = sizeStr
  pInfo["Description"] = getNodeText(desc)

  quickAttrs = sope.find("div", attrs={"class":"row product-attributes d-none d-lg-block col-12"})
  if quickAttrs!=None:
    dts = quickAttrs.find_all("dt")
    for dt in dts:
      title = getNodeText(dt.find("h3"))
      if len(title) > 0:
        value = getNodeText(dt.findNextSibling("dd"))
        pInfo[title] = value
        addHeader(title)
  spans = sope.find_all("span", attrs = {"style":"font-weight: bold;"})
  for span in spans:
    title = getNodeText(span)
    if len(title) > 0:
      value = getNodeText(span.findNextSibling("span"))
      pInfo[title] = value
      addHeader(title)
  # print(pInfo)
  products.append(pInfo.copy())


def getProductList(url, type1, type2):
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  trs = sope.find_all("div", attrs={"class":"col-6 col-lg-4 product-click"})
  for tr in trs:
    pLink = tr.find("a")
    if pLink != None:
      linkSrc = pLink["href"]
      getProductInfo(linkSrc, type1, type2)

def getProductType(fileName, type1):
  with open(fileName,'r') as file_to_read:
    content=file_to_read.read()
    types = json.loads(content)
    for type in types:
      # print(type["url"]+type["title"])
      getProductList(type["url"]+"?sz=300", type1, type["title"])

# getProductList('https://www.johnnyseeds.com/flowers/snapdragon/?sz=300', 'type1', 'type2')
# getProductInfo('https://www.johnnyseeds.com/flowers/snapdragon/madame-butterfly-cherry-bronze-f1-snapdragon-seed-4665.html#tabpanel_2-1', 'type1', 'type2')
getProductType('Vegetables.json', 'Vegetables')


excelUtils.generateExcel('johnnyseeds.xlsx', products, header)