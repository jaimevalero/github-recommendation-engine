import pandas as pd
import os
import sys
import requests
import json
from   requests.auth import HTTPBasicAuth
import pyjq


def Load_Starred_Repos() :
  df = pd.DataFrame()
  df = pd.read_csv('TopStaredRepositories.csv')
  df = df.dropna(subset=['Tags'], how='all')
  df['Url'] = "http://github.com/" + df['Username'] + "/" +df['Repository Name']
  df['Tags'] = df['Tags'] + ","
  df.to_csv("clean_TopStaredRepositories.csv")
  df        = pd.read_csv('clean_TopStaredRepositories.csv')
  df_backup = pd.read_csv('clean_TopStaredRepositories.csv')
  return df, df_backup

def Generate_Tag_Matrix(df):
  # Generate tag list
  mergedlist = []
  for i in df['Tags'].dropna().str.split(","): mergedlist.extend(i)
  tags = sorted(set(mergedlist))
  #
  for tag in tags:
    df[tag] = 0
    df.loc[df['Tags'].str.contains(tag+","),tag] = 1
  #
  just_dummies = pd.get_dummies(df['Language'])
  df = pd.concat([df, just_dummies], axis=1)
  # Remove columns not needed
  COLUMNS_TO_REMOVE_LIST = [ 'Username','Repository Name','Description','Last Update Date','Language','Number of Stars','Tags','Url', 'Unnamed: 0']
  for column in COLUMNS_TO_REMOVE_LIST: del df[column]
  df.columns = df.columns.str.lower()
  #
  return df

def Enrich_Tag_Matrix(df,json_response,i):
    repo_names       = pyjq.all(".[%s] | .name"        %i,  json_response )
    repo_languages   = pyjq.all(".[%s] | .language"    %i,  json_response )
    repo_description = pyjq.all(".[%s] | .description" %i,  json_response )
    repo_topics      = pyjq.all(".[%s] | .topics"      %i,  json_response )
    #

    new_repo_index = df.index.max() + 1
    df.loc[new_repo_index] = 0

    print (repo_names , repo_languages, repo_description , repo_topics, i,new_repo_index)
    #
    for i in ( repo_languages + repo_description[0].split() + list(repo_topics[0]) ) :
        if i.lower()  in df.columns :
            if i : df[i.lower()].loc[new_repo_index] = 1

    #for column in df.columns :
    #  if df[column].loc[new_repo_index] > 0 :
    #    print ( column  )
    #

    return df

def Load_User_Repos(github_user):
    PERSONAL_TOKEN = "ac995cdbc4e65c85609434538bd8a135d4c933d9"
    url     = 'https://api.github.com/users/%s/repos' % github_user
    headers = { 'content-type': 'application/json',
                'Accept-Charset': 'UTF-8' ,
                'Accept' : 'application/vnd.github.mercy-preview+json' }
    r                = requests.get(url,  headers=headers , auth=HTTPBasicAuth('jaimevalero', PERSONAL_TOKEN))
    return r.json()


os.chdir("/Users/jaimevalerodebernabe/git/github-recommendation-engine")

#MAIN

# Load Data and user Repos
df, df_backup = Load_Starred_Repos()
json_response = Load_User_Repos(github_user="jaimevalero")

# Generate Tag Matrix
df = Generate_Tag_Matrix(df)
# For each repo
i=1
df = Enrich_Tag_Matrix(df,json_response,i)

#add repo to tag_matrix
#calculate_distance_matrix
#print nearest result


print(df)
