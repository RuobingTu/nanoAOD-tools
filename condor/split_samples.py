"""
Splits sample files in the `source_dir` into training and testing data 

Creates 'train' and 'test' directories in the `source_dir` and moves the files in them

"""
import os
import subprocess

eosbase = "root://cmseos.fnal.gov/"

def eos_rec_search(startdir,suffix,dirs):
    dirlook = subprocess.check_output(f"eos {eosbase} ls {startdir}", shell=True).decode('utf-8').split("\n")[:-1]
    donedirs = [[] for d in dirlook]
    for di,d in enumerate(dirlook):
        if d.endswith(suffix):
            donedirs[di].append(startdir+"/"+d)
        elif d=="log":
            continue
        else:
            # print(f"Searching {d}")
            donedirs[di] = donedirs[di] + eos_rec_search(startdir+"/"+d,suffix,dirs+donedirs[di])
    donedir = [d for da in donedirs for d in da]
    return dirs+donedir

from pathlib import Path
import random
import shutil
from math import ceil

#source_dir = '/store/user/cmantill/PFNano/training/ak15_pfnano_Nov29/'
#source_dir = '/store/user/cmantill/PFNano/training/ak8_pfnano_Nov29/'
#source_dir = '/store/user/cmantill/PFNano/training/ak15_Oct29/'
#source_dir = '/store/user/lpcdihiggsboost/cmantill/DNNtuples/'
#source_dir = '/store/user/lpchbb/cmantill/v2_2/DNNTuples/'
source_dir = '/store/user/lpcdihiggsboost/cmantill/DNNtuples_coli/'
SPLIT_FRAC = 0.15  # fraction of data for testing

samples = os.listdir(f"/eos/uscms/{source_dir}")

for sample in samples:
    if sample == 'test' or sample == 'train': continue

    print(f"splitting {sample}")
    Path(f'/eos/uscms/{source_dir}/train/{sample}').mkdir(parents=True, exist_ok=True)
    Path(f'/eos/uscms/{source_dir}/test/{sample}').mkdir(parents=True, exist_ok=True)

    curdir = f"{source_dir}/{sample}/"
    files = eos_rec_search(curdir,".root",[])
    
    random.shuffle(files)
    split_index = ceil(len(files) * SPLIT_FRAC)

    if len(files)==1:
        f = files[0].split('/')[-1]
        fl = files[0].replace(eosbase,'/eos/uscms/')
        shutil.move(f'/eos/uscms/{fl}', f'/eos/uscms/{source_dir}/test/{sample}/{f}')
    else:
        for file in files[:split_index]:
            fl = file.replace(eosbase,'/eos/uscms/')
            f = file.split('/')[-1]
            shutil.move(f'/eos/uscms/{fl}', f'/eos/uscms/{source_dir}/test/{sample}/{f}')
        for file in files[split_index:]:
            fl = file.replace(eosbase,'/eos/uscms/')
            f = file.split('/')[-1]
            shutil.move(f'/eos/uscms/{fl}', f'/eos/uscms/{source_dir}/train/{sample}/{f}')
