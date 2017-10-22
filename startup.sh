cd /Users/jaimevalerodebernabe/git/github-recommendation-engine
 #source /root/scripts/api-search/my_project/bin/activate /etc/profile
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rh/python27/root/usr/lib64/
export PATH=$PATH:/Users/jaimevalerodebernabe/git/github-recommendation-engine/html

# alias flask='cd /root/scripts/api-search; ./startup.sh'

rm -f /tmp/cache*
netstat -tlpn | grep :5000 | awk ' { print $7} ' | cut -d\/ -f1 | xargs kill -9 2>/dev/null

nohup gunicorn -b 0.0.0.0:5000  -w 6  github-recommendation-engine:app  --timeout 30 --log-level=debug  &


#tail -f log-api-search.log  nohup.out
#gunicorn -b 0.0.0.0:5000 -w 2 flask-app:app --timeout 30 --log-level=debug
#gunicorn -b 0.0.0.0:5000 -w 2 flask-app:app --timeout 30 --log-level=debug

gunicorn -b 0.0.0.0:5000  -w 2  flask-app:app  --timeout 30 --log-level=debug 



