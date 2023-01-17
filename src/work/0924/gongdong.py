from itertools import product
import sys

sys.path.append('../..')
from lib import excelUtils
from lib import httpUtils
from lib import textUtil
from lib.htmlEleUtils import getNodeText
products = []
header=['link', 'type1', 'type2', 'Type Nav', 'Type Description', 'Product Name',"Img Name","Product Description", "Key Features"]

def addHeader(title):
  if title not in header:
    header.append(title)

def getProductInfo(url, typeInfo):
  print(str(len(products)) + ":" + url)
  sope = httpUtils.getRenderdHtmlFromUrl(url)
  specArea = sope.find("div", attrs={"class":"richtext fz18 lh34 mt20 over-hides"})
  pName = sope.find("h1", attrs={"class":"titles fz40 bold1"})
  pInfo = typeInfo.copy()
  pInfo["link"] = url
  pInfo["Product Name"] = getNodeText(pName)
  specs = specArea.find_all("li")
  specs += specArea.find_all("p")
  for spec in specs:
    speccStr = getNodeText(spec)
    if speccStr.find(":") > -1:
      specParts = speccStr.split(":")
      title = specParts[0]
      value = speccStr.replace(title+":", "").replace(title+" :","").replace(title+"  :","")
      pInfo[title] = value
      addHeader(title)
      if value.find(":") >-1:
        title2 = value.split(":")[0]
        value2 = value.replace(title+":", "").replace(title+" :","").replace(title+"  :","")

  h2s = sope.find_all("h2")
  for h2 in h2s:
    title = getNodeText(h2)
    if title.find("Product Description") > -1:
      pInfo["Product Description"] = getNodeText(h2.nextSibling.nextSibling)
    if title.find("Key Features") > -1:
      pInfo["Key Features"] = getNodeText(h2.findNextSibling("ul"))
  

  tableSpec = sope.find("div", attrs={"class":"over-tabs"})
  if tableSpec!=None:
    tableSpecTrs = tableSpec.find_all("tr")
    titleTr = tableSpecTrs[0]
    valueTr = tableSpecTrs[1]
    titleTds = titleTr.find_all("td")
    valueTds = valueTr.find_all("td")
    for inx, td in enumerate(titleTds):
      title = getNodeText(td)
      pInfo[title] = getNodeText(valueTds[inx])
      addHeader(title)
  imgArea = sope.find("div", attrs={"class":"swiper-wrapper"})
  img = imgArea.find("img")
  if img != None:
    imgName = textUtil.text4FileName(pInfo["Product Name"])+".png"
    httpUtils.urllib_download("https://en.gongdong.com"+img["src"], imgName)
    pInfo["Img Name"] = imgName
  products.append(pInfo.copy())


def getProductList(url, t1, t2):
  sope = httpUtils.getRenderdHtmlFromUrl(url)
  typeNav = sope.find("ul", attrs={"class":"breadcrumb"})
  desc = sope.find("div", attrs={"class":"richtext cors lh32 mt30"})
  tableArea = sope.find("div", attrs={"class":"richtext mt40 d-hs"})
  trs = tableArea.find_all("tr")
  for tr in trs:
    pLink = tr.find("a")
    if pLink!=None:
      src = pLink["href"]
      if src.find("/") == 0:
        src = "https://en.gongdong.com"+src
      print(src)
      getProductInfo(src, {"type1":t1, "type2":t2, "Type Nav":getNodeText(typeNav), "Type Description":  getNodeText(desc) })


def getProductType(url):
  sope = httpUtils.getHtmlFromUrl(url)
  typeArea = sope.find("div", attrs={"class":"sep-siderbar-list mt20"})
  type1s = typeArea.find_all("li", attrs={"class":"bold"})
  for type1 in type1s:
    type1Name = getNodeText(type1.find("a"))
    type2s = type1.find_all("li")
    for type2 in type2s:
      type2Link = type2.find("a")
      type2Name = getNodeText(type2Link)
      # print(type1Name+"----"+ type2Name+":"+type2Link["href"])
      getProductList("https://en.gongdong.com"+type2Link["href"],type1Name, type2Name)

getProductType('https://en.gongdong.com/products/serum-clot-activator-tube/')
# getProductInfo("https://en.gongdong.com/products-applications/25cm2-cell-culture-flask-non-treated/",{})
excelUtils.generateExcel('gongdong.xlsx', products, header)