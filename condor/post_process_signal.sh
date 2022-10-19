VERSION=v17-6jets-BDT

python runHHH6b.py --option 0 -o ${VERSION} --year 2017 --run-signal -n 1 --post
python runHHH6b.py --option 1 -o ${VERSION} --year 2017 --run-signal -n 1 --post
python runHHH6b.py --option 2 -o ${VERSION} --year 2017 --run-signal -n 1 --post
python runHHH6b.py --option 3 -o ${VERSION} --year 2017 --run-signal -n 1 --post

PATHOUTPUT=/isilon/data/users/mstamenk/eos-triple-h/samples-${VERSION}-nanoaod
mkdir $PATHOUTPUT


python /isilon/data/users/mstamenk/hhh-6b-producer/CMSSW_11_1_0_pre5_PY3/src/PhysicsTools/NanoAODTools/scripts/haddnano.py $PATHOUTPUT/GluGluToHHHTo6B_SM.root ${VERSION}_ak8_option*_2017/signal/parts/*.root 




