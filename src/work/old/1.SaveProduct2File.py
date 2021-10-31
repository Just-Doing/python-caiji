from urllib.request import urlopen
from bs4 import BeautifulSoup
import http.client

http.client._MAXHEADERS = 1000
urls=[
	 "https://www.horizondiscovery.com/cell-lines/all-products/explore-by-your-research-area/epigenetics",
	 "https://www.horizondiscovery.com/cell-lines/all-products/explore-by-your-research-area/deubiquitinating-enzymes",
	 "https://www.horizondiscovery.com/cell-lines/all-products/explore-by-your-research-area/dna-damage-pathway",
	 "https://www.horizondiscovery.com/cell-lines/all-products/explore-by-your-research-area/bromodomain-containing-proteins",
	 "https://www.horizondiscovery.com/cell-lines/all-products/explore-by-your-research-area/histone-acetylation"
]
# urls=[
	 # "https://www.horizondiscovery.com/cell-lines/all-products/explore-by-your-research-area/epigenetics"
 # ]
txtFile = open('D://list.txt','w')
for url in urls:
	response1 = urlopen(url)
	htmlStr = response1.read()
	scope = BeautifulSoup(htmlStr, "html.parser",from_encoding="utf-8")
	links=scope.find_all("a")
	for l in links:
		hrefstr = l["href"]
		if hrefstr.find("cat=15") > 0:
			productsurl = "https://www.horizondiscovery.com" + hrefstr
			productshtml = urlopen(productsurl).read()
			productscope = BeautifulSoup(productshtml, "html.parser", from_encoding="utf-8");
			products = productscope.find_all(name="a", attrs={"itemprop":"url"})
			lenthOfproducts = l.get_text() + "===have:" + str(len(products))+"\n"
			txtFile.write(lenthOfproducts)
			print(lenthOfproducts)
			i=0
			for product in products:
				if(len(product.get_text()) != 2):
					i=i+1
					txtFile.write(str(i)+":" + product.get_text() + "========"+product["href"]+"\n")
					print(str(i)+":" + product.get_text())
txtFile.close()
