VERSION=v17-6jets-BDT

python runHHH6b.py --option 0 -o ${VERSION} --year 2017 -n 1 --post
python runHHH6b.py --option 1 -o ${VERSION} --year 2017 -n 1 --post
python runHHH6b.py --option 2 -o ${VERSION} --year 2017 -n 1 --post
python runHHH6b.py --option 3 -o ${VERSION} --year 2017 -n 1 --post

PATHOUTPUT=/isilon/data/users/mstamenk/eos-triple-h/samples-${VERSION}-nanoaod
mkdir $PATHOUTPUT


#python /isilon/data/users/mstamenk/hhh-6b-producer/CMSSW_11_1_0_pre5_PY3/src/PhysicsTools/NanoAODTools/scripts/haddnano.py $PATHOUTPUT/QCD6B.root ${VERSION}_ak8_option*_2017/mc/parts/QCD_*_6b_*.root 
python /isilon/data/users/mstamenk/hhh-6b-producer/CMSSW_11_1_0_pre5_PY3/src/PhysicsTools/NanoAODTools/scripts/haddnano.py $PATHOUTPUT/QCD.root ${VERSION}_ak8_option*_2017/mc/parts/QCD*0_Tun*.root ${VERSION}_ak8_option*_2017/mc/parts/QCD*Inf_Tun*.root 
python /isilon/data/users/mstamenk/hhh-6b-producer/CMSSW_11_1_0_pre5_PY3/src/PhysicsTools/NanoAODTools/scripts/haddnano.py $PATHOUTPUT/QCD6B.root ${VERSION}_ak8_option*_2017/mc/parts/QCD*_6b_*.root 
python /isilon/data/users/mstamenk/hhh-6b-producer/CMSSW_11_1_0_pre5_PY3/src/PhysicsTools/NanoAODTools/scripts/haddnano.py $PATHOUTPUT/WWTo4Q.root ${VERSION}_ak8_option*_2017/mc/parts/WWTo4Q_*.root 
python /isilon/data/users/mstamenk/hhh-6b-producer/CMSSW_11_1_0_pre5_PY3/src/PhysicsTools/NanoAODTools/scripts/haddnano.py $PATHOUTPUT/WWZ.root ${VERSION}_ak8_option*_2017/mc/parts/WWZ_*.root 
python /isilon/data/users/mstamenk/hhh-6b-producer/CMSSW_11_1_0_pre5_PY3/src/PhysicsTools/NanoAODTools/scripts/haddnano.py $PATHOUTPUT/ZJetsToQQ.root ${VERSION}_ak8_option*_2017/mc/parts/ZJetsToQQ_*.root 
python /isilon/data/users/mstamenk/hhh-6b-producer/CMSSW_11_1_0_pre5_PY3/src/PhysicsTools/NanoAODTools/scripts/haddnano.py $PATHOUTPUT/ZZZ.root ${VERSION}_ak8_option*_2017/mc/parts/ZZZ_*.root 
python /isilon/data/users/mstamenk/hhh-6b-producer/CMSSW_11_1_0_pre5_PY3/src/PhysicsTools/NanoAODTools/scripts/haddnano.py $PATHOUTPUT/WJetsToQQ.root ${VERSION}_ak8_option*_2017/mc/parts/WJetsToQQ_*.root 
python /isilon/data/users/mstamenk/hhh-6b-producer/CMSSW_11_1_0_pre5_PY3/src/PhysicsTools/NanoAODTools/scripts/haddnano.py $PATHOUTPUT/WWW.root ${VERSION}_ak8_option*_2017/mc/parts/WWW_*.root 
python /isilon/data/users/mstamenk/hhh-6b-producer/CMSSW_11_1_0_pre5_PY3/src/PhysicsTools/NanoAODTools/scripts/haddnano.py $PATHOUTPUT/WZZ.root ${VERSION}_ak8_option*_2017/mc/parts/WZZ_*.root 
python /isilon/data/users/mstamenk/hhh-6b-producer/CMSSW_11_1_0_pre5_PY3/src/PhysicsTools/NanoAODTools/scripts/haddnano.py $PATHOUTPUT/ZZTo4Q.root ${VERSION}_ak8_option*_2017/mc/parts/ZZTo4Q_*.root 
python /isilon/data/users/mstamenk/hhh-6b-producer/CMSSW_11_1_0_pre5_PY3/src/PhysicsTools/NanoAODTools/scripts/haddnano.py $PATHOUTPUT/TT.root ${VERSION}_ak8_option*_2017/mc/parts/TT_*.root 




