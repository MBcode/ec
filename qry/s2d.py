#qry.py is just the SPARQL part of qry2.py, while the clustering has been spun out to b2c.py
#all the code in ../assert & ../search as clowder at least as a backup, 
#this finally breaks free&be small like these early querys I wanted to finish
import os
import sys
import json
#import requests #could use later
from SPARQLWrapper import SPARQLWrapper, JSON

if(len(sys.argv)>1):
    qry_str=sys.argv[1]
else:
    qry_str = "Tectonophysics Seymour Island"
    #qry_str = "sea ice"
    #qry_str = "organic"
#-do not use this top one, that q set in js
gqs = """ prefix schema: <http://schema.org/> \
SELECT ?subj ?disurl ?score  ?name ?description \
 WHERE { \
   ?lit bds:search \"${q}\" . \
   ?lit bds:matchAllTerms "false" . \
   ?lit bds:relevance ?score . \
   ?subj ?p ?lit . \
   BIND (?subj as ?s) {  \
         SELECT  ?s (MIN(?url) as ?disurl) { \
             ?s a schema:Dataset . \
             ?s schema:distribution ?dis . \
            ?dis schema:url ?url . \
         } GROUP BY ?s  } \
   ?s schema:name ?name . \
   ?s schema:description ?description .  \
   filter(?score > 0.1). \
    OPTIONAL {?s schema:datePublished ?datep .} \
    OPTIONAL {?s schema:publisher ?pub . \
               ?pub schema:name ?pubname .} \
 } \
ORDER BY DESC(?score)""" 
#not use js qry above; condiser using t2.qry
# that would do all the aggr-counts w/o d16.js
#----
q1s= """PREFIX schema: <http://schema.org/>
select distinct ?s ?o where {
    { ?s schema:description|schema:keywords|schema:name ?o .}"""
qss=f'FILTER regex(?o, "{qry_str}", "i")'
q2s="}"  #but could add optional here
#-
#use the one below in py:
#might start w/filter, &allow for geting more, but then no clustering by defualt bc more noise
#SELECT ?subj ?pub ?datep ?disurl ?score  ?name ?description
            #even w/the 'distinct' got one duplicate, which clustering doesn't like, &is good to know about
q1 = """prefix schema: <http://schema.org/>
 SELECT distinct ?subj ?pubname ?datep ?geo ?disurl ?score  ?name ?description
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
    OPTIONAL {?s schema:datePublished ?datep .}
    OPTIONAL {?s schema:publisher ?pub .
               ?pub schema:name ?pubname .}
OPTIONAL {?s 
    schema:spatialCoverage/schema:name|schema:spatialCoverage/schema:geo ?geo}
  }
  ORDER BY DESC(?score)"""
 #  OPTIONAL {?s schema:spatialCoverage ?space .
 #             ?space schema:geo ?geo .  }
                #?geo schema:box ?box .
                #though these are blank-nodes
 #but might use more of t2.qry &run in js in end ;for now use2get optional's in for md-elts
#--pick a qry to use/try new one w/optionals to get the metadata-facets to filter on
#maybe actually do call w/sparql-dataframe to get aggregation math right away
#don't have to put in links like did w/clusters, just counts, &can requery this time
#--
def sq2b(qry_str):
    "free-text(sparql)query of blazegraph endpoint, bindings" 
    endpoint = "https://graph.geodex.org/blazegraph/namespace/cdf/sparql"
 #  endpoint = os.getenv('dev_endpoint')
    sparql = SPARQLWrapper(endpoint)
    ##q=gqs.replace('${q}',qry_str)
    q=q1+qs+q2
    #q=q1s+qss+q2s  #got a dup even w/this, so check this again in yasgui etc
    sparql.setQuery(q)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    #print(f'sq2b:{results}')
    bindings= results["results"]["bindings"]
 #  print(f'ret:{bindings}')
    return bindings


#sparql describe could give out similar info

def add2dict(key,v,d):
    #d.add(k,v) #more internal to class
    d[key]=v

def ld1js(d):  #thought abt mapping, but could append2new dict like I do w/incrKeyCount
    "jsonld to just js, for one search hit"
    tmp={}
    for k, v in d.items():
        v2 = v['value']
        #add k,v2  to the .js version of this hit, just below/finsh
        add2dict(k,v2,tmp)
    return tmp

def ld2js(d):
    "jsonld to just js"
    tmpa=[]
    for hit in d:
        d=ld1js(hit)
        tmpa.append(d)
    return tmpa


def s2d(qry_str):
    "just sparql to json/dict for facetedsearch"
    b=sq2b(qry_str)   
    d=ld2js(b)
    s=json.dumps(d, indent=2)
    print(f'ld2js:{s}') 

s2d(qry_str)
#sq2(qry_str) #only in qry.py now

#have other files w/sparql-dataframe, might be nice bc could do facet-aggregation math quickly
#probably take out dateframe&unused qry on top next
#just need to make a flask route for this, or might just swap out the fillSearch.py external call for this
 #so the rough template can be put in; though probably go to something w/the new simpler top you see in
 # http://mbobak-ofc.ncsa.illinois.edu/search1.htm &but if could use the fast in page filter w/counts at
 # http://mbobak-ofc.ncsa.illinois.edu/facetedsearch/
