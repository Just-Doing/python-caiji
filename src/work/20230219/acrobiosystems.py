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
header=[]
sizeHeader=[]

def getBrowser():
  chrome_options = webdriver.ChromeOptions()
  # chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-gpu')
  chrome_options.add_argument("window-size=1024,768")
  chrome_options.add_argument("--proxy-server=http://127.0.0.1:33210")

  # chrome_options.add_argument("--no-sandbox")
  browser = webdriver.Chrome(chrome_options=chrome_options)
  return browser

def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)

def getProductInfo(browser, url, type, cat, spec, desc):
  print(str(len(products)) + ":" + url)
  pInfo = {
    "link": url,
    "type": type,
    "Cat. No.": cat,
    "Species":spec,
    "Product Description": desc
  }

  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  nav = sope.find("div", attrs={"class":"crumb"})
  if nav == None:
    time.sleep(20)
    getProductInfo(getBrowser(), url, type, cat, spec, desc)


  lis1 = []
  lis2 = []
  leftArea = sope.find("div", attrs={"class":"pidLeft"})
  rightArea = sope.find("div", attrs={"class":"pidRight"})
  if leftArea != None:
    lis1 = leftArea.find_all("li")
  if rightArea != None:
    lis2 = rightArea.find_all("li")

  for li in lis1+lis2:
    divs = li.find_all("div", recursive=False)
    if len(divs)>0:
      title = getNodeText(divs[0])
      value = getNodeText(li).replace(title,"")
      if len(title) >0:
        pInfo[title] = value
        addHeader(header, title)
  imgItems = sope.find_all("div", attrs={"class":"item_name"})
  for imgItem in imgItems:
    title = getNodeText(imgItem)
    if len(title)>0:
      value = getNodeText(imgItem.parent).replace("Protocol","").replace("Report","")
      if len(value) > 0:
        pInfo[title] = value
        addHeader(header, title)
  sizeArea = sope.find("div", attrs={"class":"box1 goods"})
  if sizeArea != None:
    sizeLis = sizeArea.find_all("div", attrs={"class":"li"})
    for inx, sizeLi in enumerate(sizeLis):
      sizeTitle = "size-"+str(inx)
      priceTitle = "price-"+str(inx)
      size = getNodeText(sizeLi.find("h4"))
      price=getNodeText(sizeLi.find("div", attrs={"class":"con"}).find("p"))
      pInfo[sizeTitle] = size
      pInfo[priceTitle] = price.replace("Price(USD) :","")
      addHeader(sizeHeader, sizeTitle)
      addHeader(sizeHeader, priceTitle)
  
  products.append(pInfo.copy())


def getProductList(browser, url, type):
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  nav = sope.find("div", attrs={"class":"crumb"})
  if nav == None:
    time.sleep(20)
    getProductList(getBrowser(), url, type)

  plTb = sope.find("table", attrs={"class":"layui-table productSearchTable"})
  if plTb != None:
    trs = plTb.find("tbody").find_all("tr")
    for tr in trs:
      tds = tr.find_all("td")
      pLink = tr.find("a")
      if pLink != None:
        linkSrc = pLink["href"]
        getProductInfo(browser, "https://www.acrobiosystems.com"+linkSrc, type, getNodeText(tds[0]), getNodeText(tds[1]), getNodeText(tds[2]))
  else:
    getProductInfo(browser, url, type, '', '', '')

def getProductType(browser, fileName):
  with open(fileName,'r') as file_to_read:
    content=file_to_read.read()
    types = json.loads(content)
    for type in types:
      getProductList(browser, "https://www.acrobiosystems.com"+type["url"], type["name"])

# getProductList('https://www.acrobiosystems.com/L-1547-3C-like%20Proteinase.html', 'type1')
# getProductInfo('https://www.acrobiosystems.com/P4820-Human-4-1BB-Ligand--TNFSF9-%2871-254%29-Protein-Fc-Tag-active-trimer-premium-grade.html', 'type1', 'type2','','')

getProductType(getBrowser(),'data.json')


excelUtils.generateExcel('acrobiosystems.xlsx', products,['link','type','Cat. No.', 'Species', 'Product Description']+sizeHeader+ header)