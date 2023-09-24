from itertools import product
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json

sys.path.append('../../..')
from lib import excelUtils
from lib import httpUtils
from lib import textUtil
from lib.htmlEleUtils import getNodeText
from lib.htmlEleUtils import getInnerHtml
products = []
headers=['link','cas', 'name','value'
]
AcuteEffects = []
DepositorProvidedPubMedCitationsData = []
DepositorSuppliedPatentIdentifiersData = []

def addHeader(title):
  if title not in headers and len(title) > 0:
    headers.append(title)

def getProductInfo(url, cid, type):
	print(str(len(products))+ type["cas"] + url)
	productListHtml = httpUtils.getHtmlStrFromUrl(url)
	tempInfo = {
		"cas":type["cas"],
		"value":""
	}
	tempInfo["value"] += "PubChem CID" +"    "+ str(cid) +"\r\n"
	tempInfo["value"] += "Structure" +" \r\n"
	if productListHtml == None:
		time.sleep(2)
		productListHtml = httpUtils.getHtmlStrFromUrl(url)
	
	
	if productListHtml == None:
		time.sleep(2)
		productListHtml = httpUtils.getHtmlStrFromUrl(url)
	if productListHtml != None:


		data = json.loads(productListHtml.decode("utf-8", errors='ignore'))
		Section = data["Record"]["Section"]

		try:
			imgSrc="https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?cid=" + str(cid) + "&t=l"
			imgName = type["cas"].replace("/","").replace("<","").replace(">","")
			httpUtils.urllib_download(imgSrc, imgName+"2d.png")
			tempInfo["value"] += imgName+"2d.png"+"\r\n"
		except:
			tempInfo["Structures"] = ""

		try:
			img3dSrc="https://pubchem.ncbi.nlm.nih.gov/image/img3d.cgi?&cid=" + str(cid) + "&t=l"
			imgName = type["cas"].replace("/","").replace("<","").replace(">","")
			httpUtils.urllib_download(img3dSrc, imgName+"3d.png")
			tempInfo["value"] += imgName+"3d.png"+"\r\n"
		except:
			tempInfo["Structures"] = ""


		ChemicalSafetyStr = ""
		ChemicalSafety = list(filter(lambda o: o["TOCHeading"]=="Chemical Safety", Section))
		if len(ChemicalSafety):
			ChemicalSafetyInformation = ChemicalSafety[0]["Information"]
			if ChemicalSafetyInformation != None and len(ChemicalSafetyInformation):
				ChemicalSafetyInformationVal = ChemicalSafetyInformation[0]["Value"]
				if ChemicalSafetyInformationVal != None:
					if "StringWithMarkup" in ChemicalSafetyInformationVal:
						strings = ChemicalSafetyInformationVal["StringWithMarkup"][0]["Markup"]
						for string in strings:
							ChemicalSafetyStr += string["Extra"]+"  ,"
		tempInfo["value"] += "Chemical Safety\r\n"			
		tempInfo["value"] += ChemicalSafetyStr+"\r\n"
		ChemicalAndPhysicalProperties = list(filter(lambda o: o["TOCHeading"] == "Chemical and Physical Properties", Section))
		if len(ChemicalAndPhysicalProperties):
			ChemicalSection = ChemicalAndPhysicalProperties[0]["Section"]
			ComputedProperties = list(filter(lambda o: o["TOCHeading"] == "Computed Properties", ChemicalSection))
			if len(ComputedProperties):
				ComputedPropertiesSection = ComputedProperties[0]["Section"]
				MolecularWeight = list(filter(lambda o:["TOCHeading"] == "Molecular Weight", ComputedPropertiesSection))
				if len(MolecularWeight):
					molValue = MolecularWeight[0]["Information"][0]["Value"]
					tempInfo["value"] += "Molecular Weight"+"\r\n"
					tempInfo["value"] += molValue["StringWithMarkup"][0]["String"] + molValue["Unit"] +"\r\n"
					tempInfo["value"] += MolecularWeight[0]["Information"][0]["Reference"]

		NamesAndIdentifiers= list(filter(lambda o: o["TOCHeading"] == "Names and Identifiers", Section))
		if len(NamesAndIdentifiers):
			NamesAndIdentifiersSection = NamesAndIdentifiers[0]["Section"]
			MolecularFormula = list(filter(lambda o: o["TOCHeading"] == "Molecular Formula", NamesAndIdentifiersSection))
			if len(MolecularFormula):
					tempInfo["value"] += "Molecular Formula"+"\r\n"
					tempInfo["value"] += MolecularFormula[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]+"\r\n"

			Synonyms = list(filter(lambda o: o["TOCHeading"] == "Synonyms", NamesAndIdentifiersSection))
			if len(Synonyms):
				SynonymsSection = list(filter(lambda o: o["TOCHeading"]=="Depositor-Supplied Synonyms", Synonyms[0]["Section"]))
				if len(SynonymsSection):
					SynonymsStr = ""
					for sy in SynonymsSection[0]["Information"][0]["Value"]["StringWithMarkup"]:
						SynonymsStr += sy["String"] +"\r\n"
					tempInfo["value"] += "Synonyms"+"\r\n"
					tempInfo["value"] += SynonymsStr
			CreateDate = list(filter(lambda o: o["TOCHeading"] == "Create Date", NamesAndIdentifiersSection))
			if len(CreateDate):
				tempInfo["value"] += "Create Date"+"\r\n"
				tempInfo["value"] += CreateDate[0]["Information"][0]["Value"]["DateISO8601"][0] +"\r\n"

			ModifyDate = list(filter(lambda o: o["TOCHeading"] == "Modify Date", NamesAndIdentifiersSection))
			if len(ModifyDate):
				tempInfo["value"] += "Modify Date"+"\r\n"
				tempInfo["value"] += ModifyDate[0]["Information"][0]["Value"]["DateISO8601"][0] + "\r\n"

			RecordDescription = list(filter(lambda o: o["TOCHeading"] == "Record Description", NamesAndIdentifiersSection))
			if len(RecordDescription):
				tempInfo["value"] += "Description"+"\r\n"
				tempInfo["value"] += RecordDescription[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"] +"\r\n"
				tempInfo["value"] += (RecordDescription[0]["Information"][0]["Reference"][0] if "Reference" in RecordDescription[0]["Information"][0] else "") +"\r\n"

			tempInfo["value"] += "2 Names and Identifiers"+"\r\n"
			tempInfo["value"] += "2.1 Computed Descriptors"+"\r\n"
			
			ComputedDescriptors = list(filter(lambda o: o["TOCHeading"] == "Computed Descriptors", NamesAndIdentifiersSection))
			if len(ComputedDescriptors):
				ComputedDescriptorsSection = ComputedDescriptors[0]["Section"]
				IUPACName = list(filter(lambda o: o["TOCHeading"] =="IUPAC Name" , ComputedDescriptorsSection))
				if len(IUPACName):
					tempInfo["value"] += "2.1.1 IUPAC Name"+"\r\n"
					tempInfo["value"] += IUPACName[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"] + "\r\n"
					tempInfo["value"] += IUPACName[0]["Information"][0]["Reference"][0] + "\r\n"

				InChI = list(filter(lambda o: o["TOCHeading"] =="InChI" , ComputedDescriptorsSection))
				if len(InChI):
					tempInfo["value"] += "2.1.2 InChI"+"\r\n"
					tempInfo["value"] += InChI[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"] + "\r\n"
					tempInfo["value"] += InChI[0]["Information"][0]["Reference"][0] + "\r\n"

				InChIKey = list(filter(lambda o: o["TOCHeading"] =="InChIKey" , ComputedDescriptorsSection))
				if len(InChIKey):
					tempInfo["value"] += "2.1.3 InChIKey"+"\r\n"
					tempInfo["value"] += InChIKey[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"] + "\r\n"
					tempInfo["value"] += InChIKey[0]["Information"][0]["Reference"][0] + "\r\n"
				
				CanonicalSMILES = list(filter(lambda o: o["TOCHeading"] =="Canonical SMILES" , ComputedDescriptorsSection))
				if len(CanonicalSMILES):
					tempInfo["value"] += "2.1.4 Canonical SMILES"+"\r\n"
					tempInfo["value"] += CanonicalSMILES[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"] + "\r\n"
					tempInfo["value"] += CanonicalSMILES[0]["Information"][0]["Reference"][0] + "\r\n"
				
				if len(MolecularFormula):
					tempInfo["value"] += "2.2 Molecular Formula"+"\r\n"
					tempInfo["value"] += MolecularFormula[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]+"\r\n"
					if len(MolecularFormula[0]["Information"])>1:
						tempInfo["value"] += (MolecularFormula[0]["Information"][1]["Reference"][0] if "Reference" in MolecularFormula[0]["Information"][1] else "") +"\r\n"

			tempInfo["value"] += "2.3 Other Identifiers"+"\r\n"

			OtherIdentifiers = list(filter(lambda o: o["TOCHeading"] =="Other Identifiers" , NamesAndIdentifiersSection))
			if len(OtherIdentifiers):
				OtherIdentifiersSection = OtherIdentifiers[0]["Section"]
				CAS = list(filter(lambda o: o["TOCHeading"] == "CAS", OtherIdentifiersSection))
				if len(CAS):
					tempInfo["value"] += "2.3.1 CAS"+"\r\n"
					tempInfo["value"] += CAS[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]+"\r\n"

				DeprecatedCAS = list(filter(lambda o: o["TOCHeading"] == "Deprecated CAS", OtherIdentifiersSection))
				if len(DeprecatedCAS):
					tempInfo["value"] += "2.3.2 Deprecated CAS"+"\r\n"
					tempInfo["value"] += DeprecatedCAS[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]+"\r\n"

				EuropeanCommunityNumber = list(filter(lambda o: o["TOCHeading"] == "European Community (EC) Number", OtherIdentifiersSection))
				if len(EuropeanCommunityNumber):
					tempInfo["value"] += "2.3.3 European Community (EC) Number"+"\r\n"
					tempInfo["value"] += EuropeanCommunityNumber[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]+"\r\n"


				NSCNumber = list(filter(lambda o: o["TOCHeading"] == "NSC Number", OtherIdentifiersSection))
				if len(NSCNumber):
					tempInfo["value"] += "2.3.4 NSC Number"+"\r\n"
					tempInfo["value"] += NSCNumber[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]+"\r\n"
				
				UNNumber = list(filter(lambda o: o["TOCHeading"] == "UN Numberr", OtherIdentifiersSection))
				if len(UNNumber):
					tempInfo["value"] += "2.3.5 UN Number"+"\r\n"
					tempInfo["value"] += UNNumber[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]+"\r\n"

				UNII = list(filter(lambda o: o["TOCHeading"] == "UNII", OtherIdentifiersSection))
				if len(UNNumber):
					tempInfo["value"] += "2.3.6 UNII"+"\r\n"
					tempInfo["value"] += UNII[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]+"\r\n"

				DSSToxSubstanceID = list(filter(lambda o: o["TOCHeading"] == "DSSTox Substance ID", OtherIdentifiersSection))
				if len(DSSToxSubstanceID):
					tempInfo["value"] += "2.3.7 DSSTox Substance ID"+"\r\n"
					tempInfo["value"] += DSSToxSubstanceID[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]+"\r\n"


				NikkajiNumber = list(filter(lambda o: o["TOCHeading"] == "Nikkaji Number", OtherIdentifiersSection))
				if len(NikkajiNumber):
					tempInfo["value"] += "2.3.8 Nikkaji Number"+"\r\n"
					tempInfo["value"] += NikkajiNumber[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]+"\r\n"

				Wikidata = list(filter(lambda o: o["TOCHeading"] == "Wikidata", OtherIdentifiersSection))
				if len(Wikidata):
					tempInfo["value"] += "2.3.9 Wikidata"+"\r\n"
					tempInfo["value"] += Wikidata[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]+"\r\n"
	
		

		

		if len(ChemicalAndPhysicalProperties):
			ChemicalSection = ChemicalAndPhysicalProperties[0]["Section"]
			ComputedProperties = list(filter(lambda o: o["TOCHeading"] == "Computed Properties", ChemicalSection))
			
			tempInfo["value"] += "3 Chemical and Physical Properties"+"\r\n"
			if len(ComputedProperties):
				tempInfo["value"] += "3.1 Computed Properties"+"\r\n"
				ComputedPropertiesSection = ComputedProperties[0]["Section"]
				ComputedPropertiesStr = ""
				for sect in ComputedPropertiesSection:
					title = sect["TOCHeading"]
					value = sect["Information"][0]["Value"]
					valueStr = ""
					if "StringWithMarkup" in value:
						valueStr = value["StringWithMarkup"][0]["String"] 
						if "Unit" in value:
							valueStr += value["Unit"]
						valueStr += "\r\n"
						valueStr += sect["Information"][0]["Reference"][0]+"\r\n"
					else:
						if "Number" in value:
							valueStr = str(value["Number"][0])
							if "Unit" in value:
								valueStr += value["Unit"]
							valueStr += "\r\n"
							valueStr += sect["Information"][0]["Reference"][0]+"\r\n"
					ComputedPropertiesStr += title + "\r\n"
					ComputedPropertiesStr += valueStr
				tempInfo["value"] += ComputedPropertiesStr +"\r\n"

		tempInfo["value"] += "3.2 Experimental Properties"+"\r\n"
		tempInfo["value"] += "3.2.1 Physical Description"+"\r\n"
		if len(NamesAndIdentifiers):
			NamesAndIdentifiersSection = NamesAndIdentifiers[0]["Section"]
			RecordDescription = list(filter(lambda o: o["TOCHeading"] == "Record Description", NamesAndIdentifiersSection))
			if len(RecordDescription):
				tempInfo["value"] += RecordDescription[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"] +"\r\n"

		if len(ChemicalAndPhysicalProperties):
			ChemicalSection = ChemicalAndPhysicalProperties[0]["Section"]
			ExperimentalProperties = list(filter(lambda o: o["TOCHeading"] == "Experimental Properties", ChemicalSection))
			if len(ExperimentalProperties):
				ExperimentalPropertiesSect = ExperimentalProperties[0]["Section"]
				BoilingPoint = list(filter(lambda o: o["TOCHeading"] == "Boiling Point", ExperimentalPropertiesSect))
				if len(BoilingPoint):
					tempInfo["value"] += "3.2.2 Boiling Point"+"\r\n"
					tempInfo["value"] += BoilingPoint[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"] if "StringWithMarkup" in BoilingPoint[0]["Information"][0]["Value"] else ""

				MeltingPoint = list(filter(lambda o: o["TOCHeading"] == "Melting Point", ExperimentalPropertiesSect))
				if len(MeltingPoint):
					tempInfo["value"] += "3.2.3 Melting Point"+"\r\n"
					tempInfo["value"] += MeltingPoint[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"] if "StringWithMarkup" in MeltingPoint[0]["Information"][0]["Value"] else ""


	products.append(tempInfo.copy())

def getProductList(type):
	cas = ""
	if len(type["cas"])>0:
		cas = type["cas"]
	if len(cas) == 0:
		products.append({
			"cas": cas
		})
	else:
		sope = httpUtils.getJson("https://pubchem.ncbi.nlm.nih.gov/rest/pug/concepts/name/JSON?name="+cas)
		if "ConceptsAndCIDs" not in sope:
			products.append({
				"cas": cas
			})
		else:
			if "CID" in sope["ConceptsAndCIDs"]:
				cids = sope["ConceptsAndCIDs"]["CID"]
				if len(cids):
					cid =cids[0]
					getProductInfo("https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/"+str(cid)+"/JSON/",cid,  type)
	




fileName="cat.json"
with open(fileName,'rb') as file_to_read:
	content=file_to_read.read()
	types = json.loads(content)
	for type in types:
		getProductList(type)
# getProductList({"cas":"145819-92-7","name":"xxxx"})

excelUtils.generateExcelMultipleSheet('pubchem.xlsx', [
	{
		"name":"产品参数示例",
		"header": headers,
		"data": products
	}
])