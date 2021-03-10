import os
import subprocess
import json

eosbase = "root://cmseos.fnal.gov/"
eosdir = "/store/user/cmantill/PFNano/"

dirlist = [
    ["2017_preUL_private", "2017preULpriv", 
     ["GravitonToHHToWWWW"]],
    ["2017", "2017UL",
     ["QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8"
      "QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8",
      "QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8",
      "QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8",
      "QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8",
      "QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8",
      "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8"]],
    ["2017_preUL", "2017preUL",
     ["VBFHToWWToLNuQQ_M125_NNPDF31_TuneCP5_PSweights_13TeV_powheg_JHUGen710_pythia8",
      "GluGluHToWWToLNuQQ_M125_NNPDF31_TuneCP5_PSweights_13TeV_powheg_JHUGen710_pythia8"
      "GluGluZH_HToWW_M125_13TeV_powheg_pythia8_TuneCP5",
      "HWminusJ_HToWW_M125_13TeV_powheg_pythia8_TuneCP5",
      "HWplusJ_HToWW_M125_13TeV_powheg_pythia8_TuneCP5",
      "HZJ_HToWW_M125_13TeV_powheg_jhugen714_pythia8_TuneCP5",
      "GluGluToHHTo2B2WToLNu2J_node_1_TuneCP5_PSWeights_13TeV-madgraph-pythia8",
      "GluGluToHHTo2B2VLNu2J_node_cHHH1_TuneCP5_PSWeights_13TeV-powheg-pythia8",
      "GluGluToHHTo4V_node_cHHH1_TuneCP5_PSWeights_13TeV-powheg-pythia8"]],
]

def eos_rec_search(startdir,suffix,skiplist,dirs):
    dirlook = subprocess.check_output("eos %s ls %s"%(eosbase,startdir), shell=True).decode('utf-8').split("\n")[:-1]
    donedirs = [[] for d in dirlook]
    di = 0
    for d in dirlook:
        if d.endswith(suffix):
            donedirs[di].append(startdir+"/"+d)
        #elif any(skip in d for skip in skiplist):
        #    print("Skipping %s"%d)
        else:
            print("Searching %s"%d)
            donedirs[di] = donedirs[di] + eos_rec_search(startdir+"/"+d,suffix,skiplist,dirs+donedirs[di])
        di = di + 1
    donedir = [d for da in donedirs for d in da]
    return dirs+donedir

for dirs in dirlist:
    samples = subprocess.check_output("eos %s ls %s%s"%(eosbase,eosdir,dirs[0]), shell=True).decode('utf-8').split("\n")[:-1]
    jdict = {}
    for s in samples:
        if s not in dirs[2]: continue
        print("\tRunning on %s"%s)
        curdir = "%s%s/%s"%(eosdir,dirs[0],s)
        print('curdir ',curdir)
        dirlog = eos_rec_search(curdir,".root",dirs[2],[])
        if not dirlog:
            print("Empty sample skipped")
        else: 
            jdict[s] = [eosbase+d for d in dirlog]
    print(dirs[1],[s for s in jdict])
    with open("fileset/%s.json"%(dirs[1]), 'w') as outfile:
        json.dump(jdict, outfile, indent=4, sort_keys=True)
