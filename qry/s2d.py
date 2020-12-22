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

#here can focus on bindings dict, bs the clowder search dict, which was limited; 
 #should have at least returned the url I sent in, as promoted data, if not more

def get_txtfile(fn):
    with open(fn, "r") as f:
        return f.read()

def get_txtfile_(fn):
    if os.path.exists(fn) and os.stat(fn).st_size >199:
            return get_txtfile(fn)
    else:
        return None

def get_jsonfile(fn):
    #s=get_txtfile_(fn)
    s=get_txtfile(fn)
    d=json.loads(s)
    return d

def get_jsonfile_(fn):
    if os.path.exists(fn) and os.stat(fn).st_size >199:
        return get_jsonfile(fn)
    else:
        return None

def put_txtfile(fn,s):
    with open(fn, "w") as f:
        return f.write(s)

def put_jsonfile(fn,d):
    s=json.dumps(d, indent=2)
    with open(fn, "w") as of:
        of.write(s)

#--
def sq2b_(qry_str):
    ccf = "cc/" + qry_str.replace(" ", "_")  + ".jsonld" #from global
    ccf_ = "cc/" + qry_str.replace(" ", "_")  + ".js" #from global
    b=get_jsonfile_(ccf)
    if not b:
        b=sq2b(qry_str)
        put_jsonfile(ccf,b)
        d=ld2js(b)
        put_jsonfile(ccf_,d)
    return b
#--
def sq2b__(qry_str): #rewrite above, more compace, then also .js
    "cache around sparql-qry2binding"
    #ccf- = "cc/" + qry_str.replace(" ", "_")  + ".js" #from global
    ccf = "cc/" + qry_str.replace(" ", "_")  + ".jsonld" #from global
    if os.path.exists(ccf) and os.stat(ccf).st_size >199:
        b_=get_txtfile(ccf) #actually need to read as file for now
        #print(f'already have file:{ccf}')
        b=json.loads(b_)
        #bl=len(b)
        #print(f'got bindings of len{bl}')
    else:
        b=sq2b(qry_str)
        #print(f'bindings:{b}') #dbg, not as full as returned below
        #bl=len(b)
        #print(f'writing bindings of len{bl}')
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

#use code from csq2.py where I got these elts from the jsonLD
pub_tc = {}
date_tc = {}
plc_tc = {}
def printFacetCounts(): #new
    print(json.dumps(date_tc, indent=2))
    print(json.dumps(pub_tc, indent=2))
    print(json.dumps(plc_tc, indent=2))
    #getting different values out from pub_tc after change, 
    #but not if on other machine/check, but it was in cc/ diff

# <TR>
#  <TD>2</TD>
def d2htm(d):
    print(f'<TABLE border="1" style="border: 1px solid #000000; border-collapse: collapse;" cellpadding="4">')
    for k, v in d.items():
        print(f'<tr><td>{k}</td><td>{v}</td></tr>')
    print("</table>")

def printFacetCounts2htm(): #new
    d2htm(pub_tc)
    d2htm(date_tc)
    d2htm(plc_tc)

def d2html(d,title):
    dl=len(d) #check
    print(f'{title}:{dl}')
    d2htm(d)

def printFacetCounts2htm(): #new
    d2html(pub_tc,"Publications")
    d2html(date_tc,"DatePublished")
    d2html(plc_tc,"Place")

#works but might try: https://flask-table.readthedocs.io/en/stable/ for portability

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
        #print(m3s) #dbg
        incrKeyCount(datep,date_tc)
    #pub=r.get('publisher')
    pub=r.get('pubname')
    if pub:
        pub=pub['value']
        m3s += f'publisher:{pub},'
        #print(m3s) #dbg
        incrKeyCount(pub,pub_tc)
    return m3s
#get rest of  cache2facet.py geo analog in here, should be easy but.might need some logic

#def b1hs(b1):
def b1hs(result): #original using bindings
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
    #print(rs) #for now
    m3s=b1fc(result)
    #print(f'md-elts:{m3s}') #dbg
    return rs

#haven't switched over w/these yet

def b1hs_(result): #new altered using flat dict, ready for facetedsearch 
    "bindings to html for(one)rescard"
    doi=result["subj"]
    url=result["disurl"]
    name=result["name"]
    des=result["description"]
    url2=doiDetails(doi)
    rh=f'<div class="rescard"><div class="resheader"><a href="{url}">{name}</a></div>'
    rb=f'<div class="rescontiner"><a href="{url}"><p>{des}</p><a href="{url2}">details</a><p></div></div>'
    rs=rh+rb
    #print(rs) #for now
    m3s=b1fc(result)
    #print(f'md-elts:{m3s}') #dbg
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
    d=ld2js(b)
    s=json.dumps(d, indent=2)
    print(f'ld2js:{s}')
    #print(f'bindings:{b}')
    h=b2hs(b) #binding to html
    #print(f'html:{h}') #dbg
    print(h) 
    #-can skip below if don't need clusters, but still need other metadata-put in
    #print("printFacetCounts")  #dbg
    #printFacetCounts() #new
    #now how to get this out as a re-query w/the new constraint of what was picked
     #would like to have the facets build up, so will need to update the ?q etc terms
      #but would much prefer ths faster in page demo/ideas, which are also friendlir to In_sub_topic/s
 #could use the tree part of 2nd demo to show the counts, but then still need the <form>links
    printFacetCounts2htm() #new

def s2d(qry_str):
    "just sparql to json/dict for facetedsearch"
    b=sq2b(qry_str)   
    d=ld2js(b)
    s=json.dumps(d, indent=2)
    print(f'ld2js:{s}') 

s2d(qry_str)
#sq2(qry_str)

#have other files w/sparql-dataframe, might be nice bc could do facet-aggregation math quickly
#probably take out dateframe&unused qry on top next
#just need to make a flask route for this, or might just swap out the fillSearch.py external call for this
 #so the rough template can be put in; though probably go to something w/the new simpler top you see in
 # http://mbobak-ofc.ncsa.illinois.edu/search1.htm &but if could use the fast in page filter w/counts at
 # http://mbobak-ofc.ncsa.illinois.edu/facetedsearch/
