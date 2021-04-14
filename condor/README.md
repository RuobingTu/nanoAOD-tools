# Condor submission for training inputs

## Making tarball
```bash
tar -zvcf CMSSW_11_1_0_pre5_PY3.tgz CMSSW_11_1_0_pre5_PY3 --exclude="*.root" --exclude="*.pdf" --exclude="*.pyc" --exclude=tmp --exclude="*.tgz" --exclude-vcs --exclude-caches-all --exclude="*err*" --exclude=*out_* --exclude=condor
```

## Submitting inputs for training
```
python skim.py --tag 28Feb21
```