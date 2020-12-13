#all the code in ../assert & ../search as clowder at least as a backup, this finally breaks free&be small like these early queris I wante to finish
import os
import sys
import json
import requests
from SPARQLWrapper import SPARQLWrapper, JSON

if(len(sys.argv)>1):
    qry_str=sys.argv[1]
else:
    qry_str = "Tectonophysics Seymour Island"
    #qry_str = "sea ice"
    #qry_str = "organic"
#-
gqs = """ prefix schema: <http://schema.org/> \
SELECT ?subj ?disurl ?score  ?name ?description \
 WHERE { \
   ?lit bds:search \"${q}\" . \
   ?lit bds:matchAllTerms "false" . \
   ?lit bds:relevance ?score . \
   ?subj ?p ?lit . \
   BIND (?subj as ?s) \
      {  \
         SELECT  ?s (MIN(?url) as ?disurl) { \
             ?s a schema:Dataset . \
             ?s schema:distribution ?dis . \
            ?dis schema:url ?url . \
         } GROUP BY ?s \
   } \
   ?s schema:name ?name . \
   ?s schema:description ?description .  \
   filter(?score > 0.4). \
 } \
ORDER BY DESC(?score)""" 
#might start w/filter, &allow for geting more, but then no clustering by defualt bc more noise
q1 = """prefix schema: <http://schema.org/>
 SELECT ?subj ?disurl ?score  ?name ?description
  WHERE { """
#   ?lit bds:search "carbon" .                                       
qs=f'?lit bds:search "{qry_str}" . '                                        
q2 = """  ?lit bds:matchAllTerms "false" .
    ?lit bds:relevance ?score .
    ?subj ?p ?lit .
    BIND (?subj as ?s)
       {
          SELECT  ?s (MIN(?url) as ?disurl) {
              ?s a schema:Dataset .
              ?s schema:distribution ?dis .
             ?dis schema:url ?url .
          } GROUP BY ?s
    }
    ?s schema:name ?name .
    ?s schema:description ?description .
    filter( ?score > 0.4).
  }"""
def sq2b(qry_str):
    "free-text(sparql)query of blazegraph endpoint, bindings" 
    endpoint = "https://graph.geodex.org/blazegraph/namespace/cdf/sparql"
    sparql = SPARQLWrapper(endpoint)
    #q=gqs.replace('${q}',qry_str)
    q=q1+qs+q2
    sparql.setQuery(q)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results["results"]["bindings"]

#here can focus on bindings dict, bs the clowder search dict, which was limited; 
 #should have at least returned the url I sent in, as promoted data, if not more

def get_txtfile(fn):
    with open(fn, "r") as f:
        return f.read()

def get_jsonfile(fn):
    t=get_txtfile(fn)

def b1xs(result):
    "one binding to xml str"
    rl=len(result)
    #print(f'b1xs,result:{result}') #dbg
    #print(f'{result}') #dbg
    if rl<2:
        #print(f'b1xs,result-len:{rl}') #dbg
        return ""
    rs=""
    doi=result["subj"]["value"]
    ds=f'\n<document id=\"{doi}\">'
#   print(ds) #dbg
    rs+=ds
    url=result["disurl"]["value"]
    us=f'<url>{url}</url>\n'
#   print(us) #dbg
    rs+=us
    description=result["description"]["value"]
    description=description.replace("&","_and_").replace("<"," _lt_ ")
    ss=f'<snippet>{description}</snippet></document>'
#   print(ss) #dbg
    rs+=ss
    return rs

def b2xs(b):
    "var bindings2xml(str)4 clowder2 dcs service"
    rs = """<?xml version="1.0" encoding="UTF-8"?>
        <searchresult>"""   #when in file only gets up to here
    xml_qry=f'<query>{qry_str}</query>\n'  #gotten from global
    print(xml_qry) #dbg
    rs += xml_qry
    for result in b:
        #if isinstance(result,dict):
        #    rs+= b1xs(result)
        print(f'result={result}')
        rs+= b1xs(result)
    rs += "</searchresult>"
    return rs 
#dicts are off

def xs2c(b):
    "dcs-xml(str-cache-file)call to get clusters only in json" 
    ccf = "cc/" + qry_str.replace(" ", "_")  + ".xml" #from global
    if os.path.exists(ccf) and os.stat(ccf).st_size >199:
        #x=get_txtfile(ccf) #actually need to read as file for now
        print(f'already have file:{ccf}')
    else:
        x=b2xs(b)
        xl=len(x)
        print(f'writing xml of len{xl}')
        #write, then use
        with open(ccf, "w") as of:
            of.write(x)
    cs= f'curl $dcs_url -F "dcs.clusters.only=true" -F "dcs.output.format=JSON" -F "dcs.c2stream=@{ccf}"'
    s=os.popen(cs).read()
    #try:
    #    dct=json.loads(s)
    #except:
    #    print(s) 
    dct=json.loads(s) #not getting right xml2dcs service, bc not saved well, would work around if used this
    docs=dct['documents']
    cls=dct['clusters']
    nc=len(cls)
    print(f'got {nc} clusters') #dbg
    return cls 

def sq2(qry_str): 
    "sq running from a cache"
    #will use dict to make html later, but for now make sure can make re clusters 1st
    #sq2b.py|tee  (b2htm.py )   b2xs.py| xs2c    
    b=sq2b(qry_str)
    jb=json.dumps(b, indent=2)
#   print(f'bindings:{jb}') #dbg
    x=b2xs(b)
    print(f'xml:{x}') #dbg
    c=xs2c(x)
    print(f'clusters:{c}') #dbg

sq2(qry_str)
#the xml from the print can be run by the sh file and does give back the js cluster,..still check/&clean out most of this
 #would rework a bit anyway, ..
