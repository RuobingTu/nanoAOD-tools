from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.output import FriendOutput
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from array import array

class countHistogramsProducer(Module):
    def __init__(self):
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.h_nevents = ROOT.TH1D('nEvents', 'nEvents', 1, 1, 2)
        self.nevents = 0
        self.sumlheweights = []
        self.nevents_pos = 0

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        prevdir = ROOT.gDirectory
        outputFile.cd()
        self.h_nevents.SetBinContent(1, self.nevents)
        self.h_nevents.Write("",ROOT.TObject.kOverwrite)

        tree = ROOT.TTree("sumLHE", "LHE Sum")
        sumweight_0 = array('f', [0.])
        sumweight_1 = array('f', [0.])
        sumweight_2 = array('f', [0.])
        sumweight_3 = array('f', [0.])
        sumweight_4 = array('f', [0.])
        sumweight_5 = array('f', [0.])
        sumweight_6 = array('f', [0.])
        sumweight_7 = array('f', [0.])
        sumweight_8 = array('f', [0.])
        sumweight_9 = array('f', [0.])
        sumweight_10 = array('f', [0.])
        sumweight_11 = array('f', [0.])

        nweights = len(self.sumlheweights)
        tree.Branch("sumweight_0", sumweight_0,"sumweight_0/F")
        tree.Branch("sumweight_1", sumweight_1,"sumweight_1/F")
        tree.Branch("sumweight_2", sumweight_2,"sumweight_2/F")
        tree.Branch("sumweight_3", sumweight_3,"sumweight_3/F")
        tree.Branch("sumweight_4", sumweight_4,"sumweight_4/F")
        tree.Branch("sumweight_5", sumweight_5,"sumweight_5/F")
        tree.Branch("sumweight_6", sumweight_6,"sumweight_6/F")
        tree.Branch("sumweight_7", sumweight_7,"sumweight_7/F")
        tree.Branch("sumweight_8", sumweight_8,"sumweight_8/F")
        tree.Branch("sumweight_9", sumweight_9,"sumweight_9/F")
        tree.Branch("sumweight_10", sumweight_10,"sumweight_10/F")
        tree.Branch("sumweight_11", sumweight_11,"sumweight_11/F")

        print('sum ',self.sumlheweights[4],' nevents ',self.nevents,' nevents_pos ',self.nevents_pos)
        if len(self.sumlheweights) < 10:
            sumweight_0[0] = self.sumlheweights[0]
            sumweight_1[0] = self.sumlheweights[1]
            sumweight_2[0] = self.sumlheweights[2]
            sumweight_3[0] = self.sumlheweights[3]
            sumweight_4[0] = self.sumlheweights[4]
            sumweight_5[0] = self.sumlheweights[5]
            sumweight_6[0] = self.sumlheweights[6]
            sumweight_7[0] = self.sumlheweights[7]
            try:
                sumweight_8[0] = self.sumlheweights[8]
            except:
                sumweight_8[0] = 0
            try:
                sumweight_9[0] = self.sumlheweights[9]
            except:
                sumweight_9[0] = 0
            try:
                sumweight_10[0] = self.sumlheweights[10]
            except:
                sumweight_10[0] = 0
            try:
                sumweight_11[0] = self.sumlheweights[11]
            except:
                sumweight_11[0] = 0
            tree.Fill()

        tree.Write("", ROOT.TObject.kOverwrite);
        prevdir.cd()

    def analyze(self, event):
        sign = 1
        if hasattr(event, 'Generator_weight') and event.Generator_weight < 0:
            self.nevents += -1;
            sign = -1
        else:
            self.nevents += 1;
        weights = []
        self.nevents_pos += 1;
        for i in range(event.nLHEScaleWeight):
            if len(self.sumlheweights)>i:
                self.sumlheweights[i] += event.LHEScaleWeight[i]*sign
            else:
                self.sumlheweights.append(event.LHEScaleWeight[i]*sign)
        return True

countHistogramsModule = lambda: countHistogramsProducer()
