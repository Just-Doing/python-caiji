from itertools import product
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
import re
sys.path.append('../..')
from lib import excelUtils
from lib import httpUtils
from lib import textUtil
from lib.htmlEleUtils import getNodeText
from lib.htmlEleUtils import getInnerHtml
products1 = []
products2 = []
products3 = []
products4 = []
products5 = []
products6 = []
products7 = []
products8 = []
products9 = []
products10 = []
products11 = []

headers1=['link', 'Product type1','Product type2','Product Name','size','price']
headers2=['link', 'Product type1','Product type2','Product Name','size','price']
headers3=['link', 'Product type1','Product type2','Product Name','size','price']
headers4=['link', 'Product type1','Product type2','Product Name','size','price']
headers5=['link', 'Product type1','Product type2','Product Name','size','price']
headers6=['link', 'Product type1','Product type2','Product Name','size','price']
headers7=['link', 'Product type1','Product type2','Product Name','size','price']
headers8=['link', 'Product type1','Product type2','Product Name','size','price']
headers9=['link', 'Product type1','Product type2','Product Name','size','price']
headers10=['link', 'Product type1','Product type2','Product Name','size','price']
headers11=['link', 'Product type1','Product type2','Product Name','size','price']


def addHeader(header, title):
  if title not in header and len(title) > 0:
    header.append(title)


def getProductInfo(url, type1, type2, typeIndex):
	print(typeIndex)
	if typeIndex ==0:
		print(str(len(products1)) + "=1==" + url)
	if typeIndex ==1:
		print(str(len(products2)) + "=2==" + url)
	if typeIndex ==2:
		print(str(len(products3)) + "=3==" + url)
	if typeIndex ==3:
		print(str(len(products4)) + "=4==" + url)
	if typeIndex ==4:
		print(str(len(products5)) + "=5==" + url)
	if typeIndex ==5:
		print(str(len(products6)) + "=6==" + url)
	if typeIndex ==6:
		print(str(len(products7)) + "=7==" + url)
	if typeIndex ==7:
		print(str(len(products8)) + "=8==" + url)
	if typeIndex ==8:
		print(str(len(products9)) + "=9==" + url)
	if typeIndex ==9:
		print(str(len(products10)) + "=10==" + url)
	if typeIndex ==10:
		print(str(len(products11)) + "=11==" + url)

	sope = httpUtils.getHtmlFromUrl(url)
	pNameArea = sope.find("div", attrs={"class":"IndividualProductContent"})
	pName = getNodeText(pNameArea.find("h1"))
	nameParts = pName.split(" ")

	pInfo = {
		"link": url,
		"Product type1": type1,
		"Product type2": type2,
		"Product Name": pName,
		"size": nameParts[0]+nameParts[1],
		"price": getNodeText(sope.find("span", attrs={"itemprop":"price"})),
	}
	specArea = sope.find("div", attrs={"class":"DescriptionTable"})
	strongs = specArea.find_all("strong")
	for strong in strongs:
		title = getNodeText(strong)
		value = ""
		if str(type(strong.nextSibling))=="<class 'bs4.element.Tag'>":
			value = getNodeText(strong.nextSibling)
		else:
			value = strong.nextSibling
		if value==None:
			value=""
		if ":" in title or "：" in title or ":" in value or "：" in value:
			pInfo[title] = value
			if typeIndex ==0:
				addHeader(headers1, title)
			if typeIndex ==1:
				addHeader(headers2, title)
			if typeIndex ==2:
				addHeader(headers3, title)
			if typeIndex ==3:
				addHeader(headers4, title)
			if typeIndex ==4:
				addHeader(headers5, title)
			if typeIndex ==5:
				addHeader(headers6, title)
			if typeIndex ==6:
				addHeader(headers7, title)
			if typeIndex ==7:
				addHeader(headers8, title)
			if typeIndex ==8:
				addHeader(headers9, title)
			if typeIndex ==9:
				addHeader(headers10, title)
			if typeIndex ==10:
				addHeader(headers11, title)

	if typeIndex ==0:
		products1.append(pInfo.copy())
	if typeIndex ==1:
		products2.append(pInfo.copy())
	if typeIndex ==2:
		products3.append(pInfo.copy())
	if typeIndex ==3:
		products4.append(pInfo.copy())
	if typeIndex ==4:
		products5.append(pInfo.copy())
	if typeIndex ==5:
		products6.append(pInfo.copy())
	if typeIndex ==6:
		products7.append(pInfo.copy())
	if typeIndex ==7:
		products8.append(pInfo.copy())
	if typeIndex ==8:
		products9.append(pInfo.copy())
	if typeIndex ==9:
		products10.append(pInfo.copy())
	if typeIndex ==10:
		products11.append(pInfo.copy())

def getStr(size):
	return getNodeText(size).replace(".","").replace(" ","").replace(",","")



def getProductList(url, type1, type2, typeIndex):
	sope = httpUtils.getHtmlFromUrl(url)

	ps = sope.find_all("div", attrs={"class":"SubCategoryViewSection"})
	for p in ps:
		pLink = p.find("a")
		getProductInfo("https://www.newdirections.com.au/epages/newdirections.sf/en_AU/"+pLink["href"], type1, type2, typeIndex)
		
		

def getProductType3(url, type1, type2, typeIndex):
	sope = httpUtils.getHtmlFromUrl(url)

	ps = sope.find_all("div", attrs={"class":"SubCategoryViewSection"})
	for p in ps:
			sizeOpt = p.find("select", attrs={"name":"ChangeObjectID"})
			pLink = p.find("a")
			if sizeOpt == None: #产品列表
				getProductInfo("https://www.newdirections.com.au/epages/newdirections.sf/en_AU/"+pLink["href"], type1, type2, typeIndex)
			else: #产品类型
				getProductList("https://www.newdirections.com.au/epages/newdirections.sf/en_AU/"+pLink["href"], type1, type2, typeIndex)

type1s=[]
def getProductType():
	htmlStr='<ul style="display: none;">  <li class="Category-10182066">  <a href="?ObjectPath=/Shops/newdirections/Categories/25">Anti-Bacterial &amp; Sanitisers  <span>›</span></a>  <ul style="display: none;">  <li class="Category-9687249">  <a href="?ObjectPath=/Shops/newdirections/Categories/25/102153">Ethanol Hand Sanitiser 80%  </a>  </li>  <li class="Category-9423741">  <a href="?ObjectPath=/Shops/newdirections/Categories/25/102115">Anti-Bacterial Hand &amp; Surface Sanitiser Alcohol Free  </a>  </li>  <li class="Category-9551388">  <a href="?ObjectPath=/Shops/newdirections/Categories/25/102128">Anti-Bacterial Foaming Hand Wash  </a>  </li>  <li class="Category-9136392">  <a href="?ObjectPath=/Shops/newdirections/Categories/25/102093">Anti-Bacterial Hand Gel 70% Ethanol - Colourless  </a>  </li>  <li class="Category-9521463">  <a href="?ObjectPath=/Shops/newdirections/Categories/25/102127">Anti-Bacterial Sanitiser Unscented 70% Ethanol  </a>  </li>  <li class="Category-9152200">  <a href="?ObjectPath=/Shops/newdirections/Categories/25/102104">Anti-Bacterial Sanitising Spray 70% Ethanol  </a>  </li>  </ul>  </li>  <li class="Category-36511">  <a href="?ObjectPath=/Shops/newdirections/Categories/10">Botanical Hair &amp; Skincare  <span>›</span></a>  <ul style="display: none;">  <li class="Category-3075816">  <a href="?ObjectPath=/Shops/newdirections/Categories/10/101270">Australian Lavender Skincare Range  </a>  </li>  <li class="Category-36512">  <a href="?ObjectPath=/Shops/newdirections/Categories/10/189">Australian Native Botanical Skincare   </a>  </li>  <li class="Category-36534">  <a href="?ObjectPath=/Shops/newdirections/Categories/10/100">Body, Hands &amp; Feet  </a>  </li>  <li class="Category-10718112">  <a href="?ObjectPath=/Shops/newdirections/Categories/10/102224">Clinic Range  </a>  </li>  <li class="Category-36642">  <a href="?ObjectPath=/Shops/newdirections/Categories/10/105">Cosmeceuticals  </a>  </li>  <li class="Category-11744557">  <a href="?ObjectPath=/Shops/newdirections/Categories/10/102356">COSMOS Natural Skincare  </a>  </li>  <li class="Category-3035475">  <a href="?ObjectPath=/Shops/newdirections/Categories/10/101235">Dragons Blood Skincare Range  </a>  </li>  <li class="Category-36654">  <a href="?ObjectPath=/Shops/newdirections/Categories/10/101">Face Skincare  </a>  </li>  <li class="Category-39697">  <a href="?ObjectPath=/Shops/newdirections/Categories/10/112">Floral Water Combinations  </a>  </li>  <li class="Category-39654">  <a href="?ObjectPath=/Shops/newdirections/Categories/10/128">Floral Waters  </a>  </li>  <li class="Category-36709">  <a href="?ObjectPath=/Shops/newdirections/Categories/10/102">Hair Care  </a>  </li>  <li class="Category-36755">  <a href="?ObjectPath=/Shops/newdirections/Categories/10/104">Mens Care  </a>  </li>  <li class="Category-6022302">  <a href="?ObjectPath=/Shops/newdirections/Categories/10/101760">Mum &amp; Bub Skincare Range  </a>  </li>  <li class="Category-2171732">  <a href="?ObjectPath=/Shops/newdirections/Categories/10/101048">Rose Range Skincare  </a>  </li>  <li class="Category-36777">   <a href="?ObjectPath=/Shops/newdirections/Categories/10/187">Salon &amp; Spa Range  </a>  </li>  <li class="Category-36810">  <a href="?ObjectPath=/Shops/newdirections/Categories/10/206">Ultra Gentle Range  </a>  </li>  <li class="Category-5614622">  <a href="?ObjectPath=/Shops/newdirections/Categories/10/101716">Urban Lifestyle Range  </a>  </li>  <li class="Category-12157616">  <a href="?ObjectPath=/Shops/newdirections/Categories/10/102405">Youth Clean &amp; Clear Skincare Range  </a>  </li>  </ul>  </li>  <li class="Category-36818">  <a href="?ObjectPath=/Shops/newdirections/Categories/12">Essential &amp; Other Oils  <span>›</span></a>  <ul style="display: none;">  <li class="Category-36925">  <a href="?ObjectPath=/Shops/newdirections/Categories/12/119">Essential Oils  </a>  </li>  <li class="Category-8601118">  <a href="?ObjectPath=/Shops/newdirections/Categories/12/102042">Microencapsulated Essential Oils  </a>  </li>  <li class="Category-37359">  <a href="?ObjectPath=/Shops/newdirections/Categories/12/123">Vegetable, Carrier, Emollients &amp; other Oils  </a>  </li>  <li class="Category-36819">  <a href="?ObjectPath=/Shops/newdirections/Categories/12/115">Absolutes  </a>  </li>  <li class="Category-37329">  <a href="?ObjectPath=/Shops/newdirections/Categories/12/122">Precious Oil Dilutions  </a>  </li>  <li class="Category-36915">  <a href="?ObjectPath=/Shops/newdirections/Categories/12/118">Essential Oil Blends  </a>  </li>  <li class="Category-36850">  <a href="?ObjectPath=/Shops/newdirections/Categories/12/116">Ayurvedic Oils &amp; Other Extracts  </a>  </li>  <li class="Category-36870">  <a href="?ObjectPath=/Shops/newdirections/Categories/12/211">Essential &amp; Vegetable Oils - CO2 Extracted  </a>  </li>  <li class="Category-37202">  <a href="?ObjectPath=/Shops/newdirections/Categories/12/120">Fragrant Oils  </a>  </li>  <li class="Category-4507381">  <a href="?ObjectPath=/Shops/newdirections/Categories/12/101561">Fragrant Oils - Naturally Derived  </a>  </li>  <li class="Category-37306">  <a href="?ObjectPath=/Shops/newdirections/Categories/12/121">Infused / Macerated Oils  </a>  </li>  <li class="Category-36899">  <a href="?ObjectPath=/Shops/newdirections/Categories/12/117">Massage Blends  </a>  </li>  <li class="Category-37317">  <a href="?ObjectPath=/Shops/newdirections/Categories/12/165">Oleoresins &amp; Resins  </a>  </li>  <li class="Category-37430">  <a href="?ObjectPath=/Shops/newdirections/Categories/12/124">Water Dispersible Massage Bases  </a>  </li>  <li class="Category-14305272">  <a href="https://www.newdirections.com.au/epages/newdirections.sf/en_AU/?ObjectPath=/Shops/newdirections/Categories/11/107">Certified Organic Essential Oils - ACO 10282P </a>  </li>  <li class="Category-14305273">  <a href="https://www.newdirections.com.au/epages/newdirections.sf/en_AU/?ObjectPath=/Shops/newdirections/Categories/11/106">Certified Organic Oil Blends </a>  </li>  </ul>  </li>  <li class="Category-37437">  <a href="?ObjectPath=/Shops/newdirections/Categories/14">Herbs and Extracts  <span>›</span></a>  <ul style="display: none;">  <li class="Category-7812956">  <a href="?ObjectPath=/Shops/newdirections/Categories/14/101955">Australian Native Extracts  </a>  </li>  <li class="Category-37438">  <a href="?ObjectPath=/Shops/newdirections/Categories/14/137">Dried Herbs   </a>  </li>  <li class="Category-37503">  <a href="?ObjectPath=/Shops/newdirections/Categories/14/134">Fruit &amp; Herbal Powder Extracts  </a>  </li>  <li class="Category-999065">  <a href="?ObjectPath=/Shops/newdirections/Categories/14/100664">Liquid Extracts - Glycerine Based  </a>  </li>  <li class="Category-998774">  <a href="?ObjectPath=/Shops/newdirections/Categories/14/100663">Liquid Extracts - Oil Based  </a>  </li>  <li class="Category-1009411">  <a href="?ObjectPath=/Shops/newdirections/Categories/14/100666">Liquid Extracts - Water Based  </a>  </li>  </ul>  </li>  <li class="Category-37640">  <a href="?ObjectPath=/Shops/newdirections/Categories/20">Makeup, Mineral Makeup &amp; Accessories  <span>›</span></a>  <ul style="display: none;">  <li class="Category-37642">  <a href="?ObjectPath=/Shops/newdirections/Categories/20/209">Brushes  </a>  </li>  <li class="Category-37655">  <a href="?ObjectPath=/Shops/newdirections/Categories/20/198">Makeup Products  </a>  </li>  <li class="Category-10526153">  <a href="?ObjectPath=/Shops/newdirections/Categories/20/102208">Mask Applicators  </a>  </li>  </ul>  </li>  <li class="Category-37772">  <a href="?ObjectPath=/Shops/newdirections/Categories/11">Organic Products  <span>›</span></a>  <ul style="display: none;">  <li class="Category-37773">  <a href="?ObjectPath=/Shops/newdirections/Categories/11/100611">Made with Organic Botanical Skincare - OFC 0515  </a>  </li>  <li class="Category-3220964">  <a href="?ObjectPath=/Shops/newdirections/Categories/11/101292">Made With Organic Skincare - COSMOS  </a>  </li>  <li class="Category-37783">  <a href="?ObjectPath=/Shops/newdirections/Categories/11/1029">Certified Organic Precious Oil Dilutions  </a>   </li>  <li class="Category-37797">  <a href="?ObjectPath=/Shops/newdirections/Categories/11/106">Certified Organic Oil Blends  </a>  </li>  <li class="Category-827340">  <a href="?ObjectPath=/Shops/newdirections/Categories/11/100647">Certified Organic CO2 Oils - ACO 10282P  </a>  </li>  <li class="Category-37832">  <a href="?ObjectPath=/Shops/newdirections/Categories/11/183">Certified Organic Dried Herbs - ACO 10282P  </a>  </li>  <li class="Category-37844">  <a href="?ObjectPath=/Shops/newdirections/Categories/11/107">Certified Organic Essential Oils - ACO 10282P  </a>  </li>  <li class="Category-11079871">  <a href="?ObjectPath=/Shops/newdirections/Categories/11/102246">COSMOS Approved Raw Materials  </a>  </li>  <li class="Category-37948">  <a href="?ObjectPath=/Shops/newdirections/Categories/11/181">Organic Floral Waters  </a>  </li>  <li class="Category-37953">  <a href="?ObjectPath=/Shops/newdirections/Categories/11/190">Certified Organic Infused / Macerated Oils  </a>  </li>  <li class="Category-1218760">  <a href="?ObjectPath=/Shops/newdirections/Categories/11/100678">Certified Organic Liquid Extracts  </a>  </li>  <li class="Category-37964">  <a href="?ObjectPath=/Shops/newdirections/Categories/11/108">Certified Organic Raw Materials - ACO 10282P  </a>  </li>  <li class="Category-37979">  <a href="?ObjectPath=/Shops/newdirections/Categories/11/109">Certified Organic Skincare Products  </a>  </li>  <li class="Category-37992">  <a href="?ObjectPath=/Shops/newdirections/Categories/11/110">Certified Organic Vegetable &amp; Carrier Oils  </a>  </li>  </ul>  </li>  <li class="Category-38018">  <a href="?ObjectPath=/Shops/newdirections/Categories/15">Pet Care &amp; Household Products  <span>›</span></a>  <ul style="display: none;">  <li class="Category-38025">  <a href="?ObjectPath=/Shops/newdirections/Categories/15/200">Household Products  </a>  </li>  <li class="Category-38019">  <a href="?ObjectPath=/Shops/newdirections/Categories/15/139">Pet Care  </a>  </li>  </ul>  </li>  <li class="Category-38031">  <a href="?ObjectPath=/Shops/newdirections/Categories/16">Packaging  <span>›</span></a>  <ul style="display: none;">  <li class="Category-38032">  <a href="?ObjectPath=/Shops/newdirections/Categories/16/140">Accessories  </a>  </li>  <li class="Category-38063">  <a href="?ObjectPath=/Shops/newdirections/Categories/16/182">Bags, Boxes &amp; Wrapping Solutions  </a>  </li>  <li class="Category-38432">  <a href="?ObjectPath=/Shops/newdirections/Categories/16/141">Bottles  </a>  </li>  <li class="Category-38685">  <a href="?ObjectPath=/Shops/newdirections/Categories/16/142">Caps  </a>  </li>  <li class="Category-38785">  <a href="?ObjectPath=/Shops/newdirections/Categories/16/143">Cosmetic Bags  </a>  </li>  <li class="Category-38814">  <a href="?ObjectPath=/Shops/newdirections/Categories/16/144">Dispensing Systems  </a>  </li>  <li class="Category-4389469">  <a href="?ObjectPath=/Shops/newdirections/Categories/16/101537">Face Masks with Pouches  </a>  </li>  <li class="Category-38872">  <a href="?ObjectPath=/Shops/newdirections/Categories/16/145">Jars  </a>  </li>  <li class="Category-38967">  <a href="?ObjectPath=/Shops/newdirections/Categories/16/204">Makeup Packaging  </a>  </li>  <li class="Category-38973">  <a href="?ObjectPath=/Shops/newdirections/Categories/16/146">Measuring &amp; Laboratory Apparatus  </a>    </li>  <li class="Category-39003">  <a href="?ObjectPath=/Shops/newdirections/Categories/16/147">Metal Containers  </a>  </li>  <li class="Category-39039">  <a href="?ObjectPath=/Shops/newdirections/Categories/16/148">Plastic Bulk Containers  </a>  </li>  <li class="Category-3402863">  <a href="?ObjectPath=/Shops/newdirections/Categories/16/101310">Zip Lock Bags  </a>  </li>  <li class="Category-1646556">  <a href="?ObjectPath=/Shops/newdirections/Categories/16/100871">Tubes  </a>  </li>  </ul>  </li>  <li class="Category-39065">  <a href="?ObjectPath=/Shops/newdirections/Categories/17">Raw Materials &amp; Cosmetic Ingredients  <span>›</span></a>  <ul style="display: none;">  <li class="Category-4594695">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/101568">Raw Material Kits  </a>  </li>  <li class="Category-39066">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/149">Acids  </a>  </li>  <li class="Category-39071">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/150">Active Ingredients  </a>  </li>  <li class="Category-39106">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/151">Alkalis  </a>  </li>  <li class="Category-39110">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/203">Amino Acids  </a>  </li>  <li class="Category-39118">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/152">Anionic Surfactants &amp; Shampoo Bases  </a>  </li>  <li class="Category-39127">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/180">Anti-dandruff  </a>  </li>  <li class="Category-39129">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/153">Antioxidants  </a>  </li>  <li class="Category-39133">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/154">Butters  </a>  </li>  <li class="Category-39155">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/155">Cationic Surfactants &amp; Hair Conditioner Bases  </a>  </li>  <li class="Category-39163">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/156">Clays  </a>  </li>  <li class="Category-39183">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/157">Colours  </a>  </li>  <li class="Category-39282">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/158">Emollients  </a>  </li>  <li class="Category-39304">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/159">Exfoliants  </a>  </li>  <li class="Category-39351">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/207">Hair Care  </a>  </li>  <li class="Category-39355">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/162">Humectants  </a>  </li>  <li class="Category-39360">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/202">Minerals  </a>  </li>  <li class="Category-39369">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/163">Mud &amp; Volcanic Ash  </a>  </li>  <li class="Category-39372">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/164">Nonionic Surfactants &amp; Foam Stabilisers  </a>  </li>  <li class="Category-39383">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/168">Preservatives  </a>  </li>  <li class="Category-39400">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/169">Proteins   </a>  </li>  <li class="Category-39407">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/170">Resinoids, Gums &amp; Crystals  </a>  </li>  <li class="Category-39423">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/171">Salts  </a>  </li>  <li class="Category-39436">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/173">Solubilisers &amp; Emulsifiers  </a>  </li>  <li class="Category-39447">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/174">Solvents  </a>  </li>  <li class="Category-39455">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/175">Sunscreen  </a>  </li>  <li class="Category-39462">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/176">Thickeners  </a>  </li>  <li class="Category-39482">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/178">Vitamins  </a>  </li>  <li class="Category-39494">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/179">Waxes  </a>  </li>  <li class="Category-1386700">  <a href="?ObjectPath=/Shops/newdirections/Categories/17/100726">Other Raw Materials &amp; Cosmetic Ingredients  </a>  </li>  </ul>  </li>  <li class="Category-4421544">  <a href="?ObjectPath=/Shops/newdirections/Categories/19">Beauty Booster Supplements  <span>›</span></a>  <ul style="display: none;">  <li class="Category-13551327">  <a href="?ObjectPath=/Shops/newdirections/Categories/19/102492">Beauty Boosters: Starter Set  </a>  </li>  <li class="Category-13551438">  <a href="?ObjectPath=/Shops/newdirections/Categories/19/102491">Beauty Boosters: Complete Collection  </a>  </li>  <li class="Category-13519047">  <a href="?ObjectPath=/Shops/newdirections/Categories/19/102489">Beauty Boosters™ Collagen C 30s - AUST L 275242  </a>  </li>  <li class="Category-4421545">  <a href="?ObjectPath=/Shops/newdirections/Categories/19/101544">Beauty Boosters™ Collagen C 60s - AUST L 275242  </a>  </li>  <li class="Category-13517093">  <a href="?ObjectPath=/Shops/newdirections/Categories/19/Beauty_Boosters_8482__Complexion_Perfection_60s__AUST_L_275246">Beauty Boosters™ Complexion Perfection 60s - AUST L 275246  </a>  </li>  <li class="Category-4421554">  <a href="?ObjectPath=/Shops/newdirections/Categories/19/101545">Beauty Boosters™ Complexion Perfection 120s - AUST L 275246  </a>  </li>  <li class="Category-13519105">  <a href="?ObjectPath=/Shops/newdirections/Categories/19/102490">Beauty Boosters™ Glow Getter 30s - AUST L 303994  </a>  </li>  <li class="Category-4421555">  <a href="?ObjectPath=/Shops/newdirections/Categories/19/101546">Beauty Boosters™ Glow Getter 60s - AUST L 303994  </a>  </li>  <li class="Category-13551380">  <a href="?ObjectPath=/Shops/newdirections/Categories/19/102493">Beauty Boosters: Restorative Overnight Mask  </a>  </li>  <li class="Category-13551415">  <a href="?ObjectPath=/Shops/newdirections/Categories/19/102494">Beauty Boosters: Intensive Regeneration Mask  </a>  </li>  </ul>  </li>  <li class="Category-39522">  <a href="?ObjectPath=/Shops/newdirections/Categories/13">Wellbeing  <span>›</span></a>  <ul style="display: none;">  <li class="Category-39523">  <a href="?ObjectPath=/Shops/newdirections/Categories/13/125">Aromatherapy Accessories  </a>  </li>  <li class="Category-39534">  <a href="?ObjectPath=/Shops/newdirections/Categories/13/126">Books  </a>  </li>  <li class="Category-39590">  <a href="?ObjectPath=/Shops/newdirections/Categories/13/127">Candles  </a>  </li>  <li class="Category-39770">  <a href="?ObjectPath=/Shops/newdirections/Categories/13/131">Incense  </a>  </li>  <li class="Category-39785">  <a href="?ObjectPath=/Shops/newdirections/Categories/13/133">Soap Making  </a>  </li>  </ul>  </li>  </ul>'
	sope = BeautifulSoup(htmlStr,  "html.parser", from_encoding="utf-8").find("ul")
	ps = sope.find_all("li", recursive=False)
	for inx, p in enumerate(ps):
		pLink = p.find("a")
		type1 = getNodeText(pLink)
		type1s.append(type1)
		if pLink != None and inx>=5:
			type2s = p.find_all("li")
			for type2 in type2s:
				pLink = type2.find("a")
				type2Str = getNodeText(pLink);
				# print(type1+"==="+type2Str)
				getProductType3("https://www.newdirections.com.au/epages/newdirections.sf/en_AU/"+pLink["href"], type1, type2Str, inx)

# getProductInfo('https://www.newdirections.com.au/epages/newdirections.sf/en_AU/?ObjectPath=/Shops/newdirections/Products/OCBSB100BODYLOTI','', '',1)

getProductType()




excelUtils.generateExcelMultipleSheet('newdirections2.xlsx', [
	{
		"name": type1s[0],
		"header": headers1 ,
		"data": products1
	},{
		"name": type1s[1],
		"header": headers2 ,
		"data": products2
	},{
		"name": type1s[2],
		"header": headers3 ,
		"data": products3
	},{
		"name": type1s[3],
		"header": headers4 ,
		"data": products4
	},{
		"name": type1s[4],
		"header": headers5 ,
		"data": products5
	},{
		"name": type1s[5],
		"header": headers6 ,
		"data": products6
	},{
		"name": type1s[6],
		"header": headers7 ,
		"data": products7
	},{
		"name": type1s[7],
		"header": headers8 ,
		"data": products8
	},{
		"name": type1s[8],
		"header": headers9 ,
		"data": products9
	},{
		"name": type1s[9],
		"header": headers10 ,
		"data": products10
	},{
		"name": type1s[10],
		"header": headers11 ,
		"data": products11
	}
])