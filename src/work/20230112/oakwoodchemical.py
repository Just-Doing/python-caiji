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
header=['link', 'Product Name','price','imageName']
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

def getProductInfo(url):
  print(str(len(products)) + ":" + url)
  pInfo = {}
  pInfo["link"] = url
  browser.delete_all_cookies()
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")

  pInfo["Product Name"] = getNodeText(sope.find("span", attrs={"style":"font-size: 18px; color:#333333;"}))


  trs = sope.find_all("tr")
  for tr in trs:
    tds = tr.find_all("td")
    if len(tds) ==2:
      title = getNodeText(tds[0])
      value = getNodeText(tds[1])
      if len(title)>0:
        addHeader(title)
        pInfo[title]=value

  imageName = ""
  if "Product Name" in pInfo:
    imageName = pInfo["Product Name"]+".svg"
  if "CAS Number:" in pInfo:
    imageName = pInfo["CAS Number:"]+".svg"
  imgArea = sope.find("div", attrs={"id":"painter"})
  if imgArea != None:
    image_ = imgArea.find("svg")
    with open(imageName, 'w') as f:
        f.write(str(image_))
    pInfo["imageName"] = imageName.replace(".svg",".png")
    svg_to_png(imageName, imageName.replace(".svg",".png"))
  price = sope.find("table", attrs={"id":"_ctl0_ContentPlaceHolder1_MyGrid"})
  priceStr = ""
  sizeTrs = price.find_all("tr")
  for inx, sizeTr in enumerate(sizeTrs):
    if inx > 0:
      tds = sizeTr.find_all("td")
      if len(tds) > 3:
        sizeTxt = getNodeText(tds[1])
        priceTxt = getNodeText(tds[2]).replace("Regular Price:","").replace("Your Discounted Price: $0.00","").replace("\r","").replace("\n","")
        priceStr += sizeTxt+"/"+priceTxt+";"

  pInfo["price"] = "(" + priceStr+")"
  products.append(pInfo.copy())


def getProductList(fileName):
  with open(fileName,'r') as file_to_read:
    content=file_to_read.read()
    urls = json.loads(content)
    for url in urls:
      if len(url)>0:
        getProductInfo("https://www.oakwoodchemical.com/"+url)

# getProductInfo('https://www.oakwoodchemical.com/ProductsList.aspx?CategoryID=-2&txtSearch=38730')

getProductList('data.html')


excelUtils.generateExcel('oakwoodchemical.xlsx', products, header)