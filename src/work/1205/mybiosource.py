from itertools import product
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
import random

sys.path.append('../..')
from lib import excelUtils
from lib import httpUtils
from lib import textUtil
from lib.htmlEleUtils import getNodeText
from lib.htmlEleUtils import getInnerHtml
products = []
header=['link','type','nav','Product Name', 'Full Name','cate','Unit / Price']


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

def getProductInfo(url, pInfo):
  print(str(len(products)) + ":" + url)
  browser.delete_all_cookies()
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  navs = sope.find_all("ul", attrs={"class":"uk-breadcrumb uk-margin-remove"})
  if len(navs)==0:
    time.sleep(1)
    browser.delete_all_cookies()
    browser.get(url)
    sope= BeautifulSoup(browser.page_source, "html.parser")
    navs = sope.find_all("ul", attrs={"class":"uk-breadcrumb uk-margin-remove"})
    
  if len(navs)==0:
    time.sleep(1)
    browser.delete_all_cookies()
    browser.get(url)
    sope= BeautifulSoup(browser.page_source, "html.parser")
    navs = sope.find_all("ul", attrs={"class":"uk-breadcrumb uk-margin-remove"})
  
  if len(navs)==0:
    time.sleep(1)
    browser.delete_all_cookies()
    browser.get(url)
    sope= BeautifulSoup(browser.page_source, "html.parser")
    navs = sope.find_all("ul", attrs={"class":"uk-breadcrumb uk-margin-remove"})
  
  if len(navs)==0:
    time.sleep(1)
    browser.delete_all_cookies()
    browser.get(url)
    sope= BeautifulSoup(browser.page_source, "html.parser")
    navs = sope.find_all("ul", attrs={"class":"uk-breadcrumb uk-margin-remove"})
  trs = sope.find_all("tr")
  for tr in trs:
    title = getNodeText(tr.find("td"))
    if title == "Catalog #":
      pInfo["cate"] = getNodeText(tr).replace("Catalog #","")
    if title == "Unit / Price":
      pInfo["Unit / Price"] = getNodeText(tr).replace("Unit / Price","")


  pInfo["nav"] =getNodeText(navs[1]) 
  pInfo["link"] =url 
  pInfo["Full Name"] =getNodeText(sope.find("h1", attrs={"class":"uk-text-bold uk-margin-bottom uk-margin-remove-top uk-display-block uk-heading-line uk-h3"})) 
  specs = sope.find_all("div", attrs={"class":"uk-grid uk-grid-small uk-margin-small-top"})
  for spec in specs:
    titleArea = spec.find("div", attrs={"class":"uk-width-1-5@m uk-text-primary uk-text-middle"})
    titleLink = titleArea.find("a")
    title = getNodeText(titleArea).replace(getNodeText(titleLink), "")
    value = getNodeText(spec.find("div", attrs={"class":"uk-width-expand@m uk-text-bold"}))
    if len(value) == 0:
      value = getNodeText(spec.find("div", attrs={"class":"uk-width-expand@m uk-text-meta"}))
    if len(value) == 0:
      value = getNodeText(spec.find("div", attrs={"class":"uk-width-expand@m uk-text"}))
    addHeader(title)
    pInfo[title] =value

  products.append(pInfo.copy())


def getProductType(url, type1):
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  plinkAreas = sope.find_all("div", attrs={"class":"product-listing"})
  if len(plinkAreas) == 0:
    time.sleep(1)
    browser.delete_all_cookies()
    browser.get(url)
    sope= BeautifulSoup(browser.page_source, "html.parser")
    plinkAreas = sope.find_all("div", attrs={"class":"product-listing"})
  if len(plinkAreas) == 0:
    time.sleep(1)
    browser.delete_all_cookies()
    browser.get(url)
    sope= BeautifulSoup(browser.page_source, "html.parser")
    plinkAreas = sope.find_all("div", attrs={"class":"product-listing"})
  if len(plinkAreas) == 0:
    time.sleep(1)
    browser.delete_all_cookies()
    browser.get(url)
    sope= BeautifulSoup(browser.page_source, "html.parser")
    plinkAreas = sope.find_all("div", attrs={"class":"product-listing"})
  for plinkArea in plinkAreas:
    pNameArea = plinkArea.find("h4")
    pInfo = {
      "Product Name": getNodeText(pNameArea.find("b")) ,
      "type": type1
    }
    baseInfos = plinkArea.find_all("div", attrs={"class":"uk-grid uk-grid-small"})
    for baseInfo in baseInfos:
      title = getNodeText(baseInfo.find("div", attrs={"class":"uk-width-1-6@m"}))
      value = baseInfo.find("div", attrs={"class":"uk-width-expand@m"})
      pInfo[title] = getNodeText(value)
      addHeader(title)
    pLink = plinkArea.find("a")
    getProductInfo("https://www.mybiosource.com"+pLink["href"], pInfo.copy())



for pageIndex in range(1, 4):
  getProductType("https://www.mybiosource.com/search/CLOCK?size=200&page="+str(pageIndex)+"&type=Antibody",'Antibody')
getProductType("https://www.mybiosource.com/search/CLOCK?size=200&page=1&type=Blocking+Peptide",'Blocking Peptide')
getProductType("https://www.mybiosource.com/search/CLOCK?size=200&page=1&type=ELISA+Kit",'ELISA Kit')
getProductType("https://www.mybiosource.com/search/CLOCK?size=200&page=1&type=Recombinant+Protein",'Recombinant Protein')
getProductType("https://www.mybiosource.com/search/CLOCK?size=200&page=1&type=siRNA",'siRNA')



excelUtils.generateExcel('mybiosource.xlsx', products, header)