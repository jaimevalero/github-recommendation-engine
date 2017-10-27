#!/bin/bash


cd /Users/jaimevalerodebernabe/git/github-recommendation-engine
export PATH=$PATH:/Users/jaimevalerodebernabe/git/github-recommendation-engine:/Users/jaimevalerodebernabe/git/github-recommendation-engine

source activate flask

# alias flask='cd /root/scripts/api-search; ./startup.sh'

rm -f /tmp/cache*
netstat -an | grep python | awk ' { print $3} ' | xargs kill -9 2>/dev/null

gunicorn -b 0.0.0.0:5000  -w 1  github-recommendation-engine:app  --timeout 30 --log-level=debug  




