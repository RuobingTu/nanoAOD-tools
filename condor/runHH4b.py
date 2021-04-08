#!/usr/bin/env python
from __future__ import print_function

import os
import copy

from runPostProcessing import get_arg_parser, run
import logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

nn_cfgname = 'hh4b_cfg.json'
default_config = {'run_mass_regression': False, 'mass_regression_versions': ['V01a', 'V01b', 'V01c'],
                  'jec': False, 'jes': None, 'jes_source': '', 'jes_uncertainty_file_prefix': '',
                  'jer': 'nominal', 'jmr': None, 'met_unclustered': None, 'smearMET': True, 'applyHEMUnc': False}

golden_json = {
    2016: 'Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt',
    2017: 'Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt',
    2018: 'Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt',
}

cut_dict_ak8 = {
    '5': 'Sum$(FatJet_pt > 250)>0 && (FatJet_ParticleNetMD_probXbb/(1.0-FatJet_ParticleNetMD_probXcc-FatJet_ParticleNetMD_probXqq) > 0.8)',
}

samples = {
    #2017: ['GluGluToHHTo4B_node_cHHH0_TuneCP5_PSWeights_13TeV-powheg-pythia8']
    2018: ['GluGluToHHTo4B_node_cHHH0_TuneCP5_PSWeights_13TeV-powheg-pythia8']
}

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

    if args.run_data:
        args.datasets = '%s/%d_DATA.yaml' % (args.sample_dir, year)
        args.extra_transfer = os.path.expandvars(
            '$CMSSW_BASE/src/PhysicsTools/NanoNN/data/JSON/%s' % golden_json[year])
        args.json = golden_json[year]
    else:
        args.datasets = '%s/hh4b_%d_MC.yaml' % (args.sample_dir, year)

    args.cut = cut_dict_ak8[str(option)]

    args.imports = [('PhysicsTools.NanoNN.producers.hh4bProducer','hh4bProducer_%d' %year)]
    #if not args.run_data:
    #    args.imports.extend([('PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer',
    #                          'puAutoWeight_2017' if year == 2017 else 'puWeight_%d' % year)])

    if samples:
        args.select = ','.join(samples[year])

    # select branches
    args.branchsel_in = None
    args.branchsel_out = os.path.expandvars('$CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/branch_hh4b_output.txt')

    # data, or just nominal MC
    if args.run_data or not args.run_syst:
        cfg = copy.deepcopy(default_config)
        if args.run_data:
            cfg['jes'] = None
            cfg['jer'] = None
            cfg['jmr'] = None
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

    parser.add_argument('--run-syst',
                        action='store_true', default=False,
                        help='Run all the systematic trees. Default: %(default)s'
                        )

    parser.add_argument('--run-data',
                        action='store_true', default=False,
                        help='Run over data. Default: %(default)s'
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
                        action='store_true', default=False,
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
