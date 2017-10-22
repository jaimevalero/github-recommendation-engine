from flask import request , Flask, render_template,send_from_directory , jsonify, request,redirect
import jinja2
from jinja2.ext import with_
import requests
import json
import csv
import urllib
import subprocess
import os
#import logging, logging.config, yaml
#import webservices
import os
from flask import jsonify
import pickle


#import predict
import  get_repos

#from pymemcache.client.base import Client
#client = Client(
#    ('127.0.0.1', 11211)
#)

####### LOG
#logging.config.dictConfig(yaml.load(open('logging.conf')))
#logfile    = logging.getLogger('file')
#logconsole = logging.getLogger('console')
#logfile.debug("Debug FILE")
#logconsole.debug("Debug CONSOLE")
####### End of LOG

app = Flask(__name__,  static_url_path='/Users/jaimevalerodebernabe/git/github-recommendation-engine/views')


@app.route('/')
def hello():
    #logfile.info("raiz")
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


        #return app.send_static_file(("/Users/jaimevalerodebernabe/git/github-recommendation-engine/views/%s" % view))
    if "js"   in view  :
        templateLoader = jinja2.FileSystemLoader( searchpath=['/Users/jaimevalerodebernabe/git/github-recommendation-engine/views/js'] )
        templateEnv = jinja2.Environment( loader=templateLoader , extensions=['jinja2.ext.with_'])
        template = templateEnv.get_template( view )
        print ("DETECTADO CSSS!!!", view)
        return template.render( )

        #return app.send_static_file(("/Users/jaimevalerodebernabe/git/github-recommendation-engine/html/%s" % view))

    templateLoader = jinja2.FileSystemLoader( searchpath=['/Users/jaimevalerodebernabe/git/github-recommendation-engine/views'] )
    templateEnv = jinja2.Environment( loader=templateLoader , extensions=['jinja2.ext.with_'])
    template = templateEnv.get_template( view )


    resultados = dict([])
    busqueda = request.args.get('busqueda' , 'no_busqueda')
    #size = request.args.get('size' , '15')
    #logfile.info('%s] [%s] [%s' % (request.environ['REMOTE_ADDR'],view,busqueda))

    results = get_repos.Get_Recomended_Repos(busqueda)
    config =  { "results" : results }
    # Prework


    resultados["config"  ]    = json.dumps( config  )

    print("RESULTADOS" ,resultados["config"  ])


    try :
       #salida = template.render( config     = resultados["config"]  )
       return template.render( config     = resultados["config"]  )


    except Exception:
       #logfile.error('Cannos open %s %s %s' % (view,Exception,busqueda))
       print ('cannot open', Exception)

if __name__ == "__main__" :

    #app.logger.addHandler(handler)
    app.debug = True
    app.run(host="0.0.0.0")
