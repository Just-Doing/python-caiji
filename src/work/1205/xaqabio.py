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
header=['type','Product Name']


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

def getProductInfo(url, type1):
  print(str(len(products)) + ":" + url)
  pInfo = {
    "link": url,
    "type1": type1,
  }
  
  sope= BeautifulSoup(browser.page_source, "html.parser")
 
  
  products.append(pInfo.copy())


def getProductType(url):
  browser.get(url)
  time.sleep(5)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  type1Area = sope.find("div", attrs={"id":"formTabCntId377"})
  type2Area = sope.find("div", attrs={"id":"formTabCntId378"})
  type3Area = sope.find("div", attrs={"id":"formTabCntId379"})
  type4Area = sope.find("div", attrs={"id":"formTabCntId479"})
  type5Area = sope.find("div", attrs={"id":"formTabCntId466"})

  for p in type1Area.find_all("div", attrs={"class":"J_photoForm photoForm"}):
    pName = getNodeText(p)
    products.append({
      "type": "Hot Sale Products",
      "Product Name": pName
    })

  for p in type2Area.find_all("div", attrs={"class":"J_photoForm photoForm animateModule"}):
    pName = getNodeText(p)
    products.append({
      "type": "New Products",
      "Product Name": pName
    })

  for p in type3Area.find_all("div", attrs={"class":"J_photoForm photoForm animateModule"}):
    pName = getNodeText(p)
    products.append({
      "type": "Plant Extract",
      "Product Name": pName
    })

  for p in type4Area.find_all("div", attrs={"class":"J_photoForm photoForm"}):
    pName = getNodeText(p)
    products.append({
      "type": "Animal Extract",
      "Product Name": pName
    })
    
  for p in type5Area.find_all("div", attrs={"class":"J_photoForm photoForm"}):
    pName = getNodeText(p)
    products.append({
      "type": "APIs",
      "Product Name": pName
    })

getProductType("http://www.xaqabio.com/col.jsp?id=103")


excelUtils.generateExcel('xaqabio.xlsx', products, header)