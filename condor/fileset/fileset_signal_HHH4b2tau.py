# Script to create fileset for HHH signal 

import os, glob

path = '/isilon/data/users/mstamenk/hhh-4b2tau-samples-nano/'

sample_name = 'RunIISummer20UL17NANOAODSIM_%s.root'


samples = glob.glob(path + '/' + sample_name%'*')

#print(samples)

filename = 'GluGluToHHHTo4B2Tau_SM.list'
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

