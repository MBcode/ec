#mbobak summarize a nq file, for quick queries, and quad now as subj to point to graph-url
 #this is almost like nq2ttl, but is sumarizing via the qry
import pandas as pd
fn="iris.csv" #"xdomes.csv"
#df=pd.read_csv(fn, comment='#') #not filling out well yet
#df=pd.read_csv("s.csv") #head of summary.csv, from ec.py's get_summary("")
#df=pd.read_csv("summary_urn.csv") #head of summary.csv, from ec.py's get_summary("")
#df=pd.read_csv("s2.csv") #from similar summarizition but of my stoere, that uses URLs for graph
 #after reading csv via qry, which could be done w/rdflib like in 2nq.py but w/ec like qry
#subj g resourceType name description pubname placenames kw datep
#context = "@prefix : <http://schema.org/> ." #might get larger, eg.incl dcat
context = "@prefix : <https://schema.org/> ." #https for now
#started by tweaking fnq of fn.nq then dump to fn.csv which could read here
# but can use ec.py utils, to just load summary.qry and get df right away
# then iterate over it  ;load ec like I do w/check.py and use
#could have summary in here, or give a get_summary_txt then get_summary(fnq)
#after this get max lat/lon and put as latitude/longnitude, then get centriod
 #consider a version of the query where the vars are already the so:keywords
 #but after changinge ResourceType to 'a', .. oh, this doesn't have : so special case anyway
#used this query on all of geodec using ec.py's get_summary and dumped to summary.csv
qry="""
PREFIX bds: <http://www.bigdata.com/rdf/search#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix schema: <http://schema.org/>
prefix sschema: <https://schema.org/>
SELECT distinct ?g ?subj ?pubname (GROUP_CONCAT(DISTINCT ?placename; SEPARATOR=", ") AS ?placenames)
        (GROUP_CONCAT(DISTINCT ?kwu; SEPARATOR=", ") AS ?kw)
       ?datep  (GROUP_CONCAT(DISTINCT ?url; SEPARATOR=", ") AS ?disurl) #(MAX(?score1) as ?score)
        ?name ?description ?resourceType 
    #(MAX(?lat) as ?maxlat) (Min(?lat) as ?minlat) (MAX(?lon) as ?maxlon) (Min(?lon) as ?minlon)
         WHERE {
  #         ?lit bds:search "Norway" . #"Antarctica " .
  #         ?lit bds:matchAllTerms false .
  #         ?lit bds:relevance ?score1 .
  #         ?lit bds:minRelevance 0.24 .
  #         ?subj ?p ?lit .
  #         #filter( ?score1 > 0.14).
#BIND (IF (exists {?subj a schema:Dataset .} || exists{?subj a sschema:Dataset .} , "data",
#     (IF (exists {?subj a schema:SoftwareApplication .} || exists{?subj a sschema:SoftwareApplication .}   
#, "tool", "other")) ) AS ?resourceType).

          graph ?g {
             ?subj schema:name|sschema:name ?name .
             ?subj schema:description|sschema:description ?description . 
       #    Minus {?subj a sschema:ResearchProject } .
       #    Minus {?subj a schema:ResearchProject } .
       #    Minus {?subj a schema:Person } .
       #    Minus {?subj a sschema:Person } .
#   ?subj a schema:Dataset|sschema:Dataset|schema:SoftwareApplication|sschema:SoftwareApplication .
    { ?subj rdf:type schema:Dataset . } UNION { ?subj rdf:type sschema:Dataset . } UNION
    { ?subj rdf:type schema:DataCatalog . } UNION { ?subj rdf:type sschema:DataCatalog . }
            }
            values (?type ?resource_Type) {
            (schema:Dataset "Dataset")
            (sschema:Dataset "Dataset")
            (schema:DataCatalog "DataCatalog")
            (sschema:DataCatalog "DataCatalog")
             (schema:SoftwareApplication  "tool")
             (sschema:SoftwareApplication  "tool")
              } ?subj a ?type .
        optional {?subj schema:distribution/schema:url|schema:subjectOf/schema:url ?url .}
        OPTIONAL {?subj schema:datePublished|sschema:datePublished ?date_p .}
        OPTIONAL {?subj schema:publisher/schema:name|sschema:publisher/sschema:name|schema:publisher/schema:legalName|sschema:publisher/sschema:legalName  ?pub_name .}
        OPTIONAL {?subj schema:spatialCoverage/schema:name|sschema:spatialCoverage/sschema:name|sschema:sdPublisher ?place_name .}
#OPTIONAL {?subj schema:spatialCoverage/schema:geo/schema:latitude|sschema:spatialCoverage/sschema:geo/schema:latitude ?lat .}
#OPTIONAL {?subj schema:spatialCoverage/schema:geo/schema:longitude|sschema:spatialCoverage/sschema:geo/schema:longitude ?lon .}
        OPTIONAL {?subj schema:keywords|sschema:keywords ?kwu .}
            BIND ( IF ( BOUND(?date_p), ?date_p, "No datePublished") as ?datep ) .
            BIND ( IF ( BOUND(?pub_name), ?pub_name, "No Publisher") as ?pubname ) .
            BIND ( IF ( BOUND(?place_name), ?place_name, "No spatialCoverage") as ?placename ) .
            BIND ( IF ( BOUND(?resource_Type), ?resource_Type, "other") as ?resourceType ) .
        }
# GROUP BY ?g ?subj ?pubname ?placename ?kw ?datep ?url ?score1 ?name ?description  ?resourceType 
    GROUP BY ?g ?subj ?pubname ?placenames ?kw ?datep ?disurl #?score 
        ?name ?description  ?resourceType 
        #?minlat ?maxlat ?minlon ?maxlon
        ORDER BY DESC(?score) 
        """
        #using more constrained qry now in get_summary.txt * now above
df=pd.read_csv("summary-gc1.csv") #head of summary.csv, from ec.py's get_summary("")
#all are tabbed after context
#a                       :Dataset ;
# then :so-keyword ;   last w/.
#column names:
# "subj" , "g" , "resourceType" , "name" , "description" , "pubname" , "placenames" , "kw" , "datep" ,
#next time just get a mapping file/have qry w/so keywords as much a possilbe
urns = {}
import json
def is_str(v):
    return type(v) is str
print(f'{context}')
for index, row in df.iterrows():
    gu=df["g"][index]
    #skip the small %of dups, that even new get_summary.txt * has
    #if not urns.get(gu):
    #   urns[gu]=1
    #else: 
    # break from loop
    rt=row['resourceType']
    name=json.dumps(row['name'])
    description=row['description']
    if is_str(description):
        sdes=json.dumps(description)
        #sdes=description.replace(' / ',' \/ ').replace('"','\"')
        #sdes=sdes.replace(' / ',' \/ ').replace('"','\"')
      # sdes=sdes.replace('"','\"')
    else:
        sdes=f'"{description}"'
    kw_=row['kw']
    if is_str(kw_):
        kw=json.dumps(kw_)
    else:
        kw=f'"{kw_}"'
    pubname=row['pubname']
    datep=row['datep']
    placename=row['placenames']
    s=row['subj']
    print(" ")
    print(f'<{gu}>')
    #print(f'        a {rt} ;')
    if rt == "tool":
        print(f'        a :SoftwareApplication ;')
    else:
        print(f'        a :Dataset ;')
   #print(f'        :name "{name}" ;')
    print(f'        :name {name} ;')
   #print(f'        :description """{description}""" ;')
   #print(f'        :description """{sdes}""" ;')
    print(f'        :description ""{sdes}"" ;')
   #print(f'        :keyword "{kw}" ;')
    print(f'        :keyword {kw} ;')
    print(f'        :publisher "{pubname}" ;')
    print(f'        :place "{placename}" ;')
    print(f'        :date "{datep}" ;') #might be: "No datePublished"
    print(f'        :subjectOf <{s}> .')
#got a bad:         :subjectOf <metadata-doi:10.17882/42182> .
#incl original subj, just in case for now
#lat/lon not in present ui, but in earlier version
