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

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

http.client._MAXHEADERS = 1000


def urllib_download(url, fileName):
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(
            url, fileName.replace("/", "").replace("\\", "")
        )
    except:
        print('no')



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
    try:
        url = urllib.parse.quote(
            url, safe=string.printable
        ).replace(' ', '%20')
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36"
        }
        print('sleep----'+str(timeout))
        time.sleep(timeout)
        htmlHeader = requests.head(url)
        if htmlHeader.status_code ==200:
            request_obj = urllib.request.Request(url=url, headers=headers)
            response_obj = urllib.request.urlopen(request_obj)
            html_code = response_obj.read()
            sope = BeautifulSoup(html_code, "html.parser", from_encoding="utf-8")
            timeout = 0
            return sope
        else:
            timeout += 1
            print("error: getHtmlFromUrl===>"+str(timeout))
            getHtmlFromUrl(url, timeout)
    except:
        timeout += 1
        print("error: getHtmlFromUrl===>"+str(timeout))
        getHtmlFromUrl(url, timeout)


def getRenderdHtmlFromUrl(url):
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("window-size=1024,768")
    chrome_options.add_argument("cookie=locale=en-US; _ga=GA1.2.1179411107.1676549188; countryJC=US; japanCurrency=JPY; mce_country_name=United%20States; mce_country_tel=%20; mce_country_type=1; sevenDaysSeoCookies=0D2750A6DD796FB8; mce_historyProducts=%2FFerrostatin-1.html%3BFerrostatin-1%3B1; tencentSig=6217980928; _qddaz=QD.wjabtv.6cd2p9.le72aqgl; JSESSIONID=YWRmNTBhNjgtNzhlOC00NzY4LWEwNTAtNjA1ZGM4MzkwMjRj; _gid=GA1.2.1090483539.1676794343; mce_2019_notice=true; disposableSeoCookie=2FEABCAC527CD3FF; _qdda=3-1.4fvqy0; _qddab=3-18llkv.leb429iy")
    chrome_options.add_argument("--proxy-server=http://127.0.0.1:33210")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(chrome_options=chrome_options)

    browser.get(url)
    return BeautifulSoup(browser.page_source, "html.parser", from_encoding="utf-8")


def getJson(url):
    timeout = 0
    try:
        r = requests.get(url, headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        datas = json.loads(r.text)
        time.sleep(timeout)
        timeout = 0
        return datas
    except:
        print("error: getJson===>"+str(timeout))
        timeout += 1
        getJson(url)

def postJson(url, body,timeout=0):
    try:
        r = requests.post(url, data=body, headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        })

        datas = json.loads(r.text)
        time.sleep(timeout)
        timeout = 0
        return datas
    except:
        timeout += 1
        print("error: postJson===>"+str(timeout))
        getJson(url, timeout)
    