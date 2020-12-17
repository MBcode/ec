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
#-do not use this top one, that q set in js
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
#-
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
 SELECT distinct ?subj ?pubname ?datep ?disurl ?score  ?name ?description
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
  }
  ORDER BY DESC(?score)"""
 #but might use more of t2.qry &run in js in end ;for now use2get optional's in for md-elts
#--pick a qry to use/try new one w/optionals to get the metadata-facets to filter on
#maybe actually do call w/sparql-dataframe to get aggregation math right away
#don't have to put in links like did w/clusters, just counts, &can requery this time
#--
def sq2df(qry_str):
    "sparql to df"
    import sparql_dataframe
    endpoint = "https://graph.geodex.org/blazegraph/namespace/cdf/sparql"
    q=q1+qs+q2
    df = sparql_dataframe.get(endpoint, q)
#--
def sq2b(qry_str):
    "free-text(sparql)query of blazegraph endpoint, bindings" 
    endpoint = "https://graph.geodex.org/blazegraph/namespace/cdf/sparql"
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

#here can focus on bindings dict, bs the clowder search dict, which was limited; 
 #should have at least returned the url I sent in, as promoted data, if not more

def get_txtfile(fn):
    with open(fn, "r") as f:
        return f.read()

def get_jsonfile(fn):
    t=get_txtfile(fn)

#--
def sq2b_(qry_str):
    "cache around sparql-qry2binding"
    ccf = "cc/" + qry_str.replace(" ", "_")  + ".js" #from global
    if os.path.exists(ccf) and os.stat(ccf).st_size >199:
        b_=get_txtfile(ccf) #actually need to read as file for now
        print(f'already have file:{ccf}')
        b=json.loads(b_)
        bl=len(b)
        print(f'got bindings of len{bl}')
    else:
        b=sq2b(qry_str)
        print(f'bindings:{b}') #dbg, not as full as returned below
        bl=len(b)
        print(f'writing bindings of len{bl}')
        b_=json.dumps(b, indent=2)
        #write, then use
        with open(ccf, "w") as of:
            of.write(b_)
    return b
#--
#when I was making the xml4dcs in b2xs.. I could have made a more compact dict, that was all ready for the binding2html
 #but can get it again for now
#----html-gen fncs: 
def doiDetails(doi):
    return f'https://graph.geodex.org/blazegraph/#explore:cdf:%3C{doi}3%3E'

#pubdate ={}
#pubname ={}
  # if datep:
  #     #pubdate[datep]
  #     incrKeyCount
#use code from csq2.py where I got these elts from the jsonLD
pub_tc = {}
date_tc = {}
def printFacetCounts(): #new
    print(json.dumps(date_tc, indent=2))
    print(json.dumps(pub_tc, indent=2))

 #only problem is it should default to 0
def incrKeyCount(key,d):
    v=d.get(key)
    if not v:
        d[key] = 0
    d[key] += 1

def b1fc(r):
    "one hit's binding to incr facet-count"
    m3s=""
    #datep=r.get('datePublished')
    datep=r.get('datep')
    if datep:
        datep=datep['value']
        m3s += f'date:{datep}'
        ##date_tc[date]+=1
        #print(m3s)
        incrKeyCount(datep,date_tc)
    #pub=r.get('publisher')
    pub=r.get('pubname')
    if pub:
        pub=pub['value']
        m3s += f'publisher:{pub},'
        ##pub_tc[pub]+=1
        #print(m3s)
        incrKeyCount(pub,pub_tc)
    return m3s

#def b1hs(b1):
def b1hs(result):
    "bindings to html for(one)rescard"
    doi=result["subj"]["value"]
    url=result["disurl"]["value"]
    name=result["name"]["value"]
    #description=result["description"]["value"]
    des=result["description"]["value"]
    url2=doiDetails(doi)
    rh=f'<div class="rescard"><div class="resheader"><a href="{url}">{name}</a></div>'
    rb=f'<div class="rescontiner"><a href="{url}"><p>{des}</p><a href="{url2}">details</a><p></div></div>'
    rs=rh+rb
    print(rs) #for now
    m3s=b1fc(result)
    print(f'md-elts:{m3s}')
    return rs

def b2hs(b):
    "bindings to html for(all)rescards"
    rs=""
    for result in b:
        rs+=b1hs(result)
    return rs

#bindings will have the optional filterable md-elts now, but have2see how used by filter widgets
 #sounds like it just needs the range of values w/counts, ;which can get from sparql-qry too
  #along w/more optional to normalize the publisher, which varies, so will look into that

#---qry+fill middle of search page
def sq2(qry_str): 
    "sq running from a cache"
    #will use dict to make html later, but for now make sure can make re clusters 1st
    #sq2b.py|tee  (b2htm.py )   b2xs.py| xs2c    
    #get the filter-facet metadata through optional lines in sparql qry
    #b=sq2b(qry_str)   
    b=sq2b_(qry_str)   
    bl=len(b)
    print(f'sq2b_ bindings of len{bl}')
    #jb=json.dumps(b, indent=2)
    h=b2hs(b) #binding to html
    print(f'html:{h}') #dbg
    #-can skip below if don't need clusters, but still need other metadata-put in
    print("printFacetCounts") 
    printFacetCounts() #new

sq2(qry_str)

#have other files w/sparql-dataframe, might be nice bc could do facet-aggregation math quickly
def tdf(): #install is trickier than sparqlwrapper alone, so maybe cound w/in the qry
    sq2df(qry_str)
