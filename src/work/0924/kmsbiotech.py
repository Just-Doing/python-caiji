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
header=['link', 'Product Name']

def addHeader(title):
  if title not in header:
    header.append(title)

def getProductInfo(url):
  print(str(len(products)) + ":" + url)
  sope = httpUtils.getRenderdHtmlFromUrl(url)
  specArea = sope.find("div", attrs={"class":"sofish-typo s-veditor-show"})
  pName = sope.find("div", attrs={"class":"product-title text-ellipsis-2"})
  pInfo = {}
  pInfo["link"] = url
  pInfo["Product Name"] = getNodeText(pName)
  specStr = getInnerHtml(specArea)
  specStr = specStr.replace('<br style="padding: 0px; margin: 0px;"/>',"/r/n")
  specSope = BeautifulSoup(specStr, "html.parser", from_encoding="utf-8")
  specSpans = specSope.find_all("span")
  for specSpan in specSpans:
    specs = getNodeText(specSpan).split("/r/n")
    for spec in specs:
      specPart = spec.strip().split("：")
      if len(specPart) == 2:
        title = specPart[0]
        value = specPart[1]
        addHeader(title)
        pInfo[title] = value
  products.append(pInfo.copy())


def getProductList(url):
  sope = httpUtils.getHtmlFromUrl(url)
  proArea = sope.find("ul", attrs={"class":"proLists"})
  lis = proArea.find_all("li")
  for li in lis:
    pLink = li.find("a")
    if pLink!=None:
      src = pLink["href"]
      if src.find("/") == 0:
        src = "http://www.kmsbiotech.com"+src
      getProductInfo(src)

for pIndex in range(1, 13):
  getProductList("http://www.kmsbiotech.com/usercategory/product/209662/pages/"+str(pIndex)+"/")


# getProductInfo("http://www.kmsbiotech.com/product/633369/")

excelUtils.generateExcel('kmsbiotech.xlsx', products, header)