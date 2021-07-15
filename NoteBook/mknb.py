#start to prototype the code to create a NB, that will become a gist; that uses a template but inserts the url to open
# then the UI will open the url for this file, and it won't have to be taken from the nb-url in the nb
# and if it is a gist, can be opened in colab directly; rob liked a rendered gist after suggesting nbpreview
##url = "http://example.com/file.csv"
#dwnurl  = "https://darchive.mblwhoilibrary.org/bitstream/1912/23805/1/dataset-753388_hhq-chlorophyll__v1.tsv"
#dwnurl="https://darchive.mblwhoilibrary.org/bitstream/1912/26532/1/dataset-752737_bergen-mesohux-2017-dissolved-nutrients__v1.tsv"
    #now turn this into a flask service that take the dwnurl
#fn = dwnurl.replace("/","_").replace(":__","/",1) + ".ipynb"
#plan is to inject the url into a template and write it to fn, so a direct link2it can come from the search gui
#print(f'open:{fn}')
#could check then open the NB if there, but might change template4a bit, so wait till settles

#probably better to use: https://github.com/nteract/papermill to inject the url, but maybe not, bc want above naming
# though this could probably execute the whole nb, &the script here could move output to that fn

base_url = "http://141.142.218.86:8081/notebooks/"

def pm(dwnurl, fn):
    import papermill as pm
    pm.execute_notebook(
       'mybinder-read-pre-gist.ipynb', #path/to/input.ipynb',
       fn,  #'path/to/output.ipynb',
       parameters = dict(url=dwnurl)
    )
    return base_url + fn

    #above had problems(on1machine), so have cli backup in case:
def pm2(dwnurl, fn):
    import os
    cs=f'papermill mybinder-read-pre-gist.ipynb {fn} -p url {dwnurl}'
    print(cs)
    os.system(cs)
    return base_url + fn

#once service below working, also add mk the gist w/: req_create_gist.py but make sure the url w/it's hash gets returned
# will also need to be able to find this gist given the dwnlink, to not reimpliment, so might have2do a gist search,
# but exmpl already gives a listing of all of them, so look for the fn part&cmp
#via, some setup then:
def post_gist(fn):
    import requests
    import json
    import os
    from pathlib import Path
    GITHUB_API="https://api.github.com"
    API_TOKEN=os.getenv('gist_token')
    url=GITHUB_API+"/gists"
    headers={'Authorization':'token %s'%API_TOKEN}
    params={'scope':'gist'}
    txt = Path(fn).read_text()  #should incl full output of papermil run w/dwnload url param
    fn_=fn.replace("https/","") #filepath2filename only  #also4 http only  #might change description 
    payload={"description":"GIST created by py code","public":True,"files":{fn_:{"content":txt}}}
    res=requests.post(url,headers=headers,params=params,data=json.dumps(payload))
    #also a way2go through present gists, if had2find if it already exists
    return res #might want to(instead)ret&save gist url

def tpg(fn="https/darchive.mblwhoilibrary.org_bitstream_1912_26532_1_dataset-752737_bergen-mesohux-2017-dissolved-nutrients__v1.tsv.ipynb"): #test
    r=post_gist(fn)
    print(r)

#works in tp2.py
#pm2(dwnurl, fn)

def mknb(dwnurl_str):
    if(dwnurl_str and dwnurl_str.startswith("http")):
        fn = dwnurl_str.replace("/","_").replace(":__","/",1) + ".ipynb"
        r=pm(dwnurl_str, fn)
    else:
        r=f'bad-url:{dwnurl_str}'
    return r

from flask import Flask
from markupsafe import escape
app = Flask(__name__)

@app.route('/mknb/<dwnurl>')
def mk_nb(dwnurl):
    "grep jsonld, get as html"
    dwnurl_str=escape(dwnurl)
    #fn = dwnurl_str.replace("/","_").replace(":__","/",1) + ".ipynb"  #dwnloadURL2filePath it's saved in, ;almost as sep fnc, 
    #r=pm(dwnurl_str, fn)                                                #then could call from pm-fncs &only take 1arg
    r= mknb(dwnurl_str)
    return r

if __name__ == '__main__':
    import sys
    if(len(sys.argv)>1):
        dwnurl_str = sys.argv[1]
        r=mknb(dwnurl_str)
        print(r)