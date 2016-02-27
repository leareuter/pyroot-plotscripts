import sys
import os
sys.path.insert(0, '../')
from scriptgenerator import *
from plotutils import *

#mcweight='2.0*2.67*(Evt_Odd==0)*(N_Jets>=4 && N_BTagsM>=2)*((N_Jets==4 && N_BTagsM==3)||(N_Jets==4&&N_BTagsM==4)||(N_Jets==5&&N_BTagsM==3)||(N_Jets==5&&N_BTagsM>=4)||(N_Jets>=6&&N_BTagsM==2)||(N_Jets>=6&&N_BTagsM==3)||(N_Jets>=6&&N_BTagsM>=4)||(BoostedTopHiggs_TopHadCandidate_TopMVAOutput >= -0.485 && BoostedTopHiggs_HiggsCandidate_HiggsTag >= 0.8925))'
#mcweightAll='2.67*(N_Jets>=4 && N_BTagsM>=2)*((N_Jets==4 && N_BTagsM==3)||(N_Jets==4&&N_BTagsM==4)||(N_Jets==5&&N_BTagsM==3)||(N_Jets==5&&N_BTagsM>=4)||(N_Jets>=6&&N_BTagsM==2)||(N_Jets>=6&&N_BTagsM==3)||(N_Jets>=6&&N_BTagsM>=4)||(BoostedTopHiggs_TopHadCandidate_TopMVAOutput >= -0.485 && BoostedTopHiggs_HiggsCandidate_HiggsTag >= 0.8925))'
mcweightAll='2.67'
mcweight='2.0*2.67'

sel_singleel="(N_LooseMuons==0)*(N_Jets>=4 && N_BTagsM>=2)" # need to veto muon events in electron dataset to avoid double countung
sel_singlemu="(N_LooseElectrons==0)*(N_Jets>=4 && N_BTagsM>=2)" # and vice versa...

# hcc is uu dd ss cc with ids 1 2 3 4
hccSel='*((abs(GenHiggs_DecProd1_PDGID)==1 && abs(GenHiggs_DecProd2_PDGID)==1) || (abs(GenHiggs_DecProd1_PDGID)==2 && abs(GenHiggs_DecProd2_PDGID)==2) || (abs(GenHiggs_DecProd1_PDGID)==3 && abs(GenHiggs_DecProd2_PDGID)==3) || (abs(GenHiggs_DecProd1_PDGID)==4 && abs(GenHiggs_DecProd2_PDGID)==4) )'
# htt is mumu tautau with ids 13 15
httSel='*((abs(GenHiggs_DecProd1_PDGID)==13 && abs(GenHiggs_DecProd2_PDGID)==13) || (abs(GenHiggs_DecProd1_PDGID)==15 && abs(GenHiggs_DecProd2_PDGID)==15))'
# hgg is gammagamma with id 22
hggSel='*((abs(GenHiggs_DecProd1_PDGID)==22 && abs(GenHiggs_DecProd2_PDGID)==22))'
# hgluglu with id 21
hglugluSel='*((abs(GenHiggs_DecProd1_PDGID)==21 && abs(GenHiggs_DecProd2_PDGID)==21))'
# hww with id 24
hwwSel='*((abs(GenHiggs_DecProd1_PDGID)==24 && abs(GenHiggs_DecProd2_PDGID)==24))'
# hzz with id 23
hzzSel='*((abs(GenHiggs_DecProd1_PDGID)==23 && abs(GenHiggs_DecProd2_PDGID)==23))'
# hzg with id 23 and id 22
hzgSel='*((abs(GenHiggs_DecProd1_PDGID)==23 && abs(GenHiggs_DecProd2_PDGID)==22) || (abs(GenHiggs_DecProd1_PDGID)==22 && abs(GenHiggs_DecProd2_PDGID)==23))'



path_76x="/nfs/dust/cms/user/hmildner/samples76X"

# names of the systematics (proper names needed e.g. for combination)
weightsystnames=["",
                 "_CMS_ttH_CSVLFUp","_CMS_ttH_CSVLFDown","_CMS_ttH_CSVHFUp","_CMS_ttH_CSVHFDown",
                 "_CMS_ttH_CSVHFStats1Up","_CMS_ttH_CSVHFStats1Down","_CMS_ttH_CSVLFStats1Up","_CMS_ttH_CSVLFStats1Down",
                 "_CMS_ttH_CSVHFStats2Up","_CMS_ttH_CSVHFStats2Down","_CMS_ttH_CSVLFStats2Up","_CMS_ttH_CSVLFStats2Down",
                 "_CMS_ttH_CSVCErr1Up","_CMS_ttH_CSVCErr1Down","_CMS_ttH_CSVCErr2Up","_CMS_ttH_CSVCErr2Down",
                 #"_CMS_ttH_TopPtUp","_CMS_ttH_TopPtDown",
                 "_CMS_ttH_PUUp","_CMS_ttH_PUDown",
                 "_CMS_ttH_Q2scale_ttbarOtherUp","_CMS_ttH_Q2scale_ttbarOtherDown",
                 "_CMS_ttH_Q2scale_ttbarPlusBUp","_CMS_ttH_Q2scale_ttbarPlusBDown",
                 "_CMS_ttH_Q2scale_ttbarPlus2BUp","_CMS_ttH_Q2scale_ttbarPlus2BDown",
                 "_CMS_ttH_Q2scale_ttbarPlusBBbarUp","_CMS_ttH_Q2scale_ttbarPlusBBbarDown",
                 "_CMS_ttH_Q2scale_ttbarPlusCCbarUp","_CMS_ttH_Q2scale_ttbarPlusCCbarDown",
                 #"_CMS_ttH_NNPDFUp","_CMS_ttH_NNPDFDown",
                 "_CMS_ttH_eff_muUp","_CMS_ttH_eff_muDown",  
                 "_CMS_ttH_eff_elUp","_CMS_ttH_eff_elDown",
                 #"_CMS_ttH_MuonIDUp","_CMS_ttH_MuonIDDown",
                 #"_CMS_ttH_MuonIsoUp","_CMS_ttH_MuonIsoDown",
                 #"_CMS_ttH_MuonTriggerUp","_CMS_ttH_MuonTriggerDown",                 
           ]

systs_all_samples=["",
                  "_CMS_ttH_CSVLFUp","_CMS_ttH_CSVLFDown","_CMS_ttH_CSVHFUp","_CMS_ttH_CSVHFDown",
                  "_CMS_ttH_CSVHFStats1Up","_CMS_ttH_CSVHFStats1Down","_CMS_ttH_CSVLFStats1Up","_CMS_ttH_CSVLFStats1Down",
                  "_CMS_ttH_CSVHFStats2Up","_CMS_ttH_CSVHFStats2Down","_CMS_ttH_CSVLFStats2Up","_CMS_ttH_CSVLFStats2Down",
                  "_CMS_ttH_CSVCErr1Up","_CMS_ttH_CSVCErr1Down","_CMS_ttH_CSVCErr2Up","_CMS_ttH_CSVCErr2Down",
                   "_CMS_ttH_PUUp","_CMS_ttH_PUDown",
                   "_CMS_ttH_eff_muUp","_CMS_ttH_eff_muDown",  
                 "_CMS_ttH_eff_elUp","_CMS_ttH_eff_elDown",
                   "_CMS_scale_jUp","_CMS_scale_jDown",
                  #"_CMS_ttH_MuonIDUp","_CMS_ttH_MuonIDDown",
                  #"_CMS_ttH_MuonIsoUp","_CMS_ttH_MuonIsoDown",
                  #"_CMS_ttH_MuonTriggerUp","_CMS_ttH_MuonTriggerDown",
                   ]

systs_ttbar= [
	      #"_CMS_ttH_NNPDFUp","_CMS_ttH_NNPDFDown",
	      "_CMS_ttH_PSscaleUp","_CMS_ttH_PSscaleDown",
	      ]
systs_tt_lf=["_CMS_ttH_Q2scale_ttbarOtherUp","_CMS_ttH_Q2scale_ttbarOtherDown",]
systs_tt_b=["_CMS_ttH_Q2scale_ttbarPlusBUp","_CMS_ttH_Q2scale_ttbarPlusBDown"]
systs_tt_2b=[ "_CMS_ttH_Q2scale_ttbarPlus2BUp","_CMS_ttH_Q2scale_ttbarPlus2BDown"]
systs_tt_bb=[ "_CMS_ttH_Q2scale_ttbarPlusBBbarUp","_CMS_ttH_Q2scale_ttbarPlusBBbarDown"]
systs_tt_cc=[ "_CMS_ttH_Q2scale_ttbarPlusCCbarUp","_CMS_ttH_Q2scale_ttbarPlusCCbarDown"]



PSSystnames=["",
		 "","","","",
		 "","","","",
		 "","","","",
		 "","","","",
		 #"_CMS_ttH_TopPtUp","_CMS_ttH_TopPtDown",
		 "","",
		 "","",
		 "","",
		 "","",
		 "","",
		 "","",
		 "","",
		 "","",
                 "_CMS_ttH_PSscaleUp","_CMS_ttH_PSscaleDown",
                 "","",
		 "","",
		 "","",
                 ]

errorSystnames=["",
		 "_CMS_ttH_CSVLFUp","_CMS_ttH_CSVLFDown","_CMS_ttH_CSVHFUp","_CMS_ttH_CSVHFDown",
                 "_CMS_ttH_CSVHFStats1Up","_CMS_ttH_CSVHFStats1Down","_CMS_ttH_CSVLFStats1Up","_CMS_ttH_CSVLFStats1Down",
                 "_CMS_ttH_CSVHFStats2Up","_CMS_ttH_CSVHFStats2Down","_CMS_ttH_CSVLFStats2Up","_CMS_ttH_CSVLFStats2Down",
                 "_CMS_ttH_CSVCErr1Up","_CMS_ttH_CSVCErr1Down","_CMS_ttH_CSVCErr2Up","_CMS_ttH_CSVCErr2Down",
		 #"_CMS_ttH_TopPtUp","_CMS_ttH_TopPtDown",
                 "_CMS_ttH_PUUp","_CMS_ttH_PUDown",
		 "_CMS_ttH_Q2scale_ttbarOtherUp","_CMS_ttH_Q2scale_ttbarOtherDown",
                 "_CMS_ttH_Q2scale_ttbarPlusBUp","_CMS_ttH_Q2scale_ttbarPlusBDown",
                 "_CMS_ttH_Q2scale_ttbarPlus2BUp","_CMS_ttH_Q2scale_ttbarPlus2BDown",
                 "_CMS_ttH_Q2scale_ttbarPlusBBbarUp","_CMS_ttH_Q2scale_ttbarPlusBBbarDown",
                 "_CMS_ttH_Q2scale_ttbarPlusCCbarUp","_CMS_ttH_Q2scale_ttbarPlusCCbarDown",
                 #"_CMS_ttH_NNPDFUp","_CMS_ttH_NNPDFDown",
                 "_CMS_ttH_eff_muUp","_CMS_ttH_eff_muDown",  
                 "_CMS_ttH_eff_elUp","_CMS_ttH_eff_elDown",
                 "_CMS_scale_jUp","_CMS_scale_jDown",
                 "_CMS_ttH_PSscaleUp","_CMS_ttH_PSscaleDown",
                 #"","",
		 #"","",
		 #"","",
                 ]


# corresponding weight names
mu_down_sf=1.1402
mu_up_sf=0.8727
pdf_05_sf=0.950964383883
pdf_67_sf=1.04093344845


## in future use Muon SF
muSF="muonIDHelper.GetSF(muonPt,muonEta,0)*muonIsoHelper.GetSF(muonPt,muonEta,0)*muonTriggerHelper.GetSF(muonPt,muonEta,0)"
#muSF="1.0"
#usualweights="(1*Weight_PU*TMath::Sign(1.0,Weight)*"+muSF+"*Weight_CSV)"
usualweights="(1*Weight_PU*TMath::Sign(1.0,Weight)*"+muSF+"*Weight_CSV)"


systweights=["NomWeight:="+usualweights+"*(DoWeights==1)+(DoWeights==0)*1.0",
             "dummyWeight_CSVLFup:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*Weight_CSVLFup*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             "dummyWeight_CSVLFdown:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*Weight_CSVLFdown*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             "dummyWeight_CSVHFup:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*Weight_CSVHFup*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             "dummyWeight_CSVHFdown:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*Weight_CSVHFdown*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             "dummyWeight_CSVHFStats1up:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*Weight_CSVHFStats1up*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             "dummyWeight_CSVHFStats1down:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*Weight_CSVHFStats1down*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             "dummyWeight_CSVLFStats1up:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*Weight_CSVLFStats1up*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             "dummyWeight_CSVLFStats1down:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*Weight_CSVLFStats1down*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             "dummyWeight_CSVHFStats2up:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*Weight_CSVHFStats2up*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             "dummyWeight_CSVHFStats2down:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*Weight_CSVHFStats2down*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             "dummyWeight_CSVLFStats2up:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*Weight_CSVLFStats2up*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             "dummyWeight_CSVLFStats2down:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*Weight_CSVLFStats2down*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             "dummyWeight_CSVCErr1up:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*Weight_CSVCErr1up*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             "dummyWeight_CSVCErr1down:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*Weight_CSVCErr1down*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             "dummyWeight_CSVCErr2up:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*Weight_CSVCErr2up*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             "dummyWeight_CSVCErr2down:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*Weight_CSVCErr2down*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
            ####"rwtptup:=(2.0*(Weight_TopPt - 1.0)+1.0):=1*Weight_PU*Weight_CSV","rwtptdown:=Weight_TopPt:=1*Weight_PU*Weight_CSV",
             "dummyWeight_PUup:=(TMath::Sign(1.0,Weight)*Weight_PUup*"+muSF+"*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             "dummyWeight_PUdown:=(TMath::Sign(1.0,Weight)*Weight_PUdown*"+muSF+"*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             "QScaleTTLFUp:=Weight_muRueight_muRdowpmuFup*"+usualweights+"/"+str(mu_up_sf),
             "QScaleTTLFDown:=WnmuFdown*"+usualweights+"/"+str(mu_down_sf),
             "QScaleTTBUp:=Weight_muRupmuFup*"+usualweights+"/"+str(mu_up_sf),
             "QScaleTTBDown:=Weight_muRdownmuFdown*"+usualweights+"/"+str(mu_down_sf),
             "QScaleTTtwoBUp:=Weight_muRupmuFup*"+usualweights+"/"+str(mu_up_sf),
             "QScaleTTtwoBDown:=Weight_muRdownmuFdown*"+usualweights+"/"+str(mu_down_sf),
             "QScaleTTBBUp:=Weight_muRupmuFup*"+usualweights+"/"+str(mu_up_sf),
             "QScaleTTBBDown:=Weight_muRdownmuFdown*"+usualweights+"/"+str(mu_down_sf),
             "QScaleTTCCUp:=Weight_muRupmuFup*"+usualweights+"/"+str(mu_up_sf),
             "QScaleTTCCDown:=Weight_muRdownmuFdown*"+usualweights+"/"+str(mu_down_sf),
             #"PDFweightUp:=Weight_NNPDFid260067*"+usualweights+"/"+str(pdf_67_sf),
             #"PDFWeightDown:=Weight_NNPDFid260005*"+usualweights+"/"+str(pdf_05_sf),
             "dummyCMS_ttH_eff_muUp:="+usualweights+"*(DoWeights==1)*(1.01*(N_TightMuons==1)+1.0*(N_TightMuons==0))+(DoWeights==0)*1.0",
             "dummyCMS_ttH_eff_muDown:="+usualweights+"*(DoWeights==1)*(0.99*(N_TightMuons==1)+1.0*(N_TightMuons==0))+(DoWeights==0)*1.0",
             "dummyCMS_ttH_eff_elUp:="+usualweights+"*(DoWeights==1)*(1.01*(N_TightElectrons==1)+1.0*(N_TightElectrons==0))+(DoWeights==0)*1.0",
             "dummyCMS_ttH_eff_elDown:="+usualweights+"*(DoWeights==1)*(0.99*(N_TightElectrons==1)+1.0*(N_TightElectrons==0))+(DoWeights==0)*1.0",
             #"MuonIDUp:=(1*Weight_PU*muonIDHelper.GetSF(muonPt,muonEta,1)*muonIsoHelper.GetSF(muonPt,muonEta,0)*muonTriggerHelper.GetSF(muonPt,muonEta,0)*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             #"MuonIDDown:=(1*Weight_PU*muonIDHelper.GetSF(muonPt,muonEta,-1)*muonIsoHelper.GetSF(muonPt,muonEta,0)*muonTriggerHelper.GetSF(muonPt,muonEta,0)*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             #"MuonIsoUp:=(1*Weight_PU*muonIDHelper.GetSF(muonPt,muonEta,0)*muonIsoHelper.GetSF(muonPt,muonEta,1)*muonTriggerHelper.GetSF(muonPt,muonEta,0)*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             #"MuonIsoDown:=(1*Weight_PU*muonIDHelper.GetSF(muonPt,muonEta,0)*muonIsoHelper.GetSF(muonPt,muonEta,-1)*muonTriggerHelper.GetSF(muonPt,muonEta,0)*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             #"MuonTriggerUp:=(1*Weight_PU*muonIDHelper.GetSF(muonPt,muonEta,0)*muonIsoHelper.GetSF(muonPt,muonEta,0)*muonTriggerHelper.GetSF(muonPt,muonEta,1)*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             #"MuonTriggerDown:=(1*Weight_PU*muonIDHelper.GetSF(muonPt,muonEta,0)*muonIsoHelper.GetSF(muonPt,muonEta,0)*muonTriggerHelper.GetSF(muonPt,muonEta,-1)*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             ]

#systweights=["NomWeight:="+usualweights+"*(DoWeights==1)+(DoWeights==0)*1.0",
             #"dummyWeight_CSVLFup:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*csvReweighter.getCSVWeight(jetPts,jetEtas,jetCSVs,jetFlavors,9,csvWgtHF,csvWgtLF,csvWgtCF))*(DoWeights==1)+(DoWeights==0)*1.0",
             #"dummyWeight_CSVLFdown:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*csvReweighter.getCSVWeight(jetPts,jetEtas,jetCSVs,jetFlavors,10,csvWgtHF,csvWgtLF,csvWgtCF))*(DoWeights==1)+(DoWeights==0)*1.0",
             #"dummyWeight_CSVHFup:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*csvReweighter.getCSVWeight(jetPts,jetEtas,jetCSVs,jetFlavors,11,csvWgtHF,csvWgtLF,csvWgtCF))*(DoWeights==1)+(DoWeights==0)*1.0",
             #"dummyWeight_CSVHFdown:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*csvReweighter.getCSVWeight(jetPts,jetEtas,jetCSVs,jetFlavors,12,csvWgtHF,csvWgtLF,csvWgtCF))*(DoWeights==1)+(DoWeights==0)*1.0",
             #"dummyWeight_CSVHFStats1up:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*csvReweighter.getCSVWeight(jetPts,jetEtas,jetCSVs,jetFlavors,13,csvWgtHF,csvWgtLF,csvWgtCF))*(DoWeights==1)+(DoWeights==0)*1.0",
             #"dummyWeight_CSVHFStats1down:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*csvReweighter.getCSVWeight(jetPts,jetEtas,jetCSVs,jetFlavors,14,csvWgtHF,csvWgtLF,csvWgtCF))*(DoWeights==1)+(DoWeights==0)*1.0",
             #"dummyWeight_CSVLFStats1up:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*csvReweighter.getCSVWeight(jetPts,jetEtas,jetCSVs,jetFlavors,17,csvWgtHF,csvWgtLF,csvWgtCF))*(DoWeights==1)+(DoWeights==0)*1.0",
             #"dummyWeight_CSVLFStats1down:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*csvReweighter.getCSVWeight(jetPts,jetEtas,jetCSVs,jetFlavors,18,csvWgtHF,csvWgtLF,csvWgtCF))*(DoWeights==1)+(DoWeights==0)*1.0",
             #"dummyWeight_CSVHFStats2up:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*csvReweighter.getCSVWeight(jetPts,jetEtas,jetCSVs,jetFlavors,15,csvWgtHF,csvWgtLF,csvWgtCF))*(DoWeights==1)+(DoWeights==0)*1.0",
             #"dummyWeight_CSVHFStats2down:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*csvReweighter.getCSVWeight(jetPts,jetEtas,jetCSVs,jetFlavors,16,csvWgtHF,csvWgtLF,csvWgtCF))*(DoWeights==1)+(DoWeights==0)*1.0",
             #"dummyWeight_CSVLFStats2up:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*csvReweighter.getCSVWeight(jetPts,jetEtas,jetCSVs,jetFlavors,19,csvWgtHF,csvWgtLF,csvWgtCF))*(DoWeights==1)+(DoWeights==0)*1.0",
             #"dummyWeight_CSVLFStats2down:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*csvReweighter.getCSVWeight(jetPts,jetEtas,jetCSVs,jetFlavors,20,csvWgtHF,csvWgtLF,csvWgtCF))*(DoWeights==1)+(DoWeights==0)*1.0",
             #"dummyWeight_CSVCErr1up:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*csvReweighter.getCSVWeight(jetPts,jetEtas,jetCSVs,jetFlavors,21,csvWgtHF,csvWgtLF,csvWgtCF))*(DoWeights==1)+(DoWeights==0)*1.0",
             #"dummyWeight_CSVCErr1down:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*csvReweighter.getCSVWeight(jetPts,jetEtas,jetCSVs,jetFlavors,22,csvWgtHF,csvWgtLF,csvWgtCF))*(DoWeights==1)+(DoWeights==0)*1.0",
             #"dummyWeight_CSVCErr2up:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*csvReweighter.getCSVWeight(jetPts,jetEtas,jetCSVs,jetFlavors,23,csvWgtHF,csvWgtLF,csvWgtCF))*(DoWeights==1)+(DoWeights==0)*1.0",
             #"dummyWeight_CSVCErr2down:=(1*TMath::Sign(1.0,Weight)*Weight_PU*"+muSF+"*csvReweighter.getCSVWeight(jetPts,jetEtas,jetCSVs,jetFlavors,24,csvWgtHF,csvWgtLF,csvWgtCF))*(DoWeights==1)+(DoWeights==0)*1.0",
            #####"rwtptup:=(2.0*(Weight_TopPt - 1.0)+1.0):=1*Weight_PU*Weight_CSV","rwtptdown:=Weight_TopPt:=1*Weight_PU*Weight_CSV",
             #"dummyWeight_PUup:=(TMath::Sign(1.0,Weight)*Weight_PUup*"+muSF+"*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             #"dummyWeight_PUdown:=(TMath::Sign(1.0,Weight)*Weight_PUdown*"+muSF+"*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             #"QScaleTTLFUp:=Weight_muRupmuFup*"+usualweights+"/"+str(mu_up_sf),
             #"QScaleTTLFDown:=Weight_muRdownmuFdown*"+usualweights+"/"+str(mu_down_sf),
             #"QScaleTTBUp:=Weight_muRupmuFup*"+usualweights+"/"+str(mu_up_sf),
             #"QScaleTTBDown:=Weight_muRdownmuFdown*"+usualweights+"/"+str(mu_down_sf),
             #"QScaleTTtwoBUp:=Weight_muRupmuFup*"+usualweights+"/"+str(mu_up_sf),
             #"QScaleTTtwoBDown:=Weight_muRdownmuFdown*"+usualweights+"/"+str(mu_down_sf),
             #"QScaleTTBBUp:=Weight_muRupmuFup*"+usualweights+"/"+str(mu_up_sf),
             #"QScaleTTBBDown:=Weight_muRdownmuFdown*"+usualweights+"/"+str(mu_down_sf),
             #"QScaleTTCCUp:=Weight_muRupmuFup*"+usualweights+"/"+str(mu_up_sf),
             #"QScaleTTCCDown:=Weight_muRdownmuFdown*"+usualweights+"/"+str(mu_down_sf),
             #"PDFweightUp:=Weight_NNPDFid260067*"+usualweights+"/"+str(pdf_67_sf),
             #"PDFWeightDown:=Weight_NNPDFid260005*"+usualweights+"/"+str(pdf_05_sf),
             ##"MuonIDUp:=(1*Weight_PU*muonIDHelper.GetSF(muonPt,muonEta,1)*muonIsoHelper.GetSF(muonPt,muonEta,0)*muonTriggerHelper.GetSF(muonPt,muonEta,0)*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             ##"MuonIDDown:=(1*Weight_PU*muonIDHelper.GetSF(muonPt,muonEta,-1)*muonIsoHelper.GetSF(muonPt,muonEta,0)*muonTriggerHelper.GetSF(muonPt,muonEta,0)*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             ##"MuonIsoUp:=(1*Weight_PU*muonIDHelper.GetSF(muonPt,muonEta,0)*muonIsoHelper.GetSF(muonPt,muonEta,1)*muonTriggerHelper.GetSF(muonPt,muonEta,0)*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             ##"MuonIsoDown:=(1*Weight_PU*muonIDHelper.GetSF(muonPt,muonEta,0)*muonIsoHelper.GetSF(muonPt,muonEta,-1)*muonTriggerHelper.GetSF(muonPt,muonEta,0)*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             ##"MuonTriggerUp:=(1*Weight_PU*muonIDHelper.GetSF(muonPt,muonEta,0)*muonIsoHelper.GetSF(muonPt,muonEta,0)*muonTriggerHelper.GetSF(muonPt,muonEta,1)*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             ##"MuonTriggerDown:=(1*Weight_PU*muonIDHelper.GetSF(muonPt,muonEta,0)*muonIsoHelper.GetSF(muonPt,muonEta,0)*muonTriggerHelper.GetSF(muonPt,muonEta,-1)*Weight_CSV)*(DoWeights==1)+(DoWeights==0)*1.0",
             #]

#"Weight_pileupup:=((Weight_PU!=0.0) ? Weight_PUup/Weight_PU : Weight_PUup)","Weight_pileupdown:=((Weight_PU!=0.0) ? Weight_PUdown/Weight_PU : Weight_PUdown)",


assert len(systweights)==len(weightsystnames)

othersystnames=[
		"_CMS_scale_jUp",
                "_CMS_scale_jDown",
               #"_CMS_res_jUp",
               #"_CMS_res_jDown"
               "_CMS_ttH_PSscaleUp",
               "_CMS_ttH_PSscaleDown"
                ]

othersystfilenames=[
		    "JESUP",
                    "JESDOWN",
                   #"JERUP",
                   #"JERDOWN"
                   "scaleup",
                   "scaledown"
                   ]

# data samples (name, color, path to files, selection, nickname_without_special_characters,optional: number of events for cross check)

samples_data_controlplots=[Sample('SingleMu',ROOT.kBlack,path_76x+'/mu_*/*nominal*.root',sel_singlemu,'SingleMu'),
                           Sample('SingleEl',ROOT.kBlack,path_76x+'/el_*/*nominal*.root',sel_singleel,'SingleEl')
                       ]
                       
#samples_data_controlplots_swold=[Sample('SingleMu',ROOT.kBlack,path_swold+'/mu_*/*nominal*.root',sel_singlemu,'SingleMu'),
                           #Sample('SingleEl',ROOT.kBlack,path_swold+'/el_*/*nominal*.root',sel_singleel,'SingleEl')
                       #]
                       
#samples_data_bdtplots=[Sample('SingleMu',ROOT.kBlack,path_incl4252+'/mu_*/*nominal*.root',sel_singlemu,'SingleMu'),
                           #Sample('SingleEl',ROOT.kBlack,path_incl4252+'/el_*/*nominal*.root',sel_singleel,'SingleEl')
                       #]

#<<<<<<< HEAD
#ttbarMCweight='*(((0.000919641*(N_GenTopHad==1 && N_GenTopLep==1)+0.000707116*(N_GenTopLep==2 && N_GenTopHad==0)+0.0084896859*(N_GenTopHad==2 && N_GenTopLep==0))/Weight_XS )*(N_BTagsM>=4)+(0.0084896859)*(N_BTagsM<4))'
#ttbarMCweight_incl='*(0.0084896859)'
#=======
#ttbarMCweight='*(0.000919641*(N_GenTopHad==1 && N_GenTopLep==1)+0.000707116*(N_GenTopLep==2 && N_GenTopHad==0)+0.0084896859*(N_GenTopHad==2 && N_GenTopLep==0))/Weight_XS'
ttbarMCweight='*0.0084896859/Weight_XS'
#>>>>>>> 69e2a4cf566105ed512b7dd9d5b1a3d3586dfe54
samplesControlPlots=[Sample('t#bar{t}H',ROOT.kBlue+1,path_76x+'/ttH*/*nominal*.root',mcweight,'ttH',systs_all_samples) ,     
#         Sample('t#bar{t}',ROOT.kRed+1,path_76x+'/ttbar/*nominal*.root',mcweight,'ttbar') ,     
         Sample('t#bar{t}+lf',ROOT.kRed-7,path_76x+'/ttbar_????_*/*nominal*.root',mcweight+'*(GenEvt_I_TTPlusCC==0&&GenEvt_I_TTPlusBB==0)'+ttbarMCweight,'ttbarOther',systs_all_samples+systs_ttbar+systs_tt_lf,0.05),
         Sample('t#bar{t}+c#bar{c}',ROOT.kRed+1,path_76x+'/ttbar_????_*/*nominal*.root',mcweight+'*(GenEvt_I_TTPlusCC==1)'+ttbarMCweight,'ttbarPlusCCbar',systs_all_samples+systs_ttbar+systs_tt_cc,0.5),
         Sample('t#bar{t}+b',ROOT.kRed-2,path_76x+'/ttbar_????_*/*nominal*.root',mcweight+'*(GenEvt_I_TTPlusBB==1)'+ttbarMCweight,'ttbarPlusB',systs_all_samples+systs_ttbar+systs_tt_b,0.5),
         Sample('t#bar{t}+2b',ROOT.kRed+2,path_76x+'/ttbar_????_*/*nominal*.root',mcweight+'*(GenEvt_I_TTPlusBB==2)'+ttbarMCweight,'ttbarPlus2B',systs_all_samples+systs_ttbar+systs_tt_2b,0.5),
         Sample('t#bar{t}+b#bar{b}',ROOT.kRed+3,path_76x+'/ttbar_????_*/*nominal*.root',mcweight+'*(GenEvt_I_TTPlusBB==3)'+ttbarMCweight,'ttbarPlusBBbar',systs_all_samples+systs_ttbar+systs_tt_bb,0.5),  
         Sample('Single Top',ROOT.kMagenta,path_76x+'/st*/*nominal*.root',mcweightAll,'SingleTop',systs_all_samples) , 
         Sample('V+jets',ROOT.kGreen-3,path_76x+'/??ets*/*nominal*.root',mcweightAll,'Vjets',systs_all_samples) , 
         Sample('t#bar{t}+V',ROOT.kBlue-10,path_76x+'/tt?_*/*nominal*.root',mcweightAll,'ttV',systs_all_samples),         
         Sample('Diboson',ROOT.kAzure+2,path_76x+'/??/*nominal*.root',mcweightAll,'Diboson',systs_all_samples) , 
#         Sample('QCD',ROOT.kYellow ,path_76x+'/QCD*/*nominal*root',mcweight,'QCD') , 
]

ttbarMCweight='*(0.000919641*(N_GenTopHad==1 && N_GenTopLep==1)+0.000707116*(N_GenTopLep==2 && N_GenTopHad==0)+0.0084896859*(N_GenTopHad==2 && N_GenTopLep==0))/Weight_XS'

#ttbarMCweight='*0.0084896859/Weight_XS'
samplesLimits=[Sample('t#bar{t}H',ROOT.kBlue+1,path_76x+'/ttH*/*nominal*.root',mcweight,'ttH',systs_all_samples) ,     
#         Sample('t#bar{t}',ROOT.kRed+1,path_76x+'/ttbar/*nominal*.root',mcweight,'ttbar') ,     
	      Sample('t#bar{t}H, H to b#bar{b}',ROOT.kBlue+1,path_76x+'/ttHbb*/*nominal*.root',mcweight,'ttH_hbb',systs_all_samples) ,  
	      Sample('t#bar{t}H, H to c#bar{c}',ROOT.kBlue+1,path_76x+'/ttHnonbb*/*nominal*.root',mcweight+hccSel,'ttH_hcc',systs_all_samples) ,  
	      Sample('t#bar{t}H, H to #tau#tau',ROOT.kBlue+1,path_76x+'/ttHnonbb*/*nominal*.root',mcweight+httSel,'ttH_htt',systs_all_samples) ,  
	      Sample('t#bar{t}H, H to #gamma#gamma',ROOT.kBlue+1,path_76x+'/ttHnonbb*/*nominal*.root',mcweight+hggSel,'ttH_hgg',systs_all_samples) ,  
	      Sample('t#bar{t}H, H to gluglu',ROOT.kBlue+1,path_76x+'/ttHnonbb*/*nominal*.root',mcweight+hglugluSel,'ttH_hgluglu',systs_all_samples) ,  
	      Sample('t#bar{t}H, H to WW',ROOT.kBlue+1,path_76x+'/ttHnonbb*/*nominal*.root',mcweight+hwwSel,'ttH_hww',systs_all_samples) ,  
	      Sample('t#bar{t}H, H to ZZ',ROOT.kBlue+1,path_76x+'/ttHnonbb*/*nominal*.root',mcweight+hzzSel,'ttH_hzz',systs_all_samples) ,  
	      Sample('t#bar{t}H, H to #gamma Z',ROOT.kBlue+1,path_76x+'/ttHnonbb*/*nominal*.root',mcweight+hzgSel,'ttH_hzg',systs_all_samples) , Sample('t#bar{t}+lf',ROOT.kRed-7,path_76x+'/ttbar_????_*/*nominal*.root',mcweight+'*(GenEvt_I_TTPlusCC==0&&GenEvt_I_TTPlusBB==0)'+ttbarMCweight,'ttbarOther',systs_all_samples+systs_ttbar+systs_tt_lf,0.05), Sample('t#bar{t}+c#bar{c}',ROOT.kRed+1,path_76x+'/ttbar_????_*/*nominal*.root',mcweight+'*(GenEvt_I_TTPlusCC==1)'+ttbarMCweight,'ttbarPlusCCbar',systs_all_samples+systs_ttbar+systs_tt_cc,0.5),
	      Sample('t#bar{t}+b',ROOT.kRed-2,path_76x+'/ttbar_????_*/*nominal*.root',mcweight+'*(GenEvt_I_TTPlusBB==1)'+ttbarMCweight,'ttbarPlusB',systs_all_samples+systs_ttbar+systs_tt_b,0.5),
	      Sample('t#bar{t}+2b',ROOT.kRed+2,path_76x+'/ttbar_????_*/*nominal*.root',mcweight+'*(GenEvt_I_TTPlusBB==2)'+ttbarMCweight,'ttbarPlus2B',systs_all_samples+systs_ttbar+systs_tt_2b,0.5), Sample('t#bar{t}+b#bar{b}',ROOT.kRed+3,path_76x+'/ttbar_????_*/*nominal*.root',mcweight+'*(GenEvt_I_TTPlusBB==3)'+ttbarMCweight,'ttbarPlusBBbar',systs_all_samples+systs_ttbar+systs_tt_bb,0.5),
	      Sample('Single Top',ROOT.kMagenta,path_excl4252+'/st*/*nominal*.root',mcweightAll,'singlet',systs_all_samples) , 
	      Sample('Z+jets',ROOT.kGreen-3,path_excl4252+'/Zjets*/*nominal*.root',mcweightAll,'zjets',systs_all_samples) , 
	      Sample('W+jets',ROOT.kGreen-7,path_excl4252+'/WJets*/*nominal*.root',mcweightAll,'wjets',systs_all_samples) , 
	      Sample('t#bar{t}+W',ROOT.kBlue-10,path_excl4252+'/ttW_*/*nominal*.root',mcweightAll,'ttbarW',systs_all_samples),
	      Sample('t#bar{t}+Z',ROOT.kBlue-6,path_excl4252+'/ttZ_*/*nominal*.root',mcweightAll,'ttbarZ',systs_all_samples),
	      Sample('Diboson',ROOT.kAzure+2,path_excl4252+'/??/*nominal*.root',mcweightAll,'diboson',systs_all_samples) , 
	      #Sample('QCD',ROOT.kYellow ,path_76x+'/QCD*/*nominal*root',mcweightAll,'QCD') , 
]





