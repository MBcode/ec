#!/usr/bin/env python3
import ec #mknb2 will all turn utils into services, for eg. pyscript pages
#mknb.py has all the gist/colab w/caching, and working service,  clean&hook up soon

#1st cut at a version of mknb.py that can handle sending in(differing)ext info to the new template
 #&right now, just incl the tgy.py gist-mgt which should not only to the post but look up cached gists,returing colab urls

#start to prototype the code to create a NB, that will become a gist; that uses a template but inserts the url to open
# then the UI will open the url for this file, and it won't have to be taken from the nb-url in the nb
# and if it is a gist, can be opened in colab directly; rob liked a rendered gist after suggesting nbpreview
#dwnurl  = "https://darchive.mblwhoilibrary.org/bitstream/1912/23805/1/dataset-753388_hhq-chlorophyll__v1.tsv"
#dwnurl="https://darchive.mblwhoilibrary.org/bitstream/1912/26532/1/dataset-752737_bergen-mesohux-2017-dissolved-nutrients__v1.tsv"
    #now turn this into a flask service that take the dwnurl

#plan is to inject the url into a template and write it to fn, so a direct link2it can come from the search gui

#used: https://github.com/nteract/papermill to inject the url, &can run it too

#base_url = "http://141.142.218.86:8081/notebooks/"  #was when I tested a jupyterhub intemediate;maybe binder friendly too
#will mv them below post_gist so they can call that and return the colab-nb vs the testing/jupyterhub one

#import urllib.parse #mostly want safe filenames v url's right now, but enough overlap worth using

#=original gist code: ;now only testing, rm-soon
def tpg(fn="https/darchive.mblwhoilibrary.org_bitstream_1912_26532_1_dataset-752737_bergen-mesohux-2017-dissolved-nutrients__v1.tsv.ipynb"): #test
    r=post_gist(fn)
    print(r)
#==will replace this w/tgy.py code, that includes finding a fn in the gitsts, vs remaking it
import os
import json
import csv

def first_str(s):
    r=s.split(' ', 1 )
    return r[0]

useEC=None #"yes"
if useEC:
    AUTH_TOKEN=os.getenv('ec_gist_token') #for when post to earthcube gists, soon
else:
    AUTH_TOKEN=os.getenv('gist_token')

#https://github.com/ThomasAlbin/gistyc
import gistyc

# Initiate the GISTyc class with the auth token
gist_api = gistyc.GISTyc(auth_token=AUTH_TOKEN)

#in mknb called post_gist, could call create_
#def mk_gist(fn):
def post_gist(fn):
    fcu = find_gist(fn)
    if fcu:
        print(f'found saved gist:{fn}')
        return fcu
    else:
        #return gist_api.create_gist(file_name=fn)
        print(f'file_name={fn}')
        gist_api.create_gist(file_name=fn)
        #could look up url, but find should do it, also makes sure it's there/in a way
        fcu = find_gist(fn)
        print(f'found-made-gist:{fcu}')
        return fcu

def update_gist(fn): #might come into play later
    return gist_api.update_gist(file_name=fn)

# Get a list of GISTs
gist_list = gist_api.get_gists()
g=gist_list #could get this in each fnc that needs it, or leave it global
#g=None, just reset in flask app before calling mknb fnc
 #might need to update in other places, maybe even w/in find_gist

def file_ext(fn):
    st=os.path.splitext(fn)
    return st[-1]

def path_leaf(path):
    import ntpath
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def gist_fn(gj):
    return list(gj['files'].keys())[0]

def colab_url(gist_id,fn):
    if useEC:
        return 'https://colab.research.google.com/gist/earthcube/' + gist_id + "/" + fn
    else:
        return 'https://colab.research.google.com/gist/MBcode/' + gist_id + "/" + fn


def htm_url(url): 
    #return f"""<html><head><meta http-equiv = "refresh" content = "0; url={url}" /></head><body><a href={url}>notebook to view your data</a></body></html>"""
    return f"""<html><head><meta http-equiv = "refresh" content = "0; url={url}" /></head><body><a href={url}>nb</a></body></html>"""

def htm_url_(url): #old1before fwd to colab-NB-url
    return f'<html><a href={url}>notebook to view your data</a></html>'

def print_nb_gists(g): #was used before writing find_gist
    for gn in range(len(g)):
        fn=gist_fn(g[gn])
        ft=file_ext(fn)
        if(ft=='.ipynb'):
            print("Gist URL : %s"%(g[gn]['url']))
            #print("GIST ID: %s"%(g[gn]['id']))
            gist_id = (g[gn]['id'])
            print(f'GIST_ID:{gist_id}')
            print(f'fn: {fn}')
            cu = colab_url(gist_id,fn)
            print(f'url: {cu}')
        else:
            print(f'it was of type:{ft}')

#print_nb_gists(g)
#ffn = 'darchive.mblwhoilibrary.org_bitstream_1912_23805_1_dataset-753388_hhq-chlorophyll__v1.tsv.ipynb'

#be able to find a fn w/in the list: g
#def find_gist(ffn):
def find_gist(ffnp):
    ffn=path_leaf(ffnp)
    g = gist_api.get_gists() #was in global but refresh here
    for gn in range(len(g)):
        fn=gist_fn(g[gn])
        if(ffn == fn):
            gist_id = (g[gn]['id'])
            cu = colab_url(gist_id,fn)
            hcu=htm_url(cu)
            return hcu
    return None #don't want2end w/o a ret

#fcu = find_gist(ffn)
#print(f'fn has a nb:{fcu}')

#will need to find a way to post to 'earthcube' gists
#==
#change dwnurl to path for the nb that pagemill makes, so if we see it again, it can just reuse cached version
def dwnurl2fn(dwnurl):
    #fn = dwnurl.replace("/","_").replace(":__","/",1) + ".ipynb"
    #fn = dwnurl.replace("/","_").replace(":__","/",1).replace("?","") + ".ipynb"
    fn = dwnurl.replace("/","_").replace(":__","/",1).replace("?","").replace("#","_") + ".ipynb"
    #fn = dwnurl.replace("/","_").replace(":__","/",1).replace("?","").replace("#","_").replace(" ; ","_") + ".ipynb"
    return fn

#pagemill insert param&run the NB
#def pm(dwnurl, fn):
def pm_nb(dwnurl, ext=None):
    import papermill as pm
    from os import path
    fn=dwnurl2fn(dwnurl)
    if path.exists(fn):
        print(f'reuse:{fn}')
    else: #could use the template.ipynb w/o cached data, if the 1st try w/'mybinder-read-pre-gist.ipynb' fails
        try:
            e = pm.execute_notebook(
               'template.ipynb', #path/to/input.ipynb',
               fn,  #'path/to/output.ipynb',
               parameters = dict(url=dwnurl, ext=ext)
            )
        except:
            print(f'except:{e}') #might have to catch this exception
        print(f'pm:{e}') #might have to catch this exception
    #return base_url + fn
    return post_gist(fn) #htm w/link to colab of the gist

    #above had problems(on1machine), so have cli backup in case:

    #only use above if can keep it from executing, like I do in the other cli calls

def pm_nb3(dwn_url, ext=None, urn=None):
    import os
    from os import path
    dwnurl=dwn_url.strip('/')
    fn=dwnurl2fn(dwnurl)
    if path.exists(fn):
        print(f'reuse:{fn}')
    else:
        if ext:
            sext=ext.replace(" ","_").replace("(","_").replace(")","_").replace(";","_").replace("\n",' ') 
            sext1=first_str(sext)
            print(f'ext:{sext},1:{sext1}')
          # ext_arg=f' -p ext {sext1} '
            ext_arg=f' -p ext "{sext1}" '
        else:
            ext_arg=""
        if urn:
          # urn_arg=f' -p urn {urn} '
            urn_arg=f' -p urn "{urn}" '
        else:
            urn_arg=""
        #cs=f'papermill --prepare-only template.ipynb {fn} -p contenturl {dwnurl} {ext_arg} {urn_arg}'
      # cs=f'papermill --prepare-only template.ipynb {fn} -p url {dwnurl} {ext_arg} {urn_arg}'
        cs=f'papermill --prepare-only template.ipynb {fn} -p url "{dwnurl}" {ext_arg} {urn_arg}'
        print(cs)
        os.system(cs)
    return post_gist(fn)

def pm_q3(q):
    import os
    from os import path
    fn= "q/" + q + ".ipynb"
    if path.exists(fn):
        print(f'reuse:{fn}')
    else:
        cs=f'papermill --prepare-only sparql.ipynb {fn} -p q {q}'
        print(cs)
        os.system(cs)
    return post_gist(fn)

def prepare_only(inp,fn,d):
    import papermill as pm
    import os
    from os import path
    e=None
    #if path.exists(fn):
    #    print(f'reuse:{fn}')
    #else:
    try:
        e = pm.execute_notebook(inp,fn,parameters=d,prepare_only=True)
    except:
        print(f'except:{e}') #might have to catch this exception
    #print(f'pm:{e}') #might have to catch this exception
    #return post_gist(fn) #htm w/link to colab of the gist
    print(f'prepared_ in:{fn}')
    return fn

def pm_c(c):  #sending json via cli is making it loose the quotes
    import os
    from os import path
    print(f'c={c}')
    if not c:
        print("WARN:pm_c w/no collection")
        return ""
    cd=json.loads(c)
    #name = cd.name
    name = cd.get("name")
    if not name:
        name = "note_yet"
    fn= "c/" + name + ".ipynb"
    if path.exists(fn):
        print(f'reuse:{fn}')
    else:
        #cs=f'papermill --prepare-only sparql.ipynb {fn} -p c {c}'
        cs=f'papermill --prepare-only sparql.ipynb {fn} '
        for key in cd:
            val= json.dumps(cd[key]).replace("\'","\"")
            cs2= f" -p {key} '{val}'"
            cs += cs2
        print(cs)
        os.system(cs)
        #prepare_only("sparql.ipynb",fn,c)
    return post_gist(fn)

def pm_dtq(d,q,t):
    import os
    from os import path
    #fn= "c/" + q + ".ipynb"
    fn= "c/" + name + ".ipynb"
    if path.exists(fn):
        print(f'reuse:{fn}')
    else:
        cs=f'papermill --prepare-only sparql.ipynb {fn} -p q {q} -p {URNs} '
        print(cs)
        os.system(cs)
    return post_gist(fn)

def pm_dtq(datasets,tools=None,queries=None):
    import os
    from os import path
    #fn= "c/" + q + ".ipynb"
    fn= "c/" + name + ".ipynb"
    if path.exists(fn):
        print(f'reuse:{fn}')
    else:
        t_args = ( f' -p {tools} ' if tools else "")
        q_args = ( f' -p {queries} ' if queries else "")
        cs=f'papermill --prepare-only sparql.ipynb {fn} -p q {q} -p {datasets} {t_args} {q_args} '
        print(cs)
        os.system(cs)
    return post_gist(fn)

#def pm2(dwnurl, fn):
#def pm_nb2(dwn_url, ext=None):

def mknb(dwnurl_str,ext=None,urn=None):
    "url2 pm2gist/colab nb"
    if(dwnurl_str and dwnurl_str.startswith("http")):
        #fn=dwnurl2fn(dwnurl_str) #already done in pm_nb
        #r=pm_nb(dwnurl_str, ext)
        #r=pm_nb2(dwnurl_str, ext)
        r=pm_nb3(dwnurl_str, ext, urn)
    else:
        r=f'bad-url:{dwnurl_str}'
    return r

from flask import Flask
from flask import request
#from flask_ipban import IpBan
app = Flask(__name__)
#ip_ban = IpBan(ban_seconds=200)
#ip_ban.init_app(app)
#blockip=os.getenv("blockip")
#if blockip:
#    ip_ban.block(blockip)

@app.route('/mknb/') 
def mk_nb():
    "make a NoteBook"
    dwnurl_str = request.args.get('url',  type = str)
    print(f'url={dwnurl_str}')
    ext = request.args.get('ext', default = 'None',   type = str)
    print(f'ext={ext}')
    urn = request.args.get('urn', default = 'None',   type = str)
    print(f'urn={urn}')
    r= mknb(dwnurl_str,ext,urn)
    return r

@app.route('/mkQ/') 
def mk_Q():
    "make a NoteBook"
    q = request.args.get('q',  type = str)
    print(f'q={q}')
    #r= mkQ(q) #just pagemill directly
    r= pm_q3(q)
    return r

@app.route('/mkC/') 
def mk_C():
    "make a NoteBook"
    c = request.args.get('collection',  type = str)
    print(f'c={c}')
    #cj=json.loads(c)
    #r= pm_c(cj)
    print(f'pm_c:{c}')
    r= pm_c(c)
    return r

#start-mknb2
@app.route('/txt_query/') 
def txt_query():
    q = request.args.get('q',  type = str)
    print(f'q={q}')
    r= ec.txt_query_summary(q)
    print(r)
    return r.to_json()

@app.route('/get_graph/') 
def get_graph():
    g = request.args.get('g',  type = str)
    print(f'g={g}')
    r= ec.get_graph(g)
    print(r)
    return r.to_json()

@app.route('/txt_query_csv/') 
def txt_query_csv():
    q = request.args.get('q',  type = str)
    print(f'q={q}')
    r= ec.txt_query_summary(q)
    print(r)
    return r.to_csv(None,encoding='utf-8',lineterminator='\n',index=False,quoting=csv.QUOTE_NONNUMERIC)

@app.route('/get_graph_csv/') 
def get_graph_csv():
    g = request.args.get('g',  type = str)
    print(f'g={g}')
    r= ec.get_graph(g)
    print(r)
    return r.to_csv(None,encoding='utf-8',lineterminator='\n',index=False,quoting=csv.QUOTE_NONNUMERIC)

@app.route('/txt_query_tsv/') 
def txt_query_tsv():
    q = request.args.get('q',  type = str)
    print(f'q={q}')
    r= ec.txt_query_summary(q)
    print(r)
    return r.to_csv(None, sep='\t', encoding='utf-8',lineterminator='\n',index=False,quoting=csv.QUOTE_NONNUMERIC)

@app.route('/get_graph_tsv/') 
def get_graph_tsv():
    g = request.args.get('g',  type = str)
    print(f'g={g}')
    r= ec.get_graph(g)
    print(r)
    return r.to_csv(None, sep='\t', encoding='utf-8',lineterminator='\n',index=False,quoting=csv.QUOTE_NONNUMERIC)

#end-mknb2
#open collection, of sparqlNB-query=q and an array of URNs for the datasets
@app.route('/mkQ2/')  #qry&URN's come in an "[array,of,elts]"
def mk_Q2():
    "make a NoteBook for a collection"
    q = request.args.get('name',  type = str) #suggest: user:collectionName to can be shared/reused easily
    print(f'name={name}')
    q = request.args.get('Qs',  type = str)
    print(f'Qs={Qs}')
    urn = request.args.get('URNs', default = 'None',   type = str)
    print(f'URNs={URNs}')
    #r= mkQ(q) #just pagemill directly
    r= pm_q_d(Qs,URNs)
    return r

#open collection, of sparqlNB-query=q and an array of URNs for the datasets
#dave has large json chunks, which I got him2limit a bit,but will still not scale
@app.route('/mkQ3/')  #qry&URN's come in an "[array,of,elts]"
def mk_Q3():
    "make a NoteBook for a collection"
    q = request.args.get('datasets',  type = str) 
    print(f'data={datasets}')
    q = request.args.get('Qs',  type = str)
    print(f'Qs={queries}')
    urn = request.args.get('URNs', default = 'None',   type = str)
    print(f'tools=={tools}')
    #r= mkQ(q) #just pagemill directly
    r= pm_dtq(datasets,tools,queries)
    return r


@app.route('/logbad/')  #have try/except, so log errors soon, also have 'log' file in NB from wget/etc
def log_bad():
    dwnurl_str = request.args.get('url',  type = str)
    lbs= f'log_bad:url={dwnurl_str}'
    print(lbs) #just in the log for now
    err = request.args.get('error', default = 'None',   type = str)
    if err:
        print(f'error:{err}')
    else:
        err=""
    return err

@app.route('/alive/') 
def alive():
    return """{"alive": "yes"}"""

@app.route('/testj/') 
def testj():
    return """{"id":3098,"uid":"f574baca-6934-40c0-9baf-074c1c9f1336","name":"Sid Down","two_word_name":"Ima Klotz","four_word_name":"Maude L. T. Ford","name_with_initials":"Chris P. Wheatzenraisins","name_with_middle":"Debroah Barrows Upton","first_name":"Lemuel","middle_name":"Marvin","last_name":"Fahey","male_first_name":"Jay","female_first_name":"Veta","prefix":"Mrs.","initials":"PYQ"}"""

@app.route('/txt_query_csv_q/') 
def txt_query_csv_q():
    q = request.args.get('q',  type = str)
    print(f'q={q}')
    fn = f'q/{q}.csv'
    from os.path import exists #can check if cached file there
    if exists(fn):
        return fn
    else:
        r= ec.txt_query_summary(q)
        print(r)
        print(fn)
        r.to_csv(fn,encoding='utf-8',lineterminator='\n',index=False,quoting=csv.QUOTE_NONNUMERIC)
        return fn

@app.route('/get_graph_csv_g/') 
def get_graph_csv_g():
    g = request.args.get('g',  type = str)
    print(f'g={g}')
    fn = f'g/{g}.csv'
    from os.path import exists #can check if cached file there
    if exists(fn):
        return fn
    else:
        r= ec.get_graph(g)
        print(r)
        r.to_csv(fn,encoding='utf-8',lineterminator='\n',index=False,quoting=csv.QUOTE_NONNUMERIC)
        return fn


if __name__ == '__main__':
    import sys
    if(len(sys.argv)>1):
        dwnurl_str = sys.argv[1]
        if(len(sys.argv)>2):
            ext=sys.argv[2]
        else:
            ext=None
        g = gist_api.get_gists() #set the global w/fresh value
        r=mknb(dwnurl_str, ext) #or trf.py test, that will be in ipynb template soon
        print(r)
    else: #w/o args, just to run a service:
        #app.run(host='0.0.0.0', port=8004, debug=True)
        app.run(host='0.0.0.0', port=3031, debug=True)
#this works, incl pm&gist caches, &now flask works too 
#remember diff btw dwnurl_str, filename-path, &filename alone, &what gets compared to find_gist
#dv said he will have in a container, so will need token evn var, and http/s dirs, for now
