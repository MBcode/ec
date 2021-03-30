#I already have code here that could run the qry, and w/a little cmp, at least dups
 #might try just a bit of it here; vs the aliases I have used so far: see m29
import os
import sys
import json
#import requests #could use later
from SPARQLWrapper import SPARQLWrapper, JSON

#▶<198 m29local: /earthcube/sparql_query> gred q: src/testconfigs/fullTextTests.js
ql = [ 'norway',
       'lidar',
       'Tethyan',
       'Haugtjern Norway',
       'Steens Reversal',
       'corelyzer archive',
       'Haugtjern Norway',
       'Steens Reversal',
       'corelyzer archive',
       '2019 northridge earthquake']

base_fn = "m29q.rq"

def get_txtfile(fn):
    with open(fn, "r") as f:
        return f.read()

def put_txtfile(fn,s):
    with open(fn, "w") as f:
        return f.write(s)

def qs2b(qry_str):
    endpoint = "https://graph.geodex.org/blazegraph/namespace/nabu/sparql"
 #  endpoint = os.getenv('dev_endpoint')
    sparql = SPARQLWrapper(endpoint)
    gqs=get_txtfile(base_fn)
    q=gqs.replace('${q}',qry_str) 
    sparql.setQuery(q)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    #print(f'sq2b:{results}')
    bindings= results["results"]["bindings"]
    print(f'ret:{bindings}')
    return bindings

def tq():
    qs2b("Norway")
