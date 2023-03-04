from itertools import product
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json

sys.path.append('../..')
from lib import excelUtils
from lib import httpUtils
from lib import textUtil
from lib.htmlEleUtils import getNodeText
from lib.htmlEleUtils import getInnerHtml
products = []
headers=['link','cas',
'RecordTitle',
'Description',
'Description1',
'Description2',
'Description3',
'IUPAC_Name',
'InChI',
'InChIKey',
'CanonicalSMILES',
'Formula_Name',
'IsomericSMILES',
'DepositorSuppliedStr',
'CASinfoStr',
'Related CAS',
'Molecular Weight',
'XLogP3',
'Hydrogen Bond Donor Count',
'Hydrogen Bond Acceptor Count',
'Rotatable Bond Count',
'Exact Mass',
'Monoisotopic Mass',
'Topological Polar Surface Area',
'Heavy Atom Count',
'Formal Charge',
'Complexity',
'Isotope Atom Count',
'Defined Atom Stereocenter Count',
'Undefined Atom Stereocenter Count',
'Defined Bond Stereocenter Count',
'Undefined Bond Stereocenter Count',
'Covalently-Bonded Unit Count',
'Compound Is Canonicalized',
'Physical Description',
'Color/Form',
'Boiling Point',
'Melting Point',
'Solubility',
'Density',
'Shelf Life',
'Flash Point',
'Refractive Index',
'LogP',
'Signal',
'GHSHazardStatements',
'PrecautionaryStatementCodes']
DepositorProvidedPubMedCitationsData = []
DepositorSuppliedPatentIdentifiersData = []

def addHeader(title):
  if title not in headers and len(title) > 0:
    headers.append(title)

def getProductInfo(url, cid, cas):
	print(str(len(products))+ cas + url)
	
	productListHtml = httpUtils.getHtmlStrFromUrl(url)
	tempPinfo = {
		"cas":cas,
		"link": url
	}
	data = json.loads(productListHtml)
	Section = data["Record"]["Section"]

	try:
		tempPinfo["RecordTitle"] = data["Record"]["RecordTitle"]
		referenceChEBI = list(filter(lambda i: i["SourceName"]=="ChEBI", data["Record"]["Reference"]))
		referenceDrugBank = list(filter(lambda i: i["SourceName"]=="DrugBank", data["Record"]["Reference"]))
		referenceFDA = list(filter(lambda i: i["SourceName"]=="FDA Pharm Classes", data["Record"]["Reference"]))
		desc1=""
		desc2=""
		desc3=""
		if len(referenceChEBI)>0:
			desc1 += "Source: ChEBI;"
			desc1 += "Record Name:"+referenceChEBI[0]["Name"]+";"
			desc1 += "URL:"+referenceChEBI[0]["URL"]+";"
			desc1 += "Description:"+referenceChEBI[0]["Description"]+";"
		if len(referenceDrugBank)>0:
			desc2 += "Source: DrugBank;"
			desc2 += "Record Name:"+referenceDrugBank[0]["Name"]+";"
			desc2 += "URL:"+referenceDrugBank[0]["URL"]+";"
			desc2 += "Description:"+referenceDrugBank[0]["Description"]+";"
			desc2 += "License Note:"+referenceDrugBank[0]["LicenseNote"]+";"
			desc2 += "License URL:"+referenceDrugBank[0]["LicenseURL"]+";"
		if len(referenceFDA)>0:
			desc3 += "Source: DrugBank;"
			desc3 += "Record Name:"+referenceFDA[0]["Name"]+";"
			desc3 += "URL:"+referenceFDA[0]["URL"]+";"
			desc3 += "Description:"+referenceFDA[0]["Description"]+";"
			desc3 += "License Note:"+referenceFDA[0]["LicenseNote"]+";"
			desc3 += "License URL:"+referenceFDA[0]["LicenseURL"]+";"
		tempPinfo["Description1"] = desc1
		tempPinfo["Description2"] = desc2
		tempPinfo["Description3"] = desc3
		imgSrc="https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?cid=" + str(cid) + "&t=l"
		httpUtils.urllib_download(imgSrc, cas+".png")
	except:
		tempPinfo["Description1"] = ''
		tempPinfo["Description2"] = ''
		tempPinfo["Description3"] = ''
		tempPinfo["RecordTitle"] = ''
	# Names and Identifiers
	nameAndIdenti = list(filter(lambda o: o["TOCHeading"]=="Names and Identifiers", Section))
	Computed_Descriptors = list(filter(lambda o: o["TOCHeading"]=="Computed Descriptors", nameAndIdenti[0]["Section"]))

	IUPAC_Name=""
	InChI=""
	InChIKey=""
	CanonicalSMILES=""
	Formula_Name=""
	IsomericSMILES=""
	DepositorSuppliedStr=""
	Description = ""
	IUPAC_NameInfoList = list(filter(lambda o: o["TOCHeading"]=="IUPAC Name", Computed_Descriptors[0]["Section"]))
	if len(IUPAC_NameInfoList):
		IUPAC_NameInfo = IUPAC_NameInfoList[0]["Information"]
		for o in IUPAC_NameInfo: IUPAC_Name += o["Value"]["StringWithMarkup"][0]["String"]+";"

	InChIInfoList = list(filter(lambda o: o["TOCHeading"]=="InChI", Computed_Descriptors[0]["Section"]))
	if len(InChIInfoList):
		InChIInfo = InChIInfoList[0]["Information"]
		for o in InChIInfo: InChI += o["Value"]["StringWithMarkup"][0]["String"]+";"

	InChIKeyInfoList = list(filter(lambda o: o["TOCHeading"]=="InChIKey", Computed_Descriptors[0]["Section"]))
	if len(InChIKeyInfoList):
		InChIKeyInfo = InChIKeyInfoList[0]["Information"]
		for o in InChIKeyInfo: InChIKey += o["Value"]["StringWithMarkup"][0]["String"]+";"

	CanonicalSMILESInfoList = list(filter(lambda o: o["TOCHeading"]=="Canonical SMILES", Computed_Descriptors[0]["Section"]))
	if len(CanonicalSMILESInfoList):
		CanonicalSMILESInfo = CanonicalSMILESInfoList[0]["Information"]
		for o in CanonicalSMILESInfo: CanonicalSMILES += o["Value"]["StringWithMarkup"][0]["String"]+";"

	IsomericSMILESList = list(filter(lambda o: o["TOCHeading"]=="Canonical SMILES", Computed_Descriptors[0]["Section"]))
	if len(IsomericSMILESList):
		CanonicalSMILESInfo = IsomericSMILESList[0]["Information"]
		for o in CanonicalSMILESInfo: IsomericSMILES += o["Value"]["StringWithMarkup"][0]["String"]+";"

	Molecular_FormulaList = list(filter(lambda o: o["TOCHeading"]=="Molecular Formula", nameAndIdenti[0]["Section"]))
	if len(Molecular_FormulaList):
		Molecular_Formula = Molecular_FormulaList[0]["Information"]
		for o in Molecular_Formula: Formula_Name += o["Value"]["StringWithMarkup"][0]["String"]+";"

	SynonymsList = list(filter(lambda o: o["TOCHeading"]=="Synonyms", nameAndIdenti[0]["Section"]))
	if len(SynonymsList):
		if "Section" in SynonymsList[0]:
			SynonymsSections = SynonymsList[0]["Section"]
			DepositorSuppliedList = list(filter(lambda o: o["TOCHeading"]=="Depositor-Supplied Synonyms", SynonymsSections))
			if len(DepositorSuppliedList):
				DepositorSuppliedInfo = DepositorSuppliedList[0]["Information"][0]["Value"]["StringWithMarkup"]
				for o in DepositorSuppliedInfo: DepositorSuppliedStr += o["String"]+";"

	RecordDescriptionList = list(filter(lambda o: o["TOCHeading"]=="Record Description", nameAndIdenti[0]["Section"]))
	if len(RecordDescriptionList):
		if len(RecordDescriptionList[0]["Information"]):
			for o in RecordDescriptionList[0]["Information"][0]["Value"]["StringWithMarkup"]: Description += o["String"] + "\n"

	tempPinfo["IUPAC_Name"] = IUPAC_Name
	tempPinfo["InChI"] = InChI
	tempPinfo["InChIKey"] = InChIKey
	tempPinfo["CanonicalSMILES"] = CanonicalSMILES
	tempPinfo["Formula_Name"] = Formula_Name
	tempPinfo["IsomericSMILES"] = IsomericSMILES
	tempPinfo["DepositorSuppliedStr"] = DepositorSuppliedStr
	tempPinfo["Description"] = Description
	CASinfoStr=""
	OtherCASinfoStr=""
	OtherIdentifiers = list(filter(lambda o: o["TOCHeading"]=="Other Identifiers", nameAndIdenti[0]["Section"]))
	if len(OtherIdentifiers):
		CAS_NameInfoList = list(filter(lambda o: o["TOCHeading"]=="CAS", OtherIdentifiers[0]["Section"]))
		if len(CAS_NameInfoList):
			CAS_NameInfo = CAS_NameInfoList[0]["Information"]
			CASinfoList = list(filter(lambda o: o.get("Name") and o["Name"]=="CAS", CAS_NameInfo))
			OtherCASinfoList = list(filter(lambda o: o.get("Name") and o["Name"]=="Other CAS", CAS_NameInfo))
			if len(CASinfoList):
				CASinfo = CASinfoList[0]["Value"]["StringWithMarkup"]
				for CAS in CASinfo: CASinfoStr += CAS["String"]+";"
			if len(OtherCASinfoList):
				OtherCASinfo=OtherCASinfoList[0]["Value"]["StringWithMarkup"]
				for OtherCAS in OtherCASinfo: OtherCASinfoStr += OtherCAS["String"]+";"
	tempPinfo["CASinfoStr"] = CASinfoStr
	tempPinfo["Related CAS"] = OtherCASinfoStr

	#	Chemical and Physical Properties	
	ChemicalandPhysicalProperties = list(filter(lambda o: o["TOCHeading"]=="Chemical and Physical Properties", Section))
	if len(ChemicalandPhysicalProperties):
		ComputedProperties = list(filter(lambda o: o["TOCHeading"]=="Computed Properties", ChemicalandPhysicalProperties[0]["Section"]))
		if len(ComputedProperties):
			for key in ComputedProperties[0]["Section"]: 
				pName = key["TOCHeading"]
				pValue = ""
				unit = key["Information"][0]["Value"].get("Unit")
				Numbers = key["Information"][0]["Value"].get("Number")
				Strings = key["Information"][0]["Value"].get("StringWithMarkup")
				if Numbers:
					for number in Numbers: pValue += str(number) + ";"
				if Strings:
					for strValue in Strings: pValue += strValue["String"] + ";"
				if len(pValue): pValue = pValue[0:len(pValue)-1]
				pValue= pValue + (unit if(unit) else "")
				addHeader(pValue)
				tempPinfo[pName]=pValue
	#Experimental Properties
	PhysicalDescriptionInfoStr = ""
	ColorFormInfoStr=""
	BoilingPointStr=""
	MeltingPointInfoStr=""
	SolubilityInfoStr=""
	DensityInfoStr=""
	StabilityShelfLifeInfoStr=""
	FlashPointInfoStr=""
	RefractiveIndexInfoStr=""
	LogPInfoStr=""
	ExperimentalProperties = list(filter(lambda o: o["TOCHeading"]=="Experimental Properties", ChemicalandPhysicalProperties[0]["Section"]))
	if len(ExperimentalProperties):
		PhysicalDescriptionList = list(filter(lambda o: o["TOCHeading"]=="Physical Description", ExperimentalProperties[0]["Section"]))
		if len(PhysicalDescriptionList):
			PhysicalDescriptionInfo = PhysicalDescriptionList[0]["Information"]
			for PhysicalDescription in PhysicalDescriptionInfo: PhysicalDescriptionInfoStr+=PhysicalDescription["Value"]["StringWithMarkup"][0]["String"]+";"
			
		ColorFormList = list(filter(lambda o: o["TOCHeading"]=="Color/Form", ExperimentalProperties[0]["Section"]))
		if len(ColorFormList):
			ColorFormInfo = ColorFormList[0]["Information"]
			for ColorForm in ColorFormInfo: ColorFormInfoStr+=ColorForm["Value"]["StringWithMarkup"][0]["String"]+";"
	
		BoilingPointList = list(filter(lambda o: o["TOCHeading"]=="Boiling Point", ExperimentalProperties[0]["Section"]))
		if len(BoilingPointList):
			BoilingPointInfo = BoilingPointList[0]["Information"]
			for BoilingPoint in BoilingPointInfo: BoilingPointStr += BoilingPoint["Value"]["StringWithMarkup"][0]["String"]+";"
			
		MeltingPointList = list(filter(lambda o: o["TOCHeading"]=="Melting Point", ExperimentalProperties[0]["Section"]))
		if len(MeltingPointList):
			MeltingPointInfo = MeltingPointList[0]["Information"]
			for MeltingPoint in MeltingPointInfo:
				StringWithMarkupValue = MeltingPoint["Value"].get("StringWithMarkup")
				if StringWithMarkupValue: MeltingPointInfoStr += StringWithMarkupValue[0]["String"]+";"
							
		LogPList = list(filter(lambda o: o["TOCHeading"]=="LogP", ExperimentalProperties[0]["Section"]))
		if len(LogPList):
			LogPInfo = LogPList[0]["Information"]
			for LogP in LogPInfo:
				LogPValue = LogP["Value"].get("StringWithMarkup")
				if LogPValue: LogPInfoStr += LogPValue[0]["String"]+";"

		SolubilityList = list(filter(lambda o: o["TOCHeading"]=="Solubility", ExperimentalProperties[0]["Section"]))
		if len(SolubilityList):
			SolubilityInfo = SolubilityList[0]["Information"]
			for Solubility in SolubilityInfo:
				StringWithMarkupValue = Solubility["Value"].get("StringWithMarkup")
				if StringWithMarkupValue: SolubilityInfoStr += StringWithMarkupValue[0]["String"]+";"
			
		DensityList = list(filter(lambda o: o["TOCHeading"]=="Density", ExperimentalProperties[0]["Section"]))
		if len(DensityList):
			DensityInfo = DensityList[0]["Information"]
			for Density in DensityInfo: DensityInfoStr += Density["Value"]["StringWithMarkup"][0]["String"]+";"

		StabilityShelfLifeList = list(filter(lambda o: o["TOCHeading"]=="Stability/Shelf Life", ExperimentalProperties[0]["Section"]))
		if len(StabilityShelfLifeList):
			StabilityShelfLifeInfo = StabilityShelfLifeList[0]["Information"]
			for StabilityShelfLife in StabilityShelfLifeInfo: StabilityShelfLifeInfoStr += StabilityShelfLife["Value"]["StringWithMarkup"][0]["String"]+";"
			
		FlashPointList = list(filter(lambda o: o["TOCHeading"]=="Flash Point", ExperimentalProperties[0]["Section"]))
		if len(FlashPointList):
			FlashPointInfo = FlashPointList[0]["Information"]
			for FlashPoint in FlashPointInfo: FlashPointInfoStr += FlashPoint["Value"]["StringWithMarkup"][0]["String"]+";"
							
		RefractiveIndexList = list(filter(lambda o: o["TOCHeading"]=="Refractive Index", ExperimentalProperties[0]["Section"]))
		if len(RefractiveIndexList):
			RefractiveIndexInfo = RefractiveIndexList[0]["Information"]
			for RefractiveIndex in RefractiveIndexInfo: RefractiveIndexInfoStr += RefractiveIndex["Value"]["StringWithMarkup"][0]["String"]+";"
	tempPinfo["Physical Description"] = PhysicalDescriptionInfoStr
	tempPinfo["Color/Form"] = ColorFormInfoStr
	tempPinfo["Boiling Point"] = BoilingPointStr
	tempPinfo["Melting Point"] = MeltingPointInfoStr
	tempPinfo["Solubility"] = SolubilityInfoStr
	tempPinfo["Density"] = DensityInfoStr
	tempPinfo["Shelf Life"] = StabilityShelfLifeInfoStr
	tempPinfo["Flash Point"] = FlashPointInfoStr
	tempPinfo["Refractive Index"] = RefractiveIndexInfoStr
	tempPinfo["LogP"] = LogPInfoStr
	GHSHazardStatementsStr = ""
	PrecautionaryStatementCodesStr=""
	SafetyandHazards = list(filter(lambda o: o["TOCHeading"]=="Safety and Hazards", Section))
	if len(SafetyandHazards):
		SafetyandHazardsSection = SafetyandHazards[0]["Section"]
		HazardsIdentification = list(filter(lambda o: o["TOCHeading"]=="Hazards Identification", SafetyandHazardsSection))
		if len(HazardsIdentification):
			GHSClassification = list(filter(lambda o: o["TOCHeading"]=="GHS Classification", HazardsIdentification[0]["Section"]))

			if len(GHSClassification):
				GHSClassificationInfo = GHSClassification[0]["Information"]
				SignalProp = list(filter(lambda o: o["Name"]=="Signal", GHSClassificationInfo))
				GHSHazardStatementsProp = list(filter(lambda o: o["Name"]=="GHS Hazard Statements", GHSClassificationInfo))
				PrecautionaryStatementCodesProp = list(filter(lambda o: o["Name"]=="Precautionary Statement Codes", GHSClassificationInfo))
				if len(SignalProp):
					tempPinfo["Signal"] = SignalProp[0]["Value"]["StringWithMarkup"][0]["String"]

				if len(GHSHazardStatementsProp):
					for o in GHSHazardStatementsProp[0]["Value"]["StringWithMarkup"]: GHSHazardStatementsStr += o["String"]+";"
				
				if len(PrecautionaryStatementCodesProp):
					for o in PrecautionaryStatementCodesProp[0]["Value"]["StringWithMarkup"]: PrecautionaryStatementCodesStr += o["String"]+";"
		tempPinfo["GHSHazardStatements"]= GHSHazardStatementsStr
		tempPinfo["PrecautionaryStatementCodes"]= PrecautionaryStatementCodesStr
		DepositorProvidedPubMedCitationsUrl = "https://pubchem.ncbi.nlm.nih.gov/sdq/sdqagent.cgi?infmt=json&outfmt=json&query={%22select%22:%22*%22,%22collection%22:%22pubmed%22,%22where%22:{%22ands%22:[{%22cid%22:%22"+str(cid)+"%22},{%22pmidsrcs%22:%22xref%22}]},%22order%22:[%22articlepubdate,desc%22],%22start%22:0,%22limit%22:10,%22nullatbottom%22:1,%22width%22:1000000,%22listids%22:0}"
		DepositorProvidedPubMedCitations = httpUtils.getJson(DepositorProvidedPubMedCitationsUrl)
		DepositorSuppliedPatentIdentifiersUrl ="https://pubchem.ncbi.nlm.nih.gov/sdq/sdqagent.cgi?infmt=json&outfmt=json&query={%22select%22:%22*%22,%22collection%22:%22patent%22,%22where%22:{%22ands%22:[{%22cid%22:%22"+str(cid)+"%22}]},%22order%22:[%22prioritydate,desc%22],%22start%22:0,%22limit%22:10,%22nullatbottom%22:1,%22width%22:1000000,%22listids%22:0}"
		DepositorSuppliedPatentIdentifiers = httpUtils.getJson(DepositorSuppliedPatentIdentifiersUrl)

		for o in DepositorProvidedPubMedCitations["SDQOutputSet"][0]["rows"]:
			o["CAS"]=cas
			DepositorProvidedPubMedCitationsData.append(o.copy())

		for o in DepositorSuppliedPatentIdentifiers["SDQOutputSet"][0]["rows"]:
			o["CAS"]=cas
			DepositorSuppliedPatentIdentifiersData.append(o.copy())
	products.append(tempPinfo.copy())

def getProductList(cas):
	productListHtml = httpUtils.getHtmlStrFromUrl("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"+cas+"/cids/JSON")
	if productListHtml!=None:
		data = json.loads(productListHtml)
		if len(data["IdentifierList"]["CID"]) >0:
			cid = data["IdentifierList"]["CID"][0]
			try:
				getProductInfo("https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/"+str(cid)+"/JSON/", cid,cas)
			except:
				products.append({"cas":cas, cid: cid})
	else:
		products.append({"cas":cas})

fileName="cat.txt"
with open(fileName,encoding="utf-8") as file_to_read:
	index = 1
	type=1
	while True:
		lines = file_to_read.readline()
		if not lines:
				break
		getProductList(lines.replace("\n",""))
# getProductList("107-75-5")

excelUtils.generateExcelMultipleSheet('pubchem.xlsx', [
	{
		"name":"产品参数示例",
		"header": headers,
		"data": products
	},
	{
		"name":"参考文献整理示例",
		"header":['CAS','pmid','articlepubdate','articletitle','articlejourname'],
		"data": DepositorProvidedPubMedCitationsData
	},
	{
		"name":"专利整理示例",
		"header":['CAS','publicationnumber','title','prioritydate','grantdate'],
		"data": DepositorSuppliedPatentIdentifiersData
	}
])