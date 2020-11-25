#text search of a SPARQL endpoint
 #output ready for carrot2 clustering

 #can use via CLI or call service: @app.route('/search3/<qry>') in ss2sq.py
  #considering making it the backup for when search/ goes down again too
import os
import sys
import json
import requests

if(len(sys.argv)>1):
    qry_str=sys.argv[1]
else:
    qry_str = "organic"

def qs2dcs(qry_str):
    "query clowder to-dcs format"
    from SPARQLWrapper import SPARQLWrapper, JSON
    endpoint = os.getenv('dev_endpoint')
    sparql = SPARQLWrapper(endpoint)
    #q0 = """PREFIX schema: <http://schema.org/>
    #select distinct ?s ?o where {
    #    { ?s schema:description ?o .} UNION
    #    { ?s schema:keywords ?o .} UNION
    #    { ?s schema:name ?o .}
    #    FILTER regex(?o, "nitrogen", "i").  }"""
    #qry_str = "carbon"
    q1 = "PREFIX schema: <http://schema.org/> \nselect distinct ?s ?o where {\n"
    q2 = "{ ?s schema:description ?o .} UNION \n { ?s schema:keywords ?o .} UNION  \n{ ?s schema:name ?o .} \n  FILTER regex(?o,\""
    q4 = "\", \"i\"). \n }"
    q = q1 + q2 + qry_str + q4
    #print(q)
    #print(results) 
    sparql.setQuery(q)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    cout = """<?xml version="1.0" encoding="UTF-8"?>
        <searchresult>"""
    xml_qry=f'<query>{qry_str}</query>'
    print(cout,xml_qry)
    i=0
    for result in results["results"]["bindings"]:
        print(f'<document id=\"{i}\">')
        url=result["s"]["value"]
        print(f'<url>{url}</url>')
        description=result["o"]["value"]
        print(f'<snippet>{description}</snippet></document>')
        i=i+1
    print("</searchresult>")
    #presently xml ready for carro2 clustering, but will make that an output format for /cluster route
    # and will get a uniform output as say geodex puts out, though final html is ok too

    #before fuseki & then this blazegraph instance I also had a cache of HDT files, so have code w/:
    #from hdt import HDTDocument ;which when worked up allows for same breadth & could take the per repo
    # checkbox info (w/o having to make subgraphs, or putting restriction in sparql query)for other stores
#-
def first(l):
    from collections.abc import Iterable
    if isinstance(l,list):
        return l[0]
    elif isinstance(l,Iterable):
        return list(l)[0]
    else:
        return l

def httpP(str):
    #str.startswith('http')
    return str.startswith('http')

def getURLs(l):
    if isinstance(l,str):
        l=l.split()
    #filter(httpP,l)
    return filter(httpP,l)
#-
def cq(qry_str):
    "clowder search query"
    clowder_host = os.getenv('clowder_host')
    r = requests.get(f"{clowder_host}/api/search?query={qry_str}")
    if(r.status_code == 200):
        #ret = json.dumps(r.json()['results'], indent=2)
        ret = r.json()['results']
        rl=len(ret)
        print(f'cq:{rl}') #dbg
        return ret
    else:
        #return r.status_code
        print(f'cq:bad:{rs}') #dbg
        rs= r.status_code
        return rs

#-also use cj2h, for below
def qc2dcs(qry_str):
    "query clowder to-dcs format"
    rj=cq(qry_str)

    cout = """<?xml version="1.0" encoding="UTF-8"?>
        <searchresult>"""
    xml_qry=f'<query>{qry_str}</query>'
    print(cout,xml_qry)
    i=0
    for r in rj:
        name=r['name']
        description=r['description']
        url=first(getURLs(description))
        #url2= clowder_host + '/datasets/' + r['id']
        print(f'<document id=\"{i}\">')
        print(f'<url>{url}</url>')
        #print(f'<snippet>{description}</snippet></document>')
        print(f'<snippet>{name}')
        print(f'{description}</snippet></document>')
        i=i+1
    print("</searchresult>")

#cluster clowder results this time
qc2dcs(qry_str)

#would be cool if could call dcs clustering service from here, but sending via shell file is ok too
