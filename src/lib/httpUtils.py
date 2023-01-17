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
    chrome_options.add_argument("cookie=GUID=31567ed4-9619-4bcd-bfe7-24de624cf13e|NULL|1668438432655; accessToken=0496fa71-642e-11ed-840a-0f4440cb7236; rxVisitor=1668438432244QPKL9SEEV80AABS78UE5RGQBEE7I5RRF; _vwo_uuid_v2=DB6F3A6813F6CA54C20A2A34F266CA909|907bb526d729b797ea98b47c3a75406c; _vwo_uuid=DB6F3A6813F6CA54C20A2A34F266CA909; OptanonAlertBoxClosed=2022-11-14T15:08:01.608Z; _gcl_au=1.1.2131336344.1668438482; fs_cid=1.0; _fbp=fb.1.1668438484086.844217155; mdLogger=false; kampyle_userid=05e8-a1de-7b3c-0f42-60ed-a8b8-502c-42b6; _gid=GA1.2.545605824.1668518820; DECLINED_DATE=1668519042899; dtCookie=v_4_srv_14_sn_7EBA131D02380B4F537E501F21E4317A_perc_88744_ol_0_mul_1_app-3A49e38e2e60c8cd4b_1; akaalb_origin-alb=~op=origin_upc:NASA|~rv=35~m=NASA:0|~os=a22342633dc1bd552d693ae0b80a3fbd~id=7636dcf81f285d8715804d5308b7c8c9; _vis_opt_s=3%7C; _vis_opt_test_cookie=1; _vwo_ds=3%3At_0%2Ca_0%3A0%241668518826%3A45.55330664%3A%3A37_0%3A8_0%3A1; ln_or=d; fs_uid=#15R99F#6265955296235520:4996993164398592:::#/1700054820; JabmoSP0ses.5e8a=*; language=en; country=US; isMarketplaceCatalogEnabled=true; _vis_opt_exp_146_combi=2; _vis_opt_exp_149_combi=2; _vis_opt_exp_150_combi=2; _vis_opt_exp_151_combi=2; _vis_opt_exp_152_combi=2; _vis_opt_exp_153_combi=2; _vis_opt_exp_154_combi=2; _vis_opt_exp_207_combi=2; _vis_opt_exp_208_combi=2; _vis_opt_exp_105_combi=2; _vis_opt_exp_155_combi=1; _vis_opt_exp_155_goal_1=1; _vis_opt_exp_105_goal_1=1; BVBRANDID=1a94ade3-1282-4c11-99b9-b19e3a62ec26; BVImplmain_site=15557; kampylePageLoadedTimestamp=1668602431690; ak_bmsc=8A80E0C02F6F3932869599009F6A53BB~000000000000000000000000000000~YAAQJgMkF1JGaWSEAQAAvwC2gBGk05QPHAF9LbuFcIql4oRI96caCVj/IHvSpLz+C96b9zdk+MHJ8zugVtzRkm2L6obCDM9lOS+7Fzl/wuBSuUvNbcRNzdQN0u5YeEWqFoahzBTDlf7U5coizA5GfexLXUvrRdI6d/ZSHnNzDJvW9TdCVBdhEvpcGvWD97fWW4wbb4oRdSodktAUPYcGakiQcLMVyL8mwrmoX8AMsZn4boW2q5IwoA2BQcLq05gIgcgXc9CUartVxBgd52l0uLC2glw+S1xuRfmaGhTmFBvql1iNT1eU5t6k8BPU/xQOghIwyL9IEpQkQE1YWpZhwwsBTWYAjsp/VETxtVarlU4lIEkUAogyNcVpgKxD5rCvaY3G1GAHhUax0Fj9o506wmJXtpwCkEG6pvqAT/OFntHF2BB18xi6FuQzbZfFtreaRB5zeIDuQuLDSXQuQp7sSPTEFN8TwOUknshwoJu36fOghBXGmApRCOcF4VwaJ+jVh7FoIIiZxxhlo7h8yEaeUltXFww+Q6K6hxDLdEzFD9vNoEwAGWC+6fUAaexqIfe0pkMpQ4Ov; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Nov+16+2022+21%3A52%3A03+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.32.0&geolocation=US%3BWA&isIABGlobal=false&hosts=&consentId=a542011c-3dcc-41b8-92e2-b3fffb7687b9&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false; _vwo_sn=82391%3A24%3A%3A%3A1; BVBRANDSID=bdb4592b-ca46-4073-9ee0-4d492d7dcc00; _gat_UA-51006100-1=1; _dc_gtm_UA-51006100-1=1; _ga_BQZS3WQYGJ=GS1.1.1668601222.2.1.1668606727.60.0.0; _uetsid=f1d58fc064e811edba67b14d09c6da5c; _uetvid=f1d59df064e811ed9fa14d4d31403213; _ga=GA1.2.1513262916.1668518716; JabmoSP0id.5e8a=4915cadd-cda9-4d31-9440-b5f75c725c96.1668518857.2.1668606731.1668520845.edca989b-2e1d-44d3-b94f-1c49173b9396.b585bc37-84dd-4209-bca1-8847b381cbac.c979f179-55b4-4061-9509-d6a4861631ea.1668601223968.162; rxvt=1668608534358|1668601215790; dtPC=14$6722312_640h-vBNDCABCTNPJAPMKPDFIANMGLBFGNLQNR-0e0; kampyleUserSession=1668606735612; kampyleUserSessionsCount=12; kampyleSessionPageCounter=1; kampyleUserPercentile=29.94383814780539; dtLatC=1; bm_sv=C3A9F50FEC56320FF6B53B5B9FEDF403~YAAQBwMkF1AiM3aEAQAA20C2gBGU5g4WB5Qbh5QW8kYjrBiAiz0okmTtQ2bRWetWhPi/gqv3mZHSQfAzOQKJd+DPLsvBThMNNwpsv964dblRdToNriDBYjTdaoi2Kqu1Dd6BAn9sueVwGh95yTB2KEL749nPoGqditKNVX0Ego81HIQ0fA4bHmFpaLtcGqC+DKqwLeH218U5XX99kqEMajRWNHv5F6h7mbmpiausxwz/lLy395E/H9FrzS8YnZD1LPdfBaZNfOE=~1")

    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(chrome_options=chrome_options)

    browser.get(url)
    return BeautifulSoup(browser.page_source, "html.parser", from_encoding="utf-8")


def getProductList(url, body):
    r = requests.post(url, data=body, headers={
        'Content-Type': 'application/x-www-form-urlencoded'
    })

    datas = json.loads(r.text)
    return datas
