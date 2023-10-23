import os

# Updated on Jan 10 2023
# 2023
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2022/{}.list".format('/Muon/Run2022C-PromptNanoAODv10_v1-v1/NANOAOD', 'Run2022B'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2022/{}.list".format('/Muon/Run2022C-PromptNanoAODv10_v1-v1/NANOAOD', 'Run2022C'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2022/{}.list".format('/Muon/Run2022D-PromptNanoAODv10_v2-v1/NANOAOD', 'Run2022D'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2022/{}.list".format('/Muon/Run2022E-PromptNanoAODv10_v1-v3/NANOAOD', 'Run2022E'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2022/{}.list".format('/Muon/Run2022F-PromptNanoAODv10_v1-v2/NANOAOD', 'Run2022F'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2022/{}.list".format('/Muon/Run2022F-PromptNanoAODv10_v1-v2/NANOAOD', 'Run2022F'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2022/{}.list".format('/Muon/Run2022G-PromptNanoAODv10_v1-v1/NANOAOD', 'Run2022G'))

# Updated on Apr 30 2023
#os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/JetMET0/Run2023A-PromptNanoAODv11p9_v2-v1/NANOAOD', 'JetMET0Run2023A'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/JetMET0/Run2023B-PromptNanoAODv12_v1-v1/NANOAOD', 'JetMET0Run2023B'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/JetMET0/Run2023C-PromptNanoAODv12_v2-v2/NANOAOD', 'JetMET0Run2023C'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/JetMET0/Run2023C-PromptNanoAODv12_v3-v1/NANOAOD', 'JetMET0Run2023Cv3'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/JetMET0/Run2023C-PromptNanoAODv12_v4-v1/NANOAOD', 'JetMET0Run2023Cv4'))

#os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/JetMET1/Run2023A-PromptNanoAODv11p9_v2-v1/NANOAOD', 'JetMET1Run2023A'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/JetMET1/Run2023B-PromptNanoAODv12_v1-v1/NANOAOD', 'JetMET1Run2023B'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/JetMET1/Run2023C-PromptNanoAODv12_v2-v4/NANOAOD', 'JetMET1Run2023C'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/JetMET1/Run2023C-PromptNanoAODv12_v3-v1/NANOAOD', 'JetMET1Run2023Cv3'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/JetMET1/Run2023C-PromptNanoAODv12_v4-v1/NANOAOD', 'JetMET1Run2023Cv4'))

#os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/Muon0/Run2023A-PromptNanoAODv11p9_v2-v1/NANOAOD', 'Muon0Run2023A'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/Muon0/Run2023B-PromptNanoAODv12-v1-v1/NANOAOD', 'Muon0Run2023B'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/Muon0/Run2023C-PromptNanoAODv12_v2-v2/NANOAOD', 'Muon0Run2023C'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/Muon0/Run2023C-PromptNanoAODv12_v3-v1/NANOAOD', 'Muon0Run2023Cv3'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/Muon0/Run2023C-PromptNanoAODv12_v4-v1/NANOAOD', 'Muon0Run2023Cv4'))

os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/Muon0/Run2023C-PromptReco-v4/NANOAOD', 'Muon0PromptRun2023C'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/Muon0/Run2023D-PromptReco-v1/NANOAOD', 'Muon0PromptRun2023D'))

#os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/Muon1/Run2023A-PromptNanoAODv11p9_v2-v1/NANOAOD', 'Muon1Run2023A'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/Muon1/Run2023B-PromptNanoAODv12_v1-v1/NANOAOD', 'Muon1Run2023B'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/Muon1/Run2023C-PromptNanoAODv12_v2-v2/NANOAOD', 'Muon1Run2023C'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/Muon1/Run2023C-PromptNanoAODv12_v3-v1/NANOAOD', 'Muon1Run2023Cv3'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/Muon1/Run2023C-PromptNanoAODv12_v4-v1/NANOAOD', 'Muon1Run2023Cv4'))

os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/Muon1/Run2023C-PromptReco-v4/NANOAOD', 'Muon1PromptRun2023C'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/Muon1/Run2023D-PromptReco-v1/NANOAOD', 'Muon1PromptRun2023D'))

os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/ParkingHH/Run2023C-PromptNanoAODv12_v2-v1/NANOAOD', 'ParkingHHRun2023C'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/ParkingHH/Run2023C-PromptNanoAODv12_v3-v1/NANOAOD', 'ParkingHHRun2023Cv3'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/ParkingHH/Run2023C-PromptNanoAODv12_v4-v1/NANOAOD', 'ParkingHHRun2023Cv4'))

os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/ParkingVBF1/Run2023C-PromptNanoAODv12_v2-v1/NANOAOD ', 'ParkingVBF1Run2023C'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/ParkingVBF1/Run2023C-PromptNanoAODv12_v3-v1/NANOAOD ', 'ParkingVBF1Run2023Cv3'))
os.system("dasgoclient -query=\"file dataset={}\" 2>&1 | tee trigger/2023/{}.list".format('/ParkingVBF1/Run2023C-PromptNanoAODv12_v4-v1/NANOAOD ', 'ParkingVBF1Run2023Cv4'))


