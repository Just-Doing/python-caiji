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
header=['link','type','Product Name']


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

def getProductInfo(url):
  print(str(len(products)) + ":" + url)
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  pInfo = {
    "link": url,
  }
  nameArea = sope.find("div", attrs={"class":"col-lg-12 col-md-12 col-sm-12 col-xs-12 follow-box-title"})

  pInfo["Product Name"] = getNodeText(nameArea)
  specs = sope.find_all("div", attrs={"class":"prd-des-lis"})
  for spec in specs:
    titleArea = spec.find("div", attrs={"class":"col-lg-4 col-md-4 col-sm-12 col-xs-12 prod-categorty"})
    valArea = spec.find("div", attrs={"class":"col-lg-8 col-md-8 col-sm-12 col-xs-12 clearfix prod-categorty prod-category-back"})
    valArea2 = spec.find("div", attrs={"class":"col-lg-8 col-md-8 col-sm-12 col-xs-12 clearfix prod-categorty prod-category-back synonymWrapper"})
    if titleArea!=None:
      title = getNodeText(titleArea)
      value = getNodeText(valArea)
      if len(value) == 0:
        value = getNodeText(valArea2)
      addHeader(title)

      pInfo[title] = value
  print(pInfo)

  products.append(pInfo.copy())


def getProductType(url):
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  trs = sope.find_all("div", attrs={"class":"single-details"})
  for tr in trs:
    pLink = tr.find("a")
    if pLink != None:
      linkSrc = pLink["href"]
      getProductInfo(linkSrc)


# getProductInfo("https://www.lobachemie.com/Alcohols-0059A/tertBUTANOL-CASNO-75-65-0.aspx", 'Alcohols')
for pIndex in range(1, 7):
  getProductType("https://www.parchem.com/Solvents-chemicals-supplier-distributor~"+str(pIndex)+".aspx")
# getProductType("https://www.parchem.com/Solvents-chemicals-supplier-distributor~1.aspx")

excelUtils.generateExcel('parchem.xlsx', products, header)