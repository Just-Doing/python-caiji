from itertools import product
import sys
from selenium import webdriver
from bs4 import BeautifulSoup
import time

sys.path.append('../..')
from lib import excelUtils
from lib import httpUtils
from lib import textUtil
from lib.htmlEleUtils import getNodeText
from lib.htmlEleUtils import getInnerHtml
products = []
header=['link','nav', 'Product Name', 'Formulation','Solubility','Purity','Description','Reagent Appearance','Stability']
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("window-size=1024,768")

# chrome_options.add_argument("--no-sandbox")
browser = webdriver.Chrome(chrome_options=chrome_options)
def addHeader(title):
  if title not in header:
    header.append(title)

def getProductInfo(url):
  print(str(len(products)) + ":" + url)

  browser.get(url)
  time.sleep(5)
  sope= BeautifulSoup(browser.page_source, "html.parser")

  nav = sope.find("span", attrs={"class":"navigation_page"})
  pName = sope.find("h1", attrs={"itemprop":"name"})
  pInfo = {}
  pInfo["link"] = url
  pInfo["nav"] = getNodeText(nav)
  pInfo["Product Name"] = getNodeText(pName)
  sizeArea = browser.find_elements_by_class_name('attribute_select')
  if len(sizeArea)>0:
    sizes=sizeArea[0].find_elements_by_tag_name("option")
    if len(sizes)>0:
      for sizeInx in range(0, len(sizes)):
        sizeOpt = sizes[sizeInx]
        sizeOpt.click()
        sizeSope= BeautifulSoup(browser.page_source, "html.parser")
        price = sizeSope.find("span", attrs={"id":"our_price_display"})
        sizeTitle = "size"+str(sizeInx)
        priceTitle = "price"+str(sizeInx)
        pInfo[sizeTitle] = sizeOpt.text
        pInfo[priceTitle] = getNodeText(price)
        addHeader(sizeTitle)
        addHeader(priceTitle)
  trs = sope.find_all("tr")
  for tr in trs:
    tds = tr.find_all("td")
    if len(tds) == 2:
      title = getNodeText(tds[0])
      value = getNodeText(tds[1])
      pInfo[title] = value

  products.append(pInfo.copy())


def getProductList(url):
  sope = httpUtils.getHtmlFromUrl(url)
  lis = sope.find_all("li", attrs={"class":"ajax_block_product"})
  for li in lis:
    pLink = li.find("a")
    if pLink != None:
      src = pLink["href"]
      getProductInfo(src)


getProductList("https://novateinbio.com/search?search_query=diabetes&search_query=diabetes&orderby=position&orderway=desc&n=143")


# getProductInfo("https://novateinbio.com/growth-factors/73192-Leptin-Rat.html?search_query=diabetes&results=143#/567-product_size-200ug")

excelUtils.generateExcel('novateinbio.xlsx', products, header)