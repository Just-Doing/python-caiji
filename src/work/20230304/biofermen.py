from itertools import product
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
import _thread


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

def getProductInfo(browser, url, type):
  print(str(len(products)) + ":" + url)
  pInfo = {
    "link": url,
    "Protuct name": type["name"],
    "CAS": type["CAS"],
    "URL": type["URL"],
    "Catalog": type["Catalog"]
  }

  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  nav = sope.find("header", attrs={"class":"ncbi-header"})
  if nav == None:
    time.sleep(20)
    getProductInfo(getBrowser(), url, type)
  journal = sope.find("div", attrs={"class":"article-citation"})
  pInfo["journal"] =  getNodeText(journal)
  title = sope.find("h1", attrs={"class":"heading-title"})
  pInfo["title"] =  getNodeText(title)
  authors = sope.find("div", attrs={"class":"inline-authors"})
  pInfo["authors"] =  getNodeText(authors)
  pubmed = sope.find("span", attrs={"class":"identifier pubmed"})
  pInfo["pubmed"] =  getNodeText(pubmed).replace("PMID:","").replace("\n","")
  abstract = sope.find("div", attrs={"id":"abstract"})
  pInfo["abstract"] =  getNodeText(abstract)


  print(pInfo)
  products.append(pInfo.copy())


def getProductList(browser, url, type):
  browser.get(url)
  sope= BeautifulSoup(browser.page_source, "html.parser")
  nav = sope.find("header", attrs={"class":"ncbi-header"})
  if nav == None:
    time.sleep(20)
    getProductList(getBrowser(), url, type)

  listRes = sope.find("section", attrs={"class":"search-results-list"})
  if listRes == None:
    getProductInfo(browser, url, type)
  else:
    articles = listRes.find_all("article")
    if len(articles) == 0:
      products.append({
        "link": url,
        "Protuct name": type["name"],
        "CAS": type["CAS"],
        "URL": type["URL"],
        "Catalog": type["Catalog"]
      })
    else:
      for article in articles:
        pLink = article.find("a")
        getProductInfo(browser, "https://pubmed.ncbi.nlm.nih.gov"+pLink["href"], type)


def getProductType(browser, fileName, inx):
  with open(fileName,'rb') as file_to_read:
    content=file_to_read.read()
    types = json.loads(content)
    for type in types:
      getProductList(browser, "https://pubmed.ncbi.nlm.nih.gov/?term="+type["name"].replace(" ", "+"), type)
  excelUtils.generateExcel('biofermen'+str(inx)+'.xlsx', products,['link','Protuct name','CAS', 'URL', 'Catalog','journal','title','authors','pubmed','abstract'])

try:
	# _thread.start_new_thread( getProductType, (getBrowser(),'data1.json',1) )
	# _thread.start_new_thread( getProductType, (getBrowser(),'data2.json' ,2) )
	# _thread.start_new_thread( getProductType, (getBrowser(),'data3.json' ,3) )
	# _thread.start_new_thread( getProductType, (getBrowser(),'data4.json' ,4) )
	_thread.start_new_thread( getProductType, (getBrowser(),'data5.json' ,6) )
except:
	print ("Error: 无法启动线程")
while 1:
   pass



