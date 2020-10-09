#code below is from the colab NB that I shared awhile ago
# can be more than a shim to get non-auth clowder search
#since it's an API shim, will assume called from NB or other code,
# for which I will give the qr.py example
from flask import Flask
from markupsafe import escape
app = Flask(__name__)
import requests
import json
import os
#import re #consider the strip.py code also used here,but better2just store that way 1st

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
