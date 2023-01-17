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
header=['link','type1','Product Name','Chemical Name']


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
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  spec1s = sope.find_all("div", attrs={"class":"tabrow"})
  spec2s = sope.find_all("div", attrs={"class":"tabrow1"})
  for spec1 in (spec1s + spec2s):
    title = getNodeText(spec1.find("div", attrs={"class":"tabrowleft"}))
    value = getNodeText(spec1.find("div", attrs={"class":"tabrowright"}))
    if len(title) > 0:
      pInfo[title] = value
      addHeader(title)
  headerArea = sope.find("div", attrs={"id":"productheader"})
  pInfo["Product Name"] = getNodeText(headerArea.find("h1"))
  pInfo["Chemical Name"] = getNodeText(headerArea.find("span", attrs={"itemprop":"alternateName"}))
  sizes = sope.find_all("div", attrs={"class":"pricetablerow"})
  for inx, size in enumerate(sizes):
    sizeTxt = getNodeText(size.find("div", attrs={"class":"price-col-5"}))
    price = getNodeText(size.find("div", attrs={"class":"price-col-7"}))
    if len(sizeTxt) and sizeTxt != "BULK":
      pInfo["Unit"+str(inx)] = sizeTxt
      pInfo["Price"+str(inx)] = price
      addHeader("Unit"+str(inx))
      addHeader("Price"+str(inx))
  descriptionArea = sope.find("h2", attrs={"itemprop":"description"})
  descriptions = descriptionArea.find_all("span")
  for description in descriptions:
    valuestr = getNodeText(description)
    if valuestr.find("MF:") > -1:
      pInfo["MF"] = valuestr.replace("MF:", "")
    if valuestr.find("MW:") > -1:
      pInfo["MW"] = valuestr.replace("MW:", "")
  bs = sope.find_all("b")
  for b in bs:
    bStr = getNodeText(b)
    if bStr.find("Purity:")> -1:
      pInfo["Purity"] = getNodeText(b.nextSibling)
  
  structureimg = sope.find("img", attrs={"id":"structureimg"})
  if structureimg != None and 'CAS RN' in pInfo:
    pInfo["img"] = pInfo["CAS RN"]+".png"
    httpUtils.urllib_download(structureimg["src"], pInfo["img"])
  products.append(pInfo.copy())


def getProductType(url, type1):
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  plinkAreas = sope.find_all("td", attrs={"class":"borderbtmname"})
  for plinkArea in plinkAreas:
    plink = plinkArea.find("a")
    if plink != None:
      getProductInfo("https://www.glentham.com"+plink["href"], type1)



getProductType("https://www.glentham.com/en/products/categories/chitin-chitosan/view-50-all/", 'Chitin & Chitosan')
getProductType("https://www.glentham.com/en/products/categories/fungal-origin-chitin-chitosan/view-50-all/",'Fungal Origin Chitin & Chitosan')
for pageIndex in range(1, 3):
  getProductType("https://www.glentham.com/en/products/categories/polysaccharides/view-100-all/?page="+str(pageIndex),'Polysaccharides')
for pageIndex in range(1, 3):
  getProductType("https://www.glentham.com/en/products/categories/steroids/view-100-all/?page="+str(pageIndex),'Steroids')



excelUtils.generateExcel('glentham.xlsx', products, header)