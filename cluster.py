

import pandas as pd
from pathlib import Path
import requests

import json
import numpy as np

import gzip
import _pickle as cPickle

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
import operator

with gzip.GzipFile(r"Users_Tag_Matrix.data.gz", "rb") as input_file:
    df = cPickle.load(input_file)
df = df.tail(8000)# Make a copy of DF
df_tr = df



for n_clusters in range(20):
    if n_clusters < 3: continue
kmeans = KMeans(n_clusters = n_clusters, random_state = 0).fit(df)
labels = kmeans.labels_
silhouette_avg = silhouette_score(df, labels)
print("For n_clusters =", n_clusters, "The average silhouette_score is :", silhouette_avg)

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
    pd.DataFrame.from_dict(sorted_dict_tags).tail(10)
    print("Users", sub_df.shape[0])#
    new_role = pd.DataFrame.from_dict(sorted_dict_tags).tail(10).T.iloc[0: 2]
    new_role.columns = pd.DataFrame.from_dict(sorted_dict_tags).tail(10).T.iloc[0]
    total =  float(sub_df.shape[0])
    new_role  = new_role.iloc[1: 2] / total
    roles = pd.concat((new_role, roles))
    
roles.fillna(0, inplace=True)
roles.to_csv("Roles.csv")

>>> jaime = df.tail(1)


kmeans.predict(jaime)[0]

github_user = "jaimevalero"

import scipy

for i in range (13) : scipy.spatial.distance.euclidean(centroids[i],  jaime.values.tolist()[0])
