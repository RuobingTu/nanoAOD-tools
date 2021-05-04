from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


class countHistogramsProducer(Module):
    def __init__(self):
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        print('begin File countHist nentries in file ',inputFile,inputFile.Get("Events").GetEntries())
        self.h_nevents = ROOT.TH1D('nEvents', 'nEvents', 1, 1, 2)
        self.nevents = 0

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        print('finalized counting nevents ',self.nevents)
        prevdir = ROOT.gDirectory
        outputFile.cd()
        self.h_nevents.SetBinContent(1, self.nevents)
        self.h_nevents.Write("",ROOT.TObject.kOverwrite)
        prevdir.cd()

    def analyze(self, event):
        if hasattr(event, 'Generator_weight') and event.Generator_weight < 0:
            self.nevents += -1;
        else:
            self.nevents += 1;
        return True

countHistogramsModule = lambda: countHistogramsProducer()
