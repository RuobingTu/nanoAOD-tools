VERSION=v3-4b2tau

python2 runHHH4b2tau.py --option 0 -o ${VERSION} --year 2017 --run-signal -n 1
condor_submit jobs_${VERSION}_ak8_option0_2017/signal/submit.cmd

python2 runHHH4b2tau.py --option 1 -o ${VERSION} --year 2017 --run-signal -n 1
condor_submit jobs_${VERSION}_ak8_option1_2017/signal/submit.cmd

python2 runHHH4b2tau.py --option 2 -o ${VERSION} --year 2017 --run-signal -n 1
condor_submit jobs_${VERSION}_ak8_option2_2017/signal/submit.cmd

python2 runHHH4b2tau.py --option 3 -o ${VERSION} --year 2017 --run-signal -n 1
condor_submit jobs_${VERSION}_ak8_option3_2017/signal/submit.cmd
