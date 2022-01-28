
import pandas as pd
from pathlib import Path
import requests
import get_repos
import json
import pyjq
import os
import pickle
import numpy as np
import time
import operator
import gzip
import _pickle as cPickle


def Load_User_Directory(df, num_users_to_read):
    """ Load a dataframe with the tags of users given a user directory.

    Keyword arguments:
    df -- DataFrame to load the tags for each user
    num_users_to_read -- Number of user to load (-1 to load all users in the directory)
    """
    #
    NUMBER_OF_USERS=17461
    #
    #my_file = Path("Users_Tag_Matrix.data.gz")

    my_file = Path("Users_Tag_Matrix.data.gz")
    if my_file.exists():
        #with open(r"Users_Tag_Matrix.data", "rb") as input_file:
        #    df = pickle.load(input_file)
        with gzip.GzipFile(r"Users_Tag_Matrix.data.gz", "rb") as input_file:
            df = cPickle.load( input_file)

        if df.shape[0] == NUMBER_OF_USERS :
            print("Loaded 17461 users", df.shape )
            return df
    #
    USER_FILES_PATH="scripts/files/users"
    try: 
        github_user_list = os.listdir(USER_FILES_PATH)
    except:
        github_user_list = []
        
    if num_users_to_read == -1 : num_users_to_read = len(github_user_list)
    #
    for i in range(num_users_to_read):
        #print ("Extracting: ", github_user_list[i], i)
        if github_user_list[i]  in df.index :
            #print ("Already parsed: " ,  github_user_list[i])
            continue
        if i <= len(github_user_list)  :
            # For each user, we load the json file
            try:
                json_response = Load_User_File(github_user_list[i])
            except Exception: continue
            if json_response is None : print ("Error -1 json not loaded ",  github_user)
            df = Get_User_Tags(df, json_response, -1, github_user_list[i])
    #
    print("Size: ",df.shape , len(github_user_list[:num_users_to_read]) )
    df.fillna(0, inplace=True)
    #
    #with open(r"Users_Tag_Matrix.data", "wb") as output_file:
        #pickle.dump(df, output_file)

    with gzip.GzipFile(r"Users_Tag_Matrix.data.gz", "wb") as output_file:
        cPickle.dump(df, output_file)
    #
    return df

def Load_User_File(github_user):
    """
    Load the contents of a JSON file
    Keyword arguments:
    github_user -- name of the file in the form <username>.json
    """
    GITHUB_USER_PATH= "scripts/files/users/%s" % github_user
    my_file = Path(GITHUB_USER_PATH)
    # Are results cached ?
    if my_file.exists():
        print ("Cached : ", GITHUB_USER_PATH)
        with open( GITHUB_USER_PATH, "r") as input_file:
            json_response = json.load(input_file)
        return json_response

def Get_User_Tags(df, json_response, i, github_user):
    """
    Calculate the tags for a user.

    """
    all_repos_tags = pd.DataFrame(0, columns=df.columns, index=pyjq.all(".[] | .name", json_response))

    num_repos = len(pyjq.all(".[] | .name",  json_response))
    #
    new_element = pd.DataFrame(0, np.zeros(1), columns =df.columns)
    tags = {}
    #
    for i in range(num_repos):
        repo_names       = pyjq.all(".[%s] | .name"        % i,  json_response)
        repo_languages   = pyjq.all(".[%s] | .language"    % i,  json_response)
        repo_description = pyjq.all(".[%s] | .description" % i,  json_response)
        repo_topics      = pyjq.all(".[%s] | .topics"      % i,  json_response)

        #
        # print (repo_names,repo_languages,repo_languages,repo_topics)
        #
        # We have two structure:
        #
        # all_repos_tags = a dataframe with a row per repo with values [0,1]
        # new_element = One row dataframa with the sum of frecuencies of all repos.
        reponame_lower = repo_names[0].lower()
        all_repos_tags.loc[reponame_lower] = 0

        if repo_description[0] is None: repo_description = ['kk']
        if repo_languages[0]   is None: repo_languages   = ['kk']
        if repo_topics[0]      is None: repo_topics      = ['kk']
        #
        try:  repo_names[0]       = repo_names[0].lower()
        except Exception: pass
        try:  repo_languages[0]   = repo_languages[0].lower()
        except Exception: pass
        try:  repo_description[0] = repo_description[0].lower()
        except Exception: pass
        try:  repo_topics[0]      = repo_topics[0].lower()
        except Exception: pass
        #
        # Avoid this names because of are substring of another tag ()
        COLUMNS_TO_SKIP=["java" , "c"]
        if repo_languages[0] in df.columns :
            new_element[repo_languages[0]] += (i+1)
            tags[repo_languages[0]] = 0
            all_repos_tags.loc[reponame_lower][repo_languages[0]] = 1

            print(" Log Added tag 1 : ", (i+1)," " ,repo_names[0] ," " , repo_languages[0])
        for column in df.columns:
            if column in COLUMNS_TO_SKIP : continue
            if column in repo_topics[0] :
                new_element[column] += (i+1)
                all_repos_tags.loc[reponame_lower][column] = 1
                tags[column] = 0
                print(" Log Added tag 2 : ", (i+1)," " ,repo_names[0] ," " , column)
            else:
                if len(column) > 4 :
                    if column in repo_names[0] or column.replace("-"," ") in repo_names[0]:
                        print(" Log Added tag 3 : ", (i+1)," " ,repo_names[0] ," " , column)
                        new_element[column] += (i+1)
                        all_repos_tags.loc[reponame_lower][column] = 1
                        tags[column] = 0
                    else :
                        if column in repo_description[0] or column.replace("-"," ") in repo_description[0]:
                            print(" Log Added tag 4 : ", (i+1)," " ,repo_names[0] ," " , column)
                            new_element[column] += (i+1)
                            all_repos_tags.loc[reponame_lower][column] = 1
                            tags[column] = 0
        # end range repos
    print(" Log new_element.shape: ", new_element.shape , " github_user:", github_user)
    #
    total=new_element.iloc[0].sum()
    #print(tags)
    if total != 0 :
        for i in tags  :
            if new_element[i].iloc[0] != 0 :
                new_element[i] =  ( new_element[i].iloc[0]/total)
                #print (i , new_element[i].iloc[0] )
        #

    try:
        all_repos_tags['repos'] = all_repos_tags['Unnamed: 0']
        del all_repos_tags['Unnamed: 0']
        all_repos_tags = all_repos_tags.set_index('repos')
    except Exception:
        pass

    new_element['names']=github_user
    new_element = new_element.set_index(new_element.names)
    del(new_element['names'])
    #
    df = pd.concat([df, new_element])
    print("Added : ", github_user ,df.shape)
    return df, all_repos_tags

def Load_Initial_data():
    """
       Load common data structures
       Keyword arguments:
       df -- DataFrame to load the tags for each user
       df_tags -- Dataframe with the tag list
    """
    # Load
    df_tags       = get_repos.Generate_Tag_Matrix(pd.DataFrame())
    df            = pd.DataFrame(columns = df_tags.columns)
    df = Load_User_Directory(df, -1)

    my_file = Path("Users_Tag_Matrix.data")
    if my_file.exists():
        with open(r"Users_Tag_Matrix.data", "rb") as input_file:
            df = pickle.load(input_file)
    return df_tags, df

def Get_User_Favorites(dict_repos, neighbour_user, correlation_factor):
    fname="scripts/files/starred/%s" % neighbour_user.replace(".json","")
    with open(fname) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    for i in content :
        try:  dict_repos[i] += correlation_factor
        except Exception: dict_repos[i] = correlation_factor
    return dict_repos


def Reduce_Tag_Ponder_Matrix(df,github_user,all_repos_tags):
    """
    Remove github user magnitudes
    """

    otro = pd.DataFrame(index=df.index)
    for column in df.columns :
        if df.loc[github_user][column] > 0 :
            otro[column] = df[column]

    df = otro
    df = df[(df.T != 0).any()]

    otro = pd.DataFrame(columns = df. columns , index=all_repos_tags.index)
    for column in df.columns:
        otro[column] = all_repos_tags[column]

    all_repos_tags = otro

    return df,all_repos_tags


def Calculate_Nearest_Neighbours(df,github_user):
    # Temp Dataframe
    user = pd.DataFrame(index=df.index)
    user["total"] = 0
    # Substract the value of the user dimensions, for each columns
    for column in df.columns :
        df[column] -= df.loc[github_user][column]
        # We calculate the euclidean distance, respect 0,0....,0, the github_user cordinates
        user["total"] +=  (df[column] ** 2)
    user["total"] = user["total"] ** 0.5
    # Number of NNs
    neighbours_number = round(2*df.shape[0]**0.5)+1
    users = user["total"].sort_values().head(neighbours_number+1).tail(neighbours_number)
    # The close to 0 the distance for a given user, the more weight for that user.
    # We do that by : Weight(given_user) = Inverse(distance(github_user,given_user))
    users = 1/users
    # We list all the repos voted for this user, multiplied for the Weight for that user
    dict_repos={}
    for neighbour_user in users.index :
        correlation_factor=users.loc[neighbour_user]
        dict_repos=Get_User_Favorites(dict_repos, neighbour_user, correlation_factor)
    sorted_dict_repos = sorted(dict_repos.items(), key=operator.itemgetter(1))
    return sorted_dict_repos

def Enrich_Stared_Descriptions(stared_repos, df_stared_descriptions):
    dict_stared_descriptions = {}
    print(" Log Entering Enrich_Stared_Descriptions")
    print(" Log Entering Enrich_Stared_Descriptions2", stared_repos, df_stared_descriptions.shape)
    print(" Log Entering Enrich_Stared_Descriptions3", df_stared_descriptions.shape.index)
    for repo in stared_repos :
        repo = repo.replace("https://github.com/","")
        try:
            print(" Log processiing2", repo)
            dict_stared_descriptions[repo] = df_stared_descriptions.loc[repo].to_dict()
            print(" Log Enrich_Stared_Descriptions" , df_stared_descriptions.loc[repo].to_dict())
            print(" Log Enrich_Stared_Descriptions2", dict_stared_descriptions[repo])
        except Exception:
            continue
  #  print("dict_stared_descriptions", dict_stared_descriptions)

    return dict_stared_descriptions

# Main
####### NUEVO
def Get_Stared_Repos(github_user,loc) :
    print("Log Get_Stared_Repos")
    print("Log Get_Stared_Repos", github_user, loc)
    stared_repos = []
    stared_tags  = {}
    dict_stared_descriptions = {}
    sorted_dict_repos ={}
    start = time.time()
    results = []
    all_results = {}
    all_repos_tags = pd.DataFrame()
    df_reduced = pd.DataFrame()
    # github_user = "rubengarciacarrasco"

    ALL_RESULTS_PATH= "/tmp/cache-all_results-%s.tmp" % github_user
    print((start - time.time()), "get_repos.Load_User_Repos")
    my_file = Path(ALL_RESULTS_PATH)


    # Are results cached ?
    if my_file.exists():
        print ("Cahed : ", ALL_RESULTS_PATH)
        with open( r"/tmp/cache-all_results-%s.tmp" % github_user, "rb") as input_file:
            all_results = pickle.load(input_file)
        return all_results

    # Query github for the user
    json_response = get_repos.Load_User_Repos(github_user)
    num_repos = len(pyjq.all(".[] | .name", json_response))

    df_tags, df = Load_Initial_data()
    print((start - time.time()), "Load_Initial_data ")

    # Add user
    df, all_repos_tags = Get_User_Tags(df, json_response, 1000, github_user)
    print((start - time.time()), "Get_User_Tags")

    df,all_repos_tags = Reduce_Tag_Ponder_Matrix(df,github_user,all_repos_tags)

    print((start - time.time()), "Reduce_Tag_Ponder_Matrix")
    print("all_repos_tags", all_repos_tags.shape , all_repos_tags, df.shape)

    stared_tags = df.loc[github_user].to_dict()

    sorted_dict_repos = Calculate_Nearest_Neighbours(df,github_user)
    print((start - time.time()), "Calculate_Nearest_Neighbours")

    #print ("sorted_dict_repos",sorted_dict_repos)
    for repo in range (min(24,len(sorted_dict_repos))) :
        #print ("https://github.com/%s" % (list(sorted_dict_repos)[-repo-1][0]), list(sorted_dict_repos)[-repo-1][1] )
        stared_repos.append("https://github.com/%s" % (list(sorted_dict_repos)[-repo-1][0]))

    print((start - time.time()), "Before enrich Enrich_Stared_Descriptions", stared_repos)
    print((start - time.time()), "Before enrich Enrich_Stared_Descriptions", loc.df_stared_descriptions)

    dict_stared_descriptions = Enrich_Stared_Descriptions(stared_repos, loc.df_stared_descriptions)

    # Change df and reduce it
    df = loc.static_df.copy(deep=True)

    for column in all_repos_tags :
        df_reduced[column] = df[column]

    print("df_reduced", df_reduced.shape)

    for i in range(num_repos):
        tags_cloud = []
        #df        = loc.static_df.copy(deep=True)
        df= df_reduced.copy(deep=True)
        df_backup = loc.static_df_backup.copy(deep=True)
        repo_names = pyjq.all(".[%s] | .name" % i, json_response)
        repo_names[0] = repo_names[0].lower()

        print("Before concat i", i ,df.shape)
        #all_repos_tags.to_csv("kk-all_repos_tags.csv")
        df = pd.concat([df, all_repos_tags.iloc[i:i+1]])
        print("After concat i", i ,df.shape)

        # calculate_distance_matrix
        df_dist = get_repos.Generate_Distance_Matrix(df_backup, df, repo_names)
        print((start - time.time(), "Generate_Distance_Matrix done"),df_backup.shape, df.shape , len(repo_names) )

        # Case repo without labels
        if df_dist is None: continue

        # print nearest result
        #df_reduced.to_csv("kk-df_reduced.csv")
        curren_repo = get_repos.Get_Closest_Repo(
            df_dist,
            df_backup,
            df,
            [tag for tag in df.columns if df.iloc[-1][tag] != 0 and tag != 'Unnamed: 0'] )
        results = results + curren_repo
        print((start - time.time(), "Get_Closest_Repo done"))

    print ("Generando all results")
    all_results = {
        "busqueda" : github_user,
        "stared_repos": stared_repos,
        "stared_tags": stared_tags,
        "dict_stared_descriptions": dict_stared_descriptions,
        "results": results }

    with open(ALL_RESULTS_PATH, "wb") as output_file:
        pickle.dump(all_results, output_file)

    #with open( "last_response.json" , "w") as output_file:
    #    json.dump(all_results, output_file)

    return all_results

# ('apex/up', 905), ('goreleaser/goreleaser', 916), ('tonybeltramelli/pix2code', 922), ('kubernetes/kompose', 941), ('google/python-fire', 951), ('cockroachdb/cockroach', 964), ('kailashahirwar/cheatsheets-ai', 970), ('moby/moby', 974), ('torvalds/linux', 991), ('zeit/hyper', 991), ('c-bata/go-prompt', 997), ('jlevy/the-art-of-command-line', 997), ('ansible/ansible-container', 1010), ('gravitational/teleport', 1014), ('requests/requests', 1037), ('localstack/localstack', 1043), ('google/grumpy', 1049), ('bcicen/ctop', 1062), ('serverless/serverless', 1083), ('golang/dep', 1089), ('dgraph-io/badger', 1108), ('avelino/awesome-go', 1118), ('prometheus/prometheus', 1137), ('kubernetes/kubernetes', 1158), ('openfaas/faas', 1158), ('cncf/landscape', 1160), ('froala/design-blocks', 1164), ('go-ego/riot', 1204), ('kubernetes/kops', 1204), ('mholt/caddy', 1210), ('aksakalli/gtop', 1212), ('spf13/cobra', 1233), ('open-guides/og-aws', 1252), ('envoyproxy/envoy', 1256), ('GoogleCloudPlatform/distroless', 1256), ('jwasham/coding-interview-university', 1264), ('pingcap/tidb', 1264), ('vahidk/EffectiveTensorflow', 1310), ('donnemartin/system-design-primer', 1314), ('kubernetes/minikube', 1327), ('tensorflow/tensorflow', 1348), ('aymericdamien/TensorFlow-Examples', 1419), ('GoogleChrome/puppeteer', 1504), ('mr-mig/every-programmer-should-know', 1590), ('istio/istio', 1665), ('ansible/awx', 1688)]
