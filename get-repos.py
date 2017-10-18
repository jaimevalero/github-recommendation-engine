
import sys
import requests
import json
from   requests.auth import HTTPBasicAuth
import pyjq


#>>> mergedlist
#['nonprofits', 'certification', 'curriculum', 'react', 'nodejs', 'javascript', 'd3', 'teachers', 'community', 'education', 'programming', 'math', 'learn-to-code', 'careers', 'javascript', 'css', 'html', 'bootstrap', 'jekyll-site', 'scss', 'education', 'list', 'books', 'resource']


# Load Data
PERSONAL_TOKEN = "ac995cdbc4e65c85609434538bd8a135d4c933d9"

#github_user = sys.argv[1]
github_user="jaimevalero"

url     = 'https://api.github.com/users/%s/repos' % github_user
headers = { 'content-type': 'application/json',
            'Accept-Charset': 'UTF-8' , 
            'Accept' : 'application/vnd.github.mercy-preview+json' }

r                = requests.get(url,  headers=headers , auth=HTTPBasicAuth('jaimevalero', PERSONAL_TOKEN))
json_response    = r.json()

# Extract data
repos_names      = pyjq.all(".[] | .name"    ,     json_response )
repo_languages   = pyjq.all(".[] | .language",     json_response )
repo_description = pyjq.all(".[] | .description",  json_response )
repo_topics      = pyjq.all(".[] | .topics",       json_response )

# Flat multi dimensional array
repo_topics_flatlist = [item for sublist in repo_topics for item in sublist]
#['python', 'scikitlearn-machine-learning']
 
#['ansible-swarm-playbook', 'Cfish', 'cifras_y_letras-test', 'epg-icinga', 'itop-docker', 'itop-utilities', 'jaimevalero78.github.io', 'jupyter-learning', 'learning-machine-learning', 'openstack-monitoring', 'openstack-utilities', 'shell-microservice-exposer', 'techradar', 'test-branching']

# Load csv
import pandas as pd
df = pd.read_csv('TopStaredRepositories.csv')
df = df.dropna(subset=['Tags'], how='all')
df['Url'] = "http://github.com/" + df_backup['Username'] + "/" +df_backup['Repository Name']
df['Tags'] = df['Tags'] + ","
df_backup = df

df.to_csv("clean_TopStaredRepositories.csv")
df        = pd.read_csv('clean_TopStaredRepositories.csv')
df_backup = pd.read_csv('clean_TopStaredRepositories.csv')




# Get Tags
mergedlist = []
for i in df['Tags'].dropna().str.split(","):
   mergedlist.extend(i)

tags = sorted(set(mergedlist))



for tag in tags:
  tag
  df[tag] = 0 
  df.loc[df['Tags'].str.contains(tag+","),tag] = 1


just_dummies = pd.get_dummies(df['Language'])

df = pd.concat([df, just_dummies], axis=1) 


COLUMNS_TO_REMOVE_LIST = [ 'Username','Repository Name','Description','Last Update Date','Language','Number of Stars','Tags','Url', 'Unnamed: 0']
for column in COLUMNS_TO_REMOVE_LIST: del df[column]



from scipy.spatial import distance
df.to_csv("salida.csv")
distance.euclidean(df[1:2],df[2:3])

from scipy.spatial.distance import squareform, pdist
#df_dist = pd.DataFrame(squareform(pdist(df)))

df_dist.to_csv("distances.csv")

#for row in df_dist.iterrows():
#    i, data = row
#    print(i,df_backup.Url.loc[i])
#    kk = df_dist
#    kk.loc[kk[i] == 0, i] = 1000
#    min = kk[i].min()
#    similar =kk.loc[kk[i] == min].index[0]
#    print ( i,similar )
#    print ( min, df_backup.Url.loc[i] ,df_backup.Url.loc[similar]) 


repos = list(df_backup['Username'] + "/" +df_backup['Repository Name'])
from scipy.spatial.distance import squareform
res = pdist(df, 'euclidean')
squareform(res)
df_dist = pd.DataFrame(squareform(res), index=repos, columns= repos)
df_dist.to_csv("distances.csv")



for i in df_dist.columns :
  #i='atom/atom'
  df_dist.loc[df_dist[i] == 0, i] = 1000
  min = df_dist[i].min()
  #similar =df_dist.loc[df_dist[i] == min].index[0]
  kk = df_dist[i]
  print ( kk[df_dist[i] == min].index, i, min)

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
