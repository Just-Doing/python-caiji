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
header=['link','type1','type2', 'Product Name','Description','Unit Size']
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
  pName = sope.find("h1", attrs={"id":"product_title"})

  timeToWaite = 1
  while(pName == None):
    browser.get(url)
    time.sleep(timeToWaite)
    timeToWaite += 1
    sope= BeautifulSoup(browser.page_source, "html.parser")
    pName = sope.find("h1", attrs={"id":"product_title"})
  timeToWaite = 1


  pInfo["Product Name"] = getNodeText(pName)

  sizeArea = sope.find("div", attrs={"class":"info-wrap_WRAPPER"})
  if sizeArea!=None:
    pInfo["Unit Size"] = getNodeText(sizeArea.find("div", attrs={"class":"name"}))
  desc = sope.find("div", attrs={"id":"this_long_description"})
  pInfo["Description"] = getNodeText(desc)
  

  trs = sope.find_all("tr")
  for tr in trs:
    tds = tr.find_all("td")
    if len(tds) == 2:
      title = getNodeText(tds[0])
      value = getNodeText(tds[1])
      if len(title) >0:
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

def getProductType(fileName, type1, type2):
  with open(fileName,'r') as file_to_read:
    content=file_to_read.read()
    types = json.loads(content)
    for type in types:
      getProductInfo(type["url"], type1, type2)


# getProductInfo('https://parkseed.com/eucalyptus-baby-blue/p/52301-PK-P1/', 'type1', 'type2')
getProductType('Vegetables.json', 'Vegetables','')
getProductType('Fruits.json', 'Fruits','')
getProductType('Flowers.json', 'Flowers','')
getProductType('Herbs.json', 'Herbs','')
getProductType('OrganicHeirloom.json', 'Organic + Heirloom','')

getProductType('Plants1.json', 'Plants','Perennials')
getProductType('Plants2.json', 'Plants','Flower Bulbs')
getProductType('Plants3.json', 'Plants','Shrubs')
getProductType('Plants4.json', 'Plants','Trees')


excelUtils.generateExcel('parkseed.xlsx', products, header)