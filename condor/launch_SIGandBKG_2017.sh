VERSION=v9_4AK8PNetjet2Tau

python runHHH4b2tauPNetAK4.py --option 92 --jobdir v9_4AK8PNetjet2Tau -o /eos/user/r/rtu/savePNetOut --year 2017 -n 1 # --post
# condor_submit jobs_${VERSION}_ak4_option92_2017/mc/submit.cmd
