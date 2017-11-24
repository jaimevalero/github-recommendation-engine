

import pandas as pd
from pathlib import Path
import requests

import json
import numpy as np

import gzip
import _pickle as cPickle

from sklearn.cluster import KMeans

with gzip.GzipFile(r"Users_Tag_Matrix.data.gz", "rb") as input_file:
    df = cPickle.load(input_file)

#Make a copy of DF
df_tr = df

#Cluster the data
NUM_CLUSTERS = 9
kmeans = KMeans(n_clusters=NUM_CLUSTERS, random_state=0).fit(df)
labels = kmeans.labels_

#Glue back to originaal data
df_tr['clusters'] = labels
for cluster in range(NUM_CLUSTERS):
    sub_df = df[df['clusters'] == cluster]
    ##
    dict_tags = {}
    for column in sub_df.columns :
        if sub_df[column].sum() > 0 : dict_tags[column] = sub_df[column].sum()
    dict_tags.pop('clusters', None)
    sorted_dict_tags = sorted(dict_tags.items(), key=operator.itemgetter(1))
    pd.DataFrame.from_dict(sorted_dict_tags).tail(10)
    print("Users", sub_df.shape[0])