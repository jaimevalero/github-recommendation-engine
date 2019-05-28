import pandas as pd
from pathlib import Path
import requests
from requests.auth import HTTPBasicAuth
import pyjq
from scipy.spatial import distance
from scipy.spatial.distance import squareform, pdist
import pickle
import time
import re
import json
import numpy as np



def Load_Starred_Repos():
    df = pd.DataFrame()
    df = pd.read_csv('TopStaredRepositories.csv')

    df['Url'] = "http://github.com/" + \
        df['Username'] + "/" + df['Repository Name']
    df['Tags'].fillna("", inplace=True)
    df['Tags'] = df['Tags'] + ","
    df.to_csv("clean_TopStaredRepositories.csv")
    df = pd.read_csv('clean_TopStaredRepositories.csv')

    df_stared_descriptions = pd.read_csv("stared-descriptions.csv")
    df_stared_descriptions = df_stared_descriptions.set_index(['repo'])

    df['Language'] = df.loc[:, 'Language'].str.lower()
    df_backup = df.copy(deep=True)
    return df, df_backup , df_stared_descriptions


def Load_User_Repos(github_user):
    GITHUB_USER_PATH= "/tmp/cache-github_user-%s.tmp" % github_user
    my_file = Path(GITHUB_USER_PATH)
    # Are results cached ?
    if my_file.exists():
        print ("Cached : ", GITHUB_USER_PATH)
        with open( GITHUB_USER_PATH, "r") as input_file:
            results = json.load(input_file)
        return results
    else:
        PERSONAL_TOKEN = "ac995cdbc4e65c85609434538bd8a135d4c933d9"
        url = 'https://api.github.com/users/%s/repos?sort=updated&direction=asc' % github_user
        headers = {'content-type': 'application/json',
                   'Accept-Charset': 'UTF-8',
                   'Accept': 'application/vnd.github.mercy-preview+json'}
        r = requests.get(url,  headers=headers, auth=HTTPBasicAuth(
            "jaimevalero", PERSONAL_TOKEN))
        # Store results
        json_response = r.json()
        # ("json_response" , json_response)
        with open( GITHUB_USER_PATH , "w") as output_file:
            json.dump(json_response, output_file)
        return json_response


def Generate_Tag_Matrix(df):
    my_file = Path("Generate_Tag_Matrix.data")
    if my_file.exists():
        with open(r"Generate_Tag_Matrix.data", "rb") as input_file:
            df = pd.read_pickle(input_file)

        return df
    else:

        # Generate tag list
        mergedlist = []
        df['Description'].fillna("", inplace=True)
        for i in df['Tags'].dropna().str.split(","):
            mergedlist.extend(i)
        tags = sorted(set(mergedlist))
        # Encode languages in single column
        just_dummies = pd.get_dummies(df['Language'])
        for column in just_dummies.columns:
            if column not in df.columns:
                df[column] = just_dummies[column]

        df['Tags'].fillna("", inplace=True)
        for tag in tags:
            if tag not in df.columns:
                df[tag] = 0
            try:
                if len(tag) > 4 :
                    df.loc[df['Repository Name'].str.contains(tag), tag] = 1
                    df.loc[df['Description'].str.contains(tag), tag] = 1
                df.loc[df['Tags'].str.contains(tag + ","), tag] = 1
            except Exception:
                pass
        # Remove columns not needed
        df.set_index(['Repository Name'])
        COLUMNS_TO_REMOVE_LIST = ['', 'Username' ,'Repository Name', 'Description',
                                  'Last Update Date', 'Language', 'Number of Stars', 'Tags', 'Url','Gravatar' ,'Unnamed: 0']
        RARE_TAGS_LIST = [ 'example', 'jupyter notebook ', 'monitor','ava' , 'cs', 'github','algorithms','learn','learning','http' ,'https','alert', 'beego', 'cheatsheet', 'clipboard', 'code-completion', 'commerce', 'contenteditable', 'crawling', 'curriculum', 'datetime', 'definition', 'ecommerce', 'filters', 'flexibility', 'forum', 'gitignore', 'hiring', 'hosts', 'htaccess', 'idioms', 'kanban', 'ligatures', 'logger', 'microblog', 'mobile-first', 'multi-language', 'nonprofits', 'offline-first', 'plotly', 'publishing', 'recyclerview', 'reddit', 'samples', 'scraping', 'shadowsocksr', 'slider', 'statusline', 'tabbar', 'takeover', 'timepicker', 'utils', 'crystal', 'julia', 'activeadmin', 'agera', 'angular-cli', 'anime', 'ant-design', 'awesome-swift', 'bazel', 'bitbar', 'bootstrap-datepicker', 'bootswatch', 'botkit', 'bourbon', 'bower', 'cakephp', 'capistrano', 'certbot', 'clean-code', 'cocos2d', 'cocos2d-x', 'corefx', 'cyclejs', 'deeplearning4j', 'devdocs', 'devise', 'discourse', 'dotfiles', 'dubbo', 'echarts', 'emacs', 'engineering-blogs', 'enzyme', 'faker', 'fastjson', 'fastlane', 'firefox', 'flask', 'gatsby', 'gitlab', 'godot', 'grafana', 'grape', 'graphql-js', 'guzzle', 'hackathon', 'hexo-theme', 'hiring-without-whiteboards', 'howler', 'httpie', 'hubot', 'ijkplayer', 'inferno', 'interviews', 'jekyll', 'jquery-validation', 'jstips', 'kaminari', 'kibana', 'kitematic', 'lazysizes', 'libgdx', 'linux-dash', 'linux-insides', 'lodash', 'luigi', 'marionette', 'mastodon', 'medium-editor', 'mithril', 'mousetrap', 'nightwatch', 'nodemailer', 'normalizr', 'nuklear', 'nylas-mail', 'opencv', 'pelican', 'phabricator', 'phalcon', 'phaser', 'piwik', 'playframework', 'polymer', 'postal', 'postcss', 'postgrest', 'pouchdb', 'powerline', 'preact', 'prefixer', 'protip', 'protobuf', 'quill', 'ramda', 'ratchet', 'react-boilerplate', 'react-component', 'react-sketchapp', 'redash', 'redox', 'redux-form', 'restify', 'roslyn', 'select2', 'selfhosted', 'servo', 'sidekiq', 'sinatra', 'smartcrop', 'spacegray', 'spacemacs', 'spree', 'storybook', 'stylus', 'swagger', 'swagger-ui', 'sweetalert', 'terraform', 'theme-next', 'ui-router', 'ungit', 'vapor', 'vim-go', 'waifu2x', 'webpack-dashboard', 'webtorrent', 'wechat-weapp', 'wekan', 'whiteboard', 'xgboost', 'zxing']



        for column in COLUMNS_TO_REMOVE_LIST + RARE_TAGS_LIST:
            try:
                del df[column]
            except Exception:
                pass

        df.columns = df.columns.str.lower()
        #df.to_csv("Generate_Tag_Matrix.csv")

        with open(r"Generate_Tag_Matrix.data", "wb") as output_file:
            pickle.dump(df, output_file)

    return df


def Reduce_Tag_Matrix(df):
    #with open(r"kk.data", "wb") as output_file:
    #    pickle.dump(df, output_file)
    #with open(r"kk.data", "rb") as input_file:
    #    df = pd.read_pickle(input_file)

    ### Quedarnos solo con las columnas activas
    df_reduced = pd.DataFrame()
    NUM_ELEMENTS=len(df)-1
    #df.iloc[:][NUM_ELEMENTS:].fillna(0, inplace=True)

    print("Start Reduce_Tag_Matrix", df.shape,NUM_ELEMENTS)
    user_repo = df.iloc[NUM_ELEMENTS:]
    #user_repo = df.iloc[-1]
    for column in df.columns :
        existe = user_repo[column].values[0]
        #print("columna", column, existe)
        if existe != 0 : df_reduced[column] = df[column]

    df = df_reduced.copy(deep=True)
    print("End Reduce_Tag_Matrix. dimensions" ,df.shape,df_reduced.shape)

    return df

def Enrich_Tag_Matrix(df, json_response, i, tags_cloud):
    repo_names       = pyjq.all(".[%s] | .name"        % i,  json_response)
    repo_languages   = pyjq.all(".[%s] | .language"    % i,  json_response)
    repo_description = pyjq.all(".[%s] | .description" % i,  json_response)
    repo_topics      = pyjq.all(".[%s] | .topics"      % i,  json_response)
    #
    tags_cloud = []
    #
    #print (repo_names,repo_languages,repo_languages,repo_topics)
    if repo_description[0] is None: repo_description = ['kk']
    if repo_languages[0]   is None: repo_languages = ['kk']
    if repo_topics[0]   is None:    repo_topics = ['kk']
    #
    try:
        repo_names[0]     = repo_names[0].lower()
        repo_languages[0] = repo_languages[0].lower()
        repo_topics[0]    = repo_topics[0].lower()
    except Exception:
        pass
    #
    new_element = pd.DataFrame(0, [df.index.max() + 1], columns=df.columns)
    # Concat new user repo dataframe to stared repos dataframe
    for column in df.columns:
        if column in repo_languages[0] :
            new_element[column] = 1
            tags_cloud.append(column)
        if column in repo_topics[0] :
            new_element[column] = 1
            tags_cloud.append(column)
        else:
            if len(column) > 4 :
                if column in repo_names[0] or column.replace("-"," ") in repo_names[0]:
                    new_element[column] = 1
                    tags_cloud.append(column)
                else :
                    if column in repo_description[0] or column.replace("-"," ") in repo_description[0]:
                        new_element[column] = 1
                        tags_cloud.append(column)
    #
    #print("tags_cloud" ,tags_cloud)
    df = pd.concat([df, new_element])
    return df, repo_names,tags_cloud


def Generate_Distance_Matrix(df_backup, df, repo_names):
    repos = list(df_backup['Username'] + "/" + df_backup['Repository Name'])
    print("Generate_Distance_Matrix repo_names 1",repo_names, len(repos))

    repos.extend(repo_names)
    print("Generate_Distance_Matrix repo_names 2 ",repo_names, len(repos))

    df = Reduce_Tag_Matrix(df)
    if df.shape == (0, 0) : return

    res = pdist(df, 'euclidean')
    squareform(res)
    df_dist = pd.DataFrame(squareform(res), index=repos, columns=repos)
    return df_dist

##### Sacar tags lista repositorios, y del último
def Get_Common_Tags(url,df,df_backup):

    a = int(df_backup.loc[df_backup['Url'] == url , 'Unnamed: 0' ].head(1))
    serie1 = df.iloc[a]
    serie2 = df.tail(1)
    common_tags = []
    for i in df.columns :
        if float(serie1[i]) > 0 and float(serie2[i]) > 0 : common_tags.append(i)
    #if len(common_tags) > 0 :  print("common_tags !!!!!!!!!!!!!!!!!!!!!!!!!!!!",common_tags)
    return common_tags

def Get_Closest_Repo(df_dist,df_backup,df,tags_cloud):
    result_array = []
    i = df_dist.columns[-1]
    df_dist.loc[df_dist[i] == 0, i] = 1000
    min = df_dist[i].min()
    kk = df_dist[i]
    #print(kk[df_dist[i] == min].index, i, min)
    for recomended_repo in (kk[df_dist[i] == min].index[0:30]):
        description = df_backup.loc[df_backup['Url'] == (
            'http://github.com/%s' % recomended_repo), 'Description'].iloc[0]
        gravatar =   df_backup.loc[df_backup['Url'] == (
            'http://github.com/%s' % recomended_repo), 'Gravatar'].iloc[0]
        common_tags_temp = []
        common_tags_temp = Get_Common_Tags( 'http://github.com/%s' % recomended_repo , df , df_backup)
        if len(common_tags_temp) > 0 :
            result_array.append({
                "score": min,
                "user_repo_name": i,
                "user_repo_tags": tags_cloud ,
                "recomended_repo_name": recomended_repo,
                "recomended_repo_image": gravatar ,
                "recomended_repo_description": str(re.sub('<[^<]+?>', '', str(description))).replace('"','').replace("'","")  ,
                "common_tags" : common_tags_temp  })

    return result_array


# MAIN
def Get_Recomended_Repos(github_user,loc) :

    results=[]
    start = time.time()

    # Query cache
    USER_CACHE_FILE="/tmp/last_usr.data-%s.data" % github_user
    if Path( USER_CACHE_FILE ).exists():
        with open( USER_CACHE_FILE, "rb") as input_file:
            results = pd.read_pickle(input_file)
            print((start - time.time(), "Datos cacheados " , "/tmp/last_usr.data-%s.data"  %github_user ))
        return results



    # Load Data and user Repos
    json_response = Load_User_Repos(github_user)

    print((start - time.time(), "Datos Cargados"))

    # For each repo
    num_repos = len(pyjq.all(".[] | .name",  json_response),)
    print(num_repos)
    tags_cloud = []
    for i in range(num_repos):

        df = pd.DataFrame()
        df_backup = pd.DataFrame()
        print((start - time.time(), "Antes bloqueo"))

        df        = loc.static_df.copy(deep=True)
        df_backup = loc.static_df_backup.copy(deep=True)

        print((start - time.time(), "Despues bloqueo"))

        #df, df_backup = Load_Starred_Repos()

        print((start - time.time(), "Load_Starred_Repos done"))

        #df = Generate_Tag_Matrix(df)
        print((start - time.time(), "Generate_Tag_Matrix done"))

        # add repo to tag_matrix
        df, repo_names, tags_cloud = Enrich_Tag_Matrix(df, json_response, i,tags_cloud)
        print((start - time.time(), "Enrich_Tag_Matrix done"))

        # calculate_distance_matrix
        df_dist = Generate_Distance_Matrix(df_backup, df, repo_names)
        print((start - time.time(), "Generate_Distance_Matrix done"))



        # print nearest result
        curren_repo = Get_Closest_Repo(df_dist,df_backup,df,tags_cloud)
        results = results + curren_repo
        print((start - time.time(), "Get_Closest_Repo done"))



    if not Path( USER_CACHE_FILE).exists():
        with open( USER_CACHE_FILE , "wb") as output_file:
            pickle.dump(results, output_file)
        return results
