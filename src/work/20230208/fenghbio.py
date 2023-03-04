from itertools import product
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


sys.path.append('../..')
from lib import excelUtils
from lib import httpUtils
from lib import textUtil
from lib.htmlEleUtils import getNodeText
from lib.htmlEleUtils import getInnerHtml
products = []
header=['link','type', 'Product Name','size','发货方式']
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("window-size=1024,768")
chrome_options.add_argument("--proxy-server=http://127.0.0.1:33210")

# chrome_options.add_argument("--no-sandbox")
browser = webdriver.Chrome(chrome_options=chrome_options)

def svg_to_png(svgSrc, pngSrc):
  pic = svg2rlg(svgSrc)
  renderPM.drawToFile(pic, pngSrc)

def addHeader(title):
  if title not in header and len(title) > 0:
    header.append(title)

def getProductInfo(url,type1):
  print(str(len(products)) + ":" + url)
  pInfo = {
    "type":type1
  }
  pInfo["link"] = url
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  pName = sope.find("div", attrs={"class":"goodsnames"})
  
  timeToWaite = 1
  while(pName == None):
    browser.get(url)
    time.sleep(timeToWaite)
    timeToWaite += 1
    sope= BeautifulSoup(browser.page_source, "html.parser")
    pName = sope.find("div", attrs={"class":"goodsnames"})
  timeToWaite = 1
  pInfo["Product Name"] = getNodeText(pName)
  size = sope.find("font", attrs={"class":"shop word_c"})
  pInfo["size"] = getNodeText(size)
  sendWay = sope.find("li", attrs={"class":"padd loop labelinput"})
  pInfo["发货方式"] = getNodeText(sendWay).replace("发货方式：","")

  trs = sope.find_all("li")
  for tr in trs:
    spans = tr.find_all("span")
    if len(spans) == 2:
      title = getNodeText(spans[0])
      value = getNodeText(spans[1])
      if len(title) >0:
        pInfo[title] = value
        addHeader(title)
  # print(pInfo)
  products.append(pInfo.copy())


def getProductList(url, type1):
  print(url)
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  listArea = sope.find("div", attrs={"class":"prclist_page"})
  trs = listArea.find_all("div", attrs={"class":"prcitem"})
  for tr in trs:
    pLink = tr.find("a")
    if pLink != None:
      linkSrc = "http://www.fenghbio.cn/" + pLink["href"]
      getProductInfo(linkSrc, type1)



# getProductInfo('http://www.fenghbio.cn/goods.php?id=87090', 'type1', 'type2')
# getProductList("http://www.fenghbio.cn/category.php?id=43&price_min=0&price_max=0&page=1&sort=sort_order&order=DESC")
for pIndex in range(1, 6):
  getProductList("http://www.fenghbio.cn/category.php?id=69&price_min=0&price_max=0&page="+str(pIndex)+"&sort=shop_price&order=ASC",'植物细胞载体')
getProductList("http://www.fenghbio.cn/category.php?id=76",'枯草杆菌载体')
getProductList("http://www.fenghbio.cn/category.php?id=80",'丝状真菌载体')
getProductList("http://www.fenghbio.cn/category.php?id=77",'鱼类系列质粒')
getProductList("http://www.fenghbio.cn/category.php?id=74",'杆菌系列质粒')
getProductList("http://www.fenghbio.cn/category.php?id=71",'球菌系列质粒')
for pIndex in range(1, 6):
  getProductList("http://www.fenghbio.cn/category.php?id=69&price_min=0&price_max=0&page="+str(pIndex)+"&sort=shop_price&order=ASC",'植物细胞载体')


excelUtils.generateExcel('fenghbio.xlsx', products, header)