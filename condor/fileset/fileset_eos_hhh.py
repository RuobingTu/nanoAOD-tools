import os
import subprocess
import json

pfnano_tag = "v9"


year = '2017'
dataset = "JetHT"
sample = '%s%s'%(dataset,year)

letters = {'2017' : ['B','C','D','E','F']}

letter = 'B'



sample_dict = {}

for s in [sample]:
    dataset_dict = {}
    for ds in ['JetHT']:
        list_samples = []
        for letter in letters[year]:
            data_input = 'v9/textfiles/UL%s_%s_Run%s%s-UL%s.txt'%(year, dataset, year ,letter, year)
            with open(data_input , 'r') as f:
                lines = f.read().split('\n')
            lines = [l for l in lines if l != '']
        dataset_dict[ds] = lines
    sample_dict[s] = dataset_dict

with open(f"{pfnano_tag}/{year}.json", 'w') as f:
    json.dump(sample_dict, f, indent=4, sort_keys = True)


