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
header=['link','type','nav','size0', 'price0','size1', 'price1','size2', 'price2','size3', 'price3','size4', 'price4','size5', 'price5', 
'Product Name','Key features and details','Description','Related conjugates and formulations','Host species'
,'Tested applications','Species reactivity','Immunogen','Positive control','General notes','Form','Storage instructions',
'Dissociation constant (KD)','Storage buffer','Concentration','Purity','Clonality','Clone number','Isotype'
,'Research areas','Applications','Function','Tissue specificity','Involvement in disease','Sequence similarities','Domain','Post-translationalmodifications','Cellular localization']


def addHeader(title):
  if title not in header and len(title) > 0:
    header.append(title)

def getProductInfo(url, type):
  print(str(len(products)) + ":" + url)
  pInfo = {}
  pInfo["type"] = type
  pInfo["link"] = url
  sope = httpUtils.getRenderdHtmlFromUrl(url)
  keyfeatures = sope.find("section", attrs={"id":"key-features"})
  pInfo["Key features and details"] = getNodeText(keyfeatures)
  Related = sope.find("div", attrs={"class":"conjugates-tool__content__inner"})
  pInfo["Related conjugates and formulations"] = getNodeText(Related)
  nav = sope.find("nav", attrs={"class":"breadcrumb h-padding-lt-lrg"})
  pInfo["nav"] = getNodeText(nav)
  pName = sope.find("h1", attrs={"class":"title"})
  pInfo["Product Name"] = getNodeText(pName)
  applicaton = sope.find("div", attrs={"id":"description_applications"})
  if applicaton != None:
    applicaton = applicaton.find("table")
    pInfo["Applications"] = getNodeText(applicaton)
  lis = sope.find_all("li", attrs={"class":"attribute"})
  for li in lis:
    titleArea = li.find("h3")
    if titleArea == None:
      titleArea = li.find("div", attrs = {"class":"name"})
    title = getNodeText(titleArea)
    value = getNodeText(li.find("div", attrs={"class":"value"}))
    if title == "Chemical structure":
      img = li.find("img")
      if img != None:
        imgName = str(len(products))+'.png'
        pInfo["Chemical structure"] = imgName
        httpUtils.urllib_download("https://www.abcam.com"+img["src"], imgName )
    else:
      pInfo[title] = value
    sizeArea = sope.find("div", attrs={"class":"size-selector-radios"})
    if sizeArea != None:
      sizes = sizeArea.find_all("span", attrs={"class":"product-size"})
      for inx, size in enumerate(sizes):
        sizeInfo = size.find_all("span")
        sizeTxt = "size"+str(inx)
        priceTxt = "price"+str(inx)
        pInfo[sizeTxt] = getNodeText(sizeInfo[0])
        pInfo[priceTxt] = getNodeText(sizeInfo[1])
    else:
      size0 = getNodeText(sope.find("div", attrs={"class":"size-price-placeholder"}))
      price = getNodeText(sope.find("span", attrs={"class":"price-holder"}))
      pInfo["size0"] = size0
      pInfo["price0"] = price
  products.append(pInfo.copy())


def getProductList(fileName, type):
  with open(fileName,'r') as file_to_read:
    content=file_to_read.read()
    sope = BeautifulSoup(content, "html.parser", from_encoding="utf-8")
    ps = sope.find_all("div", attrs={"class":"clearfix selection-item res res-item-Primary antibodies has-img js-item-treated"})
    for p in ps:
      linkArea = p.find("h3")
      pLink = linkArea.find("a")
      getProductInfo("https://www.abcam.com"+pLink["href"], type)

# getProductList('Agonists.txt', 'Agonists, activators, antagonists and inhibitors /Cytoskeleton')

getProductList('Primaryantibodies.txt', 'Antibodies /Cytoskeleto')


# getProductInfo("https://www.abcam.com/vimentin-antibody-epr3776-cytoskeleton-marker-ab92547.html?productWallTab=ShowAll",'ss')

excelUtils.generateExcel('abcam.xlsx', products, header)