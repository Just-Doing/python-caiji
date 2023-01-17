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
header=['link','Category','CAS号','Product Name','price','imageName']


def addHeader(title):
  if title not in header and len(title) > 0:
    header.append(title)

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("window-size=1024,768")

# chrome_options.add_argument("--no-sandbox")
browser = webdriver.Chrome(chrome_options=chrome_options)

def getProductInfo(url, type):
  print(str(len(products)) + ":" + url)
  browser.delete_all_cookies()
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  nav = sope.find("div", attrs={"class":"crumbs matp"})
  if nav == None:
    browser.delete_all_cookies()
    browser.get(url)
    sope= BeautifulSoup(browser.page_source, "html.parser")
    nav = sope.find("div", attrs={"class":"crumbs matp"})
  if nav == None:
    browser.delete_all_cookies()
    browser.get(url)
    sope= BeautifulSoup(browser.page_source, "html.parser")
    nav = sope.find("div", attrs={"class":"crumbs matp"})

  pInfo = {
    "Category": type,
    "link": url
  }
  baseInfos = sope.find_all("li", attrs={"class":"proulllli"})
  for baseInfo in baseInfos:
    ebs = baseInfo.find_all("b")
    for b in ebs:
      title = getNodeText(b)
      if title == "names：":
        pInfo["Product Name"] = getNodeText(baseInfo).replace("names：", "")
      else:
        titlePart = title.split("：")
        if len(titlePart) > 1:
          addHeader(titlePart[0])
          pInfo[titlePart[0]] = titlePart[1]


    spans = baseInfo.find_all("span")
    for span in spans:
      title = getNodeText(span)
      titlePart = title.split("：")
      if len(titlePart) == 1:
        titlePart = title.split(":")
      if len(titlePart)>1:
        addHeader(titlePart[0])
        pInfo[titlePart[0]] = titlePart[1]

  specTbs = sope.find_all("table",attrs={"class":"protwtab"})
  specStr = ""
  for specTb in specTbs:
    trs = specTb.find_all("tr")
    if len(trs) > 0:
      ths = trs[0].find_all("th")
      if len(ths)>2:
        title = getNodeText(ths[1])
        if title == "规格":
          for inx,tr in enumerate(trs):
            if inx>0:
              tds = tr.find_all("td")
              specStr += "("+getNodeText(tds[1])+"/"+getNodeText(tds[4])+");"
  pInfo["price"] = specStr
  infoTrs = sope.find_all("tr")
  for infoTr in infoTrs:
    tds = infoTr.find_all("td")
    if len(tds) == 2:
      title = getNodeText(tds[0])
      value = getNodeText(tds[1])
      addHeader(title)
      pInfo[title] = value

  imageName = ""
  if "Product Name" in pInfo:
    imageName = pInfo["Product Name"]+".png"
  if "CAS号" in pInfo:
    imageName = pInfo["CAS号"]+".png"
  pInfo["imageName"] = imageName
  imgArea = sope.find("i", attrs={"id":"D2"})
  img = imgArea.find("img")
  if img!=None:
    httpUtils.urllib_download("http://bio-fount.com"+img["src"], imageName)

  products.append(pInfo.copy())


def getProductType(url, type1):
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  plinkAreas = sope.find("ul", attrs={"id":"mo"}).find_all("li", attrs={"class":"fl"})
  if len(plinkAreas) == 0:
    time.sleep(1)
    browser.delete_all_cookies()
    browser.get(url)
    sope= BeautifulSoup(browser.page_source, "html.parser")
    plinkAreas = sope.find_all("article")
  for plinkArea in plinkAreas:
    pLink = plinkArea.find("a")
    getProductInfo("http://bio-fount.com"+pLink["href"], type1)



# getProductType("http://bio-fount.com/cn/goods-list/1375.html",'cDNA Clones')
# getProductInfo("http://bio-fount.com/cn/goods2/61740_1375.html", "a")
for pageIndex in range(1, 5):
  getProductType("http://bio-fount.com/cn/goods-list/1375__"+str(pageIndex)+".html",'脂肪族含氟砌块')
for pageIndex in range(1, 6):
  getProductType("http://bio-fount.com/cn/goods-list/1374__"+str(pageIndex)+".html",'杂环含氟砌块')
getProductType("http://bio-fount.com/cn/goods-list/1372.html",'氟标记化合物')
for pageIndex in range(1, 22):
  getProductType("http://bio-fount.com/cn/goods-list/1371__"+str(pageIndex)+".html",'芳香族含氟砌块')


excelUtils.generateExcel('bio-fount.xlsx', products, header)