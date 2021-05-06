#!/usr/bin/env python
from __future__ import print_function

import os
import copy

from runPostProcessing import get_arg_parser, run
import logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

nn_cfgname = 'hh4b_cfg.json'
default_config = {'run_mass_regression': False, 'mass_regression_versions': ['V01a', 'V01b', 'V01c'],
                  'WRITE_CACHE_FILE': False,
                  'jec': False, 'jes': None, 'jes_source': '', 'jes_uncertainty_file_prefix': '',
                  'jer': 'nominal', 'met_unclustered': None, 'smearMET': True, 'applyHEMUnc': False,
                  'allJME': False,
}

golden_json = {
    2016: 'Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt',
    2017: 'Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt',
    2018: 'Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt',
}

# Sum$() counts the number of FatJets that satisfy that condition
cut_dict_ak8 = {
    '5': 'Sum$(FatJet_pt > 250)>0 && Sum$((FatJet_ParticleNetMD_probXbb/(1.0-FatJet_ParticleNetMD_probXcc-FatJet_ParticleNetMD_probXqq))>0.8)>0',
    '10': 'Sum$(FatJet_pt > 200)>0 && Sum$(FatJet_tau3/FatJet_tau2 >= 0.54)>0',
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
    if args.run_mass_regression:
        default_config['run_mass_regression'] = True
        if args.jet_type == 'ak8':
            default_config['mass_regression_versions'] = ['ak8V01a', 'ak8V01b', 'ak8V01c']
        logging.info('Will run mass regression version(s): %s' % ','.join(default_config['mass_regression_versions']))

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

    sample_str = "hh4b"
    if option == "10": sample_str = "tt"

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
        args.imports.extend([('PhysicsTools.NanoNN.producers.hh4bProducer','hh4bProducerFromConfig')])
    else:
        args.imports = [('PhysicsTools.NanoNN.producers.hh4bProducer','hh4bProducerFromConfig')]
        args.cut = cut_dict_ak8[str(option)]

    if not args.run_data:
        args.imports.extend([('PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer',
                              'puAutoWeight_2017' if year == 2017 else 'puWeight_%d' % year)])

    # select branches
    args.branchsel_in = None
    args.branchsel_out = os.path.expandvars('$CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/branch_hh4b_output.txt')

    # data, or just nominal MC
    if args.run_data or not args.run_syst:
        cfg = copy.deepcopy(default_config)
        # set all JME to true
        cfg['allJME'] = True
        if args.run_data:
            cfg['allJME'] = False
            cfg['jes'] = None
            cfg['jer'] = None
            cfg['met_unclustered'] = None
        print('run ', args, nn_cfgname)
        run(args, configs={nn_cfgname: cfg})
        return

    # MC for syst
    if args.run_syst and not args.run_data:

        # nominal w/ PDF/Scale weights
        '''
        logging.info('Start making nominal trees with PDF/scale weights...')
        syst_name = 'LHEWeight'
        opts = copy.deepcopy(args)
        cfg = copy.deepcopy(default_config)
        opts.outputdir = os.path.join(os.path.dirname(opts.outputdir), syst_name)
        opts.jobdir = os.path.join(os.path.dirname(opts.jobdir), syst_name)
        opts.branchsel_out = os.path.expandvars('$CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/branch_hh4b_output_LHEweights.txt'
        run(opts, configs={nn_cfgname: cfg})
        '''

        # JES up/down
        for variation in ['up', 'down']:
            syst_name = 'jes_%s' % variation
            logging.info('Start making %s trees...' % syst_name)
            opts = copy.deepcopy(args)
            cfg = copy.deepcopy(default_config)
            cfg['jes'] = variation
            opts.outputdir = os.path.join(os.path.dirname(opts.outputdir), syst_name)
            opts.jobdir = os.path.join(os.path.dirname(opts.jobdir), syst_name)
            if args.run_signal:
                print('run signal')
                opts.outputdir = opts.outputdir+'_signal'
                opts.jobdir = opts.jobdir+'_signal'
            run(opts, configs={nn_cfgname: cfg})

        # JER up/down
        for variation in ['up', 'down']:
            syst_name = 'jer_%s' % variation
            logging.info('Start making %s trees...' % syst_name)
            opts = copy.deepcopy(args)
            cfg = copy.deepcopy(default_config)
            cfg['jer'] = variation
            opts.outputdir = os.path.join(os.path.dirname(opts.outputdir), syst_name)
            opts.jobdir = os.path.join(os.path.dirname(opts.jobdir), syst_name)
            if args.run_signal:
                print('run signal')
                opts.outputdir = opts.outputdir+'_signal'
                opts.jobdir = opts.jobdir+'_signal'
            run(opts, configs={nn_cfgname: cfg})

        # MET unclustered up/down
        '''
        for variation in ['up', 'down']:
            syst_name = 'met_%s' % variation
            logging.info('Start making %s trees...' % syst_name)
            opts = copy.deepcopy(args)
            cfg = copy.deepcopy(default_config)
            cfg['met_unclustered'] = variation
            opts.outputdir = os.path.join(os.path.dirname(opts.outputdir), syst_name)
            opts.jobdir = os.path.join(os.path.dirname(opts.jobdir), syst_name)
            run(opts, configs={nn_cfgname: cfg})
        '''

def main():
    parser = get_arg_parser()

    parser.add_argument('--option',
                        type=str,
                        required=True,
                        help='Selection option'
                        )

    parser.add_argument('--run-syst',
                        action='store_true', default=False,
                        help='Run all the systematic trees. Default: %(default)s'
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

    parser.add_argument('--run-mass-regression',
                        action='store_true', default=True,
                        help='Run mass regression. Default: %(default)s'
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
                         'data' if opts.run_data else 'mc', 'syst' if opts.run_syst else 'none')
            _process(opts)


if __name__ == '__main__':
    main()
