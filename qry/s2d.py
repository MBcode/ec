#s2d.py is a version of qry.py that relies on sparql &/or the js in facetedsearch to do the rest
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
    OPTIONAL {?s schema:publisher/schema:name ?pubname .}
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

#----
def doiDetails(doi):
    return f'https://graph.geodex.org/blazegraph/#explore:cdf:%3C{doi}3%3E'
    #w/repo & what I'd call file-base could ret http to my jsonLD cache too
#sparql describe could give out similar info #had in htm but could put in these js:flat-bindings
#want a group_concat on geo, so only one subj/hit, so if get same subj/doi again, concat geo key
 #have a dict key-ed on doi could be useful for putting clustering in later as well as making sure only1
 # but if I did that I'd still have to map over it, to ret the flat array of hit-binding for facetedsearch
#-
def d2a(d):
    "dict to array of it's values"
    tmpa=[]
    for k, v in d.items():
            tmpa.append(v)     
    return tmpa 
#-
def add2dict(key,v,d): #was considering being able to append w/in this fnc
    d[key]=v
#-
def ld1js(d):  #thought abt mapping, but could append2new dict like I do w/incrKeyCount
    "jsonld to just js, for one search hit"
    tmp={}
    for k, v in d.items():
        v2 = v['value']
        #add k,v2  to the .js version of this hit, just below/finsh
        #add2dict(k,v2,tmp) #tmp[k]=v2
        tmp[k]=v2 #add2dict(k,v2,tmp) 
    return tmp

def ld2js(d):
    "jsonld to just js"
    tmpa=[]
    for hit in d:
        d=ld1js(hit)
        tmpa.append(d)
    return tmpa
#----
subj_tc = {} #counts of each subj
subj_geo = {} #concat of geo for each subj
subj_d = {} #dict for each subj ;try
#was for facetCounts, but can reuse:
def incrKeyCount(key,d):
    v=d.get(key)
    if not v:
        d[key] = 0
    d[key] += 1
    return d[key] #new
#----
def incrKeyConcat(key,d,v2):
    v=d.get(key)
    if not v:
        d[key] = v2
    v2c = "," + v2 
    d[key] += v2c
    return d[key] 
#next part, is also a partial hack, of saving up the concat field for the main-hit-key(subj)
#----
def ld1js1(d):
    "jsonld to just 1subj js for one search hit"
#getting 1subj/hit w/o concat yet
def ld2js1(d):
    "jsonld to just 1subj js/hit"
    #tmpd={} #will do by key, but start w/  #turned into subj_d
    #tmpa=[]
    for hit in d:
        subj=hit['subj']['value']
        geo=hit['geo']['value']
        if geo.startswith("t"): #should use regexp w/ t[0-9]
            print(f'blank-node:{geo}') #dbg see if works,for now
            geo=""
        cg=incrKeyConcat(subj,subj_geo,geo) #could put ret value in this dict now or later
        #hit['geo']['value'] = cg  #would not work, bc only gets set once, then skipped, need in dict
        cc=incrKeyCount(subj,subj_tc)
        print(f'sub:{subj},w/count:{cc},cg:{cg}') #dbg
        if cc<2:
            d=ld1js(hit) #might reuse old1first, &just not add2array if have seen subj, then concat next
            subj_d[subj]=d #so can look up and alter w/concat field/s
            #tmpa.append(d)     #then can skip this, after turn d2a
        subj_d[subj]['geo'] = cg #try
    tmpa=d2a(subj_d)
    #tmpa=subj_d  #try2dbg then d2a this
    return tmpa 
#----
#can see cg getting the group_concat of geo, just not in the final array of dicts, yet

def s2d(qry_str):
    "just sparql to json/dict for facetedsearch"
    b=sq2b(qry_str)   
    #d=ld2js(b)
    d=ld2js1(b)
    s=json.dumps(d, indent=2)
    print(f'ld2js1:{s}') 

s2d(qry_str)
#sq2(qry_str) #only in qry.py now
#just need to make a flask route for this, or might just swap out the fillSearch.py external call for this
 #so the rough template can be put in; though probably go to something w/the new simpler top you see in
 # http://mbobak-ofc.ncsa.illinois.edu/search1.htm &but if could use the fast in page filter w/counts at
 # http://mbobak-ofc.ncsa.illinois.edu/facetedsearch/
