# nanoAOD-tools *Custom*
Tools for working with NanoAOD (requiring only python + root, not CMSSW)

## Set up CMSSW (w PY3), NanoAOD-tools and NanoNN

Python3 is needed to re-run the taggers w/ ONNXRuntime.
`NanoNN` is needed for taggers/regression and PF inputs.
It also contains the module for the hh4b analysis selection.

    cd CMSSW_11_1_0_pre5_PY3/src
    git clone git@github.com:cmantill/nanoAOD-tools.git PhysicsTools/NanoAODTools
    git clone git@github.com:cmantill/NanoNN.git PhysicsTools/NanoNN
    cd PhysicsTools/NanoAODTools
    cmsenv
    scram b

## Testing the post-processing step locally

They can be found in the [nanoAOD-tools](https://github.com/cms-nanoAOD/nanoAOD-tools#general-instructions-to-run-the-post-processing-step) repo.

For example, to test the [hh4bProducer](https://github.com/cmantill/NanoNN/blob/main/python/producers/hh4bProducer.py):

    python scripts/nano_postproc.py tmp/ root://cmseos.fnal.gov//store/group/lpcdihiggsboost/NanoTuples/V2p0/MC_Fall17/v1/GluGluToHHTo4B_node_cHHH1_TuneCP5_PSWeights_13TeV-powheg-pythia8/NanoTuples-V2p0_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v1/200801_230741/0000/nano_16.root -I PhysicsTools.NanoNN.producers.hh4bProducer hh4bProducer_2017 --cut "(FatJet_pt>250)" -N 1000 --bo scripts/branch_hh4b_output.txt

Here:
* `tmp` is the output directory
* `root://cmseos.fnal.gov//store/group/lpcdihiggsboost/NanoTuples/V2p0/MC_Fall17/v1/GluGluToHHTo4B_node_cHHH1_TuneCP5_PSWeights_13TeV-powheg-pythia8/NanoTuples-V2p0_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_v14-v1/200801_230741/0000/nano_16.root` is the input file
* `-I PhysicsTools.NanoNN.producers.hh4bProducer hh4bProducer_2017` is the module and function to run
* the `-c`,`--cut` option is used to pass a string expression (using the same syntax as in TTree::Draw) that will be used to select events.
* the `-J`,`--json` option is used to pass the name of a JSON file that will be used to select events. It is used for data events.
* the `-N` option is selecting only 1000 events for this test.
* `--bi` and `--bo` allows to specify the keep/drop file separately for input and output trees. For `hh4b` we use [these output branches](https://github.com/cmantill/nanoAOD-tools/blob/master/scripts/branch_hh4b_output.txt)

## Scripts to create jobs

Condor directory:

    cd Physics/NanoAODTools/condor
    
All the samples are listed [here](https://github.com/cmantill/nanoAOD-tools/tree/master/condor/samples) in yaml files that point to list of files.

The main script to produce condor jobs (and later submit them), is (runPostProcessing.py)[https://github.com/cmantill/nanoAOD-tools/blob/master/condor/runPostProcessing.py], e.g.:

    python runPostProcessing.py [-i /path/of/input] -o /path/to/output -d datasets.yaml -I PhysicsTools.NanoNN.producers.hh4bProducer hh4bProducer_2017 -n 1

However, the [runHH4b.py](https://github.com/cmantill/nanoAOD-tools/blob/master/condor/runHH4b.py) script allows to create the metadata json with all the options needed for the producer.

Inside `runHH4b.py` you can specify the samples you want to run for each year [here](https://github.com/cmantill/nanoAOD-tools/blob/master/condor/runHH4b.py#L26-L29).

To run, and create jobs:

    python runHH4b.py --option OPTION -o EOSOUTPUTDIR --year YEAR
    
Here:
* `--option` is equivalent to the selection option in the HHBoostedAnalyzer. Although for now only option=5 (signal region) has been implemented.
* `-o` is the output directory in eos.
* `--year` is the sample year.

## Preparing to running jobs

First, you need to re-tar the CMSSW environment (this needs to be re-done if you modify the producer):

   cd $CMSSW_BASE/../
   tar -zvcf CMSSW_11_1_0_pre5_PY3.tgz CMSSW_11_1_0_pre5_PY3 --exclude="*.pdf" --exclude="*.pyc" --exclude=tmp --exclude="*.tgz" --exclude-vcs --exclude-caches-all --exclude="*err*" --exclude=*out_* --exclude=condor```

and then copy to your eos directory (change username here):

   mv CMSSW_11_1_0_pre5_PY3.tgz /eos/uscms/store/user/cmantill/

You will also need to change the condor script that points to this tar in [run_processor.sh](https://github.com/cmantill/nanoAOD-tools/blob/master/condor/run_processor.sh#L10).

## Running jobs

Once you have made these changes you can run:

   python runHH4b.py --option 5 -o  /eos/uscms/store/user/cmantill/analyzer/test --year 2018

which will.

## Re-weighting samples

Compile NormalizeNtuple:

   ./NormalizeNtuple inputlist.txt 1



    
    
    