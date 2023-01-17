from itertools import product
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json

sys.path.append('../..')
from lib import excelUtils
from lib import httpUtils
from lib import textUtil
from lib.htmlEleUtils import getNodeText
from lib.htmlEleUtils import getInnerHtml
products = []
header=['link','type', 'Product Name','Quantity','Application','Description Img','size0','price0','size1','price1','size2','price2','size3','price3','size4','price4','size5','price5','size6','price6','size7','price7']


def addHeader(title):
  if title not in header and len(title) > 0:
    header.append(title)

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("window-size=1024,768")
chrome_options.add_argument("--proxy-server=http://127.0.0.1:33210")

# chrome_options.add_argument("--no-sandbox")
browser = webdriver.Chrome(chrome_options=chrome_options)

def getProductInfo(url, type):
  print(str(len(products)) + ":" + url)
  pInfo = {}
  browser.get(url)
  time.sleep(2)
  sope= BeautifulSoup(browser.page_source, "html.parser")

  nav = sope.find("div", attrs={"id":"breadcrumb_navi"})
  pName = sope.find("h1", attrs={"class":"product-info-title-desktop"})
  pInfo["link"] = url
  pInfo["type"] = type
  pInfo["Nav"] = getNodeText(nav)
  pInfo["Product Name"] = getNodeText(pName)
  specs = sope.find_all("dt", attrs={"class":"col-xs-4"})
  quantity = sope.find("select", attrs={"name":"modifiers[attribute][2]"})
  pInfo["Quantity"] = getNodeText(quantity)
  for spec in specs:
    title = getNodeText(spec)
    value = getNodeText(spec.findNextSibling("dd"))
    pInfo[title] = value
    addHeader(title)
  sizeArea = browser.find_elements_by_name('modifiers[attribute][1]')
  if len(sizeArea) > 0:
    sizes = sizeArea[0].find_elements_by_tag_name("option")
    for sizeInx in range(0, len(sizes)):
        sizeOpt = sizes[sizeInx]
        sizeOpt.click()
        sizeSope= BeautifulSoup(browser.page_source, "html.parser")
        priceArea = sizeSope.find("div", attrs={"id":"attributes-calc-price"})
        price = priceArea.find("div", attrs={"class":"current-price-container"})
        sizeTitle = "size"+str(sizeInx)
        priceTitle = "price"+str(sizeInx)
        pInfo[sizeTitle] = sizeOpt.text
        pInfo[priceTitle] = getNodeText(price)
        addHeader(sizeTitle)
        addHeader(priceTitle)
  else:
    priceArea = sope.find("div", attrs={"id":"attributes-calc-price"})
    pInfo["size0"] = getNodeText(priceArea.find("div", attrs={"class":"current-price-container"}))
  trs = sope.find_all("tr")
  for tr in trs:
    tds = tr.find_all("td")
    if len(tds) == 2:
      title =getNodeText(tds[0])
      value =getNodeText(tds[1])
      pInfo[title] = value
      addHeader(title)
  if type == "Antibodies/Cytoskeleton":
    imgArea = sope.find("div", attrs={"class":"tab-body active"})
    img = imgArea.find("img")
    if img != None:
      imgName = str(len(products))+".png"
      imgSrc = img["src"]
      if imgSrc.find("images/") == 0:
        httpUtils.urllib_download("https://www.hypermol.com/"+img["src"], imgName)
        pInfo["Description Img"] = imgName
  appSope = None
  appValue = ""
  ps = sope.find_all("p")
  for p in ps:
    title = getNodeText(p)
    if title.find("Applications") == 0:
      appSope = p
      nextP = p.nextSibling
      if nextP==None:
        nextP = p.parent.nextSibling
      nextValue = getNodeText(nextP)
      if nextValue.find("Description") == -1:
        appValue = title.replace("Applications","") + nextValue
        nextP = nextP.nextSibling
        if nextP==None:
          nextP = p.parent.nextSibling
        nextValue2 = getNodeText(nextP)
        if nextValue2.find("Description") == -1:
          appValue = appValue + nextValue2
          nextP = nextP.nextSibling
          if nextP==None:
            nextP = p.parent.nextSibling
          nextValue3 = getNodeText(nextP)
          if nextValue3.find("Description") == -1:
            appValue = appValue + nextValue3
            nextP = nextP.nextSibling
            if nextP==None:
              nextP = p.parent.nextSibling
            nextValue4 = getNodeText(nextP)
            if nextValue4.find("Description") == -1:
              appValue = appValue + nextValue4
              nextP = nextP.nextSibling
              nextValue5 = getNodeText(nextP)
              if nextValue5.find("Description") == -1:
                appValue = appValue + nextValue5
                nextP = nextP.nextSibling
                nextValue6 = getNodeText(nextP)
                if nextValue6.find("Description") == -1:
                  appValue = appValue + nextValue6
                  nextP = nextP.nextSibling
                  nextValue7 = getNodeText(nextP)
                  if nextValue7.find("Description") == -1:
                    appValue = appValue + nextValue7
                    nextP = nextP.nextSibling
                    nextValue8 = getNodeText(nextP)
                    if nextValue8.find("Description") == -1:
                      appValue = appValue + nextValue8
      break;
  if  appSope == None:
    divs = sope.find_all("div")
    for span in divs:
      title = getNodeText(span)
      if title.find("Applications") == 0:
        appSope = span
        nextP = span.nextSibling
        if nextP==None:
          nextP = span.parent.nextSibling
        nextValue = getNodeText(nextP)
        if nextValue.find("Description") == -1:
          appValue = title.replace("Applications","") + nextValue
          nextP = nextP.nextSibling
          if nextP==None:
            nextP = span.parent.nextSibling
          nextValue2 = getNodeText(nextP)
          if nextValue2.find("Description") == -1:
            appValue = appValue + nextValue2
            nextP = nextP.nextSibling
            if nextP==None:
              nextP = span.parent.parent.nextSibling
            nextValue3 = getNodeText(nextP)
            if nextValue3.find("Description") == -1:
              appValue = appValue + nextValue3
  if appSope == None:
    spans = sope.find_all("span")
    for span in spans:
      title = getNodeText(span)
      if title.find("Applications") == 0:
        nextP = span.nextSibling
        if nextP==None:
          nextP = span.parent.nextSibling
        nextValue = getNodeText(nextP)
        if nextValue.find("Description") == -1:
          appValue = title.replace("Applications","") + nextValue
          nextP = nextP.nextSibling
          if nextP==None:
            nextP = span.parent.nextSibling
          nextValue2 = getNodeText(nextP)
          if nextValue2.find("Description") == -1:
            appValue = appValue + nextValue2
            nextP = nextP.nextSibling
            if nextP==None:
              nextP = span.parent.parent.nextSibling
            nextValue3 = getNodeText(nextP)
            if nextValue3.find("Description") == -1:
              appValue = appValue + nextValue3
              nextP = nextP.nextSibling
              nextValue4 = getNodeText(nextP)
              if nextValue4.find("Description") == -1:
                appValue = appValue + nextValue4
                nextP = nextP.nextSibling
                if nextP==None:
                  nextP = span.parent.parent.parent.nextSibling
                nextValue5 = getNodeText(nextP)
                if nextValue5.find("Description") == -1:
                  appValue = appValue + nextValue5
        break;

  pInfo["Application"] = appValue
  products.append(pInfo.copy())


def getProductList(url, type):
  sope = httpUtils.getHtmlFromUrl(url)
  links = sope.find_all("a", attrs={"class":"product-url"})
  for link in links:
    src = link["href"]
    getProductInfo(src, type)

# for pIndex in range(1, 3):
#   getProductList("https://www.hypermol.com/actin-toolkit/?page="+str(pIndex), 'Actin-toolkit/Cytoskeleton')


# getProductList("https://www.hypermol.com/Actin-Trialkits/", 'Actin-Trialkits /Cytoskeleton')

# for pIndex in range(1, 8):
#   getProductList("https://www.hypermol.com/actin-and-abps/?page="+str(pIndex), 'Actin-Proteins /Cytoskeleton')

for pIndex in range(1, 3):
  getProductList("https://www.hypermol.com/cytoskeleton-buffer/?page="+str(pIndex), 'Actin-buffer /Cytoskeleton')
for pIndex in range(1, 3):
  getProductList("https://www.hypermol.com/staining-kit/?page="+str(pIndex), 'Staining Kits & Additives/Cytoskeleton')
for pIndex in range(1, 3):
  getProductList("https://www.hypermol.com/analytical-reagents/?page="+str(pIndex), 'Analytical Reagents/Cytoskeleton')
for pIndex in range(1, 5):
  getProductList("https://www.hypermol.com/antibodies/?page="+str(pIndex), 'Antibodies/Cytoskeleton')


# getProductList("https://www.hypermol.com/Actin-Trialkits/", 'Actin-Trialkits /Cytoskeleton')
# getProductInfo("https://www.hypermol.com/rhodamine-actin-alpha-actin-skeletal-muscle.html",'Antibodies/Cytoskeleton')

excelUtils.generateExcel('hypermol2.xlsx', products, header)