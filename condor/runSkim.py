import json
import os
import re
import sys

import argparse

import htcondor

pjoin = os.path.join

# list of samples to run
samples = {}
samples["AK8"] = {
    "2017preULpriv": ["GravitonToHHToWWWW"],
    "2017UL": [
        "QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8" 
        "QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8",
        "QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8",
        "QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8",
        "QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8",
        "QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8",
        "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8"
    ],
    "2017preUL": [
        "VBFHToWWToLNuQQ_M125_NNPDF31_TuneCP5_PSweights_13TeV_powheg_JHUGen710_pythia8",
        "GluGluHToWWToLNuQQ_M125_NNPDF31_TuneCP5_PSweights_13TeV_powheg_JHUGen710_pythia8"
        "GluGluZH_HToWW_M125_13TeV_powheg_pythia8_TuneCP5",
        "HWminusJ_HToWW_M125_13TeV_powheg_pythia8_TuneCP5",
        "HWplusJ_HToWW_M125_13TeV_powheg_pythia8_TuneCP5",
        "HZJ_HToWW_M125_13TeV_powheg_jhugen714_pythia8_TuneCP5",
        "GluGluToHHTo2B2WToLNu2J_node_1_TuneCP5_PSWeights_13TeV-madgraph-pythia8",
        "GluGluToHHTo2B2VLNu2J_node_cHHH1_TuneCP5_PSWeights_13TeV-powheg-pythia8",
        "GluGluToHHTo4V_node_cHHH1_TuneCP5_PSWeights_13TeV-powheg-pythia8"
    ]
}

samples["AK15"] = {
    "2017preULpriv_ak15": ["GravitonToHHToWWWW"],
    "2017preUL_ak15": [
        "VBFHToWWToLNuQQ_M125_NNPDF31_TuneCP5_PSweights_13TeV_powheg_JHUGen710_pythia8",
        "GluGluHToWWToLNuQQ_M125_NNPDF31_TuneCP5_PSweights_13TeV_powheg_JHUGen710_pythia8",
        "GluGluZH_HToWW_M125_13TeV_powheg_pythia8_TuneCP5",
        "HWminusJ_HToWW_M125_13TeV_powheg_pythia8_TuneCP5",
        "HWplusJ_HToWW_M125_13TeV_powheg_pythia8_TuneCP5",
        "HZJ_HToWW_M125_13TeV_powheg_jhugen714_pythia8_TuneCP5",
        "GluGluToHHTo4V_node_cHHH1_TuneCP5_PSWeights_13TeV-powheg-pythia8",
        "QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8",
        "QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8",
        "QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8",
        "QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8",
        "QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8",
        "QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8",
        "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8",
        "TTToHadronic_TuneCP5_13TeV-powheg-pythia8"],
}

# submit job for a dataset
def submit_job(dataset, files, tag, jet, test=False):
    
    outdir = "/store/user/cmantill/PFNano/training/%s/%s"%(tag, dataset)
        
    os.system("eos root://cmseos.fnal.gov/ mkdir -p %s"%outdir) 
            
    # max-entries (for input only now)
    nentries = 50000
    
    # script to run
    execname = "run_skim_input.sh"
    executable = os.path.abspath("./%s"%execname)

    for ifile,f in enumerate(files):
        if test:
            if ifile>0: continue

        lfiles = f
        
        cut = "(FatJet_pt>300&&FatJet_msoftdrop>20)"
        if jet=="AK15": cut = "(FatJetAK15_pt>300&&FatJetAK15_msoftdrop>20)"

        arguments = [
            f,
            nentries,
            tag,
            dataset,
            jet,
            cut
        ]
        
        # define submission settings
        subdir = "log/%s/"%tag
        os.system('mkdir -p %s'%subdir)

        condor_templ_file = open("run_skim_input.jdl")
        jobfile = pjoin(subdir, "%s_%s_%i.jdl"% (execname.replace('.sh',''), dataset, ifile) )                                                                                                           
        condor_file = open(jobfile,"w")
        for line in condor_templ_file:
            line=line.replace('DIREXE',executable)
            line=line.replace('DIRECTORY',subdir)
            line=line.replace('PREFIX',dataset)
            line=line.replace('JOBID',str(ifile))
            line=line.replace('ARGS'," ".join([str(x) for x in arguments]))
            condor_file.write(line)
        condor_file.close()
        
        os.system('condor_submit %s'%jobfile)
        
def main(args):
    for fileset in samples[args.jet].keys():
        with open("fileset/%s.json"%fileset) as f:
            datasets = json.loads(f.read())

        for dataset,files in datasets.items():
            if dataset in samples[args.jet][fileset]:
                submit_job(dataset, files, args.tag, args.jet, args.test)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--tag',        dest='tag',      default="test", help="output tag")
    parser.add_argument('--jet',        dest='jet',      default="AK8", help="jet Type")
    parser.add_argument('--test',       dest='test',     action='store_true', default=False, help="test with one file")

    args = parser.parse_args()

    main(args)
