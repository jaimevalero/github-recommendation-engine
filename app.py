from flask import request , Flask, render_template,send_from_directory , jsonify, request,redirect
import jinja2
from jinja2.ext import with_
import requests
import json
from werkzeug.local import Local
from flask import Blueprint, abort
import  get_repos
import load_user

app = Flask(__name__,  static_url_path='/Users/jaimevalerodebernabe/git/github-recommendation-engine/views')
print ("Locality Starting: ")

loc = Local()
loc.static_df, loc.static_df_backup , loc.df_stared_descriptions = get_repos.Load_Starred_Repos()
loc.static_df = get_repos.Generate_Tag_Matrix(loc.static_df)
print ("Locality Started: ")

@app.route('/')
def hello():
    return redirect("views/index.html", code=302)

# Simple api
@app.route('/api/v1/labels/reccomendations')
@app.route('/api/latest/labels/reccomendations')
def get_labels_reccomendations():
    rec_array = {}
    return rec_array
    
@app.route('/api/latest/user/<github_user>/reccomendations')
@app.route('/api/v1/user/<github_user>/reccomendations')
def get_user_reccomendations(github_user):
    busqueda=github_user
    all_results = load_user.Get_Stared_Repos(busqueda,loc)
    print("all_results", all_results)
    rec_array = all_results
    return rec_array

@app.route('/char/<view>')
def char_view(view):
    busqueda = request.args.get('busqueda' , 'jaimevalero')

    templateLoader = jinja2.FileSystemLoader( searchpath=['./views'] )
    templateEnv    = jinja2.Environment( loader=templateLoader , extensions=['jinja2.ext.with_','chartkick.ext.charts'])
    template       = templateEnv.get_template( "char.html" )

    all_results = {}
    print("detectado char")
    all_results = load_user.Get_Stared_Repos(busqueda,loc)
    print("all_results", all_results)
    try :
       return template.render( all_results = all_results)
    except Exception:
       print ('cannot open', Exception)



@app.route('/views/js/<view>')
@app.route('/views/css/<view>')
@app.route('/views/<view>')
def default_view(view):

    # Load Jinja environment
    if "css"  in view  :
        print ("DETECTADO CSSS!!!", view)
        templateLoader = jinja2.FileSystemLoader( searchpath=['/Users/jaimevalerodebernabe/git/github-recommendation-engine/views/css'] )
        templateEnv = jinja2.Environment( loader=templateLoader , extensions=['jinja2.ext.with_'])
        template = templateEnv.get_template( view )
        return template.render(  )


    if "js"   in view  :
        templateLoader = jinja2.FileSystemLoader( searchpath=['/Users/jaimevalerodebernabe/git/github-recommendation-engine/views/js'] )
        templateEnv = jinja2.Environment( loader=templateLoader , extensions=['jinja2.ext.with_'])
        template = templateEnv.get_template( view )
        print ("DETECTADO JS!!!", view)
        return template.render( )


    busqueda = request.args.get('busqueda' , 'jaimevalero')

    templateLoader = jinja2.FileSystemLoader( searchpath=['./views'] )
    templateEnv    = jinja2.Environment( loader=templateLoader , extensions=['jinja2.ext.with_','chartkick.ext.charts'])
    template       = templateEnv.get_template( "char.html" )

    all_results = {}
    all_results = load_user.Get_Stared_Repos(busqueda,loc)
    print("all_results", all_results)
    try :
       return template.render( all_results = all_results)
    except Exception:
       print ('cannot open', Exception)

if __name__ == "__main__" :

    app.debug = True
    app.run(host="0.0.0.0",  port=80)
