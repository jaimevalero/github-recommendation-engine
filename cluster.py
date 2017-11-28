

import pandas as pd
from pathlib import Path
import requests
from scipy.spatial.distance import squareform, pdist
import json
import numpy as np

import gzip
import _pickle as cPickle

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
import operator
import get_repos
import load_user

with gzip.GzipFile(r"Users_Tag_Matrix.data.gz", "rb") as input_file:
    df = cPickle.load(input_file)
df = df.tail(8000)# Make a copy of DF
df_tr = df



#for n_clusters in range(20):
#    if n_clusters < 3: continue
#kmeans = KMeans(n_clusters = n_clusters, random_state = 0).fit(df)
#labels = kmeans.labels_
#silhouette_avg = silhouette_score(df, labels)
#print("For n_clusters =", n_clusters, "The average silhouette_score is :", silhouette_avg)

with gzip.GzipFile(r"Users_Tag_Matrix.data.gz", "rb") as input_file:
    df = cPickle.load(input_file)

# So we chose
# Cluster the data
n_clusters = 12
kmeans = KMeans(n_clusters = n_clusters, random_state = 0).fit(df)
labels = kmeans.labels_#
    
roles = pd.DataFrame()# Glue back to originaal data
df['clusters'] = labels
label_df = []
for cluster in range(n_clusters):
    sub_df = df[df['clusters'] == cluster]
    dict_tags = {}
    for column in sub_df.columns:
        if sub_df[column].sum() > 0: dict_tags[column] = sub_df[column].sum()#
    dict_tags.pop('clusters', None)
    sorted_dict_tags = sorted(dict_tags.items(), key = operator.itemgetter(1))
    kk = pd.DataFrame.from_dict(sorted_dict_tags).tail(10)
    kk.columns = ['Tecnologia' , 'Peso' ]
    print(kk)
    print("Users", sub_df.shape[0])#
    new_role_element = pd.DataFrame.from_dict(sorted_dict_tags).tail(10).T.iloc[0: 2]
    new_role_element.columns = pd.DataFrame.from_dict(sorted_dict_tags).tail(10).T.iloc[0]
    total =  float(sub_df.shape[0])
    new_role_element  = new_role_element.iloc[1: 2] / total
    roles = pd.concat((new_role_element, roles))
    
roles.fillna(0, inplace=True)
roles.to_csv("Roles.csv")

roles =
import scipy

# roles = roles , corr_tags =  

#kmeans.predict(jaime)[0]


roles = pd.read_csv('Roles.csv')

github_user = "jaimevalero"
json_response = get_repos.Load_User_Repos(github_user)
df_tags, df = load_user.Load_Initial_data()
print((start - time.time()), "Load_Initial_data ")
# Add user
df, all_repos_tags = load_user.Get_User_Tags(df, json_response, 1000, github_user)
df, all_repos_tags = load_user.Reduce_Tag_Ponder_Matrix(df, github_user, all_repos_tags)

# Assign
new_role_element = pd.DataFrame(0, [roles.index.max() + 1], columns=roles.columns, )
current_user_role = df.tail(1)
current_user_role.set_index(github_user)

reduced_roles =  pd.DataFrame()

for column in set(roles.columns.values.tolist()).intersection( all_repos_tags.columns.values.tolist()) :
    new_role_element[column] = float(current_user_role[column].head(1))

roles = pd.concat([roles, new_role_element])

for column in set(roles.columns.values.tolist()).intersection(all_repos_tags.columns.values.tolist()):
    reduced_roles[column]  =  roles[column]

roles = reduced_roles
res_roles = pdist(roles, 'euclidean')
squareform(res_roles)
roles_dist = pd.DataFrame(squareform(res_roles), index=roles, columns=roles)
roles_total      =  pd.DataFrame(0, index =  roles.index, columns = ["total"])

for column in roles.columns:
    roles[column] -= roles.iloc[-1][column]
    # We calculate the euclidean distance, respect 0,0....,0, the github_user cordinates
    roles_total["total"] += (roles[column] ** 2)


roles_total["total"] = roles_total["total"] ** 0.5

