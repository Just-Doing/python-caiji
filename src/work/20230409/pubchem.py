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
headers=['link','cas', 'name',
'Structures','description0','description1','description2',
'description3','IUPAC_Name','InChI','InChIKey',
'CanonicalSMILES','Molecular Formula','IsomericSMILES',
'DepositorSuppliedStr','Description','CASinfoStr',
'Related CAS','Molecular Weight','XLogP3',
'Hydrogen Bond Donor Count','Hydrogen Bond Acceptor Count',
'Rotatable Bond Count','Exact Mass','Monoisotopic Mass',
'Topological Polar Surface Area','Heavy Atom Count',
'Formal Charge','Complexity','Isotope Atom Count',
'Defined Atom Stereocenter Count',
'Undefined Atom Stereocenter Count','Defined Bond Stereocenter Count',
'Undefined Bond Stereocenter Count','Covalently-Bonded Unit Count',
'Compound Is Canonicalized','Physical Description','Color/Form',
'Boiling Point','Melting Point','Solubility','Density',
'Shelf Life','Flash Point','Refractive Index','LogP',
'Vapor Pressure',"Henry's Law Constant",'Decomposition',
'Dissociation Constants','Odor','Pharmacological Classification',
'Distribution and Excretion','Metabolism/Metabolites',
'Mechanism of Action','Sources/Uses','Methods of Manufacturing',
'Formulations/Preparations','Analytic Laboratory Methods',
'Adverse Effects','Interactions','Antidote and Emergency Treatment',
'Human Toxicity Excerpts','Non-Human Toxicity Excerpts',
'Non-Human Toxicity Values','Ecotoxicity Values','Signal',
'GHS Hazard Statements','Precautionary Statement Codes'
]
AcuteEffects = []
DepositorProvidedPubMedCitationsData = []
DepositorSuppliedPatentIdentifiersData = []

def addHeader(title):
  if title not in headers and len(title) > 0:
    headers.append(title)

def getProductInfo(url, cid, type):
	print(str(len(products))+ type["cas"] + url)
	cas = ""
	if len(type["cas"])>0:
		cas = type["cas"]
	else:
		cas = type["name"]
	productListHtml = httpUtils.getHtmlStrFromUrl(url)
	tempPinfo = {
		"cas":type["cas"],
		"name":type["name"],
		"link": url
	}
	data = json.loads(productListHtml.decode("utf-8", errors='ignore'))
	Section = data["Record"]["Section"]

	try:
		tempPinfo["Structures"]=cas+".png"
		imgSrc="https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?cid=" + str(cid) + "&t=l"
		httpUtils.urllib_download(imgSrc, tempPinfo["Structures"])
	except:
		tempPinfo["Structures"] = ""

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
			for inx,o in enumerate(RecordDescriptionList[0]["Information"]): 
				tempPinfo["description"+str(inx)] = o["Value"]["StringWithMarkup"][0]["String"]


	tempPinfo["IUPAC_Name"] = IUPAC_Name
	tempPinfo["InChI"] = InChI
	tempPinfo["InChIKey"] = InChIKey
	tempPinfo["CanonicalSMILES"] = CanonicalSMILES
	tempPinfo["Molecular Formula"] = Formula_Name
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
				addHeader(pName)
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
	HenryLawConstantStr=""
	DecompositioDissociationConstantsStr=""
	VaporPressureStr=""
	DissociationConstantsStr=""
	OdorStr=""
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

		Odor = list(filter(lambda o: o["TOCHeading"]=="Odor", ExperimentalProperties[0]["Section"]))
		if len(Odor):
			OdorStr=Odor[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]
	
		BoilingPointList = list(filter(lambda o: o["TOCHeading"]=="Boiling Point", ExperimentalProperties[0]["Section"]))
		if len(BoilingPointList):
			BoilingPointInfo = BoilingPointList[0]["Information"]
			for BoilingPoint in BoilingPointInfo: 
				BoilingPointValue = BoilingPoint["Value"]
				if "StringWithMarkup" in BoilingPointValue:
					BoilingPointStr += BoilingPointValue["StringWithMarkup"][0]["String"]+";"
				else:
					if "Number" in BoilingPointValue and "Unit" in BoilingPointValue:
						BoilingPointStr += str(BoilingPointValue["Number"][0])+BoilingPointValue["Unit"]+";"
			
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

		VaporPressure = list(filter(lambda o: o["TOCHeading"]=="Vapor Pressure", ExperimentalProperties[0]["Section"]))
		if len(VaporPressure):
			VaporPressureStr = VaporPressure[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]

		HenryLawConstant = list(filter(lambda o: o["TOCHeading"]=="Henry's Law Constant", ExperimentalProperties[0]["Section"]))
		if len(HenryLawConstant):
			HenryLawConstantStr = HenryLawConstant[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]

		DecompositioDissociationConstants = list(filter(lambda o: o["TOCHeading"]=="Decomposition", ExperimentalProperties[0]["Section"]))
		if len(DecompositioDissociationConstants):
			DecompositioDissociationConstantsStr = DecompositioDissociationConstants[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]

		DissociationConstants = list(filter(lambda o: o["TOCHeading"]=="Dissociation Constants", ExperimentalProperties[0]["Section"]))
		if len(DissociationConstants):
			DissociationConstantsStr = DissociationConstants[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]

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
	print(RefractiveIndexInfoStr)
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
	tempPinfo["Vapor Pressure"] = VaporPressureStr
	tempPinfo["Henry's Law Constant"] = HenryLawConstantStr
	tempPinfo["Decomposition"] = DecompositioDissociationConstantsStr
	tempPinfo["Dissociation Constants"] = DissociationConstantsStr
	tempPinfo["Odor"] = OdorStr

	PharmacologicalClassificationStr = ""
	DistributionAndExcretionStr=""
	MetabolismMetabolitesStr = ""
	MechanismofActionStr = ""
	PharmacologyAndBiochemistry = list(filter(lambda o: o["TOCHeading"]=="Pharmacology and Biochemistry", Section))
	if len(PharmacologyAndBiochemistry):
		PharmacologyAndBiochemistrySection = PharmacologyAndBiochemistry[0]["Section"]
		PharmacologicalClassification = list(filter(lambda o: o["TOCHeading"].endswith("Pharmacological Classification"), PharmacologyAndBiochemistrySection))
		if len(PharmacologicalClassification):
			for o in PharmacologicalClassification[0]["Information"]: PharmacologicalClassificationStr += (o["Name"]+":"+o["Value"]["StringWithMarkup"][0]["String"]+";")

		DistributionAndExcretion = list(filter(lambda o: o["TOCHeading"].endswith("Distribution and Excretion"), PharmacologyAndBiochemistrySection))
		if len(DistributionAndExcretion):
			for o in DistributionAndExcretion[0]["Information"]: DistributionAndExcretionStr += o["Value"]["StringWithMarkup"][0]["String"]+";"

		MetabolismMetabolites = list(filter(lambda o: o["TOCHeading"].endswith("Metabolism/Metabolites"), PharmacologyAndBiochemistrySection))
		if len(MetabolismMetabolites):
			MetabolismMetabolitesStr = MetabolismMetabolites[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]

		MechanismofAction = list(filter(lambda o: o["TOCHeading"].endswith("Mechanism of Action"), PharmacologyAndBiochemistrySection))
		if len(MechanismofAction):
			MechanismofActionStr = MechanismofAction[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]
	tempPinfo["Pharmacological Classification"] = PharmacologicalClassificationStr
	tempPinfo["Distribution and Excretion"] = DistributionAndExcretionStr
	tempPinfo["Metabolism/Metabolites"] = MetabolismMetabolitesStr
	tempPinfo["Mechanism of Action"] = MechanismofActionStr


	UsesStr = ""
	MethodsOfManufacturingStr=""
	FormulationsPreparationsStr = ""
	UseAndManufacturing = list(filter(lambda o: o["TOCHeading"]=="Use and Manufacturing", Section))
	if len(UseAndManufacturing):
		UseAndManufacturingSection = UseAndManufacturing[0]["Section"]
		
		Uses = list(filter(lambda o: o["TOCHeading"]=="Uses", UseAndManufacturingSection))
		if len(Uses):
			if "Information" in Uses[0]:
				SourcesUses = list(filter(lambda o: "Name" in o and o["Name"] == "Sources/Uses", Uses[0]["Information"]))
				if len(SourcesUses) > 0:
					UsesStr = SourcesUses[0]["Value"]["StringWithMarkup"][0]["String"]
		
		MethodsOfManufacturing = list(filter(lambda o: o["TOCHeading"]=="Methods of Manufacturing", UseAndManufacturingSection))
		if len(MethodsOfManufacturing):
			for o in MethodsOfManufacturing[0]["Information"]: 
				if "StringWithMarkup" in o["Value"]:
					MethodsOfManufacturingStr += o["Value"]["StringWithMarkup"][0]["String"]+";"

		FormulationsPreparations = list(filter(lambda o: o["TOCHeading"]=="Formulations/Preparations", UseAndManufacturingSection))
		if len(FormulationsPreparations):
			for o in FormulationsPreparations[0]["Information"]: 
				if "StringWithMarkup" in o["Value"]:
					FormulationsPreparationsStr += o["Value"]["StringWithMarkup"][0]["String"]+";"

	tempPinfo["Sources/Uses"] = UsesStr
	tempPinfo["Methods of Manufacturing"] = MethodsOfManufacturingStr
	tempPinfo["Formulations/Preparations"] = FormulationsPreparationsStr
	
	AnalyticLaboratoryMethodsStr = ""
	Identification = list(filter(lambda o: o["TOCHeading"]=="Identification", Section))
	if len(Identification):
		IdentificationSection = Identification[0]["Section"]

		AnalyticLaboratoryMethods = list(filter(lambda o: o["TOCHeading"]=="Analytic Laboratory Methods", IdentificationSection))
		if len(AnalyticLaboratoryMethods):
			AnalyticLaboratoryMethodsStr = AnalyticLaboratoryMethods[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]+";"
	
	tempPinfo["Analytic Laboratory Methods"] = AnalyticLaboratoryMethodsStr

	AdverseEffectsStr = ""
	InteractionsStr = ""
	AntidoteandEmergencyTreatment = ""
	HumanToxicityExcerptsStr=""
	NonHumanToxicityExcerptsStr=""
	NonHumanToxicityValuesStr=""
	EcotoxicityValuesStr=""
	AntidoteandEmergencyTreatmentStr=""
	Toxicity = list(filter(lambda o: o["TOCHeading"]=="Toxicity", Section))
	if len(Toxicity):
		ToxicitySection = Toxicity[0]["Section"]
		toxInfo = list(filter(lambda o: o["TOCHeading"]=="Toxicological Information", ToxicitySection))
		if len(toxInfo):
			toxInfoSection = toxInfo[0]["Section"]
			AdverseEffects = list(filter(lambda o: o["TOCHeading"]=="Adverse Effects", toxInfoSection))
			if len(AdverseEffects):
				for o in AdverseEffects[0]["Information"][0]["Value"]["StringWithMarkup"]: AdverseEffectsStr += o["String"]+";"
			
			Interactions = list(filter(lambda o: o["TOCHeading"]=="Interactions", toxInfoSection))

			if len(Interactions):
				InteractionsStr = Interactions[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]+";"

			AntidoteandEmergencyTreatment = list(filter(lambda o: o["TOCHeading"]=="Antidote and Emergency Treatment", toxInfoSection))
			if len(AntidoteandEmergencyTreatment):
				AntidoteandEmergencyTreatmentStr = AntidoteandEmergencyTreatment[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]+";"

			HumanToxicityExcerpts = list(filter(lambda o: o["TOCHeading"]=="Human Toxicity Excerpts", toxInfoSection))
			if len(HumanToxicityExcerpts):
				HumanToxicityExcerptsStr = HumanToxicityExcerpts[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]+";"
			
			NonHumanToxicityExcerpts = list(filter(lambda o: o["TOCHeading"]=="Non-Human Toxicity Excerpts", toxInfoSection))
			if len(NonHumanToxicityExcerpts):
				NonHumanToxicityExcerptsStr = NonHumanToxicityExcerpts[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]+";"
				
			NonHumanToxicityValues = list(filter(lambda o: o["TOCHeading"]=="Non-Human Toxicity Values", toxInfoSection))
			if len(NonHumanToxicityValues):
				NonHumanToxicityValuesStr = NonHumanToxicityValues[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]+";"
			
			EcotoxicityValues = list(filter(lambda o: o["TOCHeading"]=="Ecotoxicity Values", toxInfoSection))
			if len(EcotoxicityValues):
				EcotoxicityValuesStr = EcotoxicityValues[0]["Information"][0]["Value"]["StringWithMarkup"][0]["String"]+";"
	
	tempPinfo["Adverse Effects"] = AdverseEffectsStr
	tempPinfo["Interactions"] = InteractionsStr
	tempPinfo["Antidote and Emergency Treatment"] = AntidoteandEmergencyTreatmentStr
	tempPinfo["Human Toxicity Excerpts"] = HumanToxicityExcerptsStr
	tempPinfo["Non-Human Toxicity Excerpts"] = NonHumanToxicityExcerptsStr
	tempPinfo["Non-Human Toxicity Values"] = NonHumanToxicityValuesStr
	tempPinfo["Ecotoxicity Values"] = EcotoxicityValuesStr


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
		tempPinfo["GHS Hazard Statements"]= GHSHazardStatementsStr
		tempPinfo["Precautionary Statement Codes"]= PrecautionaryStatementCodesStr

	
		acuteEffectUrl = "https://pubchem.ncbi.nlm.nih.gov/sdq/sdqagent.cgi?infmt=json&outfmt=json&query={%22select%22:%22*%22,%22collection%22:%22chemidplus%22,%22where%22:{%22ands%22:[{%22cid%22:%22"+str(cid)+"%22}]},%22order%22:[%22relevancescore,desc%22],%22start%22:1,%22limit%22:10,%22width%22:1000000,%22listids%22:0}"
		acuteEffectData = httpUtils.getJson(acuteEffectUrl)
		DepositorProvidedPubMedCitationsUrl = "https://pubchem.ncbi.nlm.nih.gov/sdq/sdqagent.cgi?infmt=json&outfmt=json&query={%22select%22:%22*%22,%22collection%22:%22pubmed%22,%22where%22:{%22ands%22:[{%22cid%22:%22"+str(cid)+"%22},{%22pmidsrcs%22:%22xref%22}]},%22order%22:[%22articlepubdate,desc%22],%22start%22:0,%22limit%22:10,%22nullatbottom%22:1,%22width%22:1000000,%22listids%22:0}"
		DepositorProvidedPubMedCitations = httpUtils.getJson(DepositorProvidedPubMedCitationsUrl)
		DepositorSuppliedPatentIdentifiersUrl ="https://pubchem.ncbi.nlm.nih.gov/sdq/sdqagent.cgi?infmt=json&outfmt=json&query={%22select%22:%22*%22,%22collection%22:%22patent%22,%22where%22:{%22ands%22:[{%22cid%22:%22"+str(cid)+"%22}]},%22order%22:[%22prioritydate,desc%22],%22start%22:0,%22limit%22:10,%22nullatbottom%22:1,%22width%22:1000000,%22listids%22:0}"
		DepositorSuppliedPatentIdentifiers = httpUtils.getJson(DepositorSuppliedPatentIdentifiersUrl)

		for o in acuteEffectData["SDQOutputSet"][0]["rows"]:
			o["CAS"]=cas
			AcuteEffects.append(o.copy())

		for o in DepositorProvidedPubMedCitations["SDQOutputSet"][0]["rows"]:
			o["CAS"]=cas
			DepositorProvidedPubMedCitationsData.append(o.copy())

		for o in DepositorSuppliedPatentIdentifiers["SDQOutputSet"][0]["rows"]:
			o["CAS"]=cas
			DepositorSuppliedPatentIdentifiersData.append(o.copy())
	products.append(tempPinfo.copy())

def getProductList(type):
	cas = ""
	if len(type["cas"])>0:
		cas = type["cas"]
	else:
		cas = type["name"]
	productListHtml = httpUtils.getHtmlStrFromUrl("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"+cas+"/cids/JSON")
	if productListHtml!=None:
		data = json.loads(productListHtml)
		if len(data["IdentifierList"]["CID"]) >0:
			cid = data["IdentifierList"]["CID"][0]
			try:
				getProductInfo("https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/"+str(cid)+"/JSON/", cid, type)
			except:
				products.append({"cas":type["cas"],"name":type["name"], cid: cid})
	else:
		products.append({"cas":type["cas"],"name":type["name"],})

# fileName="cat.json"
# with open(fileName,'rb') as file_to_read:
# 	content=file_to_read.read()
# 	types = json.loads(content)
# 	for type in types:
# 		getProductList(type)
getProductList({"cas":"1866-31-5","name":"xxxx"})

excelUtils.generateExcelMultipleSheet('pubchem.xlsx', [
	{
		"name":"产品参数示例",
		"header": headers,
		"data": products
	},
	{
		"name":"Acute Effects",
		"header":['CAS','sid','organism','testtype','route','dose','effect','reference'],
		"data": AcuteEffects
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