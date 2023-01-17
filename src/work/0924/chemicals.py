from itertools import product
import sys
from bs4 import BeautifulSoup

sys.path.append('../..')
from lib import excelUtils
from lib import httpUtils
from lib import textUtil
from lib.htmlEleUtils import getNodeText
from lib.htmlEleUtils import getInnerHtml
products = []
header=['link', 'Product Name','Group:','Quality:','Shipping and Storage:','Solubility:','Cas No.:']

def addHeader(title):
  if title not in header:
    header.append(title)

def getProductInfo(url):
  print(str(len(products)) + ":" + url)
  sope = httpUtils.getHtmlFromUrl(url)
  specArea = sope.find("div", attrs={"id":"content_oc"})
  if specArea!=None:
    pName = specArea.find("h1")
    pInfo = {}
    pInfo["link"] = url
    pInfo["Product Name"] = getNodeText(pName)
    specs = sope.find_all("tr")
    for spec in specs:
      tds = spec.find_all("td")
      if len(tds) == 2:
        title = getNodeText(tds[0])
        value = getNodeText(tds[1])
        pInfo[title] = value
    print(pInfo)
    products.append(pInfo.copy())


def getProductList(url):
  sope = httpUtils.getHtmlFromUrl(url)
  lis = sope.find_all("div", attrs={"class":"product-layout"})
  for li in lis:
    pLink = li.find("a")
    if pLink!=None:
      src = pLink["href"]
      if src.find("/") == 0:
        src = "https://chemicals.transmit.shop"+src
      getProductInfo(src)

for pIndex in range(1, 5):
  getProductList("https://chemicals.transmit.shop/products/natural-products?limit=100&page="+str(pIndex))


# getProductInfo("https://chemicals.transmit.shop/products/natural-products/product/96-1-5-dicaffeoylquinic-acid")

excelUtils.generateExcel('chemicals.xlsx', products, header)