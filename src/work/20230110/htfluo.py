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
header=['link','type1','type2','Product Name','CAS #:','imageName']


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
  browser.delete_all_cookies()
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  pInfo = {
    "type1": type1,
    "type2": type2,
    "link": url
  }
  content = sope.find("div", attrs={"id":"content"})
  if content == None:
    browser.delete_all_cookies()
    browser.get(url)
    sope= BeautifulSoup(browser.page_source, "html.parser")
    content = sope.find("div", attrs={"id":"content"})
  pInfo["Product Name"] = getNodeText(content.find("h1"))
  trs = sope.find_all("tr")
  for tr in trs:
    tds = tr.find_all("td")
    if len(tds) == 2:
      title = getNodeText(tds[0])
      value = getNodeText(tds[1])
      if "Data Sheet" not in title:
        addHeader(title)
        pInfo[title] = value

    imageName = ""
  if "Product Name" in pInfo:
    imageName = pInfo["Product Name"]+".png"
  if "CAS #:" in pInfo:
    imageName = pInfo["CAS #:"]+".png"
  pInfo["imageName"] = imageName
  imgArea = sope.find("ul", attrs={"class":"thumbnails"})
  img = imgArea.find("img")
  if img!=None:
    httpUtils.urllib_download(img["src"], imageName)

  products.append(pInfo.copy())


def getProductType(url, type1, type2):
  browser.delete_all_cookies()
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  plinkAreas = sope.find_all("div", attrs={"class":"product-layout product-grid col-lg-4 col-md-4 col-sm-6 col-xs-12"})
  if len(plinkAreas) == 0:
    time.sleep(1)
    browser.delete_all_cookies()
    browser.get(url)
    sope= BeautifulSoup(browser.page_source, "html.parser")
  plinkAreas = sope.find_all("div", attrs={"class":"product-layout product-grid col-lg-4 col-md-4 col-sm-6 col-xs-12"})
  for plinkArea in plinkAreas:
    pLink = plinkArea.find("a")
    getProductInfo(pLink["href"], type1, type2)



# getProductType("https://www.origene.com/search?category=cDNA+Clones&q=CLOCK&page=1",'cDNA Clones')
# getProductInfo("https://www.origene.com/catalog/antibodies/primary-antibodies/ta804783/clock-mouse-monoclonal-antibody-clone-id-oti2h7", "a")

getProductType("https://htfluo.us/index.php?route=product/category&path=79_80",'Intermediates', 'Perfluoro acrylates')
getProductType("https://htfluo.us/index.php?route=product/category&path=79_81",'Intermediates', 'Perfluoro alcohols')
getProductType("https://htfluo.us/index.php?route=product/category&path=79_82",'Intermediates', 'Perfluoro bromides')
getProductType("https://htfluo.us/index.php?route=product/category&path=79_83",'Intermediates', 'Perfluoro epoxides')
getProductType("https://htfluo.us/index.php?route=product/category&path=79_84",'Intermediates', 'Perfluoro iodides')
getProductType("https://htfluo.us/index.php?route=product/category&path=79_85",'Intermediates', 'Perfluoro methacrylates')
getProductType("https://htfluo.us/index.php?route=product/category&path=79_86",'Intermediates', 'Perfluoro olefins')
getProductType("https://htfluo.us/index.php?route=product/category&path=79_87",'Intermediates', 'Perfluoro silanes')
getProductType("https://htfluo.us/index.php?route=product/category&path=79_88",'Intermediates', 'Perfluoro thiols')
getProductType("https://htfluo.us/index.php?route=product/category&path=79_89",'Intermediates', 'Specialty chemicals')
getProductType("https://htfluo.us/index.php?route=product/category&path=90_91",'Polymers', 'PTFE')
getProductType("https://htfluo.us/index.php?route=product/category&path=90_95",'Polymers', 'Water & oil repellent')
getProductType("https://htfluo.us/index.php?route=product/category&path=92_97",'Solvents', 'Hydrofluorocarbon')
getProductType("https://htfluo.us/index.php?route=product/category&path=92_96&limit=100",'Solvents', 'Hydrofluoroether')
getProductType("https://htfluo.us/index.php?route=product/category&path=92_98",'Solvents', 'Perfluorocarbon')
getProductType("https://htfluo.us/index.php?route=product/category&path=93_99",'Surfactants', 'Fluoro surfactants')
getProductType("https://htfluo.us/index.php?route=product/category&path=94_100",'Surface Protectants', 'Water & oil repellents')


excelUtils.generateExcel('htfluo.xlsx', products, header)