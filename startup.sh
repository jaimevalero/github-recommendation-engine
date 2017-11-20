#!/bin/bash

cd /Users/jaimevalerodebernabe/git/github-recommendation-engine
export PATH=$PATH:/Users/jaimevalerodebernabe/git/github-recommendation-engine:/Users/jaimevalerodebernabe/git/github-recommendation-engine

# source /Users/jaimevalerodebernabe/miniconda3/envs/flask/bin/activate 
source activate flask

# alias flask='cd /root/scripts/api-search; ./startup.sh'

#rm -f /tmp/cache*
netstat -an | grep python | awk ' { print $3} ' | xargs kill -9 2>/dev/null
ps -ef | grep python  | awk '{print $2}' | xargs kill -9

#rm -f /tmp/*jaimevalero* Generate_Tag_Matrix.data

gunicorn -b 0.0.0.0:5000  -w 1  app:app  --timeout 300 --log-level=debug  




