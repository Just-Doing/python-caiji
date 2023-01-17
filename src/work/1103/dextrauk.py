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
header=['link','type', 'Product Name','Product Code','Description','Img Name','size0','price0','size1','price1','size2','price2','size3','price3','size4','price4','size5','price5','size6','price6','size7','price7']


def addHeader(title):
  if title not in header and len(title) > 0:
    header.append(title)

def getProductInfo(url, type):
  print(str(len(products)) + ":" + url)
  pInfo = {}
  sope = httpUtils.getRenderdHtmlFromUrl(url)
  specArea = sope.find("div", attrs={"class":"product-page-intro-text"})
  pName = specArea.find("h1")
  pCode = specArea.find("span", attrs={"class":"sku-meta"})
  desc = specArea.find("div", attrs={"class":"m-t-small"})
  pInfo["link"] = url
  pInfo["type"] = type
  pInfo["Product Name"] = getNodeText(pName)
  pInfo["Product Code"] = getNodeText(pCode).replace("Product Code:","")
  pInfo["Description"] = getNodeText(desc)
  imgArea = sope.find("div", attrs={"class":"carousel-cell is-selected"})
  if imgArea!= None:
    img = imgArea.find("img")
    if img != None:
      src = img["src"]
      imgName = pInfo["Product Code"]+".png"
      httpUtils.urllib_download(src, imgName)
      pInfo["Img Name"] = imgName
  overviewArea = sope.find("div", attrs={"id":"tab-overview"})
  if overviewArea!=None:
    lis = overviewArea.find_all("li")
    for li in lis:
      h4 = li.find("h4")
      p = li.find("p")
      title = getNodeText(h4)
      if len(title) > 0:
        addHeader(title)
        pInfo[title] = getNodeText(p)
  sizeArea = sope.find("form", attrs={"class":"variations_form cart"})
  data = json.loads(sizeArea["data-product_variations"])
  if len(data)>0:
    for sizeInx in range(0, len(data)):
      sizeOpt = data[sizeInx]
      sizeTitle = "size"+str(sizeInx)
      pInfo[sizeTitle] = str(sizeOpt["sku"])
      priceTitle = "price"+str(sizeInx)
      pInfo[priceTitle] = str(sizeOpt["display_price"])
  products.append(pInfo.copy())


def getProductList(url, type):
  sope = httpUtils.getHtmlFromUrl(url)
  lis = sope.find_all("div", attrs={"class":"product-tile-link"})
  for li in lis:
    pLink = li.find("a")
    if pLink != None:
      src = pLink["href"]
      getProductInfo(src, type)

for pIndex in range(1, 5):
  getProductList("https://www.dextrauk.com/products/blood-group-products/?sf_paged="+str(pIndex), 'Blood Group Products')

for pIndex in range(1, 7):
  getProductList("https://www.dextrauk.com/products/Glycoconjugates/?sf_paged="+str(pIndex), 'Glycoconjugates')

for pIndex in range(1, 13):
  getProductList("https://www.dextrauk.com/products/Oligosaccharides/?sf_paged="+str(pIndex), 'Oligosaccharides')
for pIndex in range(1, 11):
  getProductList("https://www.dextrauk.com/products/monosaccharides/?sf_paged="+str(pIndex), 'Monosaccharides')
for pIndex in range(1, 3):
  getProductList("https://www.dextrauk.com/products/nucleosides-nucleotides/?sf_paged="+str(pIndex), 'Nucleosides & Nucleotides')
for pIndex in range(1, 10):
  getProductList("https://www.dextrauk.com/products/Polysaccharides/?sf_paged="+str(pIndex), 'Polysaccharides')

# getProductList("https://www.dextrauk.com/products/Polysaccharides/?sf_paged=1", 'Polysaccharides')

# getProductInfo("https://www.dextrauk.com/products/blood-group-products/affinity-columns/blood-group-b-trisaccharide-sepharose-ff/",'ss')

excelUtils.generateExcel('dextrauk.xlsx', products, header)