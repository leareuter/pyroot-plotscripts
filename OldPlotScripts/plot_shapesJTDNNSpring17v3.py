import sys
import os
sys.path.insert(0, 'limittools')

from scriptgeneratorDNN import *
from plotutils import *
from limittools import renameHistos
from limittools import addPseudoData
from limittools import addRealData
from limittools import makeDatacards
from limittools import calcLimits
from limittools import replaceQ2scale
from plotconfigSpring17v3DNN import *

# output name
name='shapes_DNNJetTagv8'

# define categories
categories_=[
              ("(N_Jets==4&&N_BTagsM==2)","ljets_j4_t2",""),
              ("(N_Jets==5&&N_BTagsM==2)","ljets_j5_t2",""),
              ("(N_Jets==4&&N_BTagsM==3)","ljets_j4_t3",""),
              ("(N_Jets==4&&N_BTagsM>=4)","ljets_j4_t4",""),
              ("(N_Jets==5&&N_BTagsM==3)","ljets_j5_t3",""),
              ("(N_Jets==5&&N_BTagsM>=4)","ljets_j5_tge4",""),             
              ("(N_Jets>=6&&N_BTagsM==2)","ljets_jge6_t2",""),
              ("(N_Jets>=6&&N_BTagsM==3)","ljets_jge6_t3",""),
              ("(N_Jets>=6&&N_BTagsM>=4)","ljets_jge6_tge4","")
]
# DANGERZONE
# Need to remove the other node. Do not know what happens if the datacardmaker tries to use empty histograms
categories=[]

nhistobins= [  20,20, 	30,   30,    30,    30,   30,   30,   30 ]
minxvals=   [ 200, 200]+[0.0]*7
maxxvals=   [800,800]+[0.8]*7


# add unsplit categories
for cat in categories_:
  categories.append(cat)

print categories

# define MEM discriminator variable
memexp='(memDBp>0.0)*(memDBp_sig/(memDBp_sig+0.15*memDBp_bkg))+(memDBp<0.0)*(0.01)'

# define BDT output variables
bdtweightpath="/nfs/dust/cms/user/kelmorab/Spring17BDTWeights/"
bdtset="Spring17v1"
additionalvariables=[
			'finalbdt_ljets_j4_t2:=Evt_HT_Jets',
			'finalbdt_ljets_j5_t2:=Evt_HT_Jets',
                      #'finalbdt_ljets_j4_t3:='+bdtweightpath+'/weights_Final_43_'+bdtset+'.xml',
                      #'finalbdt_ljets_j4_t4:='+bdtweightpath+'/weights_Final_44_'+bdtset+'.xml',
                      #'finalbdt_ljets_j5_t3:='+bdtweightpath+'/weights_Final_53_'+bdtset+'.xml',
                      #'finalbdt_ljets_j5_tge4:='+bdtweightpath+'/weights_Final_54_'+bdtset+'.xml',
                      #'finalbdt_ljets_jge6_t2:='+bdtweightpath+'/weights_Final_62_'+bdtset+'.xml',
                      #'finalbdt_ljets_jge6_t3:='+bdtweightpath+'/weights_Final_63_'+bdtset+'.xml',
                      #'finalbdt_ljets_jge6_tge4:='+bdtweightpath+'/weights_Final_64_'+bdtset+'.xml',
                      #'finalbdt_ljets_boosted:='+bdtweightpath+'/weights_Final_DB_boosted_76xmem.xml',
                      "Muon_Pt","Electron_Pt","Muon_Eta","Electron_Eta","Jet_Pt","Jet_Eta","Jet_CSV","Jet_Flav","N_Jets","Jet_Phi","Jet_E","Jet_M",
                      "Evt_Pt_PrimaryLepton","Evt_E_PrimaryLepton","Evt_M_PrimaryLepton","Evt_Phi_PrimaryLepton","Evt_Eta_PrimaryLepton",
                      "Weight_CSV","Weight_CSVLFup","Weight_CSVLFdown","Weight_CSVHFup","Weight_CSVHFdown","Weight_CSVHFStats1up","Weight_CSVHFStats1down","Weight_CSVLFStats1up","Weight_CSVLFStats1down","Weight_CSVHFStats2up","Weight_CSVHFStats2down","Weight_CSVLFStats2up","Weight_CSVLFStats2down","Weight_CSVCErr1up","Weight_CSVCErr1down","Weight_CSVCErr2up","Weight_CSVCErr2down",
]

discrs =    ['finalbdt_ljets_j4_t2','finalbdt_ljets_j5_t2',
	     'aachen_Out_ttH','aachen_Out_ttH','aachen_Out_ttH','aachen_Out_ttH','aachen_Out_ttH','aachen_Out_ttH','aachen_Out_ttH',
	     ]
discrname='finaldiscr'
assert(len(nhistobins)==len(maxxvals))
assert(len(nhistobins)==len(minxvals))
assert(len(nhistobins)==len(categories))
assert(len(nhistobins)==len(discrs))

# get input for plotting function
bins= [c[0] for c in categories]
binlabels= [c[1] for c in categories]
samples=samplesShapes
allsystnames=weightsystnames[:1]

# adapt weights for exlusive samples
#systsamples=[]
#for sample in samples:
  #for sysname,sysfilename in zip(othersystnames,othersystfilenames):
    #thisnewsel=sample.selection
    #systsamples.append(Sample(sample.name+sysname,sample.color,sample.path.replace("nominal",sysfilename),thisnewsel,sample.nick+sysname,samDict=sampleDict))
  
allsamples=samples
samplesdata=samples_data_controlplots

# define plots
bdts=[]
print len(discrs),len(bins),len(binlabels),len(nhistobins),len(minxvals),len(maxxvals),
print len(zip(discrs,bins,binlabels,nhistobins,minxvals,maxxvals))
for discr,b,bl,nb,minx,maxx in zip(discrs,bins,binlabels,nhistobins,minxvals,maxxvals):
  bdts.append(Plot(ROOT.TH1F("finaldiscr_"+bl,"final discriminator ("+bl+")",nb,minx,maxx),discr,b))

print bdts
# plot everthing
outputpath=plotParallel(name,3000000,bdts,allsamples+samplesdata,[''],['1.'],weightsystnames[:1],systweights[:1],additionalvariables,[],"/nfs/dust/cms/user/kelmorab/plotscriptsSpring17/pyroot-plotscripts/treejson_Spring17v2_moreBKGs.json",othersystnames,True)

if not os.path.exists(name):
  os.makedirs(name)

# rename output histos and save in one file
renameHistos(outputpath,name+'/'+name+'_limitInput.root',allsystnames)
#replaceQ2scale( os.getcwd()+'/'+name+'/'+name+'_limitInput.root')

print samples
# add real/pseudo data
addPseudoData(name+'/'+name+'_limitInput.root',[s.nick for s in samples[9:]],binlabels,allsystnames,discrname)
#addRealData(name+'/'+name+'_limitInput.root',[s.nick for s in samples_data_controlplots],binlabels,discrname)

listOfHistoLists=createHistoLists_fromSuperHistoFile(outputpath,samples,bdts)
lolT=transposeLOL(listOfHistoLists)
#writeLOLAndOneOnTop(transposeLOL(lolT[9:]),samples[9:],lolT[0],samples[0],-1,name+'/'+name+'_controlplots')
writeListOfHistoListsAN(transposeLOL([lolT[0]]+lolT[9:]),[samples[0]]+samples[9:],"",name+'/'+name+'_shapes',True,False,False,'histo',False,True,False)
print listOfHistoLists
print samples
print samples[0]
print samples
for icat, cat in enumerate(categories):
  ttHHisto=listOfHistoLists[icat][0]
  ttHColor=samples[0].color
  ttHName=samples[0].name
  rocGraphs=[]
  rocNames=[]
  rocColors=[]
  for sample, histo in zip(samples[9:],listOfHistoLists[icat][9:]):
    rocGraphs.append(getROC(ttHHisto,histo))
    #rocGraphs[-1].SetColor(sample.color)
    rocNames.append(sample.name)
    rocColors.append(sample.color)
  writeListOfROCs(rocGraphs,rocNames,rocColors,name+'/'+name+'_ROC_'+cat[1])
  
  