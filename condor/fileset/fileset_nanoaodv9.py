import os
from pprint import pprint

#signalMCDir = {
#	"UL2016": {
#		"ZprimeTo3Gluon": "/eos/user/x/xuyan/TrijetData/NanoAODs/ZprimeTo3Glu_2016UL"
#	},
#	"UL2017": {
#		"ZprimeTo3Gluon": "/eos/user/x/xuyan/TrijetData/NanoAODs/ZprimeTo3Gluon_mCutpm0p5_20210810233621"
#	},
#	"UL2018": {
#		"ZprimeTo3Gluon": "/eos/user/x/xuyan/TrijetData/NanoAODs/ZprimeTo3Glu_2018UL"
#	}
#}

data = {
	"UL2016": {
		"JetHT" : ["/JetHT/Run2016B-ver1_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD",
					"/JetHT/Run2016B-ver2_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD",
					"/JetHT/Run2016C-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD",
					"/JetHT/Run2016D-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD",
					"/JetHT/Run2016E-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD",
					"/JetHT/Run2016F-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD",
					"/JetHT/Run2016F-UL2016_MiniAODv2_NanoAODv9-v2/NANOAOD",
					"/JetHT/Run2016G-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD",
					"/JetHT/Run2016H-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"], 
	},
	"UL2017": {
		"JetHT" : [ "/JetHT/Run2017B-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD",
                    "/JetHT/Run2017C-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD",
                    "/JetHT/Run2017D-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD",
                    "/JetHT/Run2017E-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD",
                    "/JetHT/Run2017F-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD",
                   ],
                    # QCD
                    "QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8": [ "/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"], 
                    "QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8": [  "/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"], 
                    "QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8" : ["/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"], 
                    "QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8"  : ["/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"], 
                    "QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8"  : ["/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"], 
                    "QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8" : ["/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"], 
                    "QCD_HT100to200_TuneCP5_13TeV-madgraphMLM-pythia8" : ["/QCD_HT100to200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"], 
                    "QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8" : ["/QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"], 
                    # ttbar
                    "TTToHadronic_TuneCP5_13TeV-powheg-pythia8"        : ["/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"], 
                    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8"    : ["/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"], 
                    "TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8" : ["/TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM"],
                    "TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8" : ["/TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM"],
                    # vv
                    "ZZTo4Q_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8" : ["/ZZTo4Q_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"],
                    "WWTo4Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8" : ["/WWTo4Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"],
                    #vvv
                    "WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8" : ["/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"],
                    "ZZZ_TuneCP5_13TeV-amcatnlo-pythia8" : ["/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"],
                    "WZZ_TuneCP5_13TeV-amcatnlo-pythia8" : ["/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"],
                    "WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8" : ["/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"],
                    # v+jets
                    "ZJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8" : ["/ZJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM"],
                    "ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8" : ["/ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM"],
                    "ZJetsToQQ_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8" : ["/ZJetsToQQ_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM"],
                    "ZJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8" : ["/ZJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM"],
                    "WJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8" : ["/WJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM"],
                    "WJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8" : ["/WJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM"],
                    "WJetsToQQ_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8" : ["/WJetsToQQ_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM"],
                    "WJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8" : ["/WJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM"],
	},
	"UL2018": {
		"JetHT" : ["/JetHT/Run2018A-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD",
					"/JetHT/Run2018B-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD",
					"/JetHT/Run2018C-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD",
					"/JetHT/Run2018D-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD"], 
        }
}

if __name__ == "__main__":
    #for year in ["UL2016","UL2017","UL2018"]:
    for year in ["UL2017"]:
        print(year)
        for sample, subsamples in data[year].items():
            print(sample)
            for subsample in subsamples:
                pdname = subsample.split("/")[1]
                #if("QCD" in sample):
                #    samplename = year + "_" + pdname
                #else:
                pdpostfix = subsample.split("/")[2].split("_")[0]
                samplename = year + "_" + pdname + "_" + pdpostfix
                os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee v9/textfiles/{}.txt".format(subsample, samplename))
                with open("v9/textfiles/%s.txt"%(samplename), 'r') as f:
                    list_samples = f.read()
                list_samples = list_samples.replace('/store/','root://cmsxrootd.fnal.gov//store/')
                list_name = "../list/nano/v9/%s/%s_%s.list"%(year.replace('UL',''),sample,pdpostfix.split('-')[0].replace('Run',''))
                if 'JetHT' not in sample:
                    list_name = "../list/nano/v9/%s/%s.list"%(year.replace('UL',''),sample)
                print(list_name)
                with open(list_name, 'w') as o:
                    o.write(list_samples)
