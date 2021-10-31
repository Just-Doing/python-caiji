from urllib.request import urlopen
from bs4 import BeautifulSoup
import http.client

def getHtmlFromUrl(url):
	try:
		html = urlopen(url).read()
		return html
	except Exception:
		print(Exception)
		print("重试"+url)
		getHtmlFromUrl(url)

http.client._MAXHEADERS = 1000
urls=[
	 "https://www.biolegend.com/en-us/products/alexa-fluor-647-anti-human-tigit-vstm3-antibody-14755",
"https://www.biolegend.com/en-us/products/apc-anti-human-tigit-vstm3-antibody-13758",
"https://www.biolegend.com/en-us/products/apc-fire-750-anti-human-tigit-vstm3-antibody-13740",
"https://www.biolegend.com/en-us/products/biotin-anti-human-tigit-vstm3-antibody-14558",
"https://www.biolegend.com/en-us/products/brilliant-violet-421-anti-human-tigit-vstm3-antibody-13935",
"https://www.biolegend.com/en-us/products/brilliant-violet-605-anti-human-tigit-vstm3-antibody-13936",
"https://www.biolegend.com/en-us/products/pe-anti-human-tigit-vstm3-antibody-13796",
"https://www.biolegend.com/en-us/products/pe-cy7-anti-human-tigit-vstm3-antibody-13951",
"https://www.biolegend.com/en-us/products/pe-dazzle-594-anti-human-tigit-vstm3-antibody-13937",
"https://www.biolegend.com/en-us/products/percp-cyanine5-5-anti-human-tigit-vstm3-antibody-13948",
"https://www.biolegend.com/en-us/products/purified-anti-human-tigit-vstm3-antibody-13739",
"https://www.biolegend.com/en-us/products/totalseq-a0089-anti-human-tigit-antibody-15773",
"https://www.biolegend.com/en-us/products/totalseq-b0089-anti-human-tigit-vstm3-antibody-16855",
"https://www.biolegend.com/en-us/products/totalseq-c0089-anti-human-tigit-vstm3-antibody-16856",
"https://www.biolegend.com/en-us/products/ultra-leaf-purified-anti-human-tigit-vstm3-antibody-14287",
"https://www.biolegend.com/en-us/products/leaf-low-endotoxin--azide-freepurified-anti-human-tnf-alpha-antibody-1009",
"https://www.biolegend.com/en-us/products/purified-anti-human-tnf-alpha-antibody-1010",
"https://www.biolegend.com/en-us/products/ultra-leaf-purified-anti-human-tnf-alpha-antibody-17974",
"https://www.biolegend.com/en-us/products/apc-anti-human-mrp-14-s100a9-antibody-10079",
"https://www.biolegend.com/en-us/products/fitc-anti-human-mrp-14-s100a9-antibody-6977",
"https://www.biolegend.com/en-us/products/pe-anti-human-mrp-14-s100a9-antibody-10078"
]
txtFile = open('c://list.txt','w')
for url in urls:
	pInfoHtml = getHtmlFromUrl(url)
	pubMed=[]
	if pInfoHtml!=None and len(pInfoHtml)>0:
		pInfoSoup = BeautifulSoup(pInfoHtml,"html.parser",from_encoding="utf-8")
		
		productDetailNodes = pInfoSoup.findAll(name="dt")
		if len(productDetailNodes) > 0:
			for dNode in productDetailNodes:
				s = dNode.get_text().strip()
				if s.find("Application References")>-1:
					pubMed = dNode.findNext("dd").findAll(name="a")
	specIndex=0
	if len(pubMed) > 0:
		specCount = 0
		if len(pubMed)>5:
			specCount=5 
		else:
			specCount=len(pubMed)
		while specIndex< specCount:
			specNode=pubMed[specIndex]
			if specNode.text.lower().find("pubmed") < 0:
				txtFile.write("")
				print(specIndex)
			else :
				surl = specNode["href"] if specNode != None else ""
				txtFile.write(surl)
				specIndex=specIndex+1
				print(specIndex)
	else :
		txtFile.write("")
txtFile.close()

