import pandas as pd
import os
from pathlib import Path
import sys
import requests
import json
from requests.auth import HTTPBasicAuth
import pyjq
from scipy.spatial import distance
from scipy.spatial.distance import squareform, pdist
import pickle
import time
import re

def Load_Starred_Repos():
    df = pd.DataFrame()
    df = pd.read_csv('TopStaredRepositories.csv')
    #df = df.dropna(subset=['Tags'], how='all')

    df['Url'] = "http://github.com/" + \
        df['Username'] + "/" + df['Repository Name']
    df['Tags'] = df['Tags'] + ","
    df.to_csv("clean_TopStaredRepositories.csv")
    df = pd.read_csv('clean_TopStaredRepositories.csv')

    #df_backup = pd.read_csv('clean_TopStaredRepositories.csv')
    #
    df['Language'] = df.loc[:, 'Language'].str.lower()
    df_backup = df.copy(deep=True)
    return df, df_backup


def Load_User_Repos(github_user):
    PERSONAL_TOKEN = "ac995cdbc4e65c85609434538bd8a135d4c933d9"
    url = 'https://api.github.com/users/%s/repos?sort=updated' % github_user
    headers = {'content-type': 'application/json',
               'Accept-Charset': 'UTF-8',
               'Accept': 'application/vnd.github.mercy-preview+json'}
    r = requests.get(url,  headers=headers, auth=HTTPBasicAuth(
        "jaimevalero", PERSONAL_TOKEN))
    return r.json()


def Generate_Tag_Matrix(df):
    my_file = Path("Generate_Tag_Matrix.data")
    if my_file.exists():
        #print ("Cargamos el Tag maxtrix")
        with open(r"Generate_Tag_Matrix.data", "rb") as input_file:
            df = pickle.load(input_file)
        return df
    else:

        # Generate tag list
        mergedlist = []
        for i in df['Tags'].dropna().str.split(","):
            mergedlist.extend(i)
        tags = sorted(set(mergedlist))
        # Encode languages in single column
        just_dummies = pd.get_dummies(df['Language'])
        for column in just_dummies.columns:
            if column not in df.columns:
                df[column] = just_dummies[column]

        for tag in tags:
            if tag not in df.columns:
                df[tag] = 0
            try:
                df.loc[df['Tags'].str.contains(tag + ","), tag] = 1
                df.loc[df['Description'].str.contains(tag), tag] = 1
                df.loc[df['Repository Name'].str.contains(tag), tag] = 1
            except Exception:
                pass
        # Remove columns not needed
        df.set_index(['Repository Name'])
        COLUMNS_TO_REMOVE_LIST = ['', 'Username', 'Repository Name', 'Description',
                                  'Last Update Date', 'Language', 'Number of Stars', 'Tags', 'Url','Gravatar' ,'Unnamed: 0']
        for column in COLUMNS_TO_REMOVE_LIST:
            del df[column]
        df.columns = df.columns.str.lower()

        with open(r"Generate_Tag_Matrix.data", "wb") as output_file:
            pickle.dump(df, output_file)

    return df


def Enrich_All_Tag_Matrix(df, json_response, i):
    new_element = pd.DataFrame(0, [df.index.max() + 1], columns=df.columns)

    all_tags = (pyjq.all(".[] | .name",  json_response) + pyjq.all(".[] | .language",
                                                                   json_response) + pyjq.all(".[] | .topics[]",  json_response))
    kk = pyjq.all(".[] | .description",  json_response)
    for i in kk:
        all_tags = all_tags + i.split()

    for j in all_tags:
        for k in j.lower.split("-"):
            if k is not None:
                if k in df.columns:
                    print("Setting to 1", k)
                    new_element[k] = 1
        if j is not None:
            if j.lower() in df.columns:
                print("Setting to 1", j.lower())
                new_element[j.lower()] = 1

    df = pd.concat([df, new_element])
    df.to_csv("Tag_Matrix.csv")

    return df, repo_names


def Enrich_Tag_Matrix(df, json_response, i):
    repo_names       = pyjq.all(".[%s] | .name"        % i,  json_response)
    repo_languages   = pyjq.all(".[%s] | .language"    % i,  json_response)
    repo_description = pyjq.all(".[%s] | .description" % i,  json_response)
    repo_topics      = pyjq.all(".[%s] | .topics"      % i,  json_response)
    #
    #print( repo_description, repo_names)
    if repo_description[0] is None:
        repo_description = ['kk']

    new_element = pd.DataFrame(0, [df.index.max() + 1], columns=df.columns)
    for j in (repo_names[0].split('-') + repo_languages + repo_description[0].replace(".", " ").replace(",", " ").split() + list(repo_topics[0])):
        if j is not None:
            if j.lower() in df.columns:
                #print("Setting to 1", j.lower())
                new_element[j.lower()] = 1
    # Concat new user repo dataframe to stared repos dataframe
    df = pd.concat([df, new_element])
    # df.to_csv("Enrich_Tag_Matrix.csv")

    return df, repo_names


def Generate_Distance_Matrix(df_backup, df, repo_names):
    repos = list(df_backup['Username'] + "/" + df_backup['Repository Name'])
    repos.extend(repo_names)

    res = pdist(df, 'euclidean')
    squareform(res)
    df_dist = pd.DataFrame(squareform(res), index=repos, columns=repos)
    # df_dist.to_csv("Distance_Matrix.csv")
    return df_dist

def Get_Closest_Repo(df_dist,df_backup):
    result_array = []
    i = df_dist.columns[-1]
    df_dist.loc[df_dist[i] == 0, i] = 1000
    min = df_dist[i].min()
    kk = df_dist[i]
    print(kk[df_dist[i] == min].index, i, min)
    for recomended_repo in (kk[df_dist[i] == min].index[0:12]):
        description = df_backup.loc[df_backup['Url'] == (
            'http://github.com/%s' % recomended_repo), 'Description'].iloc[0]
        gravatar =   df_backup.loc[df_backup['Url'] == (
            'http://github.com/%s' % recomended_repo), 'Gravatar'].iloc[0]
        #description
        result_array.append({
            "score": min,
            "user_repo_name": i,
            "recomended_repo_name": recomended_repo,
            "recomended_repo_image": gravatar ,
            "recomended_repo_description": str(re.sub('<[^<]+?>', '', str(description))).replace('"','').replace("'","")   })

    return result_array


# MAIN
def Get_Recomended_Repos(github_user) :

    results=[]



    if Path("/tmp/last_usr.data-%s.data").exists():
        with open(r"/tmp/last_usr.data-%s.data"  %github_user, "rb") as input_file:
            results = pickle.load(input_file)
        return results

    start = time.time()
    # run your code



    # Load Data and user Repos
    json_response = Load_User_Repos(github_user)

    print((start - time.time(), "Datos Cargados"))

    # For each repo
    num_repos = len(pyjq.all(".[] | .name",  json_response),)
    print(num_repos)
    for i in range(num_repos):

        df, df_backup = Load_Starred_Repos()

        print((start - time.time(), "Load_Starred_Repos done"))

        df = Generate_Tag_Matrix(df)
        print((start - time.time(), "Generate_Tag_Matrix done"))

        # add repo to tag_matrix
        df, repo_names = Enrich_Tag_Matrix(df, json_response, i)
        print((start - time.time(), "Enrich_Tag_Matrix done"))

        # calculate_distance_matrix
        df_dist = Generate_Distance_Matrix(df_backup, df, repo_names)
        print((start - time.time(), "Generate_Distance_Matrix done"))

        # print nearest result
        curren_repo = Get_Closest_Repo(df_dist,df_backup)
        results = results + curren_repo
        print((start - time.time(), "Get_Closest_Repo done"))


    #for i, val in enumerate(results):
    #    results[i]["recomended_repo_description"] = re.sub('<[^<]+?>', '', results[i]["recomended_repo_description"])

    if not Path("/tmp/last_usr.data-%s.data").exists():
        with open(r"/tmp/last_usr.data-%s.data"  %github_user, "wb") as output_file:
            pickle.dump(results, output_file)
    return results
     # All


def Extra_Salida():
    print("EEEEEEEXXXTTRRAA")

    seguir = False
    if seguir:
        df, df_backup = Load_Starred_Repos()
        df = Generate_Tag_Matrix(df)
        # add repo to tag_matrix
        df, repo_names = Enrich_All_Tag_Matrix(df, json_response, i)
        # calculate_distance_matrix
        df_dist = Generate_Distance_Matrix(df_backup, df, repo_names)
        # print nearest result
        Get_Closest_Repo(df_dist)

    print(Get_Recomended_Repos("jaimevalero"))
