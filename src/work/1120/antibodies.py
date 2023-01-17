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
header=['link','type1','type2','type3','Product Name','size']


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

def getProductInfo(url, type1, type2, type3):
  print(str(len(products)) + ":" + url)
  pInfo = {
    "link": url,
    "type1": type1,
    "type2": type2,
    "type3": type3
  }
  browser.get(url)
  time.sleep(2)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  dts = sope.find_all("dt")
  for dt in dts:
    title = getNodeText(dt)
    titleAreaLinks = dt.find_all("a")
    for titleAreaLink in titleAreaLinks:
      linkTxt = getNodeText(titleAreaLink)
      title = title.replace(linkTxt, "")
    titleAreaBtns = dt.find_all("a")
    for titleAreaBtn in titleAreaBtns:
      btnTxt = getNodeText(titleAreaBtn)
      title = title.replace(btnTxt, "")
    value = getNodeText(dt.findNextSibling("dd"))
    if len(title) > 0:
      pInfo[title] = value
      addHeader(title)
  pName = sope.find("h1", attrs={"class":"h3"})
  pInfo["Product Name"] = getNodeText(pName)

  size = sope.find("div", attrs={"id":"product-quantity-selector"})
  pInfo["size"] = getNodeText(size)
  products.append(pInfo.copy())


def getProductList(url, type1, type2, type3):
  browser.get(url)
  button = browser.find_element_by_xpath("//button[@class='btn btn-primary']/../button[@name='search-submit']")
  button.click()
  time.sleep(5)
  
  moreButton = browser.find_elements_by_id("more-results-action")
  while(len(moreButton) > 0):
    moreButton[0].click()
    time.sleep(5)
    moreButton = browser.find_elements_by_id("more-results-action")
  sope= BeautifulSoup(browser.page_source, "html.parser")
  ps = sope.find_all("div", attrs={"class":"card col-12 shadow mb-3"})
  for p in ps:
    pLink = p.find("a")
    getProductInfo(pLink["href"],  type1, type2, type3)

def getProductType(url):
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  h2s = sope.find_all("h2", attrs={"class":"text-primary-dark"})
  for h2 in h2s:
    type1Txt = getNodeText(h2)
    type2Area = h2.parent.nextSibling.nextSibling
    type2s = type2Area.find_all("h3")
    for type2 in type2s:
      type2Txt = getNodeText(type2)
      type3Area = type2.nextSibling.nextSibling
      type3s = type3Area.find_all("a")
      for type3 in type3s:
        type3Txt = getNodeText(type3)
        type3Link = type3["href"]
        getProductList(type3Link, type1Txt, type2Txt, type3Txt)



getProductType("https://www.antibodies-online.com/inflammasome-pathway-133/")
# getProductList("https://www.antibodies-online.com/il/il-18-47492/il-18-proteins-33014/",'1','2','3')

excelUtils.generateExcel('antibodies.xlsx', products, header)