from itertools import product
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
import re

sys.path.append('../..')
from lib import excelUtils
from lib import httpUtils
from lib import textUtil
from lib.htmlEleUtils import getNodeText
from lib.htmlEleUtils import getInnerHtml
products = []
header=['link','type1','type2','type3','Product Name','Cat']


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
    "type1": 'Kinase',
    "type2": type1,
    "type3": type2
  }
  browser.get(url)
  time.sleep(2)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  sizeArea = browser.find_elements_by_class_name('unit_selc')
  if len(sizeArea) > 0:
    sizes=sizeArea[0].find_elements_by_class_name("unit")
    if len(sizes) > 0:
      for sizeInx in range(0, len(sizes)):
        sizeOpt = sizes[sizeInx]
        sizeOpt.click()
        sizeSope= BeautifulSoup(browser.page_source, "html.parser")
        price = sizeSope.find("div", attrs={"class":"price price_now"})
        sizeTitle = "size"+str(sizeInx)
        priceTitle = "price"+str(sizeInx)
        pInfo[sizeTitle] = sizeOpt.text
        pInfo[priceTitle] = getNodeText(price)
        addHeader(sizeTitle)
        addHeader(priceTitle)
  pName = sope.find("div", attrs={"id":"commdity_header"})
  pInfo["Product Name"] = getNodeText(pName)
  cat = sope.find("span", attrs={"class":"catalog"})
  pInfo["Cat"] = getNodeText(cat)
  specs = sope.find_all("div", attrs={"class":"col-md-12 product_details"})
  for spec in specs:
    titles = spec.find_all("div", attrs={"class":"col-md-3"})
    vals = spec.find_all("div", attrs={"class":"col-md-9"})
    if len(titles) == 1 and len(vals) == 1:
      title = getNodeText(titles[0])
      value = getNodeText(vals[0])
      pInfo[title] = value
      addHeader(title)
  moleculeAltNameBody = sope.find("div", attrs={"id":"moleculeAltNameBody"})
  if moleculeAltNameBody!=None:
    pInfo["Synonyms"] = getNodeText(moleculeAltNameBody)
  products.append(pInfo.copy())

def getProductList(url,type1,type2):
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  scripts = sope.find_all("script")
  for script in scripts:
    dataStr = getNodeText(script)
    if dataStr.find("var proteinData")>-1:
      dataStr = dataStr.replace("var proteinData =","").replace(";","")
      reg = re.compile(r'ProductUrl: \'[\w\/\-\s\._]+')
      ps = re.findall(reg, dataStr)
      for data in ps:
        getProductInfo("https://www.sinobiological.com"+ data.replace("ProductUrl: '",""),type1,type2)
  
def getProductType(url, type1):
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  types = sope.find_all("div", attrs={"class":"col_main"})
  for type in types:
    type2Txt = getNodeText(type.find("h3"))
    trs = type.find_all("li")
    for tr in trs: 
      plink = tr.find("a")
      if plink != None:
        getProductList("https://www.sinobiological.com"+plink["href"], type1, type2Txt)



getProductType('https://www.sinobiological.com/research/enzymes/agc-kinase','AGC Kinase molecule')
getProductType('https://www.sinobiological.com/research/enzymes/cam-kinase','CAM Kinase molecule')
getProductType('https://www.sinobiological.com/research/enzymes/casein-kinase','Casein Kinase molecule')
getProductType('https://www.sinobiological.com/research/enzymes/cmgc-kinase','CMGC Kinase molecule')
getProductType('https://www.sinobiological.com/research/enzymes/ste-kinase','STE Kinase molecule')
getProductType('https://www.sinobiological.com/research/enzymes/tyrosine-kinase','Tyrosine Kinase molecule')
getProductType('https://www.sinobiological.com/research/enzymes/tyrosine-kinase-like-group-of-kinases','Tyrosine Kinase like group of kinase molecule')
getProductType('https://www.sinobiological.com/research/enzymes/serine-threonine-kinase','Serine Threonine kinase molecule')
getProductType('https://www.sinobiological.com/research/enzymes/histidine-kinase-hk','Histidine kinase molecule')
getProductType('https://www.sinobiological.com/research/enzymes/lipid-kinase','Lipid Kinase molecule')


# getProductList("https://www.sinobiological.com/category/enpp2",'1','2')
addHeader("Synonyms")
excelUtils.generateExcel('sinobiological.xlsx', products, header)