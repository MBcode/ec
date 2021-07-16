#mknb2.py adds all the gist/colab w/caching, and working service,  clean&hook up soon
 #cleaning up as mknb.py,  tread 2 as a tag, that I'll rm

#1st cut at a version of mknb.py that can handle sending in(differing)ext info to the new template
 #&right now, just incl the tgy.py gist-mgt which should not only to the post but look up cached gists,returing colab urls

#start to prototype the code to create a NB, that will become a gist; that uses a template but inserts the url to open
# then the UI will open the url for this file, and it won't have to be taken from the nb-url in the nb
# and if it is a gist, can be opened in colab directly; rob liked a rendered gist after suggesting nbpreview
##url = "http://example.com/file.csv"
#dwnurl  = "https://darchive.mblwhoilibrary.org/bitstream/1912/23805/1/dataset-753388_hhq-chlorophyll__v1.tsv"
#dwnurl="https://darchive.mblwhoilibrary.org/bitstream/1912/26532/1/dataset-752737_bergen-mesohux-2017-dissolved-nutrients__v1.tsv"
    #now turn this into a flask service that take the dwnurl

#plan is to inject the url into a template and write it to fn, so a direct link2it can come from the search gui
#print(f'open:{fn}')
#could check then open the NB if there, but might change template4a bit, so wait till settles

#probably better to use: https://github.com/nteract/papermill to inject the url, but maybe not, bc want above naming
# though this could probably execute the whole nb, &the script here could move output to that fn

#base_url = "http://141.142.218.86:8081/notebooks/"  #was when I tested a jupyterhub intemediate;maybe binder friendly too
#make the papermill fncs take
#will mv them below post_gist so they can call that and return the colab-nb vs the testing/jupyterhub one

#=original gist code: ;now only testing, rm-soon
def tpg(fn="https/darchive.mblwhoilibrary.org_bitstream_1912_26532_1_dataset-752737_bergen-mesohux-2017-dissolved-nutrients__v1.tsv.ipynb"): #test
    r=post_gist(fn)
    print(r)
#==will replace this w/tgy.py code, that includes finding a fn in the gitsts, vs remaking it
import os
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
        gist_api.create_gist(file_name=fn)
        #could look up url, but find should do it, also makes sure it's there/in a way
        fcu = find_gist(fn)
        return fcu

def update_gist(fn): #might come into play later
    return gist_api.update_gist(file_name=fn)

# Get a list of GISTs
gist_list = gist_api.get_gists()
g=gist_list #could get this in each fnc that needs it, or leave it global

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
    return 'https://colab.research.google.com/gist/MBcode/' + gist_id + "/" + fn

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
    for gn in range(len(g)):
        fn=gist_fn(g[gn])
        if(ffn == fn):
            gist_id = (g[gn]['id'])
            cu = colab_url(gist_id,fn)
            return cu
    return Non #don't want2end w/o a ret

#fcu = find_gist(ffn)
#print(f'fn has a nb:{fcu}')

#will need to find a way to post to 'earthcube' gists
#==
#change dwnurl to path for the nb that pagemill makes, so if we see it again, it can just reuse cached version
def dwnurl2fn(dwnurl):
    fn = dwnurl.replace("/","_").replace(":__","/",1) + ".ipynb"
    return fn

#pagemill insert param&run the NB
#def pm(dwnurl, fn):
def pm_nb(dwnurl, ext=None):
    import papermill as pm
    from os import path
    fn=dwnurl2fn(dwnurl)
    if path.exists(fn):
        print(f'reuse:{fn}')
    else:
        pm.execute_notebook(
           'mybinder-read-pre-gist.ipynb', #path/to/input.ipynb',
           fn,  #'path/to/output.ipynb',
           parameters = dict(url=dwnurl, ext=ext)
        )
    #return base_url + fn
    return post_gist(fn)

    #above had problems(on1machine), so have cli backup in case:
#def pm2(dwnurl, fn):
def pm_nb2(dwnurl, ext=None):
    import os
    fn=dwnurl2fn(dwnurl)
    cs=f'papermill mybinder-read-pre-gist.ipynb {fn} -p url ext {dwnurl}'
    print(cs)
    os.system(cs)
    #return base_url + fn
    return post_gist(fn)

def mknb(dwnurl_str,ext=None):
    "url2 pm2gist/colab nb"
    if(dwnurl_str and dwnurl_str.startswith("http")):
        #fn=dwnurl2fn(dwnurl_str) #already done in pm_nb
        r=pm_nb(dwnurl_str, ext)
    else:
        r=f'bad-url:{dwnurl_str}'
    return r

from flask import Flask
app = Flask(__name__)
from flask import request

@app.route('/mknb/') #works, but still some errs in j16-
def mk_nb():
    "make a NoteBook"
    dwnurl_str = request.args.get('url',  type = str)
    print(f'url={dwnurl_str}')
    ext = request.args.get('ext', default = 'None',   type = str)
    print(f'ext={ext}')
    r= mknb(dwnurl_str,ext)
    return r

if __name__ == '__main__':
    import sys
    if(len(sys.argv)>1):
        dwnurl_str = sys.argv[1]
        if(len(sys.argv)>2):
            ext=sys.argv[2]
        else:
            ext=None
        r=mknb(dwnurl_str, ext) #or trf.py test, that will be in ipynb template soon
        print(r)
#this works, incl pm&gist caches, &now flask works too 
#remember diff btw dwnurl_str, filename-path, &filename alone, &what gets compared to find_gist
