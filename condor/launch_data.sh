VERSION=v18-6jets-BDT-BTAG

python2 runHHH6b.py --option 0 -o ${VERSION} --year 2017 --run-data -n 1
condor_submit jobs_${VERSION}_ak8_option0_2017/data/submit.cmd

python2 runHHH6b.py --option 1 -o ${VERSION} --year 2017 --run-data -n 1
condor_submit jobs_${VERSION}_ak8_option1_2017/data/submit.cmd

python2 runHHH6b.py --option 2 -o ${VERSION} --year 2017 --run-data -n 1
condor_submit jobs_${VERSION}_ak8_option2_2017/data/submit.cmd

python2 runHHH6b.py --option 3 -o ${VERSION} --year 2017 --run-data -n 1
condor_submit jobs_${VERSION}_ak8_option3_2017/data/submit.cmd
