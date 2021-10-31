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


retryCount = 0
loadCount = 0


def getHtmlFromUrl(url, type="get", para={}):
    global retryCount
    try:
        url = urllib.parse.quote(
            url, safe=string.printable
        ).replace(' ', '%20')
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36"
        }

        request_obj = urllib.request.Request(url=url, headers=headers)
        response_obj = urllib.request.urlopen(request_obj)
        html_code = response_obj.read()
        sope = BeautifulSoup(html_code, "html.parser", from_encoding="utf-8")
        return sope
    except:
        retryCount += 1
        print(retryCount)
        if retryCount < 5:
            getHtmlFromUrl(url)


def getRenderdHtmlFromUrl(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("window-size=1024,768")

    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(chrome_options=chrome_options)

    browser.get(url)
    return browser.page_source


def getProductList(url, body):
    r = requests.post(url, data=body, headers={
        'Content-Type': 'application/x-www-form-urlencoded'
    })

    datas = json.loads(r.text)
    return datas
