VERSION=v19-6jets-BDT-BTAG

python runHHH6b.py --option 4 -o ${VERSION} --year 2018 --run-signal -n 1 --post

PATHOUTPUT=/isilon/data/users/mstamenk/eos-triple-h/samples-${VERSION}-2018-nanoaod
mkdir $PATHOUTPUT


python /isilon/data/users/mstamenk/hhh-6b-producer/CMSSW_11_1_0_pre5_PY3/src/PhysicsTools/NanoAODTools/scripts/haddnano.py $PATHOUTPUT/GluGluToHHHTo6B_SM.root ${VERSION}_ak8_option*_2018/signal/parts/*.root 




