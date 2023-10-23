import os, glob


samples = ['hh4b-sm','hh4b-bsm','hh2b2tau-sm','hh2b2tau-bsm','hhh6b-sm','hhh4b2tau-sm']

path_samples = '/isilon/data/users/mstamenk/mc-for-trigger/samples/'

path_out = 'trigger/2023/'

sample = samples[0]

for sample in samples:
    ls = glob.glob(path_samples + '/' + sample + '/*.root')
    out = ''
    for el in ls:
        out+=el+'\n'

    name_out = '%s.list'%sample

    print("Writing %s"%name_out)
    with open(path_out + '/' + name_out, 'w') as f:
        f.write(out)
        print(out)
       




