#text search of a SPARQL endpoint
 #output ready for carrot2 clustering

 #can use via CLI or call service: @app.route('/search3/<qry>') in ss2sq.py
  #considering making it the backup for when search/ goes down again too
import os
import sys
import json
from SPARQLWrapper import SPARQLWrapper, JSON
endpoint = os.getenv('dev_endpoint')
sparql = SPARQLWrapper(endpoint)
q0 = """PREFIX schema: <http://schema.org/>
select distinct ?s ?o where {
    { ?s schema:description ?o .} UNION
    { ?s schema:keywords ?o .} UNION
    { ?s schema:name ?o .}
    FILTER regex(?o, "nitrogen", "i").
}"""
#qry_str = "carbon"
if(len(sys.argv)>1):
    qry_str=sys.argv[1]
else:
    qry_str = "organic"
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
    #print("<document id=\"",i,"\">")
    print(f'<document id=\"{i}\">')
    #print("<url>",result["s"]["value"],"</url>")
    url=result["s"]["value"]
    print(f'<url>{url}</url>')
    #print("<snippet>",result["o"]["value"],"</snippet></document>")
    description=result["o"]["value"]
    print(f'<snippet>{description}</snippet></document>')
    i=i+1
print("</searchresult>")
