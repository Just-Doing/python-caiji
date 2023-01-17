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
header=['link','type','Product Name','imageName']


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
  browser.delete_all_cookies()
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  pInfo = {
    "type": type1,
    "link": url,
  }
  nameArea = sope.find("span", attrs={"id":"ContentPlaceHolder1_lblprodname"})
  timeToWaite = 1
  while(nameArea == None):
    browser.delete_all_cookies()
    browser.get(url)
    time.sleep(timeToWaite)
    timeToWaite += 1
    sope= BeautifulSoup(browser.page_source, "html.parser")
    nameArea = sope.find("span", attrs={"id":"ContentPlaceHolder1_lblprodname"})
  timeToWaite = 1

  pInfo["Product Name"] = getNodeText(nameArea)
  specs = sope.find_all("div", attrs={"class":"chem-table-col1"})
  for spec in specs:
    title = getNodeText(spec)
    value = getNodeText(spec.findNextSibling("div", attrs={"class":"chem-table-col2"}))
    addHeader(title)
    pInfo[title] = value

  trs = sope.find_all("tr")
  for tr in trs:
    tds = tr.find_all("td")
    if len(tds) == 2 :
      title = getNodeText(tds[0])
      value = getNodeText(tds[1])
      addHeader(title)
      pInfo[title] = value

  safeProp = sope.find("div", attrs={"id":"ContentPlaceHolder1_divsafety"})
  if safeProp!=None:
    spans = safeProp.find_all("span")
    for span in spans:
      valueStr = getNodeText(span)
      valuePart = valueStr.split(":")
      if len(valuePart) == 2:
        addHeader(valuePart[0])
        pInfo[valuePart[0]] = valuePart[1]

  imageName = ""
  if "Product Name" in pInfo:
    imageName = pInfo["Product Name"]+".png"
  if "CAS No." in pInfo:
    imageName = pInfo["CAS No."]+".png"
  imgArea = sope.find("span", attrs={"id":"ContentPlaceHolder1_rptmolst_lbl_msds_0"})
  if imgArea!=None:
    img = imgArea.find("img")
    if img!=None:
      imgSrc = img["src"].replace("../","https://www.lobachemie.com/")
      httpUtils.urllib_download(imgSrc, imageName)
      pInfo["imageName"] = imageName

  products.append(pInfo.copy())


def getProductType(url, type1):
  browser.delete_all_cookies()
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  tableArea = sope.find("table", attrs={"id":"ContentPlaceHolder1_grdcat"})
  trs = tableArea.find("tbody").find_all("tr")
  for tr in trs:
    pLink = tr.find("a")
    if pLink != None:
      linkSrc = pLink["href"].replace("../", "https://www.lobachemie.com/")
      getProductInfo(linkSrc, type1)


# getProductInfo("https://www.lobachemie.com/Alcohols-0059A/tertBUTANOL-CASNO-75-65-0.aspx", 'Alcohols')
#2
getProductType("https://www.lobachemie.com/laboratory-chemicals/Alcohols.aspx",'Alcohols')
getProductInfo("https://www.lobachemie.com/Alcohols-0059A/tertBUTANOL-CASNO-75-65-0.aspx", 'Alcohols')
getProductInfo("https://www.lobachemie.com/Alcohols-00059/tertBUTANOL-CASNO-75-65-0.aspx", 'Alcohols')
getProductInfo("https://www.lobachemie.com/Alcohols-00347/TRIETHYLENE-GLYCOL-CASNO-112-27-6.aspx", 'Alcohols')
#1
getProductType("https://www.lobachemie.com/laboratory-chemicals/alkyl-halides.aspx",'Alkyl Halides')
getProductType("https://www.lobachemie.com/laboratory-chemicals/allyl-halides.aspx",'Allyl Halides')
getProductType("https://www.lobachemie.com/laboratory-chemicals/aryl-halides.aspx",'Aryl Halides')
getProductType("https://www.lobachemie.com/laboratory-chemicals/dry-solvents.aspx",'Dry Solvents')
getProductType("https://www.lobachemie.com/laboratory-chemicals/esters.aspx",'Esters')
getProductType("https://www.lobachemie.com/laboratory-chemicals/Gas-Chromatography-GC-Solvents.aspx",'Gas Chromatoghaphy Solvents (GC Solvents)')
getProductType("https://www.lobachemie.com/laboratory-chemicals/gc-hs-solvents-for-gc-headspace-analysis.aspx",'GC-HS Solvents')
getProductType("https://www.lobachemie.com/laboratory-chemicals/High-Purity-Solvents.aspx",'High Purity Solvents')
getProductType("https://www.lobachemie.com/laboratory-chemicals/HPLC-Grade-Solvents.aspx",'HPLC, Spectroscopy Grade Solvents')
getProductType("https://www.lobachemie.com/laboratory-chemicals/ketones.aspx",'Ketones')
getProductType("https://www.lobachemie.com/laboratory-chemicals/lcms--solvents.aspx",'LC-MS Solvents')
getProductType("https://www.lobachemie.com/laboratory-chemicals/pesticide-residue-solvents.aspx",'Pesticide Residue Solvents (for Trace Analysis)')



excelUtils.generateExcel('lobachemie.xlsx', products, header)