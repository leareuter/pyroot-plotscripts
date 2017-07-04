from top_mass_analysis_systs import *
#sys.path.insert(0, 'limittools')
from limittools import renameHistos
from scriptgenerator import *

# name 
name = "top_mass_analysis"

# used samples
path_samples = "/nfs/dust/cms/user/mwassmer/ntuples/additional_samples/"
path_ttbar_nom = "/nfs/dust/cms/user/kelmorab/trees_Spring17_v4/"

# information to evaluate the bdts 
bdtweightpath="/nfs/dust/cms/user/kelmorab/Spring17BDTWeights/"
bdtset="Spring17v1"

# internal names of the samples
names_samples = ["ttbar_mtop1665","ttbar_mtop1695","ttbar_mtop1715","ttbar_mtop1735","ttbar_mtop1755","ttbar_mtop1785","ttbar_color_reco"]

# names for the legend
nicks_samples = ["t#bar{t} m_{t}=166.5","t#bar{t} m_{t}=169.5","t#bar{t} m_{t}=171.5","t#bar{t} m_{t}=173.5","t#bar{t} m_{t}=175.5","t#bar{t} m_{t}=178.5","t#bar{t} color reco"]

# colors for the samples
colors_samples= [ROOT.kRed,ROOT.kBlue,ROOT.kGreen,ROOT.kCyan,ROOT.kOrange,ROOT.kMagenta,ROOT.kViolet+2]

# weights for the samples
weights_samples= ["1.18133776614","1.08624210759/Weight_XS*0.014207776","1.0278242413","0.973053941949","0.921669872276","0.850422955127","1.0"]

# define the samples with variated top masses with the Sample class
samples = [Sample(nicks_samples[i],colors_samples[i],path_samples+names_samples[i]+"/*nominal*.root",weights_samples[i]+"*"+mcweightAll,names_samples[i],[""],0,None,"",-1,'MVATree') for i in range(len(names_samples))]

# define the reference samples with the Sample Class
sample_ttbar_nom = [Sample("t#bar{t} m_{t}=172.5",ROOT.kBlack,path_ttbar_nom+"ttbar_incl/*nominal*.root",mcweightAll,"ttbar_nom",weightsystnames+othersystnames,0,None,"",-1,'MVATree')]

# book some variables which are no in the tree in the first place
additionalvariables=[ 'finalbdt_ljets_j4_t3:='+bdtweightpath+'/weights_Final_43_'+bdtset+'.xml',
                      'finalbdt_ljets_j4_t4:='+bdtweightpath+'/weights_Final_44_'+bdtset+'.xml',
                      'finalbdt_ljets_j5_t3:='+bdtweightpath+'/weights_Final_53_'+bdtset+'.xml',
                      'finalbdt_ljets_j5_tge4:='+bdtweightpath+'/weights_Final_54_'+bdtset+'.xml',
                      'finalbdt_ljets_jge6_t2:='+bdtweightpath+'/weights_Final_62_'+bdtset+'.xml',
                      'finalbdt_ljets_jge6_t3:='+bdtweightpath+'/weights_Final_63_'+bdtset+'.xml',
                      'finalbdt_ljets_jge6_tge4:='+bdtweightpath+'/weights_Final_64_'+bdtset+'.xml',
                      "Muon_Pt","Electron_Pt","Muon_Eta","Electron_Eta","Jet_Pt","Jet_Eta","Jet_CSV","Jet_Flav","N_Jets","Jet_Phi","Jet_E","Jet_M",
                      "Evt_Pt_PrimaryLepton","Evt_E_PrimaryLepton","Evt_M_PrimaryLepton","Evt_Phi_PrimaryLepton","Evt_Eta_PrimaryLepton",
                      "Weight_CSV","Weight_CSVLFup","Weight_CSVLFdown","Weight_CSVHFup","Weight_CSVHFdown","Weight_CSVHFStats1up","Weight_CSVHFStats1down","Weight_CSVLFStats1up","Weight_CSVLFStats1down","Weight_CSVHFStats2up","Weight_CSVHFStats2down","Weight_CSVLFStats2up","Weight_CSVLFStats2down","Weight_CSVCErr1up","Weight_CSVCErr1down","Weight_CSVCErr2up","Weight_CSVCErr2down","N_TightMuons","N_TightElectrons"
]

# definition of categories
categoriesJT=[
              ("(N_Jets>=4&&N_BTagsM>=2)","4j2t",""),
              ("(N_Jets>=6&&N_BTagsM==2)","6j2t",""),
              ("(N_Jets==4&&N_BTagsM==3)","4j3t",""),
              ("(N_Jets==5&&N_BTagsM==3)","5j3t",""),
              ("(N_Jets>=6&&N_BTagsM==3)","6j3t",""),
              ("(N_Jets==4&&N_BTagsM>=4)","4j4t",""),
              ("(N_Jets==5&&N_BTagsM>=4)","5j4t",""),
              ("(N_Jets>=6&&N_BTagsM>=4)","6j4t","")
]

# parameters for the bdt output histograms
nhistobins= [  20,20, 	10,   10,    10,    10,   20,   10,   10 ]
minxvals=   [ 200, 200, -0.75,  -0.8, -0.8,   -0.8, -0.8, -0.8,   -0.8]
maxxvals=   [800,800,    0.8,  0.75,   0.8,    0.7,  0.8,  0.8,    0.7]
discrs =    ['finalbdt_ljets_j4_t3', 'finalbdt_ljets_j4_t4', 'finalbdt_ljets_j5_t3', 'finalbdt_ljets_j5_tge4', 'finalbdt_ljets_jge6_t2', 'finalbdt_ljets_jge6_t3', 'finalbdt_ljets_jge6_tge4']
bdts=[]
bins= [c[0] for c in categoriesJT]
binlabels= [c[1] for c in categoriesJT]
for discr,b,bl,nb,minx,maxx in zip(discrs,bins,binlabels,nhistobins,minxvals,maxxvals):
  bdts.append(Plot(ROOT.TH1F("finaldiscr_"+bl,"final discriminator ("+bl+")",nb,minx,maxx),discr,b))

# selections for categories
categoriesJTsel="("+categoriesJT[0][0]
for cat in categoriesJT[1:]:
  categoriesJTsel+="||"+cat[0]
categoriesJTsel+=")"


# category strings
catstringJT="0"
for i,cat in enumerate(categoriesJT):
    catstringJT+=("+"+str(i+1)+"*"+cat[0])
    
systsamples=[]    
for sysname,sysfilename in zip(othersystnames,othersystfilenames):
    systsamples.append(Sample(sample_ttbar_nom[0].name+sysname,sample_ttbar_nom[0].color,sample_ttbar_nom[0].path.replace("nominal",sysfilename),sample_ttbar_nom[0].selection,sample_ttbar_nom[0].nick+sysname))
   
# define the plots with some selection    
    
plotlabel="1 lepton, #geq 4 jets, #geq 2 b-tags"
plotselection="(N_Jets>=4&&N_BTagsM>=2)"
plots_inclusive=[
        Plot(ROOT.TH1F("JT" ,"jet-tag categories",len(categoriesJT),0.5,0.5+len(categoriesJT)),catstringJT,categoriesJTsel,"1 lepton"),
    #Plot(ROOT.TH1F("BCAT" ,"jet-tag + boosted categories",len(categoriesJTB),0.5,0.5+len(categoriesJTB)),catstringJTB,categoriesJTBsel,"1 lepton"),
    Plot(ROOT.TH1F("N_Jets","Number of ak4 jets",7,3.5,10.5),"N_Jets",plotselection,plotlabel),
    Plot(ROOT.TH1F("N_BTagsM","Number of b-tags",4,1.5,5.5),"N_BTagsM",plotselection,plotlabel),
    Plot(ROOT.TH1F("CSV0","B-tag of leading jet",22,-.1,1),"Jet_CSV[0]",plotselection,plotlabel),
    Plot(ROOT.TH1F("CSV1","B-tag of second jet",22,-.1,1),"Jet_CSV[1]",plotselection,plotlabel),
    Plot(ROOT.TH1F("CSV","B-tag of all jets",22,-.1,1),"Jet_CSV",plotselection,plotlabel),

    #Plot(ROOT.TH1F("CSV0NPVgeq20","B-tag of leading jet (NPV#geq20)",22,-.1,1),"Jet_CSV[0]",plotselection+"*(N_PrimaryVertices>=20)",plotlabel),
    #Plot(ROOT.TH1F("CSV1NPVgeq20","B-tag of second jet (NPV#geq20)",22,-.1,1),"Jet_CSV[1]",plotselection+"*(N_PrimaryVertices>=20)",plotlabel),
    #Plot(ROOT.TH1F("CSVNPVgeq20","B-tag of all jets (NPV#geq20)",22,-.1,1),"Jet_CSV",plotselection+"*(N_PrimaryVertices>=20)",plotlabel),

    #Plot(ROOT.TH1F("CSV0NPV15to20","B-tag of leading jet (15#leqNPV#leq20)",22,-.1,1),"Jet_CSV[0]",plotselection+"*(N_PrimaryVertices<=20 && N_PrimaryVertices>=15)",plotlabel),
    #Plot(ROOT.TH1F("CSV1NPV15to20","B-tag of second jet (15#leqNPV#leq20)",22,-.1,1),"Jet_CSV[1]",plotselection+"*(N_PrimaryVertices<=20 && N_PrimaryVertices>=15)",plotlabel),
    #Plot(ROOT.TH1F("CSVNPV15to20","B-tag of all jets (15#leqNPV#leq20)",22,-.1,1),"Jet_CSV",plotselection+"*(N_PrimaryVertices<=20 && N_PrimaryVertices>=15)",plotlabel),

    #Plot(ROOT.TH1F("CSV0NPV10to15","B-tag of leading jet (10#leqNPV#leq15)",22,-.1,1),"Jet_CSV[0]",plotselection+"*(N_PrimaryVertices<=15 && N_PrimaryVertices>=10)",plotlabel),
    #Plot(ROOT.TH1F("CSV1NPV10to15","B-tag of second jet (10#leqNPV#leq15)",22,-.1,1),"Jet_CSV[1]",plotselection+"*(N_PrimaryVertices<=15 && N_PrimaryVertices>=10)",plotlabel),
    #Plot(ROOT.TH1F("CSVNPV10to15","B-tag of all jets (10#leqNPV#leq15)",22,-.1,1),"Jet_CSV",plotselection+"*(N_PrimaryVertices<=15 && N_PrimaryVertices>=10)",plotlabel),

    #Plot(ROOT.TH1F("CSV0NPV0to10","B-tag of leading jet (0#leqNPV#leq10)",22,-.1,1),"Jet_CSV[0]",plotselection+"*(N_PrimaryVertices<=10 && N_PrimaryVertices>=0)",plotlabel),
    #Plot(ROOT.TH1F("CSV1NPV0to10","B-tag of second jet (0#leqNPV#leq10)",22,-.1,1),"Jet_CSV[1]",plotselection+"*(N_PrimaryVertices<=10 && N_PrimaryVertices>=0)",plotlabel),
    #Plot(ROOT.TH1F("CSVNPV0to10","B-tag of all jets (0#leqNPV#leq10)",22,-.1,1),"Jet_CSV",plotselection+"*(N_PrimaryVertices<=10 && N_PrimaryVertices>=0)",plotlabel),


    Plot(ROOT.TH1F("pt1","p_{T} of leading jet",50,0,500),"Jet_Pt[0]",plotselection,plotlabel),
    Plot(ROOT.TH1F("pt2","p_{T} of second jet",50,0,500),"Jet_Pt[1]",plotselection,plotlabel),
    Plot(ROOT.TH1F("pt3","p_{T} of third jet",40,0,400),"Jet_Pt[2]",plotselection,plotlabel),
    Plot(ROOT.TH1F("pt4","p_{T} of fourth jet",60,0,300),"Jet_Pt[3]",plotselection,plotlabel),
    Plot(ROOT.TH1F("pt5","p_{T} of fifth jet",40,0,200),"Jet_Pt[4]",plotselection,plotlabel),
    Plot(ROOT.TH1F("pt6","p_{T} of sixth jet",40,0,200),"Jet_Pt[5]",plotselection,plotlabel),
    #Plot(ROOT.TH1F("pt2tagged","p_{T} of second tagged jet",50,0,500),"TaggedJet_Pt[1]",plotselection,plotlabel),
    #Plot(ROOT.TH1F("pt1tagged","p_{T} of leading tagged jet",50,0,500),"TaggedJet_Pt[0]",plotselection,plotlabel),
    #Plot(ROOT.TH1F("pt3tagged","p_{T} of third tagged jet",40,0,400),"TaggedJet_Pt[2]",plotselection,plotlabel),
    #Plot(ROOT.TH1F("pt4tagged","p_{T} of fourth tagged jet",60,0,300),"TaggedJet_Pt[3]",plotselection,plotlabel),


    Plot(ROOT.TH1F("eta1","#eta of leading jet",50,-2.5,2.5),"Jet_Eta[0]",plotselection,plotlabel),
    Plot(ROOT.TH1F("eta2","#eta of second jet",50,-2.5,2.5),"Jet_Eta[1]",plotselection,plotlabel),
    Plot(ROOT.TH1F("phij1","#phi of leading jet",64,-3.2,3.2),"Jet_Phi[0]",plotselection,plotlabel),
    Plot(ROOT.TH1F("phij2","#phi of second jet",64,-3.2,3.2),"Jet_Phi[1]",plotselection,plotlabel),
    Plot(ROOT.TH1F("Evt_HT_Jets","Sum p_{T} jets",75,0,1500),"Evt_HT_Jets",plotselection,plotlabel),
    Plot(ROOT.TH1F("ptalljets","p_{T} of all jets",60,0,300),"Jet_Pt",plotselection,plotlabel),
    Plot(ROOT.TH1F("csvalljets","csv of all jets",44,-.1,1),"Jet_CSV",plotselection,plotlabel),
    Plot(ROOT.TH1F("leppt","lepton p_{T}",50,0,200),"LooseLepton_Pt[0]",plotselection,plotlabel),
    Plot(ROOT.TH1F("lepeta","lepton #eta",50,-2.5,2.5),"LooseLepton_Eta[0]",plotselection,plotlabel),
    Plot(ROOT.TH1F("elleppt","electron p_{T}",50,0,200),"Electron_Pt[0]",'Electron_Pt[0]>10',plotlabel),
    Plot(ROOT.TH1F("ellepeta","electron #eta",50,-2.5,2.5),"Electron_Eta[0]",'Electron_Pt[0]>10',plotlabel),
    Plot(ROOT.TH1F("muleppt","muon p_{T}",50,0,200),"Muon_Pt[0]",'Muon_Pt[0]>10',plotlabel),
    Plot(ROOT.TH1F("mulepeta","muon #eta",50,-2.5,2.5),"Muon_Eta[0]",'Muon_Pt[0]>10',plotlabel),

    #Plot(ROOT.TH1F("Prescale_HLT_Ele27_eta2p1_WPTight_Gsf_vX","Prescale_HLT_Ele27_eta2p1_WPTight_Gsf_vX",50,0,2.0),"Prescale_HLT_Ele27_eta2p1_WPTight_Gsf_vX",plotselection,plotlabel),
    #Plot(ROOT.TH1F("Prescale_HLT_IsoMu22_vX","Prescale_HLT_IsoMu22_vX",50,0,2.0),"Prescale_HLT_IsoMu22_vX",plotselection,plotlabel),
    #Plot(ROOT.TH1F("Prescale_HLT_IsoTkMu22_vX","Prescale_HLT_IsoTkMu22_vX",50,0,2.0),"Prescale_HLT_IsoTkMu22_vX",plotselection,plotlabel),

    Plot(ROOT.TH1F("eliso","electron relative isolation",50,0,0.15),"Electron_RelIso[0]",plotselection,plotlabel),
    Plot(ROOT.TH1F("muiso","muon relative isolation",50,0,0.15),"Muon_RelIso[0]",plotselection,plotlabel),
    Plot(ROOT.TH1F("MET","missing transverse energy",50,0,200),"Evt_Pt_MET",plotselection,plotlabel),
    Plot(ROOT.TH1F("METphi","MET #phi",64,-3.2,3.2),"Evt_Phi_MET",plotselection,plotlabel),
    Plot(ROOT.TH1F("N_PrimaryVertices","Reconstructed primary vertices",26,-.5,25.5),"N_PrimaryVertices",plotselection,plotlabel),
    Plot(ROOT.TH1F("blrAll","B-tagging likelihood ratio",44,-6,10),"TMath::Log(Evt_blr_ETH/(1-Evt_blr_ETH))",plotselection,plotlabel),
    Plot(ROOT.TH1F("Evt_M_MinDeltaRJets","dijet mass of closest jets",30,0.,150),"Evt_M_MinDeltaRJets",plotselection,plotlabel),
    Plot(ROOT.TH1F("Evt_M_MinDeltaRTaggedJets","mass of closest tagged jets",45,0.,450),"Evt_M_MinDeltaRTaggedJets",plotselection,plotlabel),
    Plot(ROOT.TH1F("Evt_Dr_MinDeltaRJets","#Delta R of closest jets",50,0.,5.0),"Evt_Dr_MinDeltaRJets",plotselection,plotlabel),
    Plot(ROOT.TH1F("Evt_Dr_MinDeltaRTaggedJets","#Delta R of closest tagged jets",50,0.,5.0),"Evt_Dr_MinDeltaRTaggedJets",plotselection,plotlabel),
    Plot(ROOT.TH1F("Evt_Jet_MaxDeta_Jets","max #Delta #eta (jet,jet)",50,0.,5.0),"Evt_Jet_MaxDeta_Jets",plotselection,plotlabel),
    Plot(ROOT.TH1F("Evt_TaggedJet_MaxDeta_Jets","max #Delta #eta (tag,jet)",50,0.,5.0),"Evt_TaggedJet_MaxDeta_Jets",plotselection,plotlabel),
    Plot(ROOT.TH1F("Evt_TaggedJet_MaxDeta_TaggedJets","max #Delta #eta (tag,tag)",60,0.,6.0),"Evt_TaggedJet_MaxDeta_TaggedJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F("Evt_H1","Evt_H1",60,-0.2,0.4),"Evt_H1",plotselection,plotlabel),
    #Plot(ROOT.TH1F("Evt_H2","Evt_H2",60,-0.2,0.4),"Evt_H2",plotselection,plotlabel),
    #Plot(ROOT.TH1F("Evt_H3","Evt_H3",50,-0.05,1.05),"Evt_H3",plotselection,plotlabel),
    #Plot(ROOT.TH1F("Evt_H4","Evt_H4",50,-0.15,0.35),"Evt_H4",plotselection,plotlabel),
    #Plot(ROOT.TH1F("Sphericity","Sphericity",50,0,1),"Evt_Sphericity",plotselection,plotlabel),
    #Plot(ROOT.TH1F("Aplanarity","Aplanarity",50,0,0.5),"Evt_Aplanarity",plotselection,plotlabel),
    #Plot(ROOT.TH1F("Evt_Deta_UntaggedJetsAverage","avg. #Delta #eta of untagged jets",45,0.,4.5),"Evt_Deta_UntaggedJetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F("Evt_Deta_TaggedJetsAverage","avg. #Delta #eta of tagged jets",45,0.,4.5),"Evt_Deta_TaggedJetsAverage",plotselection,plotlabel),
]

plotlabel="1 lepton, 4 jets, 3 b-tags"
plotselection=categoriesJT[1][0]
plotprefix="s43_"
plots43=[
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_Evt_CSV_Average","BDT_common5_input_Evt_CSV_Average",30,0.6,1.0),"BDT_common5_input_Evt_CSV_Average",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_Evt_Deta_JetsAverage","BDT_common5_input_Evt_Deta_JetsAverage",30,0.0,3.4),"BDT_common5_input_Evt_Deta_JetsAverage",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_HT","BDT_common5_input_HT",30,0.0,1000.0),"BDT_common5_input_HT",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_M3","BDT_common5_input_M3",30,0.0,600.0),"BDT_common5_input_M3",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_MET","BDT_common5_input_MET",30,0.0,300.0),"BDT_common5_input_MET",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_MHT","BDT_common5_input_MHT",30,0.0,250.0),"BDT_common5_input_MHT",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_Mlb","BDT_common5_input_Mlb",30,0.0,250.0),"BDT_common5_input_Mlb",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_all_sum_pt_with_met","BDT_common5_input_all_sum_pt_with_met",30,200,900.0),"BDT_common5_input_all_sum_pt_with_met",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_aplanarity","BDT_common5_input_aplanarity",30,0.0,0.4),"BDT_common5_input_aplanarity",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_avg_btag_disc_btags","BDT_common5_input_avg_btag_disc_btags",30,0.8,1.0),"BDT_common5_input_avg_btag_disc_btags",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_avg_dr_tagged_jets","BDT_common5_input_avg_dr_tagged_jets",30,0.0,5.0),"BDT_common5_input_avg_dr_tagged_jets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_best_higgs_mass","BDT_common5_input_best_higgs_mass",30,0.0,200.0),"BDT_common5_input_best_higgs_mass",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_closest_tagged_dijet_mass","BDT_common5_input_closest_tagged_dijet_mass",30,0.0,250.0),"BDT_common5_input_closest_tagged_dijet_mass",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_dEta_fn","BDT_common5_input_dEta_fn",30,0.0,5.0),"BDT_common5_input_dEta_fn",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_dev_from_avg_disc_btags","BDT_common5_input_dev_from_avg_disc_btags",30,0.0,0.02),"BDT_common5_input_dev_from_avg_disc_btags",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_dr_between_lep_and_closest_jet","BDT_common5_input_dr_between_lep_and_closest_jet",30,0.0,3.0),"BDT_common5_input_dr_between_lep_and_closest_jet",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_fifth_highest_CSV","BDT_common5_input_fifth_highest_CSV",30,-0.1,1.0),"BDT_common5_input_fifth_highest_CSV",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_first_jet_pt","BDT_common5_input_first_jet_pt",30,0.0,500.0),"BDT_common5_input_first_jet_pt",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_fourth_highest_btag","BDT_common5_input_fourth_highest_btag",30,-0.1,1.0),"BDT_common5_input_fourth_highest_btag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_fourth_jet_pt","BDT_common5_input_fourth_jet_pt",30,0.0,300.0),"BDT_common5_input_fourth_jet_pt",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h0","BDT_common5_input_h0",30,0.15,0.45),"BDT_common5_input_h0",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h1","BDT_common5_input_h1",30,-0.2,0.2),"BDT_common5_input_h1",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h2","BDT_common5_input_h2",30,-0.2,0.3),"BDT_common5_input_h2",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h3","BDT_common5_input_h3",30,-0.2,0.2),"BDT_common5_input_h3",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_invariant_mass_of_everything","BDT_common5_input_invariant_mass_of_everything",30,500.0,1200.0),"BDT_common5_input_invariant_mass_of_everything",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_lowest_btag","BDT_common5_input_lowest_btag",30,0.8,1.0),"BDT_common5_input_lowest_btag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_maxeta_jet_jet","BDT_common5_input_maxeta_jet_jet",30,0.0,2.0),"BDT_common5_input_maxeta_jet_jet",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_maxeta_jet_tag","BDT_common5_input_maxeta_jet_tag",30,0.0,2.0),"BDT_common5_input_maxeta_jet_tag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_maxeta_tag_tag","BDT_common5_input_maxeta_tag_tag",30,0.0,2.0),"BDT_common5_input_maxeta_tag_tag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_min_dr_tagged_jets","BDT_common5_input_min_dr_tagged_jets",30,0.0,5.0),"BDT_common5_input_min_dr_tagged_jets",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_pt_all_jets_over_E_all_jets","BDT_common5_input_pt_all_jets_over_E_all_jets",30,0.0,1.0),"BDT_common5_input_pt_all_jets_over_E_all_jets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_second_highest_btag","BDT_common5_input_second_highest_btag",30,0.8,1.0),"BDT_common5_input_second_highest_btag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_second_jet_pt","BDT_common5_input_second_jet_pt",30,0.0,300.0),"BDT_common5_input_second_jet_pt",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_sphericity","BDT_common5_input_sphericity",30,0.0,1.0),"BDT_common5_input_sphericity",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_tagged_dijet_mass_closest_to_125","BDT_common5_input_tagged_dijet_mass_closest_to_125",30,40.0,230.0),"BDT_common5_input_tagged_dijet_mass_closest_to_125",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_third_highest_btag","BDT_common5_input_third_highest_btag",30,0.8,1.0),"BDT_common5_input_third_highest_btag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_third_jet_pt","BDT_common5_input_third_jet_pt",30,0.0,300.0),"BDT_common5_input_third_jet_pt",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_CSV_Average_Tagged","Evt_CSV_Average_Tagged",30,0.82,1.0),"Evt_CSV_Average_Tagged",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_CSV_Min","Evt_CSV_Min",30,0.0,1.0),"Evt_CSV_Min",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Deta_TaggedJetsAverage","Evt_Deta_TaggedJetsAverage",30,0.0,3.0),"Evt_Deta_TaggedJetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_JetsAverage","Evt_Dr_JetsAverage",30,0.0,5.0),"Evt_Dr_JetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_MinDeltaRJets","Evt_Dr_MinDeltaRJets",30,0.0,3.0),"Evt_Dr_MinDeltaRJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_MinDeltaRLeptonJet","Evt_Dr_MinDeltaRLeptonJet",30,0.0,3.0),"Evt_Dr_MinDeltaRLeptonJet",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_MinDeltaRLeptonTaggedJet","Evt_Dr_MinDeltaRLeptonTaggedJet",30,0.0,3.0),"Evt_Dr_MinDeltaRLeptonTaggedJet",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_TaggedJetsAverage","Evt_Dr_TaggedJetsAverage",30,0.0,5.0),"Evt_Dr_TaggedJetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_E_PrimaryLepton","Evt_E_PrimaryLepton",30,0.0,500.0),"Evt_E_PrimaryLepton",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Eta_JetsAverage","Evt_Eta_JetsAverage",30,-3.0,3.0),"Evt_Eta_JetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Eta_PrimaryLepton","Evt_Eta_PrimaryLepton",30,-3,3),"Evt_Eta_PrimaryLepton",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Jet_MaxDeta_Jets","Evt_Jet_MaxDeta_Jets",30,0,5),"Evt_Jet_MaxDeta_Jets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M2_TaggedJetsAverage","Evt_M2_TaggedJetsAverage",30,0.0,400.0),"Evt_M2_TaggedJetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M3","Evt_M3",30,0.0,400.0),"Evt_M3",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_JetsAverage","Evt_M_JetsAverage",30,0.0,30.0),"Evt_M_JetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_MedianTaggedJets","Evt_M_MedianTaggedJets",30,30.0,400.0),"Evt_M_MedianTaggedJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_MinDeltaRJets","Evt_M_MinDeltaRJets",30,10.0,250.0),"Evt_M_MinDeltaRJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_MinDeltaRTaggedJets","Evt_M_MinDeltaRTaggedJets",30,10.0,300.0),"Evt_M_MinDeltaRTaggedJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_TaggedJetsAverage","Evt_M_TaggedJetsAverage",30,0.0,50.0),"Evt_M_TaggedJetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Pt_MinDeltaRJets","Evt_Pt_MinDeltaRJets",30,0.0,400.0),"Evt_Pt_MinDeltaRJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Pt_MinDeltaRTaggedJets","Evt_Pt_MinDeltaRTaggedJets",30,0.0,400.0),"Evt_Pt_MinDeltaRTaggedJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Pt_PrimaryLepton","Evt_Pt_PrimaryLepton",30,0.0,400.0),"Evt_Pt_PrimaryLepton",plotselection,plotlabel),    
    #Plot(ROOT.TH1F(plotprefix+"Evt_blr_ETH","Evt_blr_ETH",30,0.0,1.1),"Evt_blr_ETH",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"Evt_blr_ETH_transformed","Evt_blr_ETH_transformed",30,-10.0,10.0),"Evt_blr_ETH_transformed",plotselection,plotlabel),
]

plotlabel="1 lepton, 4 jets, 4 b-tags"
plotselection=categoriesJT[4][0]
plotprefix="s44_"
# weights_Final_44_MEMBDTv2.xml
plots44=[
   #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_Evt_CSV_Average","BDT_common5_input_Evt_CSV_Average",20,0.6,1.0),"BDT_common5_input_Evt_CSV_Average",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_Evt_Deta_JetsAverage","BDT_common5_input_Evt_Deta_JetsAverage",20,0.0,3.4),"BDT_common5_input_Evt_Deta_JetsAverage",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_HT","BDT_common5_input_HT",20,0.0,1000.0),"BDT_common5_input_HT",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_M3","BDT_common5_input_M3",20,0.0,600.0),"BDT_common5_input_M3",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_MET","BDT_common5_input_MET",20,0.0,300.0),"BDT_common5_input_MET",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_MHT","BDT_common5_input_MHT",20,0.0,250.0),"BDT_common5_input_MHT",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_Mlb","BDT_common5_input_Mlb",20,0.0,250.0),"BDT_common5_input_Mlb",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_all_sum_pt_with_met","BDT_common5_input_all_sum_pt_with_met",20,200,900.0),"BDT_common5_input_all_sum_pt_with_met",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_aplanarity","BDT_common5_input_aplanarity",20,0.0,0.4),"BDT_common5_input_aplanarity",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_avg_btag_disc_btags","BDT_common5_input_avg_btag_disc_btags",20,0.8,1.0),"BDT_common5_input_avg_btag_disc_btags",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_avg_dr_tagged_jets","BDT_common5_input_avg_dr_tagged_jets",20,0.0,5.0),"BDT_common5_input_avg_dr_tagged_jets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_best_higgs_mass","BDT_common5_input_best_higgs_mass",20,0.0,200.0),"BDT_common5_input_best_higgs_mass",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_closest_tagged_dijet_mass","BDT_common5_input_closest_tagged_dijet_mass",20,0.0,250.0),"BDT_common5_input_closest_tagged_dijet_mass",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_dEta_fn","BDT_common5_input_dEta_fn",20,0.0,5.0),"BDT_common5_input_dEta_fn",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_dev_from_avg_disc_btags","BDT_common5_input_dev_from_avg_disc_btags",20,0.0,0.02),"BDT_common5_input_dev_from_avg_disc_btags",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_dr_between_lep_and_closest_jet","BDT_common5_input_dr_between_lep_and_closest_jet",20,0.0,3.0),"BDT_common5_input_dr_between_lep_and_closest_jet",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_fifth_highest_CSV","BDT_common5_input_fifth_highest_CSV",20,-0.1,1.0),"BDT_common5_input_fifth_highest_CSV",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_first_jet_pt","BDT_common5_input_first_jet_pt",20,0.0,500.0),"BDT_common5_input_first_jet_pt",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_fourth_highest_btag","BDT_common5_input_fourth_highest_btag",20,0.8,1.0),"BDT_common5_input_fourth_highest_btag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_fourth_jet_pt","BDT_common5_input_fourth_jet_pt",20,0.0,300.0),"BDT_common5_input_fourth_jet_pt",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h0","BDT_common5_input_h0",20,0.15,0.45),"BDT_common5_input_h0",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h1","BDT_common5_input_h1",20,-0.2,0.2),"BDT_common5_input_h1",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h2","BDT_common5_input_h2",20,-0.2,0.3),"BDT_common5_input_h2",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h3","BDT_common5_input_h3",20,-0.2,0.2),"BDT_common5_input_h3",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_invariant_mass_of_everything","BDT_common5_input_invariant_mass_of_everything",20,500.0,1200.0),"BDT_common5_input_invariant_mass_of_everything",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_lowest_btag","BDT_common5_input_lowest_btag",20,0.8,1.0),"BDT_common5_input_lowest_btag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_maxeta_jet_jet","BDT_common5_input_maxeta_jet_jet",20,0.0,2.0),"BDT_common5_input_maxeta_jet_jet",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_maxeta_jet_tag","BDT_common5_input_maxeta_jet_tag",20,0.0,2.0),"BDT_common5_input_maxeta_jet_tag",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_maxeta_tag_tag","BDT_common5_input_maxeta_tag_tag",20,0.0,2.0),"BDT_common5_input_maxeta_tag_tag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_min_dr_tagged_jets","BDT_common5_input_min_dr_tagged_jets",20,0.0,5.0),"BDT_common5_input_min_dr_tagged_jets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_pt_all_jets_over_E_all_jets","BDT_common5_input_pt_all_jets_over_E_all_jets",20,0.0,1.0),"BDT_common5_input_pt_all_jets_over_E_all_jets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_second_highest_btag","BDT_common5_input_second_highest_btag",20,0.8,1.0),"BDT_common5_input_second_highest_btag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_second_jet_pt","BDT_common5_input_second_jet_pt",20,0.0,300.0),"BDT_common5_input_second_jet_pt",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_sphericity","BDT_common5_input_sphericity",20,0.0,1.0),"BDT_common5_input_sphericity",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_tagged_dijet_mass_closest_to_125","BDT_common5_input_tagged_dijet_mass_closest_to_125",20,40.0,230.0),"BDT_common5_input_tagged_dijet_mass_closest_to_125",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_third_highest_btag","BDT_common5_input_third_highest_btag",20,0.8,1.0),"BDT_common5_input_third_highest_btag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_third_jet_pt","BDT_common5_input_third_jet_pt",20,0.0,300.0),"BDT_common5_input_third_jet_pt",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_CSV_Average_Tagged","Evt_CSV_Average_Tagged",20,0.82,1.0),"Evt_CSV_Average_Tagged",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_CSV_Min","Evt_CSV_Min",20,0.0,1.0),"Evt_CSV_Min",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"Evt_Deta_TaggedJetsAverage","Evt_Deta_TaggedJetsAverage",20,0.0,3.0),"Evt_Deta_TaggedJetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_JetsAverage","Evt_Dr_JetsAverage",20,0.0,5.0),"Evt_Dr_JetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_MinDeltaRJets","Evt_Dr_MinDeltaRJets",20,0.0,3.0),"Evt_Dr_MinDeltaRJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_MinDeltaRLeptonJet","Evt_Dr_MinDeltaRLeptonJet",20,0.0,3.0),"Evt_Dr_MinDeltaRLeptonJet",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_MinDeltaRLeptonTaggedJet","Evt_Dr_MinDeltaRLeptonTaggedJet",20,0.0,3.0),"Evt_Dr_MinDeltaRLeptonTaggedJet",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_TaggedJetsAverage","Evt_Dr_TaggedJetsAverage",20,0.0,5.0),"Evt_Dr_TaggedJetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_E_PrimaryLepton","Evt_E_PrimaryLepton",20,0.0,500.0),"Evt_E_PrimaryLepton",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Eta_JetsAverage","Evt_Eta_JetsAverage",20,-3.0,3.0),"Evt_Eta_JetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Eta_PrimaryLepton","Evt_Eta_PrimaryLepton",20,-3,3),"Evt_Eta_PrimaryLepton",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Jet_MaxDeta_Jets","Evt_Jet_MaxDeta_Jets",20,0,5),"Evt_Jet_MaxDeta_Jets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M2_TaggedJetsAverage","Evt_M2_TaggedJetsAverage",20,0.0,400.0),"Evt_M2_TaggedJetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M3","Evt_M3",20,0.0,400.0),"Evt_M3",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_JetsAverage","Evt_M_JetsAverage",20,0.0,30.0),"Evt_M_JetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_MedianTaggedJets","Evt_M_MedianTaggedJets",20,30.0,400.0),"Evt_M_MedianTaggedJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_MinDeltaRJets","Evt_M_MinDeltaRJets",20,10.0,250.0),"Evt_M_MinDeltaRJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_MinDeltaRTaggedJets","Evt_M_MinDeltaRTaggedJets",20,10.0,300.0),"Evt_M_MinDeltaRTaggedJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_TaggedJetsAverage","Evt_M_TaggedJetsAverage",20,0.0,50.0),"Evt_M_TaggedJetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Pt_MinDeltaRJets","Evt_Pt_MinDeltaRJets",20,0.0,400.0),"Evt_Pt_MinDeltaRJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Pt_MinDeltaRTaggedJets","Evt_Pt_MinDeltaRTaggedJets",20,0.0,400.0),"Evt_Pt_MinDeltaRTaggedJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Pt_PrimaryLepton","Evt_Pt_PrimaryLepton",20,0.0,400.0),"Evt_Pt_PrimaryLepton",plotselection,plotlabel),    
    #Plot(ROOT.TH1F(plotprefix+"Evt_blr_ETH","Evt_blr_ETH",20,0.0,1.1),"Evt_blr_ETH",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"Evt_blr_ETH_transformed","Evt_blr_ETH_transformed",20,-10.0,10.0),"Evt_blr_ETH_transformed",plotselection,plotlabel),
]


plotlabel="1 lepton, 5 jets, 3 b-tags"
plotselection=categoriesJT[2][0]
plotprefix="s53_"
plots53=[
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_Evt_CSV_Average","BDT_common5_input_Evt_CSV_Average",30,0.6,1.0),"BDT_common5_input_Evt_CSV_Average",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_Evt_Deta_JetsAverage","BDT_common5_input_Evt_Deta_JetsAverage",30,0.0,3.4),"BDT_common5_input_Evt_Deta_JetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_HT","BDT_common5_input_HT",30,0.0,1000.0),"BDT_common5_input_HT",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_M3","BDT_common5_input_M3",30,0.0,600.0),"BDT_common5_input_M3",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_MET","BDT_common5_input_MET",30,0.0,300.0),"BDT_common5_input_MET",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_MHT","BDT_common5_input_MHT",30,0.0,250.0),"BDT_common5_input_MHT",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_Mlb","BDT_common5_input_Mlb",30,0.0,250.0),"BDT_common5_input_Mlb",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_all_sum_pt_with_met","BDT_common5_input_all_sum_pt_with_met",30,200,900.0),"BDT_common5_input_all_sum_pt_with_met",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_aplanarity","BDT_common5_input_aplanarity",30,0.0,0.4),"BDT_common5_input_aplanarity",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_avg_btag_disc_btags","BDT_common5_input_avg_btag_disc_btags",30,0.8,1.0),"BDT_common5_input_avg_btag_disc_btags",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_avg_dr_tagged_jets","BDT_common5_input_avg_dr_tagged_jets",30,0.0,5.0),"BDT_common5_input_avg_dr_tagged_jets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_best_higgs_mass","BDT_common5_input_best_higgs_mass",30,0.0,200.0),"BDT_common5_input_best_higgs_mass",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_closest_tagged_dijet_mass","BDT_common5_input_closest_tagged_dijet_mass",30,0.0,250.0),"BDT_common5_input_closest_tagged_dijet_mass",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_dEta_fn","BDT_common5_input_dEta_fn",30,0.0,5.0),"BDT_common5_input_dEta_fn",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_dev_from_avg_disc_btags","BDT_common5_input_dev_from_avg_disc_btags",30,0.0,0.02),"BDT_common5_input_dev_from_avg_disc_btags",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_dr_between_lep_and_closest_jet","BDT_common5_input_dr_between_lep_and_closest_jet",30,0.0,3.0),"BDT_common5_input_dr_between_lep_and_closest_jet",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_fifth_highest_CSV","BDT_common5_input_fifth_highest_CSV",30,-0.1,1.0),"BDT_common5_input_fifth_highest_CSV",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_first_jet_pt","BDT_common5_input_first_jet_pt",30,0.0,500.0),"BDT_common5_input_first_jet_pt",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_fourth_highest_btag","BDT_common5_input_fourth_highest_btag",30,-0.1,1.0),"BDT_common5_input_fourth_highest_btag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_fourth_jet_pt","BDT_common5_input_fourth_jet_pt",30,0.0,300.0),"BDT_common5_input_fourth_jet_pt",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h0","BDT_common5_input_h0",30,0.15,0.45),"BDT_common5_input_h0",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h1","BDT_common5_input_h1",30,-0.2,0.2),"BDT_common5_input_h1",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h2","BDT_common5_input_h2",30,-0.2,0.3),"BDT_common5_input_h2",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h3","BDT_common5_input_h3",30,-0.2,0.2),"BDT_common5_input_h3",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_invariant_mass_of_everything","BDT_common5_input_invariant_mass_of_everything",30,500.0,1200.0),"BDT_common5_input_invariant_mass_of_everything",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_lowest_btag","BDT_common5_input_lowest_btag",30,0.8,1.0),"BDT_common5_input_lowest_btag",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_maxeta_jet_jet","BDT_common5_input_maxeta_jet_jet",30,0.0,2.0),"BDT_common5_input_maxeta_jet_jet",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_maxeta_jet_tag","BDT_common5_input_maxeta_jet_tag",30,0.0,2.0),"BDT_common5_input_maxeta_jet_tag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_maxeta_tag_tag","BDT_common5_input_maxeta_tag_tag",30,0.0,2.0),"BDT_common5_input_maxeta_tag_tag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_min_dr_tagged_jets","BDT_common5_input_min_dr_tagged_jets",30,0.0,5.0),"BDT_common5_input_min_dr_tagged_jets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_pt_all_jets_over_E_all_jets","BDT_common5_input_pt_all_jets_over_E_all_jets",30,0.0,1.0),"BDT_common5_input_pt_all_jets_over_E_all_jets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_second_highest_btag","BDT_common5_input_second_highest_btag",30,0.8,1.0),"BDT_common5_input_second_highest_btag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_second_jet_pt","BDT_common5_input_second_jet_pt",30,0.0,300.0),"BDT_common5_input_second_jet_pt",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_sphericity","BDT_common5_input_sphericity",30,0.0,1.0),"BDT_common5_input_sphericity",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_tagged_dijet_mass_closest_to_125","BDT_common5_input_tagged_dijet_mass_closest_to_125",30,40.0,230.0),"BDT_common5_input_tagged_dijet_mass_closest_to_125",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_third_highest_btag","BDT_common5_input_third_highest_btag",30,0.8,1.0),"BDT_common5_input_third_highest_btag",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_third_jet_pt","BDT_common5_input_third_jet_pt",30,0.0,300.0),"BDT_common5_input_third_jet_pt",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_CSV_Average_Tagged","Evt_CSV_Average_Tagged",30,0.82,1.0),"Evt_CSV_Average_Tagged",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_CSV_Min","Evt_CSV_Min",30,0.0,1.0),"Evt_CSV_Min",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Deta_TaggedJetsAverage","Evt_Deta_TaggedJetsAverage",30,0.0,3.0),"Evt_Deta_TaggedJetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_JetsAverage","Evt_Dr_JetsAverage",30,0.0,5.0),"Evt_Dr_JetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_MinDeltaRJets","Evt_Dr_MinDeltaRJets",30,0.0,3.0),"Evt_Dr_MinDeltaRJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_MinDeltaRLeptonJet","Evt_Dr_MinDeltaRLeptonJet",30,0.0,3.0),"Evt_Dr_MinDeltaRLeptonJet",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_MinDeltaRLeptonTaggedJet","Evt_Dr_MinDeltaRLeptonTaggedJet",30,0.0,3.0),"Evt_Dr_MinDeltaRLeptonTaggedJet",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_TaggedJetsAverage","Evt_Dr_TaggedJetsAverage",30,0.0,5.0),"Evt_Dr_TaggedJetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_E_PrimaryLepton","Evt_E_PrimaryLepton",30,0.0,500.0),"Evt_E_PrimaryLepton",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Eta_JetsAverage","Evt_Eta_JetsAverage",30,-3.0,3.0),"Evt_Eta_JetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Eta_PrimaryLepton","Evt_Eta_PrimaryLepton",30,-3,3),"Evt_Eta_PrimaryLepton",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Jet_MaxDeta_Jets","Evt_Jet_MaxDeta_Jets",30,0,5),"Evt_Jet_MaxDeta_Jets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M2_TaggedJetsAverage","Evt_M2_TaggedJetsAverage",30,0.0,400.0),"Evt_M2_TaggedJetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M3","Evt_M3",30,0.0,400.0),"Evt_M3",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_JetsAverage","Evt_M_JetsAverage",30,0.0,30.0),"Evt_M_JetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_MedianTaggedJets","Evt_M_MedianTaggedJets",30,30.0,400.0),"Evt_M_MedianTaggedJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_MinDeltaRJets","Evt_M_MinDeltaRJets",30,10.0,250.0),"Evt_M_MinDeltaRJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_MinDeltaRTaggedJets","Evt_M_MinDeltaRTaggedJets",30,10.0,300.0),"Evt_M_MinDeltaRTaggedJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_TaggedJetsAverage","Evt_M_TaggedJetsAverage",30,0.0,50.0),"Evt_M_TaggedJetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Pt_MinDeltaRJets","Evt_Pt_MinDeltaRJets",30,0.0,400.0),"Evt_Pt_MinDeltaRJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Pt_MinDeltaRTaggedJets","Evt_Pt_MinDeltaRTaggedJets",30,0.0,400.0),"Evt_Pt_MinDeltaRTaggedJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Pt_PrimaryLepton","Evt_Pt_PrimaryLepton",30,0.0,400.0),"Evt_Pt_PrimaryLepton",plotselection,plotlabel),    
    #Plot(ROOT.TH1F(plotprefix+"Evt_blr_ETH","Evt_blr_ETH",30,0.0,1.1),"Evt_blr_ETH",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"Evt_blr_ETH_transformed","Evt_blr_ETH_transformed",30,-10.0,10.0),"Evt_blr_ETH_transformed",plotselection,plotlabel),
]


plotlabel="1 lepton, 5 jets, #geq4 b-tags"
plotselection=categoriesJT[5][0]
plotprefix="s54_"
plots54=[
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_Evt_CSV_Average","BDT_common5_input_Evt_CSV_Average",20,0.6,1.0),"BDT_common5_input_Evt_CSV_Average",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_Evt_Deta_JetsAverage","BDT_common5_input_Evt_Deta_JetsAverage",20,0.0,3.4),"BDT_common5_input_Evt_Deta_JetsAverage",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_HT","BDT_common5_input_HT",20,0.0,1000.0),"BDT_common5_input_HT",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_M3","BDT_common5_input_M3",20,0.0,600.0),"BDT_common5_input_M3",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_MET","BDT_common5_input_MET",20,0.0,300.0),"BDT_common5_input_MET",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_MHT","BDT_common5_input_MHT",20,0.0,250.0),"BDT_common5_input_MHT",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_Mlb","BDT_common5_input_Mlb",20,0.0,250.0),"BDT_common5_input_Mlb",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_all_sum_pt_with_met","BDT_common5_input_all_sum_pt_with_met",20,200,900.0),"BDT_common5_input_all_sum_pt_with_met",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_aplanarity","BDT_common5_input_aplanarity",20,0.0,0.4),"BDT_common5_input_aplanarity",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_avg_btag_disc_btags","BDT_common5_input_avg_btag_disc_btags",20,0.8,1.0),"BDT_common5_input_avg_btag_disc_btags",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_avg_dr_tagged_jets","BDT_common5_input_avg_dr_tagged_jets",20,0.0,5.0),"BDT_common5_input_avg_dr_tagged_jets",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_best_higgs_mass","BDT_common5_input_best_higgs_mass",20,0.0,200.0),"BDT_common5_input_best_higgs_mass",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_closest_tagged_dijet_mass","BDT_common5_input_closest_tagged_dijet_mass",20,0.0,250.0),"BDT_common5_input_closest_tagged_dijet_mass",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_dEta_fn","BDT_common5_input_dEta_fn",20,0.0,5.0),"BDT_common5_input_dEta_fn",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_dev_from_avg_disc_btags","BDT_common5_input_dev_from_avg_disc_btags",20,0.0,0.02),"BDT_common5_input_dev_from_avg_disc_btags",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_dr_between_lep_and_closest_jet","BDT_common5_input_dr_between_lep_and_closest_jet",20,0.0,3.0),"BDT_common5_input_dr_between_lep_and_closest_jet",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_fifth_highest_CSV","BDT_common5_input_fifth_highest_CSV",20,-0.1,1.0),"BDT_common5_input_fifth_highest_CSV",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_first_jet_pt","BDT_common5_input_first_jet_pt",20,0.0,500.0),"BDT_common5_input_first_jet_pt",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_fourth_highest_btag","BDT_common5_input_fourth_highest_btag",20,0.8,1.0),"BDT_common5_input_fourth_highest_btag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_fourth_jet_pt","BDT_common5_input_fourth_jet_pt",20,0.0,300.0),"BDT_common5_input_fourth_jet_pt",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h0","BDT_common5_input_h0",20,0.15,0.45),"BDT_common5_input_h0",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h1","BDT_common5_input_h1",20,-0.2,0.2),"BDT_common5_input_h1",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h2","BDT_common5_input_h2",20,-0.2,0.3),"BDT_common5_input_h2",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h3","BDT_common5_input_h3",20,-0.2,0.2),"BDT_common5_input_h3",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_invariant_mass_of_everything","BDT_common5_input_invariant_mass_of_everything",20,500.0,1200.0),"BDT_common5_input_invariant_mass_of_everything",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_lowest_btag","BDT_common5_input_lowest_btag",20,0.8,1.0),"BDT_common5_input_lowest_btag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_maxeta_jet_jet","BDT_common5_input_maxeta_jet_jet",20,0.0,2.0),"BDT_common5_input_maxeta_jet_jet",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_maxeta_jet_tag","BDT_common5_input_maxeta_jet_tag",20,0.0,2.0),"BDT_common5_input_maxeta_jet_tag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_maxeta_tag_tag","BDT_common5_input_maxeta_tag_tag",20,0.0,2.0),"BDT_common5_input_maxeta_tag_tag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_min_dr_tagged_jets","BDT_common5_input_min_dr_tagged_jets",20,0.0,5.0),"BDT_common5_input_min_dr_tagged_jets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_pt_all_jets_over_E_all_jets","BDT_common5_input_pt_all_jets_over_E_all_jets",20,0.0,1.0),"BDT_common5_input_pt_all_jets_over_E_all_jets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_second_highest_btag","BDT_common5_input_second_highest_btag",20,0.8,1.0),"BDT_common5_input_second_highest_btag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_second_jet_pt","BDT_common5_input_second_jet_pt",20,0.0,300.0),"BDT_common5_input_second_jet_pt",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_sphericity","BDT_common5_input_sphericity",20,0.0,1.0),"BDT_common5_input_sphericity",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_tagged_dijet_mass_closest_to_125","BDT_common5_input_tagged_dijet_mass_closest_to_125",20,40.0,230.0),"BDT_common5_input_tagged_dijet_mass_closest_to_125",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_third_highest_btag","BDT_common5_input_third_highest_btag",20,0.8,1.0),"BDT_common5_input_third_highest_btag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_third_jet_pt","BDT_common5_input_third_jet_pt",20,0.0,300.0),"BDT_common5_input_third_jet_pt",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_CSV_Average_Tagged","Evt_CSV_Average_Tagged",20,0.82,1.0),"Evt_CSV_Average_Tagged",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_CSV_Min","Evt_CSV_Min",20,0.0,1.0),"Evt_CSV_Min",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Deta_TaggedJetsAverage","Evt_Deta_TaggedJetsAverage",20,0.0,3.0),"Evt_Deta_TaggedJetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_JetsAverage","Evt_Dr_JetsAverage",20,0.0,5.0),"Evt_Dr_JetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_MinDeltaRJets","Evt_Dr_MinDeltaRJets",20,0.0,3.0),"Evt_Dr_MinDeltaRJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_MinDeltaRLeptonJet","Evt_Dr_MinDeltaRLeptonJet",20,0.0,3.0),"Evt_Dr_MinDeltaRLeptonJet",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_MinDeltaRLeptonTaggedJet","Evt_Dr_MinDeltaRLeptonTaggedJet",20,0.0,3.0),"Evt_Dr_MinDeltaRLeptonTaggedJet",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_TaggedJetsAverage","Evt_Dr_TaggedJetsAverage",20,0.0,5.0),"Evt_Dr_TaggedJetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_E_PrimaryLepton","Evt_E_PrimaryLepton",20,0.0,500.0),"Evt_E_PrimaryLepton",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Eta_JetsAverage","Evt_Eta_JetsAverage",20,-3.0,3.0),"Evt_Eta_JetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Eta_PrimaryLepton","Evt_Eta_PrimaryLepton",20,-3,3),"Evt_Eta_PrimaryLepton",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Jet_MaxDeta_Jets","Evt_Jet_MaxDeta_Jets",20,0,5),"Evt_Jet_MaxDeta_Jets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M2_TaggedJetsAverage","Evt_M2_TaggedJetsAverage",20,0.0,400.0),"Evt_M2_TaggedJetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M3","Evt_M3",20,0.0,400.0),"Evt_M3",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_JetsAverage","Evt_M_JetsAverage",20,0.0,30.0),"Evt_M_JetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_MedianTaggedJets","Evt_M_MedianTaggedJets",20,30.0,400.0),"Evt_M_MedianTaggedJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_MinDeltaRJets","Evt_M_MinDeltaRJets",20,10.0,250.0),"Evt_M_MinDeltaRJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_MinDeltaRTaggedJets","Evt_M_MinDeltaRTaggedJets",20,10.0,300.0),"Evt_M_MinDeltaRTaggedJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_TaggedJetsAverage","Evt_M_TaggedJetsAverage",20,0.0,50.0),"Evt_M_TaggedJetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Pt_MinDeltaRJets","Evt_Pt_MinDeltaRJets",20,0.0,400.0),"Evt_Pt_MinDeltaRJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Pt_MinDeltaRTaggedJets","Evt_Pt_MinDeltaRTaggedJets",20,0.0,400.0),"Evt_Pt_MinDeltaRTaggedJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Pt_PrimaryLepton","Evt_Pt_PrimaryLepton",20,0.0,400.0),"Evt_Pt_PrimaryLepton",plotselection,plotlabel),    
    #Plot(ROOT.TH1F(plotprefix+"Evt_blr_ETH","Evt_blr_ETH",20,0.0,1.1),"Evt_blr_ETH",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"Evt_blr_ETH_transformed","Evt_blr_ETH_transformed",20,-10.0,10.0),"Evt_blr_ETH_transformed",plotselection,plotlabel),
]


plotlabel="1 lepton, #geq6 jets, 2 b-tags"
plotselection=categoriesJT[0][0]
plotprefix="s62_"
plots62=[
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_Evt_CSV_Average","BDT_common5_input_Evt_CSV_Average",30,0.6,1.0),"BDT_common5_input_Evt_CSV_Average",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_Evt_Deta_JetsAverage","BDT_common5_input_Evt_Deta_JetsAverage",30,0.0,3.4),"BDT_common5_input_Evt_Deta_JetsAverage",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_HT","BDT_common5_input_HT",30,0.0,1000.0),"BDT_common5_input_HT",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_M3","BDT_common5_input_M3",30,0.0,600.0),"BDT_common5_input_M3",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_MET","BDT_common5_input_MET",30,0.0,300.0),"BDT_common5_input_MET",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_MHT","BDT_common5_input_MHT",30,0.0,250.0),"BDT_common5_input_MHT",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_Mlb","BDT_common5_input_Mlb",30,0.0,250.0),"BDT_common5_input_Mlb",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_all_sum_pt_with_met","BDT_common5_input_all_sum_pt_with_met",30,200,900.0),"BDT_common5_input_all_sum_pt_with_met",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_aplanarity","BDT_common5_input_aplanarity",30,0.0,0.4),"BDT_common5_input_aplanarity",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_avg_btag_disc_btags","BDT_common5_input_avg_btag_disc_btags",30,0.8,1.0),"BDT_common5_input_avg_btag_disc_btags",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_avg_dr_tagged_jets","BDT_common5_input_avg_dr_tagged_jets",30,0.0,5.0),"BDT_common5_input_avg_dr_tagged_jets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_best_higgs_mass","BDT_common5_input_best_higgs_mass",30,0.0,200.0),"BDT_common5_input_best_higgs_mass",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_closest_tagged_dijet_mass","BDT_common5_input_closest_tagged_dijet_mass",30,0.0,250.0),"BDT_common5_input_closest_tagged_dijet_mass",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_dEta_fn","BDT_common5_input_dEta_fn",30,0.0,5.0),"BDT_common5_input_dEta_fn",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_dev_from_avg_disc_btags","BDT_common5_input_dev_from_avg_disc_btags",30,0.0,0.02),"BDT_common5_input_dev_from_avg_disc_btags",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_dr_between_lep_and_closest_jet","BDT_common5_input_dr_between_lep_and_closest_jet",30,0.0,3.0),"BDT_common5_input_dr_between_lep_and_closest_jet",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_fifth_highest_CSV","BDT_common5_input_fifth_highest_CSV",30,-0.1,1.0),"BDT_common5_input_fifth_highest_CSV",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_first_jet_pt","BDT_common5_input_first_jet_pt",30,0.0,500.0),"BDT_common5_input_first_jet_pt",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_fourth_highest_btag","BDT_common5_input_fourth_highest_btag",30,-0.1,1.0),"BDT_common5_input_fourth_highest_btag",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_fourth_jet_pt","BDT_common5_input_fourth_jet_pt",30,0.0,300.0),"BDT_common5_input_fourth_jet_pt",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h0","BDT_common5_input_h0",30,0.15,0.45),"BDT_common5_input_h0",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h1","BDT_common5_input_h1",30,-0.2,0.2),"BDT_common5_input_h1",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h2","BDT_common5_input_h2",30,-0.2,0.3),"BDT_common5_input_h2",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h3","BDT_common5_input_h3",30,-0.2,0.2),"BDT_common5_input_h3",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_invariant_mass_of_everything","BDT_common5_input_invariant_mass_of_everything",30,500.0,1200.0),"BDT_common5_input_invariant_mass_of_everything",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_lowest_btag","BDT_common5_input_lowest_btag",30,0.8,1.0),"BDT_common5_input_lowest_btag",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_maxeta_jet_jet","BDT_common5_input_maxeta_jet_jet",30,0.0,2.0),"BDT_common5_input_maxeta_jet_jet",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_maxeta_jet_tag","BDT_common5_input_maxeta_jet_tag",30,0.0,2.0),"BDT_common5_input_maxeta_jet_tag",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_maxeta_tag_tag","BDT_common5_input_maxeta_tag_tag",30,0.0,2.0),"BDT_common5_input_maxeta_tag_tag",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_min_dr_tagged_jets","BDT_common5_input_min_dr_tagged_jets",30,0.0,5.0),"BDT_common5_input_min_dr_tagged_jets",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_pt_all_jets_over_E_all_jets","BDT_common5_input_pt_all_jets_over_E_all_jets",30,0.0,1.0),"BDT_common5_input_pt_all_jets_over_E_all_jets",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_second_highest_btag","BDT_common5_input_second_highest_btag",30,0.8,1.0),"BDT_common5_input_second_highest_btag",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_second_jet_pt","BDT_common5_input_second_jet_pt",30,0.0,300.0),"BDT_common5_input_second_jet_pt",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_sphericity","BDT_common5_input_sphericity",30,0.0,1.0),"BDT_common5_input_sphericity",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_tagged_dijet_mass_closest_to_125","BDT_common5_input_tagged_dijet_mass_closest_to_125",30,40.0,230.0),"BDT_common5_input_tagged_dijet_mass_closest_to_125",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_third_highest_btag","BDT_common5_input_third_highest_btag",30,0.8,1.0),"BDT_common5_input_third_highest_btag",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_third_jet_pt","BDT_common5_input_third_jet_pt",30,0.0,300.0),"BDT_common5_input_third_jet_pt",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_CSV_Average_Tagged","Evt_CSV_Average_Tagged",30,0.82,1.0),"Evt_CSV_Average_Tagged",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_CSV_Min","Evt_CSV_Min",30,0.0,1.0),"Evt_CSV_Min",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_Deta_TaggedJetsAverage","Evt_Deta_TaggedJetsAverage",30,0.0,3.0),"Evt_Deta_TaggedJetsAverage",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_Dr_JetsAverage","Evt_Dr_JetsAverage",30,0.0,5.0),"Evt_Dr_JetsAverage",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_Dr_MinDeltaRJets","Evt_Dr_MinDeltaRJets",30,0.0,3.0),"Evt_Dr_MinDeltaRJets",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_Dr_MinDeltaRLeptonJet","Evt_Dr_MinDeltaRLeptonJet",30,0.0,3.0),"Evt_Dr_MinDeltaRLeptonJet",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_Dr_MinDeltaRLeptonTaggedJet","Evt_Dr_MinDeltaRLeptonTaggedJet",30,0.0,3.0),"Evt_Dr_MinDeltaRLeptonTaggedJet",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_Dr_TaggedJetsAverage","Evt_Dr_TaggedJetsAverage",30,0.0,5.0),"Evt_Dr_TaggedJetsAverage",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_E_PrimaryLepton","Evt_E_PrimaryLepton",30,0.0,500.0),"Evt_E_PrimaryLepton",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_Eta_JetsAverage","Evt_Eta_JetsAverage",30,-3.0,3.0),"Evt_Eta_JetsAverage",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_Eta_PrimaryLepton","Evt_Eta_PrimaryLepton",30,-3,3),"Evt_Eta_PrimaryLepton",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_Jet_MaxDeta_Jets","Evt_Jet_MaxDeta_Jets",30,0,5),"Evt_Jet_MaxDeta_Jets",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_M2_TaggedJetsAverage","Evt_M2_TaggedJetsAverage",30,0.0,400.0),"Evt_M2_TaggedJetsAverage",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_M3","Evt_M3",30,0.0,400.0),"Evt_M3",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_M_JetsAverage","Evt_M_JetsAverage",30,0.0,30.0),"Evt_M_JetsAverage",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_M_MedianTaggedJets","Evt_M_MedianTaggedJets",30,30.0,400.0),"Evt_M_MedianTaggedJets",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_M_MinDeltaRJets","Evt_M_MinDeltaRJets",30,10.0,250.0),"Evt_M_MinDeltaRJets",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_M_MinDeltaRTaggedJets","Evt_M_MinDeltaRTaggedJets",30,10.0,300.0),"Evt_M_MinDeltaRTaggedJets",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_M_TaggedJetsAverage","Evt_M_TaggedJetsAverage",30,0.0,50.0),"Evt_M_TaggedJetsAverage",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_Pt_MinDeltaRJets","Evt_Pt_MinDeltaRJets",30,0.0,400.0),"Evt_Pt_MinDeltaRJets",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_Pt_MinDeltaRTaggedJets","Evt_Pt_MinDeltaRTaggedJets",30,0.0,400.0),"Evt_Pt_MinDeltaRTaggedJets",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_Pt_PrimaryLepton","Evt_Pt_PrimaryLepton",30,0.0,400.0),"Evt_Pt_PrimaryLepton",plotselection,plotlabel),    
    ##Plot(ROOT.TH1F(plotprefix+"Evt_blr_ETH","Evt_blr_ETH",30,0.0,1.1),"Evt_blr_ETH",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"Evt_blr_ETH_transformed","Evt_blr_ETH_transformed",30,-10.0,10.0),"Evt_blr_ETH_transformed",plotselection,plotlabel),
]


plotlabel="1 lepton, #geq6 jets, 3 b-tags"
plotselection=categoriesJT[3][0]
plotprefix="s63_"
plots63=[
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_Evt_CSV_Average","BDT_common5_input_Evt_CSV_Average",30,0.6,1.0),"BDT_common5_input_Evt_CSV_Average",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_Evt_Deta_JetsAverage","BDT_common5_input_Evt_Deta_JetsAverage",30,0.0,3.4),"BDT_common5_input_Evt_Deta_JetsAverage",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_HT","BDT_common5_input_HT",30,0.0,1000.0),"BDT_common5_input_HT",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_M3","BDT_common5_input_M3",30,0.0,600.0),"BDT_common5_input_M3",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_MET","BDT_common5_input_MET",30,0.0,300.0),"BDT_common5_input_MET",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_MHT","BDT_common5_input_MHT",30,0.0,250.0),"BDT_common5_input_MHT",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_Mlb","BDT_common5_input_Mlb",30,0.0,250.0),"BDT_common5_input_Mlb",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_all_sum_pt_with_met","BDT_common5_input_all_sum_pt_with_met",30,200,900.0),"BDT_common5_input_all_sum_pt_with_met",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_aplanarity","BDT_common5_input_aplanarity",30,0.0,0.4),"BDT_common5_input_aplanarity",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_avg_btag_disc_btags","BDT_common5_input_avg_btag_disc_btags",30,0.8,1.0),"BDT_common5_input_avg_btag_disc_btags",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_avg_dr_tagged_jets","BDT_common5_input_avg_dr_tagged_jets",30,0.0,5.0),"BDT_common5_input_avg_dr_tagged_jets",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_best_higgs_mass","BDT_common5_input_best_higgs_mass",30,0.0,200.0),"BDT_common5_input_best_higgs_mass",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_closest_tagged_dijet_mass","BDT_common5_input_closest_tagged_dijet_mass",30,0.0,250.0),"BDT_common5_input_closest_tagged_dijet_mass",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_dEta_fn","BDT_common5_input_dEta_fn",30,0.0,5.0),"BDT_common5_input_dEta_fn",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_dev_from_avg_disc_btags","BDT_common5_input_dev_from_avg_disc_btags",30,0.0,0.02),"BDT_common5_input_dev_from_avg_disc_btags",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_dr_between_lep_and_closest_jet","BDT_common5_input_dr_between_lep_and_closest_jet",30,0.0,3.0),"BDT_common5_input_dr_between_lep_and_closest_jet",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_fifth_highest_CSV","BDT_common5_input_fifth_highest_CSV",30,-0.1,1.0),"BDT_common5_input_fifth_highest_CSV",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_first_jet_pt","BDT_common5_input_first_jet_pt",30,0.0,500.0),"BDT_common5_input_first_jet_pt",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_fourth_highest_btag","BDT_common5_input_fourth_highest_btag",30,-0.1,1.0),"BDT_common5_input_fourth_highest_btag",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_fourth_jet_pt","BDT_common5_input_fourth_jet_pt",30,0.0,300.0),"BDT_common5_input_fourth_jet_pt",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h0","BDT_common5_input_h0",30,0.15,0.45),"BDT_common5_input_h0",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h1","BDT_common5_input_h1",30,-0.2,0.2),"BDT_common5_input_h1",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h2","BDT_common5_input_h2",30,-0.2,0.3),"BDT_common5_input_h2",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h3","BDT_common5_input_h3",30,-0.2,0.2),"BDT_common5_input_h3",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_invariant_mass_of_everything","BDT_common5_input_invariant_mass_of_everything",30,500.0,1200.0),"BDT_common5_input_invariant_mass_of_everything",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_lowest_btag","BDT_common5_input_lowest_btag",30,0.8,1.0),"BDT_common5_input_lowest_btag",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_maxeta_jet_jet","BDT_common5_input_maxeta_jet_jet",30,0.0,2.0),"BDT_common5_input_maxeta_jet_jet",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_maxeta_jet_tag","BDT_common5_input_maxeta_jet_tag",30,0.0,2.0),"BDT_common5_input_maxeta_jet_tag",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_maxeta_tag_tag","BDT_common5_input_maxeta_tag_tag",30,0.0,2.0),"BDT_common5_input_maxeta_tag_tag",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_min_dr_tagged_jets","BDT_common5_input_min_dr_tagged_jets",30,0.0,5.0),"BDT_common5_input_min_dr_tagged_jets",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_pt_all_jets_over_E_all_jets","BDT_common5_input_pt_all_jets_over_E_all_jets",30,0.0,1.0),"BDT_common5_input_pt_all_jets_over_E_all_jets",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_second_highest_btag","BDT_common5_input_second_highest_btag",30,0.8,1.0),"BDT_common5_input_second_highest_btag",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_second_jet_pt","BDT_common5_input_second_jet_pt",30,0.0,300.0),"BDT_common5_input_second_jet_pt",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_sphericity","BDT_common5_input_sphericity",30,0.0,1.0),"BDT_common5_input_sphericity",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_tagged_dijet_mass_closest_to_125","BDT_common5_input_tagged_dijet_mass_closest_to_125",30,40.0,230.0),"BDT_common5_input_tagged_dijet_mass_closest_to_125",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_third_highest_btag","BDT_common5_input_third_highest_btag",30,0.8,1.0),"BDT_common5_input_third_highest_btag",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_third_jet_pt","BDT_common5_input_third_jet_pt",30,0.0,300.0),"BDT_common5_input_third_jet_pt",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_CSV_Average_Tagged","Evt_CSV_Average_Tagged",30,0.82,1.0),"Evt_CSV_Average_Tagged",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_CSV_Min","Evt_CSV_Min",30,0.0,1.0),"Evt_CSV_Min",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_Deta_TaggedJetsAverage","Evt_Deta_TaggedJetsAverage",30,0.0,3.0),"Evt_Deta_TaggedJetsAverage",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_Dr_JetsAverage","Evt_Dr_JetsAverage",30,0.0,5.0),"Evt_Dr_JetsAverage",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_Dr_MinDeltaRJets","Evt_Dr_MinDeltaRJets",30,0.0,3.0),"Evt_Dr_MinDeltaRJets",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_Dr_MinDeltaRLeptonJet","Evt_Dr_MinDeltaRLeptonJet",30,0.0,3.0),"Evt_Dr_MinDeltaRLeptonJet",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_Dr_MinDeltaRLeptonTaggedJet","Evt_Dr_MinDeltaRLeptonTaggedJet",30,0.0,3.0),"Evt_Dr_MinDeltaRLeptonTaggedJet",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_Dr_TaggedJetsAverage","Evt_Dr_TaggedJetsAverage",30,0.0,5.0),"Evt_Dr_TaggedJetsAverage",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_E_PrimaryLepton","Evt_E_PrimaryLepton",30,0.0,500.0),"Evt_E_PrimaryLepton",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_Eta_JetsAverage","Evt_Eta_JetsAverage",30,-3.0,3.0),"Evt_Eta_JetsAverage",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_Eta_PrimaryLepton","Evt_Eta_PrimaryLepton",30,-3,3),"Evt_Eta_PrimaryLepton",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_Jet_MaxDeta_Jets","Evt_Jet_MaxDeta_Jets",30,0,5),"Evt_Jet_MaxDeta_Jets",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_M2_TaggedJetsAverage","Evt_M2_TaggedJetsAverage",30,0.0,400.0),"Evt_M2_TaggedJetsAverage",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_M3","Evt_M3",30,0.0,400.0),"Evt_M3",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_M_JetsAverage","Evt_M_JetsAverage",30,0.0,30.0),"Evt_M_JetsAverage",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_M_MedianTaggedJets","Evt_M_MedianTaggedJets",30,30.0,400.0),"Evt_M_MedianTaggedJets",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_M_MinDeltaRJets","Evt_M_MinDeltaRJets",30,10.0,250.0),"Evt_M_MinDeltaRJets",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_M_MinDeltaRTaggedJets","Evt_M_MinDeltaRTaggedJets",30,10.0,300.0),"Evt_M_MinDeltaRTaggedJets",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_M_TaggedJetsAverage","Evt_M_TaggedJetsAverage",30,0.0,50.0),"Evt_M_TaggedJetsAverage",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_Pt_MinDeltaRJets","Evt_Pt_MinDeltaRJets",30,0.0,400.0),"Evt_Pt_MinDeltaRJets",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_Pt_MinDeltaRTaggedJets","Evt_Pt_MinDeltaRTaggedJets",30,0.0,400.0),"Evt_Pt_MinDeltaRTaggedJets",plotselection,plotlabel),
    ##Plot(ROOT.TH1F(plotprefix+"Evt_Pt_PrimaryLepton","Evt_Pt_PrimaryLepton",30,0.0,400.0),"Evt_Pt_PrimaryLepton",plotselection,plotlabel),    
    ##Plot(ROOT.TH1F(plotprefix+"Evt_blr_ETH","Evt_blr_ETH",30,0.0,1.1),"Evt_blr_ETH",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"Evt_blr_ETH_transformed","Evt_blr_ETH_transformed",30,-10.0,10.0),"Evt_blr_ETH_transformed",plotselection,plotlabel),
]

plotlabel="1 lepton, #geq6 jets, #geq4 b-tags"
plotselection=categoriesJT[6][0]
plotprefix="s64"
plots64=[
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_Evt_CSV_Average","BDT_common5_input_Evt_CSV_Average",20,0.6,1.0),"BDT_common5_input_Evt_CSV_Average",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_Evt_Deta_JetsAverage","BDT_common5_input_Evt_Deta_JetsAverage",20,0.0,3.4),"BDT_common5_input_Evt_Deta_JetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_HT","BDT_common5_input_HT",20,0.0,1000.0),"BDT_common5_input_HT",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_M3","BDT_common5_input_M3",20,0.0,600.0),"BDT_common5_input_M3",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_MET","BDT_common5_input_MET",20,0.0,300.0),"BDT_common5_input_MET",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_MHT","BDT_common5_input_MHT",20,0.0,250.0),"BDT_common5_input_MHT",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_Mlb","BDT_common5_input_Mlb",20,0.0,250.0),"BDT_common5_input_Mlb",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_all_sum_pt_with_met","BDT_common5_input_all_sum_pt_with_met",20,200,900.0),"BDT_common5_input_all_sum_pt_with_met",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_aplanarity","BDT_common5_input_aplanarity",20,0.0,0.4),"BDT_common5_input_aplanarity",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_avg_btag_disc_btags","BDT_common5_input_avg_btag_disc_btags",20,0.8,1.0),"BDT_common5_input_avg_btag_disc_btags",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_avg_dr_tagged_jets","BDT_common5_input_avg_dr_tagged_jets",20,0.0,5.0),"BDT_common5_input_avg_dr_tagged_jets",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_best_higgs_mass","BDT_common5_input_best_higgs_mass",20,0.0,200.0),"BDT_common5_input_best_higgs_mass",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_closest_tagged_dijet_mass","BDT_common5_input_closest_tagged_dijet_mass",20,0.0,250.0),"BDT_common5_input_closest_tagged_dijet_mass",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_dEta_fn","BDT_common5_input_dEta_fn",20,0.0,5.0),"BDT_common5_input_dEta_fn",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_dev_from_avg_disc_btags","BDT_common5_input_dev_from_avg_disc_btags",20,0.0,0.02),"BDT_common5_input_dev_from_avg_disc_btags",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_dr_between_lep_and_closest_jet","BDT_common5_input_dr_between_lep_and_closest_jet",20,0.0,3.0),"BDT_common5_input_dr_between_lep_and_closest_jet",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_fifth_highest_CSV","BDT_common5_input_fifth_highest_CSV",20,-0.1,1.0),"BDT_common5_input_fifth_highest_CSV",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_first_jet_pt","BDT_common5_input_first_jet_pt",20,0.0,500.0),"BDT_common5_input_first_jet_pt",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_fourth_highest_btag","BDT_common5_input_fourth_highest_btag",20,0.8,1.0),"BDT_common5_input_fourth_highest_btag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_fourth_jet_pt","BDT_common5_input_fourth_jet_pt",20,0.0,300.0),"BDT_common5_input_fourth_jet_pt",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h0","BDT_common5_input_h0",20,0.15,0.45),"BDT_common5_input_h0",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h1","BDT_common5_input_h1",20,-0.2,0.2),"BDT_common5_input_h1",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h2","BDT_common5_input_h2",20,-0.2,0.3),"BDT_common5_input_h2",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_h3","BDT_common5_input_h3",20,-0.2,0.2),"BDT_common5_input_h3",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_invariant_mass_of_everything","BDT_common5_input_invariant_mass_of_everything",20,500.0,1200.0),"BDT_common5_input_invariant_mass_of_everything",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_lowest_btag","BDT_common5_input_lowest_btag",20,0.8,1.0),"BDT_common5_input_lowest_btag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_maxeta_jet_jet","BDT_common5_input_maxeta_jet_jet",20,0.0,2.0),"BDT_common5_input_maxeta_jet_jet",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_maxeta_jet_tag","BDT_common5_input_maxeta_jet_tag",20,0.0,2.0),"BDT_common5_input_maxeta_jet_tag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_maxeta_tag_tag","BDT_common5_input_maxeta_tag_tag",20,0.0,2.0),"BDT_common5_input_maxeta_tag_tag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_min_dr_tagged_jets","BDT_common5_input_min_dr_tagged_jets",20,0.0,5.0),"BDT_common5_input_min_dr_tagged_jets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_pt_all_jets_over_E_all_jets","BDT_common5_input_pt_all_jets_over_E_all_jets",20,0.0,1.0),"BDT_common5_input_pt_all_jets_over_E_all_jets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_second_highest_btag","BDT_common5_input_second_highest_btag",20,0.8,1.0),"BDT_common5_input_second_highest_btag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_second_jet_pt","BDT_common5_input_second_jet_pt",20,0.0,300.0),"BDT_common5_input_second_jet_pt",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_sphericity","BDT_common5_input_sphericity",20,0.0,1.0),"BDT_common5_input_sphericity",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_tagged_dijet_mass_closest_to_125","BDT_common5_input_tagged_dijet_mass_closest_to_125",20,40.0,230.0),"BDT_common5_input_tagged_dijet_mass_closest_to_125",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_third_highest_btag","BDT_common5_input_third_highest_btag",20,0.8,1.0),"BDT_common5_input_third_highest_btag",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"BDT_common5_input_third_jet_pt","BDT_common5_input_third_jet_pt",20,0.0,300.0),"BDT_common5_input_third_jet_pt",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_CSV_Average_Tagged","Evt_CSV_Average_Tagged",20,0.82,1.0),"Evt_CSV_Average_Tagged",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_CSV_Min","Evt_CSV_Min",20,0.0,1.0),"Evt_CSV_Min",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Deta_TaggedJetsAverage","Evt_Deta_TaggedJetsAverage",20,0.0,3.0),"Evt_Deta_TaggedJetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_JetsAverage","Evt_Dr_JetsAverage",20,0.0,5.0),"Evt_Dr_JetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_MinDeltaRJets","Evt_Dr_MinDeltaRJets",20,0.0,3.0),"Evt_Dr_MinDeltaRJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_MinDeltaRLeptonJet","Evt_Dr_MinDeltaRLeptonJet",20,0.0,3.0),"Evt_Dr_MinDeltaRLeptonJet",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_MinDeltaRLeptonTaggedJet","Evt_Dr_MinDeltaRLeptonTaggedJet",20,0.0,3.0),"Evt_Dr_MinDeltaRLeptonTaggedJet",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Dr_TaggedJetsAverage","Evt_Dr_TaggedJetsAverage",20,0.0,5.0),"Evt_Dr_TaggedJetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_E_PrimaryLepton","Evt_E_PrimaryLepton",20,0.0,500.0),"Evt_E_PrimaryLepton",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Eta_JetsAverage","Evt_Eta_JetsAverage",20,-3.0,3.0),"Evt_Eta_JetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Eta_PrimaryLepton","Evt_Eta_PrimaryLepton",20,-3,3),"Evt_Eta_PrimaryLepton",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Jet_MaxDeta_Jets","Evt_Jet_MaxDeta_Jets",20,0,5),"Evt_Jet_MaxDeta_Jets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M2_TaggedJetsAverage","Evt_M2_TaggedJetsAverage",20,0.0,400.0),"Evt_M2_TaggedJetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M3","Evt_M3",20,0.0,400.0),"Evt_M3",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_JetsAverage","Evt_M_JetsAverage",20,0.0,30.0),"Evt_M_JetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_MedianTaggedJets","Evt_M_MedianTaggedJets",20,30.0,400.0),"Evt_M_MedianTaggedJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_MinDeltaRJets","Evt_M_MinDeltaRJets",20,10.0,250.0),"Evt_M_MinDeltaRJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_MinDeltaRTaggedJets","Evt_M_MinDeltaRTaggedJets",20,10.0,300.0),"Evt_M_MinDeltaRTaggedJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_M_TaggedJetsAverage","Evt_M_TaggedJetsAverage",20,0.0,50.0),"Evt_M_TaggedJetsAverage",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Pt_MinDeltaRJets","Evt_Pt_MinDeltaRJets",20,0.0,400.0),"Evt_Pt_MinDeltaRJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Pt_MinDeltaRTaggedJets","Evt_Pt_MinDeltaRTaggedJets",20,0.0,400.0),"Evt_Pt_MinDeltaRTaggedJets",plotselection,plotlabel),
    #Plot(ROOT.TH1F(plotprefix+"Evt_Pt_PrimaryLepton","Evt_Pt_PrimaryLepton",20,0.0,400.0),"Evt_Pt_PrimaryLepton",plotselection,plotlabel),    
    #Plot(ROOT.TH1F(plotprefix+"Evt_blr_ETH","Evt_blr_ETH",20,0.0,1.1),"Evt_blr_ETH",plotselection,plotlabel),
    Plot(ROOT.TH1F(plotprefix+"Evt_blr_ETH_transformed","Evt_blr_ETH_transformed",20,-10.0,10.0),"Evt_blr_ETH_transformed",plotselection,plotlabel),
]
# combine all plots in one list
plots=plots_inclusive+plots64+plots63+plots62+plots54+plots53+plots44+plots43+bdts


#print samples
#print plots

#outputpath = plotParallel(name,100000,plots,samples)
outputpath=plotParallel(name,1000000,plots,sample_ttbar_nom+samples+systsamples,[''],['1.'],weightsystnames,systweights,additionalvariables,[],"/nfs/dust/cms/user/mwassmer/pyroot-plotscripts/treejson.json",othersystnames) 

listOfHistoLists=createHistoLists_fromSuperHistoFile(outputpath,samples,plots,1)
listOfHistoLists_ot=createHistoLists_fromSuperHistoFile(outputpath,sample_ttbar_nom,plots,1)

renameHistos(outputpath,outputpath[:-4]+'_syst.root',weightsystnames+othersystnames,False)

lll=createLLL_fromSuperHistoFileSyst(outputpath[:-4]+'_syst.root',sample_ttbar_nom,plots,weightsystnames+othersystnames)

#print listOfHistoLists_ot
#print "--------------------------"
#print listOfHistoLists
#print "--------------------------"
#print lll

#writeListOfHistoListsAN(listOfHistoLists,sample_ttbar_nom+samples,"",name,True,False,False,'histo',False,False,True)



labels=[plot.label for plot in plots]
#lolT=transposeLOL(listOfHistoLists)

# with this function the nominal ttbar sample is plotted with all the uncertainties on top of the samples which have variated top mass (no uncertainties for those)
plotRefWsystandOthers(listOfHistoLists,samples,listOfHistoLists_ot,sample_ttbar_nom[0],name,[[lll,3354,ROOT.kBlack,True]],logscale=False,label=labels,ratio=True,blinded=False)

