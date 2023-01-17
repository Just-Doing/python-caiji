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
header=['link','type1','type2','type3','Product Name','CAS','分子式','分子量','纯度','price','imageName']


def addHeader(title):
  if title not in header and len(title) > 0:
    header.append(title)

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("window-size=1024,768")

# chrome_options.add_argument("--no-sandbox")
browser = webdriver.Chrome(chrome_options=chrome_options)

def getProductInfo(url, type1, type2, type3, data):
  print(str(len(products)) + ":" + url)
  browser.delete_all_cookies()
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  pInfo = {
    "type1": type1,
    "type2": type2,
    "type3": type3,
    "link": url,
    "CAS": data["CAS"],
    "分子式": data["molecularFomula"] if "molecularFomula" in data else "",
    "纯度": data["purity"] if "purity" in data else "",
    "分子量": data["molecularWeight"] if "molecularWeight" in data else ""
  }
  content = sope.find("div", attrs={"class":"details"})
  timeToWaite = 1
  while(content == None):
    browser.delete_all_cookies()
    browser.get(url)
    time.sleep(timeToWaite)
    timeToWaite += 1
    sope= BeautifulSoup(browser.page_source, "html.parser")
    content = sope.find("div", attrs={"class":"details"})
  timeToWaite = 1
  pInfo["Product Name"] = getNodeText(content.find("strong"))
  sizeAreas = sope.find_all("div", attrs={"class":"row mx-0 w-100"})
  sizePriceStr = "("
  for sizeArea in sizeAreas:
    sizeTxtArea = sizeArea.find("div", attrs={"class":"col-5 d-flex flex-column mb-2 pb-1 pl-0"})
    sizeTxt = getNodeText(sizeTxtArea.find("b"))
    priceTxtArea =sizeArea.find("div", attrs={"class":"col-7 mb-0 pr-0"})
    priceTxt = getNodeText( priceTxtArea.find("span", attrs={"class":"text-danger"}))
    sizePriceStr += (sizeTxt+"/"+priceTxt)
  sizePriceStr +=")"
  pInfo["price"] = sizePriceStr
  trs = sope.find_all("tr")
  for tr in trs:
    ths = tr.find_all("th")
    tds = tr.find_all("td")
    if len(tds) == 1 and len(ths) == 1:
      title = getNodeText(ths[0])
      value = getNodeText(tds[0])
      addHeader(title)
      pInfo[title] = value

  imageName = ""
  if "Product Name" in pInfo:
    imageName = pInfo["Product Name"]+".png"
  if "CAS" in pInfo:
    imageName = pInfo["CAS"]+".png"
  imgArea = sope.find("div", attrs={"class":"col-lg-4"})
  img = imgArea.find("img")
  if img!=None:
    httpUtils.urllib_download(img["src"], imageName)
    pInfo["imageName"] = imageName

  products.append(pInfo.copy())


def getProductType(url, type1, type2, type3):
  browser.delete_all_cookies()
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  dataStr = getNodeText(sope.find("body"))
  datas = json.loads(dataStr)
  for data in datas['hits']:
    pId = data["id"]
    getProductInfo("https://www.jkchemical.com/product/"+str(pId), type1, type2, type3, data)


# getProductInfo("https://www.jkchemical.com/product/70739", '','','',{"CAS":"123","molecularFomula":"","purity":"","molecularWeight":""})
# getProductType("https://web.jkchemical.com/api/product-catalog/150/products/1",'合成溶剂', '合成用离子液体','吡咯类离子液体')
for pIndex in range(1, 8):
  getProductType("https://web.jkchemical.com/api/product-catalog/152/products/"+str(pIndex),'合成溶剂', '无水溶剂','')
for pIndex in range(1, 7):
  getProductType("https://web.jkchemical.com/api/product-catalog/154/products/"+str(pIndex),'合成溶剂', '超干溶剂','')

getProductType("https://web.jkchemical.com/api/product-catalog/150/products/1",'合成溶剂', '合成用离子液体','吡咯类离子液体')
getProductType("https://web.jkchemical.com/api/product-catalog/151/products/1",'合成溶剂', '合成用离子液体','吡啶类离子液体')
getProductType("https://web.jkchemical.com/api/product-catalog/153/products/1",'合成溶剂', '合成用离子液体','其他类离子液体')

for pIndex in range(1, 3):
  getProductType("https://web.jkchemical.com/api/product-catalog/185/products/"+str(pIndex),'合成溶剂', '合成用离子液体','季铵盐类离子液体')
for pIndex in range(1, 6):
  getProductType("https://web.jkchemical.com/api/product-catalog/187/products/"+str(pIndex),'合成溶剂', '合成用离子液体','咪唑类离子液体')
getProductType("https://web.jkchemical.com/api/product-catalog/188/products/1",'合成溶剂', '合成用离子液体','季膦盐类离子液体')
for pIndex in range(1, 5):
  getProductType("https://web.jkchemical.com/api/product-catalog/189/products/"+str(pIndex),'合成溶剂', '通用合成溶剂','')

for pIndex in range(1, 4):
  getProductType("https://web.jkchemical.com/api/product-catalog/472/products/"+str(pIndex),'溶剂', '核磁溶剂','')

getProductType("https://web.jkchemical.com/api/product-catalog/473/products/1",'溶剂', '残留分析溶剂','')

for pIndex in range(1, 3):
  getProductType("https://web.jkchemical.com/api/product-catalog/474/products/"+str(pIndex),'溶剂', 'ACS级溶剂','')

getProductType("https://web.jkchemical.com/api/product-catalog/475/products/1",'溶剂', '液相色谱-质谱溶剂','')
getProductType("https://web.jkchemical.com/api/product-catalog/476/products/1",'溶剂', '气相顶空溶剂','')
getProductType("https://web.jkchemical.com/api/product-catalog/477/products/1",'溶剂', '生物级溶剂','')
for pIndex in range(1, 3):
  getProductType("https://web.jkchemical.com/api/product-catalog/480/products/"+str(pIndex),'溶剂', '光谱溶剂','')
for pIndex in range(1, 4):
  getProductType("https://web.jkchemical.com/api/product-catalog/484/products/"+str(pIndex),'溶剂', '液相色谱溶剂','')

getProductType("https://web.jkchemical.com/api/product-catalog/486/products/1",'溶剂', '电子级溶剂','')
getProductType("https://web.jkchemical.com/api/product-catalog/2194/products/1",'溶剂', '制备色谱级溶剂','')


excelUtils.generateExcel('jkchemical.xlsx', products, header)