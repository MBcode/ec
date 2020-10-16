#Search main or backup clowder or search3 sparql endpoint(&get all metadata at once)
#ss.py + dev4c.py,  then took sparql part out into sq.py, and call it from this: ss2sq.py
#code below is from the colab NoteBook that I shared awhile ago
# can be more than a shim to get non-auth clowder search
#since it's an API shim/augmentation, will assume called from NB or other code,
 #but as I get html returns could just call it from a txt-box or directly
# for which I will give the qry.py example
# which already falls over to sq.py sparql query, should do that here for /search
#then make sure all output is close/useable for final html search results
#&add something like /cluster to produce the carrot2 clustering results
from flask import Flask
from markupsafe import escape
app = Flask(__name__)
import requests
import json
import os
#./ld holds links to full LinkedData cache

@app.route('/agrep/<qry>')
def agrep(qry):
    "agrep jsonld, get as html"
    qry_str=escape(qry) #tre-agrep is preferred
    #cs=f"agrep -d'^\{' {qry_str} ld/edi/* |sed '/^ld\//s//<p>/'"
    cs=f"getLD.sh {qry_str} "
    htm=os.popen(cs).read()
    #s=os.popen(cs).read()
    #htm= '<html>' + s + '</html>'
    return htm

@app.route('/ag/<qry>')
def ag(qry):
    "grep jsonld, get as html"
    qry_str=escape(qry) 
    cs=f"ag {qry_str} ld/* |sed '/^ld\//s//<p>/'"
    s=os.popen(cs).read()
    htm= '<html>' + s + '</html>'
    return htm

def sq(qry_str):
    #cs=f"python3 sq.py {qry_str}"
    cs=f"python3 sq.py {qry_str}|sed '/^</s//<br></'"
    s=os.popen(cs).read()
    if len(s)<8:
        print("<!--nothing from triplestore backup2grep-->")
        ag(qry_str)
    #return s 
    htm= '<html>' + s + '</html>'
    return htm

@app.route('/search3/<qry>')
def search3(qry):
    "sparql text search"
    qry_str=escape(qry) 
    #cs=f"python3 sq.py {qry_str}"
    #s=os.popen(cs).read()
    #if len(s)<8:
    #    print("<!--nothing from triplestore backup2grep-->")
    #    ag(qry)
    s = sq(qry)
    return s 

@app.route('/search/<qry>')
def search(qry):
    "text search of clowder then sparql if down"
    #was setup to fallback from earthcube to ncsa clowder at one point
    #clowder_key = os.getenv('testkey')
    clowder_key = os.getenv('eckey')
    clowder_host = os.getenv('clowder_host')
    #if not clowder_host:
    #    clowder_host = "https://earthcube.clowderframework.org"
    #    clowder_key = os.getenv('testkey')
    print(clowder_host)
    qry_str=escape(qry) 
    print(qry_str)
    #print(f'host:{clowder_host},qry:{qry_str}')
    ret=" " #shouldn't need to do this
    try:
        r = requests.get(f"{clowder_host}/api/search?query={qry_str}", headers={'X-API-Key': clowder_key})
    except:
        print("<!--exception so used backup-->")
        #ret=search3(qry)
        ret=sq(qry)
    else:
        sc=r.status_code
        ret=f'<!--status-code:{sc}-->'
        print(ret)
        #if r:
        #if(r.status_code == requests.codes.ok):
        if(r.status_code == 200):
            ret = json.dumps(r.json()['results'])
            return ret
        else:
            ret=sq(qry)
    return ret

#qry.py falls over when clowder down to search3, I'd like that try/excpt..to happen here next
 #is is a cli that calls the /search route but then backs up to the /search3 route
  #but I could just have search that right here went clowder->sparql->grep

#next get search json.. in html format, for now; 
 #bc I can't get geodex api returns, to see what they are like to match them yet
