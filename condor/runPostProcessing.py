#!/usr/bin/env python
from __future__ import print_function
from six.moves import input

import os
import sys
import json
import re
import shutil

import logging
#logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)s: %(message)s')

def get_chunks(l, n):
    """Yield successive n-sized chunks from l. """
    for i in range(0, len(l), n):
        yield l[i:i + n]

def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

def get_filenames(listfile):
    """Return files for given list"""
    cmsswdir = os.environ['CMSSW_BASE']
    listdir =  os.path.abspath(os.path.expandvars('$CMSSW_BASE/src/PhysicsTools/NanoAODTools/condor/list/'))
    if not os.path.exists(listdir + '/' + listfile):
        print("listfile: " + listdir + '/' + listfile + " does not exist. skipping.")
        return []        
    lines = open(listdir +'/' + listfile, "r").readlines()
    filenames = []
    for line in lines:
        filenames.append(line.strip())
    return filenames

def add_weight_branch_list(filelist, xsec, lumi=1., treename='Events', wgtbranch='xsecWeight'):
    from array import array
    import ROOT
    ROOT.PyConfig.IgnoreCommandLineOptions = True

    def _get_sum(tree, wgtvar):
        htmp = ROOT.TH1D('htmp', 'htmp', 1, 0, 10)
        tree.Project('htmp', '1.0', wgtvar)
        return float(htmp.Integral())

    def _fill_const_branch(tree, branch_name, buff, lenVar=None):
        if lenVar is not None:
            b = tree.Branch(branch_name, buff, '%s[%s]/F' % (branch_name, lenVar))
            b_lenVar = tree.GetBranch(lenVar)
            buff_lenVar = array('I', [0])
            b_lenVar.SetAddress(buff_lenVar)
        else:
            b = tree.Branch(branch_name, buff, branch_name + '/F')

        b.SetBasketSize(tree.GetEntries() * 2)  # be sure we do not trigger flushing                                                                                                                        
        for i in range(tree.GetEntries()):
            if lenVar is not None:
                b_lenVar.GetEntry(i)
            b.Fill()

        b.ResetAddress()
        if lenVar is not None:
            b_lenVar.ResetAddress()

    # open all files
    sumw = 0
    for fname in filelist:
        f = ROOT.TFile.Open(fname)
        run_tree = f.Get('Runs')
        sumwgts = _get_sum(run_tree, 'genEventSumw')
        sumw += sumwgts
        f.Close()

    # normalize by sumq
    for fname in filelist:
        f = ROOT.TFile(fname,'UPDATE')
        tree = f.Get(treename)
        print('fill xsec ',xsec,' lumi ',lumi ,' sumwgt ',sumw)
        xsecwgt = xsec * lumi / sumw
        xsec_buff = array('f', [xsecwgt])
        _fill_const_branch(tree, wgtbranch, xsec_buff)
        tree.Write(treename, ROOT.TObject.kOverwrite)
        f.Close()

def add_weight_branch(file, xsec, lumi=1., treename='Events', wgtbranch='xsecWeight'):
    print("Here")
    from array import array
    import ROOT
    ROOT.PyConfig.IgnoreCommandLineOptions = True

    def _get_sum(tree, wgtvar):
        htmp = ROOT.TH1D('htmp', 'htmp', 1, 0, 10)
        tree.Project('htmp', '1.0', wgtvar)
        return float(htmp.Integral())

    def _fill_const_branch(tree, branch_name, buff, lenVar=None):
        if lenVar is not None:
            b = tree.Branch(branch_name, buff, '%s[%s]/F' % (branch_name, lenVar))
            b_lenVar = tree.GetBranch(lenVar)
            buff_lenVar = array('I', [0])
            b_lenVar.SetAddress(buff_lenVar)
        else:
            b = tree.Branch(branch_name, buff, branch_name + '/F')

        b.SetBasketSize(tree.GetEntries() * 2)  # be sure we do not trigger flushing
        for i in range(tree.GetEntries()):
            if lenVar is not None:
                b_lenVar.GetEntry(i)
            b.Fill()

        b.ResetAddress()
        if lenVar is not None:
            b_lenVar.ResetAddress()

    f = ROOT.TFile(file, 'UPDATE')
    sumEv=False
    print("Here 2")
    try:
        print("Here 3")
        nevents = f.Get('nEvents')
        nevents.GetBinContent(1)
        sumev=True
    except:
        sumev=False
        
    print("Here 4")
    #try:
    if 'sumLHE' in [i.GetName() for i in f.GetListOfKeys()]:
        print("Here 5")
        lhetree = f.Get('sumLHE')
        print('lhetree ',lhetree)
    else:
    #except:
        print('no lhetree')

    print("Here 6")
    run_tree = f.Get('Runs')
    print('run tree',run_tree)
    tree = f.Get(treename)

    # fill cross section weights to the 'Events' tree
    sumwgts = _get_sum(run_tree, 'genEventSumw')
    sumevts = _get_sum(run_tree, 'genEventCount')
    print(sumwgts)
    if sumev:
        print('fill xsec ',xsec,' lumi ',lumi ,' sumevt w ',nevents.GetBinContent(1),' sumwgts ',sumwgts,' sumevts ',sumevts)
        #xsecwgt = xsec * lumi / nevents.GetBinContent(1)
        xsecwgt = xsec * lumi / sumwgts
    else:
        print('fill xsec ',xsec,' lumi ',lumi ,' sumwgt ',sumwgts,' sumevts ',sumevts)
        xsecwgt = xsec * lumi / sumwgts

    xsec_buff = array('f', [xsecwgt])
    _fill_const_branch(tree, wgtbranch, xsec_buff)

    # fill lhe re-norm factors
    if sumev:
        run_tree.GetEntry(0)
        nScaleWeights = run_tree.nLHEScaleSumw

        scale_weight_norm_buff = array('f', [nevents.GetBinContent(1) / _get_sum(lhetree,'sumweight_%i'%i) for i in range(nScaleWeights)])
        print([_get_sum(lhetree,'sumweight_%i'%i) for i in  range(nScaleWeights)])
        print(str(scale_weight_norm_buff))
        logging.info('LHEScaleWeightNormNew: ' + str(scale_weight_norm_buff))
        _fill_const_branch(tree, 'LHEScaleWeightNormNew', scale_weight_norm_buff, lenVar='nLHEScaleWeight')

    # fill LHE weight re-normalization factors
    print("Entering ScaleWeight")
    if tree.GetBranch('LHEScaleWeight'):
        print("In ScaleWeight")
        run_tree.GetEntry(0)
        nScaleWeights = run_tree.nLHEScaleSumw
        scale_weight_norm_buff = array('f', [sumwgts / _get_sum(run_tree, 'LHEScaleSumw[%d]*genEventSumw' % i) for i in range(nScaleWeights)])
        logging.info('LHEScaleWeightNorm: ' + str(scale_weight_norm_buff))
        _fill_const_branch(tree, 'LHEScaleWeightNorm', scale_weight_norm_buff, lenVar='nLHEScaleWeight')

    print("Entering PdfWeight")
    if tree.GetBranch('LHEPdfWeight'):
        print("In PdgWeight")
        run_tree.GetEntry(0)
        nPdfWeights = run_tree.nLHEPdfSumw
        pdf_weight_norm_buff = array('f', [sumwgts / _get_sum(run_tree, 'LHEPdfSumw[%d]*genEventSumw' % i) for i in range(nPdfWeights)])
        logging.info('LHEPdfWeightNorm: ' + str(pdf_weight_norm_buff))
        _fill_const_branch(tree, 'LHEPdfWeightNorm', pdf_weight_norm_buff, lenVar='nLHEPdfWeight')

    tree.Write(treename, ROOT.TObject.kOverwrite)
    f.Close()

def load_dataset_file(dataset_file):
    import yaml
    with open(dataset_file) as f:
        d = yaml.safe_load(f)

    datasets_to_lists = {}
    datasets_to_xs = {}
    lname = d['list'][0]
    for outtree_name in d:
        if outtree_name == 'list': continue
        for samp in d[outtree_name]:
            dataset = samp['dataset']
            if 'files' in samp:
                datasets_to_lists[dataset] = [lname + '/' + fname for fname in samp['files']]
            else:
                datasets_to_lists[dataset] = [lname+'/'+dataset]
            datasets_to_xs[dataset] = samp['xs']
    return datasets_to_xs, datasets_to_lists

def parse_sample_xsec(cfgfile):
    xsec_dict = {}
    with open(cfgfile) as f:
        for l in f:
            l = l.strip()
            if not l or l.startswith('#'):
                continue
            pieces = l.split()
            isData = False
            samp = pieces[0]
            try:
                xsec = float(pieces[1])
            except ValueError:
                try:
                    import numexpr
                    xsec = numexpr.evaluate(pieces[1]).item()
                except:
                    print('No xsec for ',samp)
                    pass
            if samp is None:
                logging.warning('Ignore line:\n%s' % l)
            elif not isData and xsec is None:
                logging.error('Cannot find cross section:\n%s' % l)
            else:
                if samp in xsec_dict and xsec_dict[samp] != xsec:
                    raise RuntimeError('Inconsistent entries for sample %s' % samp)
                xsec_dict[samp] = xsec
    return xsec_dict

def create_metadata(args):
    '''
    create metadata

    Metadata is a dict including:
        - options
        - 'samples': (list)
        - 'inputfiles': (dict, sample -> files)
        - 'jobs': (list of dict)
            - jobitem: (dict, keys: 'samp', 'idx', 'inputfiles')
    '''

    arg_blacklist = ['metadata', 'select', 'ignore', 'site', 'datasets']
    md = {k: args.__dict__[k] for k in args.__dict__ if k not in arg_blacklist}

    md['samples'] = []
    md['inputfiles'] = {}
    md['jobs'] = []
    md['xsec'] = {}

    def select_sample(dataset):
        samp = dataset
        keep = True
        if args.select:
            sels = args.select.split(',')
            match = False
            for s in sels:
                if re.search(s, samp):
                    logging.debug('Selecting dataset %s', dataset)
                    match = True
                    break
            if not match:
                keep = False
        elif args.ignore:
            vetoes = args.ignore.split(',')
            match = False
            for v in vetoes:
                if re.search(v, samp):
                    logging.debug('Ignoring dataset %s', dataset)
                    match = True
                    break
            if match:
                keep = False
        return keep

    datasets_to_xs, datasets_to_lists = load_dataset_file(args.datasets)

    # use file lists
    for dataset,lists in datasets_to_lists.items():
        filelist = []
        for samp in lists:
            if select_sample(samp):
                filelist.extend(get_filenames(samp+'.list'))
        if len(filelist):
            filelist = sorted(filelist)
            md['samples'].append(dataset)
            md['inputfiles'][dataset] = filelist
            md['xsec'][dataset] = datasets_to_xs[dataset]

    # sort the samples
    md['samples'] = natural_sort(md['samples'])

    # discover the files
    tidx = 0
    for samp in md['samples']:
        # sort the input list
        md['inputfiles'][samp] = natural_sort(md['inputfiles'][samp])

        # create jobs
        for idx, chunk in enumerate(get_chunks(md['inputfiles'][samp], args.nfiles_per_job)):
            md['jobs'].append({'samp': samp, 'idx': idx, 'inputfiles': chunk, 'tidx': tidx})
            tidx = tidx+1

    return md


def load_metadata(args):
    metadatafile = os.path.join(args.jobdir, args.metadata)
    with open(metadatafile) as f:
        md = json.load(f)
    return md

def check_job_status(args):
    md = load_metadata(args)
    njobs = len(md['jobs'])
    jobids = {'running': [], 'failed': [], 'completed': []}
    for jobid in range(njobs):
        logpath = os.path.join(args.jobdir, '%d.log' % jobid)
        if not os.path.exists(logpath):
            logging.debug('Cannot find log file %s' % logpath)
            jobids['failed'].append(str(jobid))
            continue
        with open(logpath) as logfile:
            errormsg = None
            finished = False
            for line in reversed(logfile.readlines()):
                if 'Job removed' in line or 'aborted' in line:
                    errormsg = line
                if 'Job submitted from host' in line:
                    # if seeing this first: the job has been resubmited
                    break
                if 'return value' in line:
                    if 'return value 0' in line:
                        finished = True
                    else:
                        errormsg = line
                    break
            if errormsg:
                logging.debug(logpath + '\n   ' + errormsg)
                jobids['failed'].append(str(jobid))
            else:
                if finished:
                    jobids['completed'].append(str(jobid))
                else:
                    jobids['running'].append(str(jobid))
    assert sum(len(jobids[k]) for k in jobids) == njobs
    all_completed = len(jobids['completed']) == njobs
    info = {k: len(jobids[k]) for k in jobids if len(jobids[k])}
    logging.info('Job %s status: ' % args.jobdir + str(info))
    print(jobids['running'])
    return all_completed, jobids


def submit(args, configs):
    logging.info('Preparing jobs...\n  - modules: %s\n  - cut: %s\n  - outputdir: %s' % (str(args.imports), args.cut, args.outputdir))

    scriptfile = os.path.join(os.path.dirname(__file__), 'run_processor.sh')
    macrofile = os.path.join(os.path.dirname(__file__), 'processor.py')
    metadatafile = os.path.join(args.jobdir, args.metadata)
    joboutputdir = os.path.join(args.outputdir, 'pieces')

    # create config file for the scripts
    configfiles = []
    if configs is not None:
        for cfgname in configs:
            cfgpath = os.path.join(args.jobdir, cfgname)
            configfiles.append(cfgpath)

    if not args.resubmit:
        # create jobdir
        if os.path.exists(args.jobdir):
            if args.batch:
                logging.warning('jobdir %s already exists! Will not submit new jobs!' % args.jobdir)
                return
            ans = input('jobdir %s already exists, remove? [yn] ' % args.jobdir)
            if ans.lower()[0] == 'y':
                shutil.rmtree(args.jobdir)
            else:
                sys.exit(1)
        os.makedirs(args.jobdir)

        # create outputdir
        if os.path.exists(joboutputdir):
            if not args.batch:
                ans = input('outputdir %s already exists, continue? [yn] ' % joboutputdir)
                if ans.lower()[0] == 'n':
                    sys.exit(1)
        else:
            os.makedirs(joboutputdir)

        # create config file for the scripts
        if configs is not None:
            for cfgname, cfgpath in zip(configs, configfiles):
                with open(cfgpath, 'w') as f:
                    json.dump(configs[cfgname], f, ensure_ascii=True, indent=2, sort_keys=True)
                shutil.copy2(cfgpath, joboutputdir)

        # create metadata file
        md = create_metadata(args)
        md['joboutputdir'] = joboutputdir
        with open(metadatafile, 'w') as f:
            json.dump(md, f, ensure_ascii=True, indent=2, sort_keys=True)
        # store the metadata file to the outputdir as well
        import gzip
        with gzip.open(os.path.join(args.outputdir, args.metadata+'.gz'), 'w') as fout:
            fout.write(json.dumps(md).encode('utf-8'))

        njobs = len(md['jobs'])
        jobids = [str(jobid) for jobid in range(njobs)]
        jobids_file = os.path.join(args.jobdir, 'submit.txt')

    else:
        # resubmit
        jobids = check_job_status(args)[1]['failed']
        jobids_file = os.path.join(args.jobdir, 'resubmit.txt')

    with open(jobids_file, 'w') as f:
        f.write('\n'.join(jobids))

    # prepare the list of files to transfer
    files_to_transfer = [#os.path.expandvars('$CMSSW_BASE/../CMSSW%s.tar.gz' % args.tarball_suffix), 
        macrofile, metadatafile] + configfiles
    if args.branchsel_in:
        files_to_transfer.append(args.branchsel_in)
        shutil.copy2(args.branchsel_in, args.jobdir)
    if args.branchsel_out:
        files_to_transfer.append(args.branchsel_out)
        shutil.copy2(args.branchsel_out, args.jobdir)
    if args.extra_transfer:
        for f in args.extra_transfer.split(','):
            files_to_transfer.append(f)
            shutil.copy2(f, args.jobdir)
    shutil.copy2(macrofile, args.jobdir)
    files_to_transfer = [os.path.abspath(f) for f in files_to_transfer]

    condordesc = '''\
universe              = vanilla
requirements          = (Arch == "X86_64") && (OpSys == "LINUX")
request_memory        = {request_memory}
request_disk          = 10000000
executable            = {scriptfile}
arguments             = $(jobid)
transfer_input_files  = {files_to_transfer}
output                = {jobdir}/$(jobid).out
error                 = {jobdir}/$(jobid).err
log                   = {jobdir}/$(jobid).log
use_x509userproxy     = true
x509userproxy         = /afs/cern.ch/user/r/rtu/private/x509up_u150678
Should_Transfer_Files = YES
initialdir            = {initialdir}
WhenToTransferOutput  = ON_EXIT
want_graceful_removal = true
periodic_release      = (NumJobStarts < 3) && ((CurrentTime - EnteredCurrentStatus) > 10*60)
{transfer_output}
{site}
{maxruntime}
{condor_extras}

queue jobid from {jobids_file}
'''.format(scriptfile=os.path.abspath(scriptfile),
           files_to_transfer=','.join(files_to_transfer),
           jobdir=os.path.abspath(args.jobdir),
           # when outputdir is on EOS, disable file transfer as file is manually copied to EOS in processor.py
           initialdir=os.path.abspath(args.jobdir) if joboutputdir.startswith('/eos') else joboutputdir,
           transfer_output='transfer_output_files = ""' if joboutputdir.startswith('/eos') else '',
           jobids_file=os.path.abspath(jobids_file),
           site='+DESIRED_Sites = "%s"' % args.site if args.site else '',
           maxruntime='+MaxRuntime = %s' % args.max_runtime if args.max_runtime else '',
           request_memory=args.request_memory,
           condor_extras=args.condor_extras,
    )
    condorfile = os.path.join(args.jobdir, 'submit.cmd')
    with open(condorfile, 'w') as f:
        f.write(condordesc)

    cmd = 'condor_submit {condorfile}'.format(condorfile=condorfile)
    print('Run the following command to submit the jobs:\n  %s' % cmd)
    if args.batch:
        import subprocess
        subprocess.Popen(cmd, shell=True).communicate()


def run_add_weight(args):
    if args.weight_file:
        xsec_dict = parse_sample_xsec(args.weight_file)
    print("Here")

    import subprocess
    md = load_metadata(args)
    parts_dir = os.path.join(args.outputdir, 'parts')
    status_file = os.path.join(parts_dir, '.success')
    print(parts_dir)
    if os.path.exists(status_file):
        return
    if not os.path.exists(parts_dir):
        os.makedirs(parts_dir)

    for samp in md['samples']:
        outfile = '{parts_dir}/{samp}_tree.root'.format(parts_dir=parts_dir, samp=samp)
        os.system('ls {outputdir}/pieces/{samp}_*_tree.root > tmp.txt'.format(outputdir=args.outputdir, samp=samp))
        with open("tmp.txt","r") as f: d = f.readlines()
        cmd = ''
        isTooLong = False
        if len(d)>100: isTooLong = True
        if isTooLong:
            #for idx, chunk in enumerate(get_chunks(d, 100)):
            #cmd += 'haddnano.py {outfile}  \n'.format(outfile=outfile.replace('.root','_%i.root'%idx), chunk=' '.join(chunk))
            for idx in range(0,10):
                cmd += 'haddnano.py {outfile} {outputdir}/pieces/{samp}_{idx}*_tree.root  \n'.format(outfile=outfile.replace('.root','_%i.root'%idx), outputdir=args.outputdir, samp=samp, idx=idx)
            print('cmd ',cmd)
        else:
            cmd = 'haddnano.py {outfile} {outputdir}/pieces/{samp}_*_tree.root \n'.format(outfile=outfile, outputdir=args.outputdir, samp=samp)
        logging.debug('...' + cmd)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = p.communicate()[0]
        log_lower = log.lower().decode('utf-8')
        if 'error' in log_lower or 'fail' in log_lower:
            logging.error(log)
        if p.returncode != 0:
            print('Hadd failed on %s!' % samp)
            continue
            #raise RuntimeError('Hadd failed on %s!' % samp)
        if isTooLong:
            #cmd = 'haddnano.py {outfile} {parts_dir}/{samp}_tree_*.root \n'.format(outfile=outfile, parts_dir=parts_dir, samp=samp)
            #os.system(cmd)
            #p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            #log = p.communicate()[0]
            #log_lower = log.lower().decode('utf-8')
            #if 'error' in log_lower or 'fail' in log_lower:
            #    logging.error(log)
            #if p.returncode == 0:
            #    os.system('rm {parts_dir}/{samp}_tree_*.root'.format(parts_dir=parts_dir, samp=samp))
            if args.weight_file:
                import glob
                filelists = glob.glob("{parts_dir}/{samp}_tree_*.root".format(parts_dir=parts_dir, samp=samp))
                print(filelists)
                dataset_xs = md['xsec'][samp]
                if dataset_xs == 1: continue
                xsec = xsec_dict[dataset_xs]
                if xsec is not None:
                    logging.info('Adding xsec weight to files, xsec=%f' % (xsec))
                    add_weight_branch_list(filelists, xsec)

        # add weight
        if args.weight_file and not isTooLong:
            dataset_xs = md['xsec'][samp]
            if dataset_xs == 1: continue
            try:
                xsec = xsec_dict[dataset_xs]
                print(xsec)
                if xsec is not None:
                    logging.info('Adding xsec weight to file %s, xsec=%f' % (outfile, xsec))
                    add_weight_branch(outfile, xsec)
            except KeyError as e:
                if '-' not in samp and '_' not in samp:
                    # data
                    logging.info('Not ing weight to sample %s' % samp)
                else:
                    raise e
    with open(status_file, 'w'):
        pass

def get_arg_parser():
    import argparse
    parser = argparse.ArgumentParser('Preprocess ntuples')
    parser.add_argument('-i', '--inputdir', default=None,
        help='Input diretory.'
    )
    parser.add_argument('-o', '--outputdir', required=True,
        help='Output directory'
    )
    parser.add_argument('-m', '--metadata',
        default='metadata.json',
        help='Metadata json file. Default: %(default)s'
    )
    parser.add_argument('--extra-transfer',
        default=None,
        help='Extra files to transfer, common separated list. Default: %(default)s'
    )
    parser.add_argument('--tarball-suffix',
        default='',
        help='Suffix of the CMSSW tarball. Default: %(default)s'
    )
    parser.add_argument('-t', '--submittype',
        default='condor', choices=['interactive', 'condor'],
        help='Method of job submission. [Default: %(default)s]'
    )
    parser.add_argument('--resubmit',
        action='store_true', default=False,
        help='Resubmit failed jobs. Default: %(default)s'
    )
    parser.add_argument('-j', '--jobdir',
        default='jobs',
        help='Directory for job files. [Default: %(default)s]'
    )
    parser.add_argument('-d', '--datasets', required=False,
        default='',
        help='Path to the dataset list file. [Default: %(default)s]'
    )
    parser.add_argument('--select',
        default='',
        help='Selected datasets, common separated regex. [Default: %(default)s]'
    )
    parser.add_argument('--ignore',
        default='',
        help='Ignored datasets, common separated regex. [Default: %(default)s]'
    )
#     parser.add_argument('--nproc',
#         type=int, default=8,
#         help='Number of jobs to run in parallel. Default: %(default)s'
#     )
    parser.add_argument('-n', '--nfiles-per-job',
        type=int, default=3,
        help='Number of input files to process in one job. Default: %(default)s'
    )
    parser.add_argument('--dryrun',
        action='store_true', default=False,
        help='Do not convert -- only produce metadata. Default: %(default)s'
    )
    parser.add_argument('--site',
        default='',
        help='Specify sites for condor submission. Default: %(default)s'
    )
    parser.add_argument('--condor-extras',
        default='',
        help='Extra parameters for condor, e.g., +AccountingGroup = "group_u_CMST3.all". Default: %(default)s'
    )
    parser.add_argument('--max-runtime',
        default='48*60*60',
        help='Max runtime, in seconds. Default: %(default)s'
    )
    parser.add_argument('--request-memory',
        default='3500',
        help='Request memory, in MB. Default: %(default)s'
    )
    parser.add_argument('--add-weight',
        action='store_true', default=False,
        help='Merge output files of the same dataset and add cross section weight using the file specified in --weight-file. Default: %(default)s'
    )
    parser.add_argument('-w', '--weight-file',
        default='samples/xsec.conf',
        help='File with xsec of each sample. If empty, xsec wgt will not be added. Default: %(default)s'
    )
    parser.add_argument('--post',
        action='store_true', default=False,
        help='Add weight. Default: %(default)s'
    )
    parser.add_argument('--batch',
        action='store_true', default=False,
        help='Batch mode, do not ask for confirmation and submit the jobs directly. Default: %(default)s'
    )

    # preserve the options in nano_postproc.py
    parser.add_argument("-s", "--postfix", dest="postfix", default=None, help="Postfix which will be appended to the file name (default: _Friend for friends, _Skim for skims)")
    parser.add_argument("-J", "--json", dest="json", default=None, help="Select events using this JSON file")
    parser.add_argument("-c", "--cut", dest="cut", default=None, help="Cut string")
    parser.add_argument("--bi", "--branch-selection-input", dest="branchsel_in", default='keep_and_drop_input.txt', help="Branch selection input")
    parser.add_argument("--bo", "--branch-selection-output", dest="branchsel_out", default='keep_and_drop_output.txt', help="Branch selection output")
    parser.add_argument("--friend", dest="friend", action="store_true", default=False, help="Produce friend trees in output (current default is to produce full trees)")
    parser.add_argument("-I", "--import", dest="imports", default=[], action="append", nargs=2, help="Import modules (python package, comma-separated list of ")
    parser.add_argument("-z", "--compression", dest="compression", default=("LZ4:4"), help="Compression: none, or (algo):(level) ")
    parser.add_argument("-P", "--prefetch", dest="prefetch", action="store_true", default=False, help="Prefetch input files locally instead of accessing them via xrootd")
    parser.add_argument("--long-term-cache", dest="longTermCache", action="store_true", default=False, help="Keep prefetched files across runs instead of deleting them at the end")
    parser.add_argument("-N", "--max-entries", dest="maxEntries", type=int, default=None, help="Maximum number of entries to process from any single given input tree")
    parser.add_argument("--first-entry", dest="firstEntry", type=int, default=0, help="First entry to process in the three (to be used together with --max-entries)")
    parser.add_argument("--justcount", dest="justcount", default=False, action="store_true", help="Just report the number of selected events")

    return parser


def run(args, configs=None):
    logging.info('Running w/ config: %s' % configs)

    if args.post:
        args.add_weight = True

    if args.add_weight:
        all_completed, _ = check_job_status(args)
        if not all_completed:
            if args.batch:
                logging.warning('\033[1;30mThere are jobs failed or still running. Skipping...\033[0m')
                return
            ans = input('Warning! There are jobs failed or still running. Continue adding weights? [yn] ')
            if ans.lower()[0] != 'y':
                return
        run_add_weight(args)

    if args.add_weight:
        return

    submit(args, configs)


if __name__ == '__main__':
    parser = get_arg_parser()
    args = parser.parse_args()

    run(args)
