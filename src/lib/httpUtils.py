import requests
from urllib.request import urlopen
import urllib
from selenium import webdriver
from bs4 import BeautifulSoup
import http.client
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.writer.excel import ExcelWriter
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
import json
import re
import copy
import string
import time
import cfscrape

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

http.client._MAXHEADERS = 1000


def urllib_download(url, fileName, timeout=0):
    url = url.replace(" ", "%20")
    url = urllib.parse.quote(
            url, safe=string.printable
        )
    while(timeout < 5):
        try:
            time.sleep(timeout)
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            time.sleep(timeout)
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(
                url, fileName.replace("/", "").replace("\\", "")
            )
            break
        except Exception as e:
            print(e)
            timeout += 1
            print("error: urllib_download"+ str(timeout))



def getHtmlFromSafeUrl(url):
    headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
		"cookie":"_ga=GA1.2.1846208171.1605273760; href=https%3A%2F%2Fwww.sinobiological.com%2Fresearch%2Ftargeted-therapy; accessId=5aff5fb0-84db-11e8-a3b3-d368cce40a8e; _gcl_au=1.1.1660157260.1645016298; Hm_lvt_2d911fad88dfe99ff8bbf610824f3e67=1645016298; sbb=%252be43ohTbVTr09K%252bxQlr1%252bK0onQvF%252bMIXgZM%252bveGXMHU%253dXTaJopSyq01ihC4cD5jOfAa8AEgsWX792EAllASK%252bEKohz0p3JxSEJFavoBnvUmw4fhBpwMcWGZ2Qy%252bRRF2U%252bMSxcQdMfdwOcT%252bR%252bo7qyEU%252br8SBQuGE8GJWgDFeSTZ4QS0HvJFVazETAoyuKMwGHYRoD68%252f7qno5Bg%252bEH9sSXM4upMLtz%252f4IdNkjX6GD0JYHbiUh%252blGTwi25Iz3IKocTDD58DE1yYiY3DxeifN7Qz6OxtXX21lrBpnvgDu9ANN%252f7TTxWWMmOIjxVG772o%252bYGkE9AMxcU5O4cIrT9cubm6dAdgw6n%252fQRZpTVxNv2TGHdHZblPNcfu4dTWVsL3aqaag%253d%253d; _gid=GA1.2.832211649.1645016298; _ce.s=v11.rlc~1645016301520; pageViewNum=13; Hm_lpvt_2d911fad88dfe99ff8bbf610824f3e67=1645017042; Currency=RMB; LocationCode=CN"
	}

    scraper = cfscrape.create_scraper()
    html_code = scraper.get(url,headers=headers).text
    return BeautifulSoup(html_code, "html.parser",from_encoding="utf-8")


def getHtmlStrFromUrl(url, timeout=0):
    try:
        url = urllib.parse.quote(
            url, safe=string.printable
        ).replace(' ', '%20')
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36"
        }
        htmlHeader = requests.head(url)
        if htmlHeader.status_code ==200:
            request_obj = urllib.request.Request(url=url, headers=headers)
            response_obj = urllib.request.urlopen(request_obj)
            time.sleep(timeout)
            html_code = response_obj.read()
            timeout = 1
            return html_code
        else:
            return None
    except:
        timeout += 1
        print("error: getHtmlStrFromUrl===>"+str(timeout))
        getHtmlStrFromUrl(url, timeout)

def getHtmlFromUrl(url, timeout=0):
    sope = None
    while(sope == None):
        try:
            url = urllib.parse.quote(
                url, safe=string.printable
            ).replace(' ', '%20')
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36",
                "x-requested-with":"XMLHttpRequest"
            }
            print('sleep----'+str(timeout))
            time.sleep(timeout)
            request_obj = urllib.request.Request(url=url, headers=headers)
            response_obj = urllib.request.urlopen(request_obj)
            html_code = response_obj.read()
            sope = BeautifulSoup(html_code, "html.parser", from_encoding="utf-8")
            timeout = 0
        except Exception as e:
            print(e)
            # timeout += 1
            # if timeout > 2:
            sope = BeautifulSoup("<html></html>", "html.parser", from_encoding="utf-8")
            print("error: getHtmlFromUrl===>"+str(timeout))
    return sope

def cutImgFromUrl(url, isScreenShotName=""):
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument("window-size=1024,768")
	chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"')
	chrome_options.add_argument("cookie=__hstc=240517788.35783e1d438e8f99e34188727b050107.1648374652176.1648374652176.1648374652176.1; hubspotutk=35783e1d438e8f99e34188727b050107; __hssrc=1; _gid=GA1.2.122553597.1648374652; _gcl_au=1.1.15847883.1648374654; _fbp=fb.1.1648374655847.2011294960; __hssc=240517788.6.1648374652176; _ga=GA1.1.457442853.1648374652; _ga_SBEXK5LM3N=GS1.1.1648374653.1.1.1648376932.0")
	chrome_options.add_argument("--no-sandbox")

	browser = webdriver.Chrome(chrome_options=chrome_options)
	browser.get(url)
	if len(isScreenShotName) > 0:
		imgEle = browser.find_element_by_xpath('//body/img[1]')
		if imgEle !=None:
			imgEle.screenshot(isScreenShotName)
                        
def getRenderdHtmlFromUrl(url):
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument("--proxy-server=http://127.0.0.1:33210")
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('--remote-debugging-port=9515')
    # chrome_options.add_argument('--disable-setuid-sandbox')
    browser = webdriver.Chrome(options=chrome_options)

    browser.get(url)
    source = browser.page_source
    browser.close()
    return BeautifulSoup(source, "html.parser", from_encoding="utf-8")


def getJson(url, timeout=0):
    print(url)
    data = None
    while(data == None):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
                "cookie":"_gcl_au=1.1.2116952823.1684651238; _gid=GA1.2.660697749.1684651238; sa-user-id=s%253A0-5a76634c-f54c-494a-75d4-506f96af671f.u6OzscqlUHXSWi9OeldaxqDNJ64LRzMDton5BSP9p58; sa-user-id-v2=s%253AWnZjTPVMSUp11FBvlq9nH7aVzWk.9OIaLHwkfNiNZuZlMoLMawwH0hbzhxkrN%252FDTlJqdfU8; calltrk_referrer=https%3A//mail.qq.com/; calltrk_landing=https%3A//sekisuidiagnostics.com/products/enzymes/%3Fblock-product-table%3D%257B%2522tax%2522%253A%257B%2522product_category%2522%253A%255B19%255D%257D%257D; ln_or=eyIyNDY1NTcyIjoiZCJ9; _hjFirstSeen=1; _hjIncludedInSessionSample_1991571=1; _hjSession_1991571=eyJpZCI6Ijg5Y2RhYzczLTg5MjMtNGU4My1hOWJjLTA4NzE2Yjk0ZWFjNCIsImNyZWF0ZWQiOjE2ODQ2NTEyNDE3NTMsImluU2FtcGxlIjp0cnVlfQ==; _hjAbsoluteSessionInProgress=0; __hstc=125659733.82c25963b999f31bebaa80e3353d4b80.1684651280013.1684651280013.1684651280013.1; hubspotutk=82c25963b999f31bebaa80e3353d4b80; __hssrc=1; _hjSessionUser_1991571=eyJpZCI6IjFiYWU5OGMyLTVkYjYtNWM0ZC1hYTk4LTM4OGZmYzJiYTU2ZSIsImNyZWF0ZWQiOjE2ODQ2NTEyNDE3MzksImV4aXN0aW5nIjp0cnVlfQ==; _ga_XJWZH89MPH=GS1.1.1684651237.1.1.1684652253.60.0.0; _ga=GA1.1.958045190.1684651238; OptanonConsent=isGpcEnabled=0&datestamp=Sun+May+21+2023+14%3A57%3A33+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.33.0&isIABGlobal=false&hosts=&consentId=41a54409-63b8-4c12-b1d7-4d6d45e3bf77&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CSSPD_BG%3A1%2CC0004%3A1%2CC0002%3A1&AwaitingReconsent=false",
                "x-requested-with":"XMLHttpRequest"
            }

            scraper = cfscrape.create_scraper()
            time.sleep(timeout)
            html_code = scraper.get(url,headers=headers).text
            timeout = 0
            data = json.loads(html_code)
        except Exception as e:
            print(e)
            print("error: getJson===>"+str(timeout))
            timeout += 1
            if timeout > 10:
                data={}
    return data

def postJson(url, body):
    data = None
    timeout=0
    while(data == None):
        try:
            headers = {
                "cookie": "_cfuvid=uYP3UwkfJZMTorqBi2Sorg1MHRkjjBb8uLXKj46aCT0-1686983078463-0-604800000; JSESSIONID=btky8xpq6QOdi_z2WuIUHBfOl91XWShTu6PWqMlm.app1; __cf_bm=gk9xHFfWJUhyCBokTDMUTeHlZ.2vOU1UYSatHtNt8XY-1686983082-0-AXRAHimuF8URpgy+tIpsKPy9TMQNEe6V9cahW6XEFqy4fD0jtL25yNNN3qGcdh0BCtumgEkvvkj6WtWkpWWYPzMt54/qI8drl1DjF9val+36; n32HasSeenSigninPopup=true; __kla_id=eyIkcmVmZXJyZXIiOnsidHMiOjE2ODY5ODMwODMsInZhbHVlIjoiIiwiZmlyc3RfcGFnZSI6Imh0dHBzOi8vd3d3Lm5ldDMyLmNvbS9lYy9lbmRvZG9udGljLXQtNTI4In0sIiRsYXN0X3JlZmVycmVyIjp7InRzIjoxNjg2OTgzMDgzLCJ2YWx1ZSI6IiIsImZpcnN0X3BhZ2UiOiJodHRwczovL3d3dy5uZXQzMi5jb20vZWMvZW5kb2RvbnRpYy10LTUyOCJ9fQ==; ABTastySession=mrasn=&lp=https%253A%252F%252Fwww.net32.com%252Fec%252Fendodontic-t-528%253Fpage%253D1; ABTasty=uid=d7zr8y5ywkgbmjtd&fst=1686983208263&pst=-1&cst=1686983208263&ns=1&pvt=1&pvis=1&th=&eas=",
                "Content-Type":"application/json"
            }
            time.sleep(timeout)
            scraper = cfscrape.create_scraper()
            html_code = scraper.post(url, json=body, headers=headers).text
            data = json.loads(html_code)
            timeout = 0
        except Exception as e:
            print(e)
            timeout += 1
            print("error: getJson===>"+str(timeout))
            if timeout > 10:
                data={}
    return data

    