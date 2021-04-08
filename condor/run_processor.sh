#!/bin/bash

jobid=$1

# remove old
source /cvmfs/cms.cern.ch/cmsset_default.sh
rm *.tgz

# copy environment
xrdcp -f root://cmseos.fnal.gov//store/user/cmantill/CMSSW_11_1_0_pre5_PY3.tgz ./CMSSW_11_1_0_pre5_PY3.tgz
tar -zxvf CMSSW_11_1_0_pre5_PY3.tgz
rm *.tgz
cd CMSSW_*/src
scram b ProjectRename
eval `scramv1 runtime -sh`
ls -l 
ls PhysicsTools/NanoAODTools/   
ls PhysicsTools/NanoNN/
export PYTHONPATH=PYTHONPATH:"${CMSSW_BASE}/lib/${SCRAM_ARCH}"
#cd PhysicsTools/NanoAODTools/

# run
cd ../../
ls -l
mkdir tmp/
python -c "import sys; print('\n'.join(sys.path))"
export TMPDIR=`pwd`
python processor.py $jobid
status=$?

ls -l

exit $status
