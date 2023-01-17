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
header=['link','type1','type2','Product Name']


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

def getProductInfo(url, type1, type2):
  print(str(len(products)) + ":" + url)
  pInfo = {
    "link": url,
    "type1": type1,
    "type2": type2
  }
  browser.get(url)
  time.sleep(2)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  tbArea = sope.find("table", attrs={"class":"table pdts-detail-table border-bottom"})
  firstTr = tbArea.find("tr")
  trs = firstTr.find_next_siblings("tr")
  trs.append(firstTr)
  for tr in trs:
    firstTd = tr.find("td")
    if firstTd!=None:
      siblingTds = firstTd.find_next_siblings("td")
      if len(siblingTds) == 1:
        title = getNodeText(firstTd)
        pInfo[title] = getNodeText(siblingTds[0])
        addHeader(title)
  size1 = sope.find("select", attrs={"id":"dvSpecific_CSB-YP"})
  if size1 ==None:
    size1=sope.find("select", attrs={"id":"dvSpecific-YP"})
  if size1 ==None:
    size1=sope.find("select", attrs={"id":"dvSpecific"})
  if size1 != None:
    options = size1.find_all("option")
    for inx, option in enumerate(options):
      sizeTitle = 'size'+str(inx)
      pInfo[sizeTitle] = getNodeText(option)
      addHeader(sizeTitle)
  else:
    size = sope.find("td", attrs={"id":"newwell_product_spef"})
    if size != None:
      pInfo["size1"] = getNodeText(size)
      addHeader("size1")
  pName = getNodeText(sope.find("h1", attrs={"class":"margin-small-right"}))
  pInfo["Product Name"] = pName
  products.append(pInfo.copy())


def getProductType(url, type1):
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  types = sope.find_all("div", attrs={"class":"table-responsive margin-large-top"})
  for type in types:
    type2Txt = getNodeText(type.find("h2"))
    trs = type.find_all("tr")
    for tr in trs: 
      plink = tr.find("a")
      if plink != None:
        getProductInfo(plink["href"], type1, type2Txt)



getProductType("https://www.cusabio.com/target/AIM2.html", 'AIM2')
getProductType("https://www.cusabio.com/target/IL18.html",'IL18')
getProductType("https://www.cusabio.com/target/IL1B.html",'IL1B')
getProductType("https://www.cusabio.com/target/NLRC4.html",'NLRC4')
getProductType("https://www.cusabio.com/target/NLRP1.html",'NLRP1')
getProductType("https://www.cusabio.com/target/NLRP3.html",'NLRP3')


# getProductList("https://www.antibodies-online.com/il/il-18-47492/il-18-proteins-33014/",'1','2','3')

excelUtils.generateExcel('cusabio.xlsx', products, header)