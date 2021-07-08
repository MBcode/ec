#start to prototype the code to create a NB, that will become a gist; that uses a template but inserts the url to open
# then the UI will open the url for this file, and it won't have to be taken from the nb-url in the nb
# and if it is a gist, can be opened in colab directly; rob liked a rendered gist after suggesting nbpreview
#url = "http://example.com/file.csv"
dwnurl  = "https://darchive.mblwhoilibrary.org/bitstream/1912/23805/1/dataset-753388_hhq-chlorophyll__v1.tsv"
dwnurl="https://darchive.mblwhoilibrary.org/bitstream/1912/26532/1/dataset-752737_bergen-mesohux-2017-dissolved-nutrients__v1.tsv"
    #now turn this into a flask service that take the dwnurl
fn = dwnurl.replace("/","_").replace(":__","/",1) + ".ipynb"
#plan is to inject the url into a template and write it to fn, so a direct link2it can come from the search gui
print(f'open:{fn}')
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

    #above had problems, so try cli too:
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
#txt = Path(fn).read_text()
#payload={"description":"GIST created by python code","public":True,"files":{fn_:{"content":txt}}}
#res=requests.post(url,headers=headers,params=params,data=json.dumps(payload))

#works in tp2.py
#pm2(dwnurl, fn)

from flask import Flask
from markupsafe import escape
app = Flask(__name__)


@app.route('/mknb/<dwnurl>')
def mknb(qry):
    "grep jsonld, get as html"
    dwnurl_str=escape(dwnurl)
    fn = dwnurl_str.replace("/","_").replace(":__","/",1) + ".ipynb"
    r=pm(dwnurl_str, fn)
    return r
