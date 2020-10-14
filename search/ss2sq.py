#Search main or backup clowder or search3 sparql endpoint(&get all metadata at once)
#ss.py + dev4c.py,  then took sparql part out into sq.py, and call it from this: ss2sq.py
#code below is from the colab NoteBook that I shared awhile ago
# can be more than a shim to get non-auth clowder search
#since it's an API shim, will assume called from NB or other code,
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

@app.route('/search/<qry>')
def search(qry):
    "new site w/simple qry"
    clowder_key = os.getenv('testkey')
    clowder_host = os.getenv('clowder_host')
    if not clowder_host:
        clowder_host = "https://earthcube.clowderframework.org"
        clowder_key = os.getenv('eckey')
    print(clowder_host)
    qry_str=escape(qry)
    print(qry_str)
    #print(f'host:{clowder_host},qry:{qry_str}')
    r = requests.get(f"{clowder_host}/api/search?query={qry_str}", headers={'X-API-Key': clowder_key})
    return json.dumps(r.json()['results'])

@app.route('/search3/<qry>')
def search3(qry):
    qry_str=escape(qry)
    cs=f"python3 sq.py {qry_str}"
    s=os.popen(cs).read()
    return s
