import sys
import os
sys.path.append('pyroot-plotscripts-base')
sys.path.append('pyroot-plotscripts-base/limittools')

from scriptgenerator import *
from plotutils import *

weightSystNames=["",
                 "_CMS_btag_lfUp","_CMS_btag_lfDown","_CMS_btag_hfUp","_CMS_btag_hfDown",
                 "_CMS_btag_hfstats1Up","_CMS_btag_hfstats1Down","_CMS_btag_lfstats1Up","_CMS_btag_lfstats1Down",
                 "_CMS_btag_hfstats2Up","_CMS_btag_hfstats2Down","_CMS_btag_lfstats2Up","_CMS_btag_lfstats2Down",
                 "_CMS_btag_cferr1Up","_CMS_btag_cferr1Down","_CMS_btag_cferr2Up","_CMS_btag_cferr2Down",
                 ]

common_weight= "1.0*((Weight_GEN_nom>0.)*1+(Weight_GEN_nom<0.)*(-1))*Weight_CSV*Weight_PU"

systWeights=[   "NomWeight:="+common_weight+"*(DoWeights==1)+(DoWeights==0)*1.0",
                "dummyWeight_CSVLFup:="+common_weight+"*Weight_CSVLFup*(DoWeights==1)+(DoWeights==0)*1.0",
                "dummyWeight_CSVLFdown:="+common_weight+"*Weight_CSVLFdown*(DoWeights==1)+(DoWeights==0)*1.0",
                "dummyWeight_CSVHFup:="+common_weight+"*Weight_CSVHFup*(DoWeights==1)+(DoWeights==0)*1.0",
                "dummyWeight_CSVHFdown:="+common_weight+"*Weight_CSVHFdown*(DoWeights==1)+(DoWeights==0)*1.0",
                "dummyWeight_CSVHFStats1up:="+common_weight+"*Weight_CSVHFStats1up*(DoWeights==1)+(DoWeights==0)*1.0",
                "dummyWeight_CSVHFStats1down:="+common_weight+"*Weight_CSVHFStats1down*(DoWeights==1)+(DoWeights==0)*1.0",
                "dummyWeight_CSVLFStats1up:="+common_weight+"*Weight_CSVLFStats1up*(DoWeights==1)+(DoWeights==0)*1.0",
                "dummyWeight_CSVLFStats1down:="+common_weight+"*Weight_CSVLFStats1down*(DoWeights==1)+(DoWeights==0)*1.0",
                "dummyWeight_CSVHFStats2up:="+common_weight+"*Weight_CSVHFStats2up*(DoWeights==1)+(DoWeights==0)*1.0",
                "dummyWeight_CSVHFStats2down:="+common_weight+"*Weight_CSVHFStats2down*(DoWeights==1)+(DoWeights==0)*1.0",
                "dummyWeight_CSVLFStats2up:="+common_weight+"*Weight_CSVLFStats2up*(DoWeights==1)+(DoWeights==0)*1.0",
                "dummyWeight_CSVLFStats2down:="+common_weight+"*Weight_CSVLFStats2down*(DoWeights==1)+(DoWeights==0)*1.0",
                "dummyWeight_CSVCErr1up:="+common_weight+"*Weight_CSVCErr1up*(DoWeights==1)+(DoWeights==0)*1.0",
                "dummyWeight_CSVCErr1down:="+common_weight+"*Weight_CSVCErr1down*(DoWeights==1)+(DoWeights==0)*1.0",
                "dummyWeight_CSVCErr2up:="+common_weight+"*Weight_CSVCErr2up*(DoWeights==1)+(DoWeights==0)*1.0",
                "dummyWeight_CSVCErr2down:="+common_weight+"*Weight_CSVCErr2down*(DoWeights==1)+(DoWeights==0)*1.0"
                ]
otherSystNames=[]
otherSystFileNames=[]

MCWeight='35.91823'

path_ntuples = "/nfs/dust/cms/user/mwassmer/DarkMatter/ntuples"

sampleDict=SampleDictionary()
sampleDict.doPrintout()

sel_MET="*(Triggered_HLT_PFMET170_X==1||Triggered_HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_X==1||Triggered_HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_X==1||Triggered_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_X==1||Triggered_HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_X==1)"

"""
Triggered_HLT_EcalHT800
Triggered_HLT_Ele105_CaloIdVT_GsfTrkIdT
Triggered_HLT_Ele27_WPTight
Triggered_HLT_PFMET170_X
Triggered_HLT_PFMETNoMu100_PFMHTNoMu100_IDTight
Triggered_HLT_PFMETNoMu110_PFMHTNoMu110_IDTight
Triggered_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight
Triggered_HLT_PFMETNoMu90_PFMHTNoMu90_IDTight
Triggered_HLT_Photon165_HE10
Triggered_HLT_Photon175
"""
"""
Sample('Z(#nu#nu)+jets p_{T,Z}=50-100',ROOT.kBlue,path_ntuples+'/DYJetsToNuNu_PtZ-50To100*/*nominal*.root',"1.13*3"+"*"+MCWeight+sel_MET,'Z_nunu_jets_e',[""],samDict=sampleDict),
Sample('Z(#nu#nu)+jets p_{T,Z}=100-250',ROOT.kBlue+2,path_ntuples+'/DYJetsToNuNu_PtZ-100To250*/*nominal*.root',"1.11*3"+"*"+MCWeight+sel_MET,'Z_nunu_jets_a',[""],samDict=sampleDict),
Sample('Z(#nu#nu)+jets p_{T,Z}=250-400',ROOT.kBlue+4,path_ntuples+'/DYJetsToNuNu_PtZ-250To400*/*nominal*.root',"1.16*3"+"*"+MCWeight+sel_MET,'Z_nunu_jets_b',[""],samDict=sampleDict),
Sample('Z(#nu#nu)+jets p_{T,Z}=400-650',ROOT.kBlue+6,path_ntuples+'/DYJetsToNuNu_PtZ-400To650*/*nominal*.root',"1.25*3"+"*"+MCWeight+sel_MET,'Z_nunu_jets_c',[""],samDict=sampleDict),
Sample('Z(#nu#nu)+jets p_{T,Z}=650-Inf',ROOT.kBlue+8,path_ntuples+'/DYJetsToNuNu_PtZ-650ToInf*/*nominal*.root',"1.41*3"+"*"+MCWeight+sel_MET,'Z_nunu_jets_d',[""],samDict=sampleDict),
                                                                                               	
Sample('W(l#nu)+jets P_{T,W}=100-250',ROOT.kGreen-7,path_ntuples+'/WJetsToLNu_Pt-100To250*/*nominal*.root',"1.14*"+MCWeight+sel_MET,'W_lnu_jets_a',[""],samDict=sampleDict),
Sample('W(l#nu)+jets p_{T,W}=250-400',ROOT.kGreen-6,path_ntuples+'/WJetsToLNu_Pt-250To400*/*nominal*.root',"1.17*"+MCWeight+sel_MET,'W_lnu_jets_b',[""],samDict=sampleDict),
Sample('W(l#nu)+jets p_{T,W}=400-600',ROOT.kGreen-5,path_ntuples+'/WJetsToLNu_Pt-400To600*/*nominal*.root',"1.24*"+MCWeight+sel_MET,'W_lnu_jets_c',[""],samDict=sampleDict),
Sample('W(l#nu)+jets p_{T,W}=600-Inf',ROOT.kGreen-4,path_ntuples+'/WJetsToLNu_Pt-600ToInf*/*nominal*.root',"1.34*"+MCWeight+sel_MET,'W_lnu_jets_d',[""],samDict=sampleDict),
                                                                                               	                                                                                                
"""

samples_data = [
            Sample('MET',ROOT.kBlack,path_ntuples+'/MET_Run2016*/*nominal*.root',"1."+sel_MET,'MET',[""],samDict=sampleDict),
            #Sample('test_d',ROOT.kGreen-7,path_ntuples+'/test/*nominal*.root',"1.",'test_d',[""],samDict=sampleDict)
        ]

samples_background = [
                        Sample('Z(#nu#nu)+jets p_{T,Z}=50-100',ROOT.kBlue,path_ntuples+'/DYJetsToNuNu_PtZ-50To100*/*nominal*.root',"1.*3*0.971"+"*"+MCWeight+sel_MET,'Z_nunu_jets_e',weightSystNames,samDict=sampleDict),
                        Sample('Z(#nu#nu)+jets p_{T,Z}=100-250',ROOT.kBlue+2,path_ntuples+'/DYJetsToNuNu_PtZ-100To250*/*nominal*.root',"1.*3*0.971"+"*"+MCWeight+sel_MET,'Z_nunu_jets_a',weightSystNames,samDict=sampleDict),
                        Sample('Z(#nu#nu)+jets p_{T,Z}=250-400',ROOT.kBlue-2,path_ntuples+'/DYJetsToNuNu_PtZ-250To400*/*nominal*.root',"1.*3*0.971"+"*"+MCWeight+sel_MET,'Z_nunu_jets_b',weightSystNames,samDict=sampleDict),
                        Sample('Z(#nu#nu)+jets p_{T,Z}=400-650',ROOT.kBlue+6,path_ntuples+'/DYJetsToNuNu_PtZ-400To650*/*nominal*.root',"1.*3*0.971"+"*"+MCWeight+sel_MET,'Z_nunu_jets_c',weightSystNames,samDict=sampleDict),
                        Sample('Z(#nu#nu)+jets p_{T,Z}=650-Inf',ROOT.kBlue+8,path_ntuples+'/DYJetsToNuNu_PtZ-650ToInf*/*nominal*.root',"1.*3*0.971"+"*"+MCWeight+sel_MET,'Z_nunu_jets_d',weightSystNames,samDict=sampleDict),

                        Sample('W(l#nu)+jets P_{T,W}=100-250',ROOT.kGreen-7,path_ntuples+'/WJetsToLNu_Pt-100To250*/*nominal*.root',"1.*"+MCWeight+sel_MET,'W_lnu_jets_a',weightSystNames,samDict=sampleDict),
                        Sample('W(l#nu)+jets p_{T,W}=250-400',ROOT.kGreen-6,path_ntuples+'/WJetsToLNu_Pt-250To400*/*nominal*.root',"1.*"+MCWeight+sel_MET,'W_lnu_jets_b',weightSystNames,samDict=sampleDict),
                        Sample('W(l#nu)+jets p_{T,W}=400-600',ROOT.kGreen-5,path_ntuples+'/WJetsToLNu_Pt-400To600*/*nominal*.root',"1.*"+MCWeight+sel_MET,'W_lnu_jets_c',weightSystNames,samDict=sampleDict),
                        Sample('W(l#nu)+jets p_{T,W}=600-Inf',ROOT.kGreen-4,path_ntuples+'/WJetsToLNu_Pt-600ToInf*/*nominal*.root',"1.*"+MCWeight+sel_MET,'W_lnu_jets_d',weightSystNames,samDict=sampleDict),
                        
                        Sample('Diboson',ROOT.kYellow-8,path_ntuples+'/??/*nominal*.root',"1."+"*"+MCWeight+sel_MET,'Diboson',weightSystNames,samDict=sampleDict),
                        Sample('Single Top',ROOT.kYellow-1,path_ntuples+'/st*/*nominal*.root',"1."+"*"+MCWeight+sel_MET,'singletop',weightSystNames,samDict=sampleDict),
                        Sample('t#bar{t}',ROOT.kYellow+2,path_ntuples+'/TT_Tune*/*nominal*.root',"1."+"*"+MCWeight+sel_MET,'ttbar',weightSystNames,samDict=sampleDict),
                        Sample('Z(ll)+jets',ROOT.kYellow+4,path_ntuples+'/DYJetsToLL*/*nominal*.root',"1."+"*"+MCWeight+sel_MET,'Z_ll_jets',weightSystNames,samDict=sampleDict),
                        Sample('QCD',ROOT.kYellow-4,path_ntuples+'/QCD*/*nominal*.root',"1."+"*"+MCWeight+sel_MET,'QCD',weightSystNames,samDict=sampleDict),
                        ]

samples_signal = [
                        Sample('VM1000m300',ROOT.kRed,path_ntuples+'/DMV_NNPDF30_Axial_Mphi-1000_Mchi-300_gSM-0p25_gDM-1p0_v2_13TeV-powheg/*nominal*.root',"1."+"*"+MCWeight+sel_MET,'DMVMed1000DM300',weightSystNames,samDict=sampleDict),
                        #Sample('test_s',ROOT.kGreen-7,path_ntuples+'/test/*nominal*.root',"1."+"*"+MCWeight,'test_s',[""],samDict=sampleDict)
			#Sample('MET',ROOT.kBlack,path_ntuples+'/MET_Run2016*/*nominal*.root',"1."+sel_MET,'MET',samDict=sampleDict)    
    ]
