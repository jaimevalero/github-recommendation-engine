
import sys
import requests
import json
from   requests.auth import HTTPBasicAuth


# Load Data

github_user = sys.argv[1]

url     = 'https://api.github.com/users/%s/repos' % github_user
headers = { 'content-type': 'application/json',
            'Accept-Charset': 'UTF-8' , 
            'Accept' : 'application/vnd.github.mercy-preview+json' }

r                = requests.get(url,  headers=headers , auth=HTTPBasicAuth('jvbm301', PERSONAL_TOKEN))
json_response    = r.json()

# Extract data
repos_names      = pyjq.all(".[] | .name"    ,     json_response )
repo_languages   = pyjq.all(".[] | .language",     json_response )
repo_description = pyjq.all(".[] | .description",  json_response )
repo_topics      = pyjq.all(".[] | .topics",       json_response )

repo_topics_flatlist = [item for sublist in kk for item in sublist]
#['python', 'scikitlearn-machine-learning']
 
#['ansible-swarm-playbook', 'Cfish', 'cifras_y_letras-test', 'epg-icinga', 'itop-docker', 'itop-utilities', 'jaimevalero78.github.io', 'jupyter-learning', 'learning-machine-learning', 'openstack-monitoring', 'openstack-utilities', 'shell-microservice-exposer', 'techradar', 'test-branching']

# Load csv
import pandas as pd
df = pd.read_csv('TopStaredRepositories.csv')
df.head(1)

# Freq 
{i:repo_languages.count(i) for i in set(repo_languages)}
#{'C': 1, 'CSS': 1, 'JavaScript': 1, 'Shell': 6, 'Jupyter Notebook': 1, None: 1, 'Python': 3}

kk = {i:repo_languages.count(i)/len(repo_languages) for i in set(repo_languages)}
{'C': 0.07142857142857142, 'CSS': 0.07142857142857142, 'JavaScript': 0.07142857142857142, 'Shell': 0.42857142857142855, 'Jupyter Notebook': 0.07142857142857142, None: 0.07142857142857142, 'Python': 0.21428571428571427}

#df['Tags'].fillna(["kk"],inplace=True)

import math

tags_list = []

# assign which languages
for i, row in df.fillna('').iterrows():
  row_list = row['Tags'].split(",")
  resul     = set(row_list).intersection(repo_topics_flatlist )
  tags_list.append( {} if len(resul) == 0 else resul )
  print (tags_list)

frame=pd.DataFrame(tags_list, columns=['Tags']) 


for key in d:
    print (key, 'corresponds to', d[key])
