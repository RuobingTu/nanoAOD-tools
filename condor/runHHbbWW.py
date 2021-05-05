#!/usr/bin/env python
from __future__ import print_function

import os
import copy

from runPostProcessing import get_arg_parser, run
import logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

nn_cfgname = 'hhbbWW_cfg.json'
default_config = {'run_mass_regression': False, 'mass_regression_versions': ['V01a', 'V01b', 'V01c'],
                  'WRITE_CACHE_FILE': False}

golden_json = {
    2016: 'Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt',
    2017: 'Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt',
    2018: 'Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt',
}

# Sum$() counts the number of FatJets that satisfy that condition
cut_dict_ak8 = {
    '1': 'Sum$(FatJet_pt > 250)>0'
}

# set samples to None this if you want to run over all the samples (e.g. for data)
# else, you can use this dict
samples = {
    2016: [], 
    2017: [],
    2018: [],
}
samples = None 

def _process(args):
    args.jet_type = 'ak8'
    default_config['jetType'] = args.jet_type
    
    default_config['run_tagger'] = True
    default_config['tagger_versions'] = ['V01']
    default_config['WRITE_CACHE_FILE'] = False

    year = int(args.year)
    option = args.option
    default_config['year'] = year
    default_config['option'] = option

    args.weight_file = 'samples/xSections.dat'

    basename = os.path.basename(args.outputdir) + '_' + args.jet_type + '_option' + option + '_' + str(year)
    args.outputdir = os.path.join(os.path.dirname(args.outputdir), basename, 'data' if args.run_data else 'mc')
    args.jobdir = os.path.join('jobs_%s' % basename, 'data' if args.run_data else 'mc')
    if args.run_signal:
        args.outputdir = args.outputdir.replace('mc','signal')
        args.jobdir = os.path.join('jobs_%s' % basename, 'signal')

    sample_str = "hhbbWW"

    if args.run_data:
        args.datasets = '%s/%s_%d_DATA.yaml' % (args.sample_dir, sample_str, year)
        args.extra_transfer = os.path.expandvars(
            '$CMSSW_BASE/src/PhysicsTools/NanoNN/data/JSON/%s' % golden_json[year])
        args.json = golden_json[year]
    elif args.run_signal:
        args.datasets = '%s/%s_%d_signalMC.yaml' % (args.sample_dir, sample_str, year)
    else:
        args.datasets = '%s/%s_%d_MC.yaml' % (args.sample_dir, sample_str, year)
        if samples:
            args.select = ','.join(samples[year])

    if args.run_signal:
        args.imports = [('PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule',
                              'countHistogramsProducer')]
        args.imports.extend([('PhysicsTools.NanoNN.producers.hhbbWWProducer','hhbbWWProducerFromConfig')])
    else:
        args.imports = [('PhysicsTools.NanoNN.producers.hhbbWWProducer','hhbbWWProducerFromConfig')]
        args.cut = cut_dict_ak8[str(option)]

    if not args.run_data:
        args.imports.extend([('PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer',
                              'puAutoWeight_2017' if year == 2017 else 'puWeight_%d' % year)])

    # select branches
    args.branchsel_in = None
    args.branchsel_out = os.path.expandvars('$CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/branch_hh4b_output.txt')

    # data, or just nominal MC
    cfg = copy.deepcopy(default_config)
    if args.run_data:
        cfg['jes'] = None
        cfg['jer'] = None
        cfg['met_unclustered'] = None
    print('run ', args, nn_cfgname)
    run(args, configs={nn_cfgname: cfg})
    return

def main():
    parser = get_arg_parser()

    parser.add_argument('--option',
                        type=str,
                        required=True,
                        help='Selection option'
                        )

    parser.add_argument('--run-data',
                        action='store_true', default=False,
                        help='Run over data. Default: %(default)s'
                        )

    parser.add_argument('--run-signal',
                        action='store_true', default=False,
                        help='Run over signal. Default: %(default)s'
                        )

    parser.add_argument('--year',
                        type=str,
                        required=True,
                        help='Year: 2016, 2017, 2018, or comma separated list e.g., `2016,2017,2018`'
                        )

    parser.add_argument('--sample-dir',
                        type=str,
                        default='samples',
                        help='Directory of the sample list files. Default: %(default)s'
                        )

    args = parser.parse_args()
    years = args.year.split(',')
    categories = ['data' if args.run_data else 'mc']

    for year in years:
        for cat in categories:
            opts = copy.deepcopy(args)
            if cat == 'data':
                opts.run_data = True
                opts.nfiles_per_job *= 2
            opts.year = year
            logging.info('year=%s, cat=%s, syst=%s', opts.year,
                         'data' if opts.run_data else 'mc', 'none')
            _process(opts)


if __name__ == '__main__':
    main()
