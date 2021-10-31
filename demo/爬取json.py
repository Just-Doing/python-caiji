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


def urllib_download(IMAGE_URL, pName):
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(
            IMAGE_URL, pName.replace("/", "").replace("\\", ""))
    except:
        print('no')


def getProductInfo(url, products):
    print(url)


def getProductList(aq, q, startIndex, products):
    url = "https://www.atcc.org/coveo/rest/v2/?sitecoreItemUri=sitecore%3A%2F%2Fliveweb%2F%7BF6F5050D-7B79-4599-B4A5-91361DAD7759%7D%3Flang%3Den%26ver%3D1&siteName=ATCC"
    d = {
        'aq': aq,
        'retrieveFirstSentences': 'true',
        'timezone': 'Asia/Shanghai',
        'disableQuerySyntax': 'false',
        'enableDuplicateFiltering': 'false',
        'enableCollaborativeRating': 'false',
        'debug': 'false',
        'context': '{}',
        'cq': '((@fz95xlanguage14674=="en" @fz95xlatestversion14674=="1") OR @syssource==("ATCC-PROD"))',
        'searchHub': 'search',
        'language': 'en',
        'pipeline': 'ATCC',
        'firstResult': startIndex,
        'numberOfResults': '100',
        'excerptLength': '200',
        'enableDidYouMean': 'true',
        'sortCriteria': 'relevancy',
        'queryFunctions': '[]',
        'rankingFunctions': '[]',
        'q': q
    }

    r = requests.post(url, data=d, headers={
                        'Content-Type': 'application/x-www-form-urlencoded'
                      })
                      
    datas = json.loads(r.text)
    for data in datas["results"]:
        getProductInfo(data["uri"], products)
