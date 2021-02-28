#!/usr/bin/env python
import os
import sys
import time
import ROOT 
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.branchselection import BranchSelection
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import InputTree
from PhysicsTools.NanoAODTools.postprocessing.framework.output import FullOutput
from PhysicsTools.NanoAODTools.postprocessing.framework.preskimming import preSkim
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Event
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import clearExtraBranches
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import eventLoop
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object


class CustomPostProcessor:
    def __init__(self, outputDir,inputFiles,cut=None,branchsel=None,modules=[],compression="LZMA:9",friend=False,postfix=None,
                 jsonInput=None,noOut=False,justcount=False,provenance=False,haddFileName=None,fwkJobReport=False,
                 histFileName=None,histDirName=None, outputbranchsel=None,maxEntries=None,firstEntry=0,
                 prefetch=False,longTermCache=False, perJet=False):
        self.outputDir=outputDir
        self.inputFiles=inputFiles
        self.cut=cut
        self.modules=modules
        self.compression=compression
        self.postfix=postfix
        self.json=jsonInput
        self.noOut=noOut
        self.friend=friend
        self.justcount=justcount
        self.provenance = provenance
        self.branchsel = BranchSelection(branchsel) if branchsel else None 
        self.outputbranchsel = BranchSelection(outputbranchsel) if outputbranchsel else None
        self.histFileName=histFileName
        self.histDirName=histDirName
        self.maxEntries = maxEntries if maxEntries else 9223372036854775807
        self.firstEntry = firstEntry
        self.perJet = perJet

    def run(self):
        outpostfix = self.postfix if self.postfix != None else ("_Friend" if self.friend else "_Skim")
        fullClone = False
        outFileNames = []
        totEntriesRead = 0
        t0 = time.time()

        print('inputFiles ',self.inputFiles)
        for fileName in self.inputFiles:
            # open file
            print("Opening file %s" % fileName)
            inFile = ROOT.TFile.Open(fileName)
            if(not inFile): #check for null pointer
                print("Unable to open file %s, exting \n" % fileName)
                return 1

            # get input tree
            inTree = inFile.Get("Events")
            nEntries = min(inTree.GetEntries() - self.firstEntry, self.maxEntries)
            totEntriesRead += nEntries

            # pre-skimming
            elist, jsonFilter = preSkim(inTree, self.json, self.cut, maxEntries=self.maxEntries, firstEntry=self.firstEntry)

            # number of events to be processed 
            nTotal = elist.GetN() if elist else nEntries
            print('Pre-select %d entries out of %s '%(nTotal,nEntries))

            inTree = InputTree(inTree, elist) 

            # output
            outFileName = os.path.join(self.outputDir, os.path.basename(fileName).replace(".root",outpostfix+".root"))
            compressionAlgo  = ROOT.ROOT.kLZMA
            compressionLevel = int(9)
            outFile = ROOT.TFile.Open(outFileName, "RECREATE", "", compressionLevel)
            outFileNames.append(outFileName)
            outFile.SetCompressionAlgorithm(compressionAlgo)
            maxEntries = self.maxEntries
            if self.perJet: #save two first jets
                maxEntries = self.maxEntries*2
            outTree = FullOutput(inFile,
                                 inTree,
                                 outFile,
                                 branchSelection=self.branchsel,
                                 outputbranchSelection=self.outputbranchsel,
                                 fullClone=fullClone, 
                                 maxEntries=maxEntries,
                                 firstEntry=self.firstEntry,
                                 jsonFilter=jsonFilter,
                                 provenance=self.provenance)
                
            t0 = time.time()
            tlast = t0
            doneEvents = 0
            acceptedEvents = 0
            if elist:
                eventRange = [(elist.GetEntry(0) if i == 0 else elist.Next()) for i in range(elist.GetN())]
            else:
                eventRange = range(self.firstEntry, self.firstEntry + nEntries) if nEntries > 0 else None

            entries = inTree.entries
            if eventRange:
                entries = len(eventRange)
            maxEvents = self.maxEntries
            if maxEvents > 0:
                entries = min(entries, self.maxEntries)
            entriesRange = range(entries) if eventRange == None else eventRange

            for m in self.modules:
                m.beginFile(inFile, outFile, inTree, outTree, entriesRange)

            for ie, i in enumerate(entriesRange):
                if maxEvents > 0 and ie >= maxEvents: break
                e = Event(inTree, ie)

                ret = True
                if self.perJet:
                    for m in self.modules:
                        ret = m.analyze(e,ie)
                        if not ret: break
                        else:
                            clearExtraBranches(inTree)
                            m.fill(e,ie)
                else:
                    clearExtraBranches(inTree)
                    for m in self.modules:
                        ret = m.analyze(e,ie)
                        if not ret: break
                    if ret and outTree is not None:
                        outTree.fill()
                if ret:
                    acceptedEvents += 1
                progress=(10000, sys.stdout)
                if progress:
                    if ie > 0 and ie % progress[0] == 0:
                        t1 = time.time()
                        progress[1].write("Processed %8d/%8d entries, %5.2f%% (elapsed time %7.1fs, curr speed %8.3f kHz, avg speed %8.3f kHz), accepted %8d/%8d events (%5.2f%%)\n" % (
                            ie, entries, ie / float(0.01 * entries),
                            t1 - t0, (progress[0] / 1000.) / (max(t1 - tlast, 1e-9)),
                            ie / 1000. / (max(t1 - t0, 1e-9)),
                            acceptedEvents, doneEvents,
                            acceptedEvents / (0.01 * doneEvents)))
                        tlast = t1
            for m in self.modules:
                m.endFile(inFile, outFile, inTree, outTree)

            outTree.write()
            outFile.Close()
            print("Done %s" % outFileName)
            
        for m in self.modules:
            m.endJob()
        print("Total time %.1f sec. to process %i events. Rate = %.1f Hz." % ((time.time() - t0), totEntriesRead, totEntriesRead / (time.time() - t0)))
