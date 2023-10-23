VERSION=v31
YEAR=$1

#python2 runHHH6b.py --option 0 -o ${VERSION} --year 2017 -n 1
#condor_submit jobs_${VERSION}_ak8_option0_2017/mc/submit.cmd

#python2 runHHH6b.py --option 1 -o ${VERSION} --year 2017 -n 1
#condor_submit jobs_${VERSION}_ak8_option1_2017/mc/submit.cmd

#python2 runHHH6b.py --option 2 -o ${VERSION} --year 2017 -n 1
#condor_submit jobs_${VERSION}_ak8_option2_2017/mc/submit.cmd

#python2 runHHH6b.py --option 3 -o ${VERSION} --year 2017 -n 1
#condor_submit jobs_${VERSION}_ak8_option3_2017/mc/submit.cmd

python2 runHHH6bPNetAK4.py --option 4 -o ${VERSION} --year ${YEAR} -n 8
condor_submit jobs_${VERSION}_ak8_option4_${YEAR}/mc/submit.cmd

