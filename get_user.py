import pandas as pd
import json
from pathlib import Path
import requests

#def Get_Data_Tags() :

import pickle
import pandas as pd

# MEDIANAS
from operator import itemgetter

medians = {}
for i in df.columns :
    print (i)
    medians[i] =  df[i].mean()

for k, v in sorted(medians.items(), key=itemgetter(1)):
    print (":::::" , k, v)


df = Load_Tag_Matrix(df = pd.DataFrame())

i = 'python'
j = "youtube"

temp_df = df[df[i] == 1 ][i]

teral
>>>
df['Tags'].fillna("", inplace=True)


for i in  df.columns :
    total = df[i].sum()
    print (i,total)

for i in  df.columns :
    temp_df = df[df[i] == 1 ]
    resul_i = temp_df[i].count()
    for j in temp_df.columns :
        if ( temp_df[j].sum() == 0 ):
            continue
        if ( i == j  ) :
             continue
        resul_j = temp_df[temp_df[j] == 1 ][j].sum()
        print (i,j, resul_j/resul_i)

i = 'jupyter notebook'
j = 'python'

for column in df.columns:
    temp_df = df[df[column] == 1 ]
    for column in temp_df

for column in df.columns:
    temp_df = df[df[column] == 1 ]
    for column in temp_df


column = 'python'

df_dist.loc[df_dist[i] == 0, i]

# Data declaration
user = "ztomer"
JSON_DIR=("scripts/files")

FULL_PATH="%s/%s.json" % (JSON_DIR, user)
my_file = Path( FULL_PATH)

with open( FULL_PATH, "rb") as input_file:
   json_response = json.load(input_file)

tags_candidates = []

repo_names       = pyjq.all(".[] | .name"        ,  json_response)
repo_languages   = pyjq.all(".[] | .language"    ,  json_response)
repo_description = pyjq.all(".[] | .description" ,  json_response)
repo_topics      = pyjq.all(".[] | .topics"      ,  json_response)

repo_names
repo_languages
repo_description
repo_topics


['.hammerspoon', 'calendar-app', 'fantasque_awesome_powerline', 'gcal-mac', 'gdb-dashboard', 'homedir', 'hydra_config', 'libswiftnav', 'mjolnir.th.hints', 'playground', 'scripts', 'sekret_tunnel', 'Zim.app']

#def Load_User_Tags(user):



df.to_csv("kk_tag_matrix.csv")


import requests
from requests.auth import HTTPBasicAuth
import pyjq
github_user = "jaimevalero"
PERSONAL_TOKEN = "ac995cdbc4e65c85609434538bd8a135d4c933d9"
url = 'https://api.github.com/users/%s/repos?sort=updated' % github_user
headers = {'content-type': 'application/json',
           'Accept-Charset': 'UTF-8',
           'Accept': 'application/vnd.github.mercy-preview+json'}
r = requests.get(url,  headers=headers, auth=HTTPBasicAuth(
    "jaimevalero", PERSONAL_TOKEN))
json_response = r.json()






#============
df = pd.DataFrame()
df = pd.read_csv('TopStaredRepositories.csv')

df['Url'] = "http://github.com/" + \
    df['Username'] + "/" + df['Repository Name']
df['Tags'].fillna("", inplace=True)
df['Description'].fillna("", inplace=True)

df['Tags'] = df['Tags'] + ","
df.to_csv("clean_TopStaredRepositories.csv")
df = pd.read_csv('clean_TopStaredRepositories.csv')

df['Language'] = df.loc[:, 'Language'].str.lower()
df_backup = df.copy(deep=True)

## Tag matrix
mergedlist = []
for i in df['Tags'].dropna().str.split(","):
    mergedlist.extend(i)

tags = []

tags = sorted(set(mergedlist))

# Encode languages in single column
just_dummies = pd.get_dummies(df['Language'])
for column in just_dummies.columns:
    if column not in df.columns:
        df[column] = just_dummies[column]

# Just to avoid
df['Description'].fillna("", inplace=True)

for tag in tags:
    if tag not in df.columns:
        df[tag] = 0
    try:
        df.loc[df['Tags'].str.contains(tag + ","), tag] = 1
        if len(tag) > 4  :
            df.loc[df['Repository Name'].str.contains(tag), tag] = 0.85
            df.loc[df['Description'].str.contains(tag), tag] = 0.66
            print("added " , tag)
    except Exception:
        print(tag)
        pass


# Remove columns not needed
df.set_index(['Repository Name'])
df.reset_index()
df.reindex(index = df['Repository Name'])

COLUMNS_TO_REMOVE_LIST = ['', 'unnamed: 0','Username', 'Repository Name', 'Description',
                          'Last Update Date', 'Language', 'Number of Stars', 'Tags', 'Url','Gravatar' ,'Unnamed: 0']
for column in COLUMNS_TO_REMOVE_LIST:
    try:
        del df[column]
        del df[column.lower]
    except Exception:
        pass

df.columns = df.columns.str.lower()

with open(r"Generate_Tag_Matrix.data", "wb") as output_file:
    pickle.dump(df, output_file)





###


i = 0
repo_names       = pyjq.all(".[%s] | .name"        % i,  json_response)
repo_languages   = pyjq.all(".[%s] | .language"    % i,  json_response)
repo_description = pyjq.all(".[%s] | .description" % i,  json_response)
repo_topics      = pyjq.all(".[%s] | .topics"      % i,  json_response)



if repo_description[0] is None:
    repo_description = ['kk']

new_element = pd.DataFrame(0, [df.index.max() + 1], columns=df.columns)
for j in (repo_names[0].split('-') + repo_languages + repo_description[0].replace(".", " ").replace(",", " ").split() + list(repo_topics[0])):
    if j is not None:
        if j.lower() in df.columns:
            print("Setting to 1", j.lower())
            new_element[j.lower()] = 1
# Concat new user repo dataframe to stared repos dataframe
df = pd.concat([df, new_element])



repos = list(df_backup['Username'] + "/" + df_backup['Repository Name'])
repos.extend(repo_names)

from scipy.spatial import distance
from scipy.spatial.distance import squareform, pdist
res = pdist(df, 'euclidean')
squareform(res)
df_dist = pd.DataFrame(squareform(res), index=repos, columns=repos)




##### Sacar tags lista repositorios, y del último
URL1 = 'http://github.com/freeCodeCamp/freeCodeCamp'
a = int(df_backup.loc[df_backup['Url'] == URL1 , 'Unnamed: 0' ])
serie1 = df.iloc[a]
serie2 = df[].tail(1)

common_tags = []
for i in df.columns :
    if float(serie1[i]) > 0 and float(serie2[i]) > 0 : common_tags.append(i)




### Repplace distance matrix
import numpy as np
#df = pd.DataFrame()
#df = pd.read_csv('test.csv')


np.logical_and(XA, XB)
  primero  segundo  tercero  cuarto  quinto  sexto  septimo
0    False    False    False    True    True  False    False

np.count_nonzero(np.logical_and(XA, XB))


# 
start = time.time()
NUM_ELEMENTS=len(df)-1
user_repo = df.iloc[NUM_ELEMENTS:]
for i in range(NUM_ELEMENTS):
    stared_repo = df.iloc[i:i+1]
    shared_tags = np.count_nonzero(np.logical_and(stared_repo, user_repo))
    if shared_tags > 0 : print(i,shared_tags)

print(start - time.time(), "Metodo 1 " )


np.count_nonzero(np.logical_and(XA, XB))
df = pd.concat([df, new_element])
