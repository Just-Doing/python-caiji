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
header=['link','Category','nav','Product Name','Cat#', 'Full Name', 'Conjugation', 'Size']


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
  browser.delete_all_cookies()
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  pInfo = {
    "Category": type
  }
  navs = sope.find_all("ul", attrs={"class":"breadcrumb"})
  if len(navs)==0:
    time.sleep(1)
    browser.delete_all_cookies()
    browser.get(url)
    sope= BeautifulSoup(browser.page_source, "html.parser")
    navs = sope.find_all("ul", attrs={"class":"breadcrumb"})
    
  pInfo["nav"] =getNodeText(navs[0]) 
  pInfo["link"] =url 
  pInfo["Product Name"] =getNodeText(sope.find("h1", attrs={"class":"name"})) 
  pInfo["Full Name"] =getNodeText(sope.find("p", attrs={"class":"long-description mt-3"})) 
  pInfo["Cat#"] =getNodeText(sope.find("h2", attrs={"class":"sku mt-0"})) .replace("CAT#:","")
  
  size=""
  baseInfos = sope.find_all("p", attrs={"class":"smaller text-muted mb-1"})
  for baseInfo in baseInfos:
    title = getNodeText(baseInfo.find("span", attrs={"class":"align-bottom"}))
    if title=="Size:":
       size = getNodeText(baseInfo).replace(title, "")
    if title=="Formulation:":
       pInfo["Formulation"] = getNodeText(baseInfo).replace(title, "")
    if title=="Conjugation:":
       pInfo["Conjugation"] = getNodeText(baseInfo).replace(title, "")

  if len(size) == 0:
    sizeArea = sope.find("div", attrs={"class":"row text-center text-md-left mb-2"})
    if sizeArea!=None:
      sizeUl = sizeArea.find("ul", attrs={"class":"cf"})
      if sizeUl != None:
        sizeSpan = sizeUl.find("span")
        size =getNodeText(sizeSpan)

  pInfo["Size"] = size
  specs = sope.find_all("tr", attrs={"class":"attribute"})
  for spec in specs:
    tds = spec.find_all("td")
    if len(tds) == 2:
      title = getNodeText(tds[0])
      value = getNodeText(tds[1])
      addHeader(title)
      pInfo[title] =value
  print(pInfo)
  products.append(pInfo.copy())


def getProductType(url, type1):
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  plinkAreas = sope.find_all("article")
  if len(plinkAreas) == 0:
    time.sleep(1)
    browser.delete_all_cookies()
    browser.get(url)
    sope= BeautifulSoup(browser.page_source, "html.parser")
    plinkAreas = sope.find_all("article")
  for plinkArea in plinkAreas:
    pLink = plinkArea.find("a")
    getProductInfo("https://www.origene.com"+pLink["href"], type1)



# getProductType("https://www.origene.com/search?category=cDNA+Clones&q=CLOCK&page=1",'cDNA Clones')
# getProductInfo("https://www.origene.com/catalog/antibodies/primary-antibodies/ta804783/clock-mouse-monoclonal-antibody-clone-id-oti2h7", "a")
for pageIndex in range(1, 6):
  getProductType("https://www.origene.com/search?category=cDNA+Clones&q=CLOCK&page="+str(pageIndex),'cDNA Clones')
for pageIndex in range(1, 6):
  getProductType("https://www.origene.com/search?category=Antibodies&q=CLOCK&page="+str(pageIndex),'Antibodies')
for pageIndex in range(1, 3):
  getProductType("https://www.origene.com/search?category=Proteins&q=CLOCK&page="+str(pageIndex),'Proteins')
for pageIndex in range(1, 5):
  getProductType("https://www.origene.com/search?category=RNAi&q=CLOCK&page="+str(pageIndex),'RNAi')
for pageIndex in range(1, 3):
  getProductType("https://www.origene.com/search?category=Gene+Expression&q=CLOCK&page="+str(pageIndex),'Gene Expression')



excelUtils.generateExcel('origene.xlsx', products, header)