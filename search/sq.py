#text search of a SPARQL endpoint
 #output ready for carrot2 clustering

 #can use via CLI or call service: @app.route('/search3/<qry>') in ss2sq.py
  #considering making it the backup for when search/ goes down again too
import os
import sys
import json
from SPARQLWrapper import SPARQLWrapper, JSON

if(len(sys.argv)>1):
    qry_str=sys.argv[1]
else:
    qry_str = "organic"


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
 } \
ORDER BY DESC(?score)""" 
def gq(qry_str):
    "geodex blazegraph"
    endpoint = "https://graph.geodex.org/blazegraph/namespace/cdf/sparql"
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(gqs)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    #print(gqs)
    #print(results) 
#   print(json.dumps(results, indent=2))
    cout = """<?xml version="1.0" encoding="UTF-8"?>
        <searchresult>"""
    xml_qry=f'<query>{qry_str}</query>'
    print(cout,xml_qry)
    i=0
    for result in results["results"]["bindings"]:
        print(f'<document id=\"{i}\">')
        #url=result["s"]["value"]
        #url=result["disurl"]["value"]
        url=result["subj"]["value"]
        print(f'<url>{url}</url>')
        #description=result["o"]["value"]
       # description=result["name"]["value"]
        description=result["description"]["value"]
        description=description.replace("&","_and_").replace("<"," _lt_ ")
        print(f'<snippet>{description}</snippet></document>')
        #print(f'<snippet>{name}')
        #print(f'{description}</snippet></document>')
        i=i+1
    print("</searchresult>")

#q0 = """PREFIX schema: <http://schema.org/>
#select distinct ?s ?o where {
#    { ?s schema:description ?o .} UNION
#    { ?s schema:keywords ?o .} UNION
#    { ?s schema:name ?o .}
#    FILTER regex(?o, "nitrogen", "i").  }"""
#qry_str = "carbon"
def sq(qry_str):
    "blazegraph from early days"
    endpoint = os.getenv('dev_endpoint')
    sparql = SPARQLWrapper(endpoint)
    q1 = "PREFIX schema: <http://schema.org/> \nselect distinct ?s ?o where {\n"
    q2 = "{ ?s schema:description ?o .} UNION \n { ?s schema:keywords ?o .} UNION  \n{ ?s schema:name ?o .} \n  FILTER regex(?o,\""
    #there is a more terse way to write this
    q4 = "\", \"i\"). \n }"
    q = q1 + q2 + qry_str + q4
    #print(sq)
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
gq(qry_str)
