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
header=['link','type1','type2', 'Product Name']
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
  pName = sope.find("div", attrs={"class":"gbtitle"}).find("h1")
  pInfo["Product Name"] = getNodeText(pName)


  trs = sope.find_all("tr")
  for tr in trs:
    ths = tr.find_all("th")
    tds = tr.find_all("td")
    if len(tds) == 1 and len(ths)==1:
      title = getNodeText(ths[0])
      value = getNodeText(tds[0])
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
      getProductInfo("http://www.biofeng.com"+type["url"], type1, type2)


# getProductInfo('http://www.biofeng.com/zaiti/zhiwu/pCambia1291Z.html', 'type1', 'type2')
getProductType('广宿主载体.json', '广宿主载体','')
getProductType('植物表达载体.json', '植物表达载体','')


excelUtils.generateExcel('biofeng.xlsx', products, header)