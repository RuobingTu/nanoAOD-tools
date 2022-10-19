# Script to create fileset for HHH signal 

import os, glob

path = '/isilon/data/users/mstamenk/qcd-ht-6b/'

sample_name = 'RunIISummer20UL17NANOAODSIM_%s.root'

qcd_samples = ['QCD_HT100to200','QCD_HT200to300','QCD_HT300to500','QCD_HT500to700','QCD_HT700to1000','QCD_HT1000to1500','QCD_HT1500to2000','QCD_HT2000toInf']

post_fix = '_6b_TuneCP5_13TeV-madgraphMLM-pythia8'

for qcd in qcd_samples:
    samples = glob.glob(path + '/' + qcd + '/' + sample_name%'*')


    #print(samples)

    filename = '%s%s.list'%(qcd,post_fix)
    filepath = '/isilon/data/users/mstamenk/hhh-6b-producer/CMSSW_11_1_0_pre5_PY3/src/PhysicsTools/NanoAODTools/condor/list/nano/v9/2017/'


    out = ''
    for s in samples:
        if s != samples[-1]:
            out += '%s\n'%s
        else:
            out += '%s'%s

    print("Writing file %s%s"%(filepath,filename))
    with open(filepath + '/' + filename, 'w') as f:
        f.write(out)

