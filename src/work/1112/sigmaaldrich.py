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
header=['link','Synonym(s)','product number','desc','Empirical Formula','CAS Number','Molecular Weight','PubChem Substance ID','sku','PackSize','Price','General description',
'Application','Packaging', 'img']


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

def getProductInfo(url, type, desc):
  print(str(len(products)) + ":" + url)
  pInfo = {}
  pInfo["product number"] = type
  pInfo["link"] = url
  pInfo["desc"] = desc
  browser.get(url)
  time.sleep(2)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  divs = sope.find_all("div")
  for div in divs:
    title = getNodeText(div)
    if title == "Synonym(s):" and "Synonym(s)" not in pInfo:
      pInfo["Synonym(s)"] = getNodeText(div.nextSibling)
    if title == "Empirical Formula (Hill Notation):":
      pInfo["Empirical Formula"] = getNodeText(div.nextSibling)
    if title == "CAS Number:" and "CAS Number" not in pInfo:
      pInfo["CAS Number"] = getNodeText(div.nextSibling)
    if title == "Molecular Weight:" and "Molecular Weight" not in pInfo:
      pInfo["Molecular Weight"] = getNodeText(div.nextSibling)
    if title == "PubChem Substance ID:" and "PubChem Substance ID" not in pInfo:
      pInfo["PubChem Substance ID"] = getNodeText(div.nextSibling)
  tbody = sope.find("tbody", attrs={"class":"MuiTableBody-root"})
  if tbody != None:
    tr = tbody.find("tr")
    tds = tr.find_all("td")
    sku = getNodeText(tds[0])
    PackSize = getNodeText(tds[1])
    Price = getNodeText(tds[3])
    pInfo["sku"] = sku
    pInfo["PackSize"] = PackSize
    pInfo["Price"] = Price
  specs = sope.find_all("div", attrs={"class":"MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-3"})
  for spec in specs:
    title = getNodeText(spec)
    if title.find("Storage Class Code")>-1:
      pInfo["Storage Class Code"] = title.replace("Storage Class Code","")
      addHeader("Storage Class Code")
    else:
      if title.find("WGK")>-1:
        pInfo["WGK"] = title.replace("WGK","")
        addHeader("WGK")
      else:
        if title.find("Flash Point(F)")>-1:
          pInfo["Flash Point(F)"] = title.replace("Flash Point(F)","")
          addHeader("Flash Point(F)")
        else:
          if title.find("Flash Point(C)")>-1:
            pInfo["Flash Point(C)"] = title.replace("Flash Point(C)","")
            addHeader("Flash Point(C)")
          else:
            pInfo[title] = getNodeText(spec.nextSibling)
            addHeader(title)
    h3s = sope.find_all("h3")
    for h3 in h3s:
      title = getNodeText(h3)
      if title == "General description":
        pInfo["General description"] = getNodeText(h3.findNextSibling("div"))
      if title == "Application":
        pInfo["Application"] = getNodeText(h3.findNextSibling("div"))
      if title == "Packaging":
        pInfo["Packaging"] = getNodeText(h3.findNextSibling("div"))
  imgArea = sope.find("img", attrs={"id":"active-image"})
  if imgArea !=None:
    httpUtils.urllib_download("https://www.sigmaaldrich.com"+imgArea["src"], str(pInfo["product number"])+".png")
    pInfo["img"] = str(pInfo["product number"])+".png"
  products.append(pInfo.copy())


def getProductList(fileName):
  with open(fileName,'r') as file_to_read:
    content=file_to_read.read()
    datas = json.loads(content)
    for pArea in datas:
      desc = pArea["desc"]
      getProductInfo("https://www.sigmaaldrich.com/US/en/product/aldrich/"+pArea["title"], pArea["title"], desc)


getProductList('sigmaaldrich.txt')


# getProductInfo("https://www.sigmaaldrich.com/US/en/product/aldrich/901332",'ss')

excelUtils.generateExcel('sigmaaldrich.xlsx', products, header)