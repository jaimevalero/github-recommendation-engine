from flask import request , Flask, render_template,send_from_directory , jsonify, request,redirect
import jinja2
from jinja2.ext import with_
import requests
import json
from werkzeug.local import Local


import  get_repos


app = Flask(__name__,  static_url_path='/Users/jaimevalerodebernabe/git/github-recommendation-engine/views')

loc = Local()

loc.static_df, loc.static_df_backup = get_repos.Load_Starred_Repos()
loc.static_df = get_repos.Generate_Tag_Matrix(loc.static_df)


@app.route('/')
def hello():
    return redirect("views/index.html", code=302)


@app.route('/views/js/<view>')
@app.route('/views/css/<view>')
@app.route('/views/<view>')
def default_view(view):
    print("EXTATICO     " ,view)

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
        print ("DETECTADO CSSS!!!", view)
        return template.render( )


    templateLoader = jinja2.FileSystemLoader( searchpath=['./views'] )
    templateEnv = jinja2.Environment( loader=templateLoader , extensions=['jinja2.ext.with_'])
    template = templateEnv.get_template( view )


    resultados = dict([])
    busqueda = request.args.get('busqueda' , 'octocat')

    results = get_repos.Get_Recomended_Repos(busqueda,loc)

    for i, val in enumerate(results):
      #print ( val)
      json.loads('  { "SEARCH_DECODED" : "%s"  } ' % ( val  ) )


    resultados["config"  ]    = json.loads('  { "SEARCH_DECODED" : "%s"  } ' % ( results  ) )
    print(resultados)

    try :
       return template.render( results     = results , search = busqueda )


    except Exception:
       print ('cannot open', Exception)

if __name__ == "__main__" :

    app.debug = True
    app.run(host="0.0.0.0")
