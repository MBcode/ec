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
#use the one below in py:
#might start w/filter, &allow for geting more, but then no clustering by defualt bc more noise
q1 = """prefix schema: <http://schema.org/>
 SELECT ?subj ?pub ?datep ?disurl ?score  ?name ?description
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
      OPTIONAL {?s schema:publisher ?pub .}
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
    #q=gqs.replace('${q}',qry_str)
    q=q1+qs+q2
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

#--below/next functions are for clustering in_subtopic facet
 #will probably break out into a separate d2c.py file soon
  #and could send the sq bindings-dict as js2it similarly
   #b2hs fnc will get bindings as-is w/all optionals in
    #so nothing extra to to there, except on the html-gen side

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
        #print(f'result={result}')
        rs+= b1xs(result)
    rs += "</searchresult>"
    return rs 
#dicts are off

def b2xs_(b):
    "cache around bindings2xml-str"
    ccf = "cc/" + qry_str.replace(" ", "_")  + ".xml" #from global
    if os.path.exists(ccf) and os.stat(ccf).st_size >199:
        x=get_txtfile(ccf) #actually need to read as file for now
        print(f'already have file:{ccf}')
    else:
        x=b2xs(b)
        print(f'xml:{x}') #dbg, not as full as returned below
        xl=len(x)
        print(f'writing xml of len{xl}')
        #write, then use
        with open(ccf, "w") as of:
            of.write(x)
    return x

def xs2c(x):
    "dcs-xml(str-cache-file)call to get clusters only in json" 
    #just needs b2xs_ check/setting the xml file to load, till can send via requests
    ccf = "cc/" + qry_str.replace(" ", "_")  + ".xml" #from global
    cs= f'curl $dcs_url -F "dcs.clusters.only=true" -F "dcs.output.format=JSON" -F "dcs.c2stream=@{ccf}"'
    s=os.popen(cs).read()
    #try:
    #    dct=json.loads(s)
    #except:
    #    print(s) 
    dct=json.loads(s) #not getting right xml2dcs service, bc not saved well, would work around if used this
    #docs=dct['documents'] #this fnc just abt clusters, but still make sure  original binidngs, make2html2
    cls=dct['clusters']
    nc=len(cls)
    print(f'got {nc} clusters') #dbg
    return cls 

#--cut out:
#only for referenc for now
def cj2h(j): #from fillSearch.py, but want a new one that is sparql-1st,&possibly only(eg.stop being slowed down by it)
    "clowder json ret to html"  #btw mapping could probably get2details, or my cache, but blaze explore links from DOIs work2:
    #if(len(j)>1)                #eg. https://graph.geodex.org/blazegraph/#explore:cdf:%3CDOI:10.15784/601173%3E
    for r in j:
        name=r['name']
        des=r['description']
        #will want to get url
        #url=httpP(des) #bool, need actual url
        url=first(getURLs(des))
        url2= clowder_host + '/datasets/' + r['id'] #use metadata-tab for 'details'
        rh=f'<div class="rescard"><div class="resheader"><a href="{url}">{name}</a></div>'
        #rb=f'<div class="rescontiner"><a href="{url}><p>{des}</p></div>'
        #I do not see ec score from clowder  to put /\
        rb=f'<div class="rescontiner"><a href="{url}"><p>{des}</p><a href="{url2}">details</a><p></div></div>'
        rs=rh+rb
        print(rs) #for now
#--
#when I was making the xml4dcs in b2xs.. I could have made a more compact dict, that was all ready for the binding2html
 #but can get it again for now
#----html-gen fncs: 
def doiDetails(doi):
    return f'https://graph.geodex.org/blazegraph/#explore:cdf:%3C{doi}3%3E'

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

def b2hs(b):
    "bindings to html for(all)rescards"
    for result in b:
        b1hs(result)

#bindings will have the optional filterable md-elts now, but have2see how used by filter widgets
 #sounds like it just needs the range of values w/counts, ;which can get from sparql-qry too
  #along w/more optional to normalize the publisher, which varies, so will look into that

#---qry+fill middle of search page
def sq2(qry_str): 
    "sq running from a cache"
    #will use dict to make html later, but for now make sure can make re clusters 1st
    #sq2b.py|tee  (b2htm.py )   b2xs.py| xs2c    
    b=sq2b(qry_str)   #get the filter-facet metadata through optional lines in sparql qry
    #jb=json.dumps(b, indent=2)
    h=b2hs(b) #binding to html
    print(f'html:{h}') #dbg
    #-can skip below if don't need clusters, but still need other metadata-put in
    x=b2xs_(b) #binding to dcs-xml
    c=xs2c(x) #dcs-xml(file)to clusters
 #  print(f'clusters:{c}') #dbg
    #if c, then can put in the html
    #h=b2hs(b) #binding to html
    #print(f'html:{h}') #dbg  #would print down here if putting cluters as part of metadata
    # at end, had rescards w/cluster info, incl links back2id's in html
    print(f'clusters:{c}') #dbg
      #this is from csq2's cls2h, ..

sq2(qry_str)
#the xml from the print can be run by the sh file and does give back the js cluster, working via this cache file
 #would rework a bit anyway, ..  ;incl direct requests.get to dcs  &:

# will try a new verion of qry2 called qry3 where all the connections can be made not by looping but by local
# graph asserts, which might not only be cleaner, but have many other potential near term benefits
#;if not new, just finish off the rest of the linking w/this small local graph
#I had thought of using owlready2 before, but even easier probably is the lib I saw used when saw the pipy flask rdf: python3-flask-rdf
# which when I 1st saw just though would do the nice LD deciding wether to give you person or machine version of a resource page
# but allows for creating a small graph, like owlready2, so both cluster&/or sortable metadata could go into this store right away
# &obviate most of the present code that makes all those links, &the start of the facet-aggregate/counts; on if needed thought

#have other files w/sparql-dataframe, might be nice bc could do facet-aggregation math quickly
def tdf(): #install is trickier than sparqlwrapper alone, so maybe cound w/in the qry
    sq2df(qry_str)
