#!/usr/bin/env python3
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
#Nov  5 17:24 get_summary.txt -> get_summary_good.txt
#still using txt file on my server right now instead
qry="""
#PREFIX bds: <http://www.bigdata.com/rdf/search#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix schema: <http://schema.org/>
prefix sschema: <https://schema.org/>
SELECT distinct ?subj ?pubname (GROUP_CONCAT(DISTINCT ?placename; SEPARATOR=", ") AS ?placenames)
        (GROUP_CONCAT(DISTINCT ?kwu; SEPARATOR=", ") AS ?kw)
        ?datep  (GROUP_CONCAT(DISTINCT ?url; SEPARATOR=", ") AS ?disurl) #(MAX(?score1) as ?score)
        ?name ?description ?resourceType ?g
        #(MAX(?lat) as ?maxlat) (Min(?lat) as ?minlat) (MAX(?lon) as ?maxlon) (Min(?lon) as ?minlon)
         WHERE {
#           ?lit bds:search "${q}" .
#           ?lit bds:matchAllTerms false .
#           ?lit bds:relevance ?score1 .
#           ?lit bds:minRelevance 0.24 .
#           ?subj ?p ?lit .
#           #filter( ?score1 > 0.14).
BIND (IF (exists {?subj a schema:Dataset .} || exists{?subj a sschema:Dataset .} , "data",
     (IF (exists {?subj a schema:SoftwareApplication .} || exists{?subj a sschema:SoftwareApplication .}   ,
     "tool", "other")) ) AS ?resourceType).
          graph ?g {
             ?subj schema:name|sschema:name ?name .
             ?subj schema:description|sschema:description ?description .
           Minus {?subj a sschema:ResearchProject } .
           Minus {?subj a schema:ResearchProject } .
           Minus {?subj a schema:Person } .
           Minus {?subj a sschema:Person } .
            }
        optional {?subj schema:distribution/schema:url|schema:subjectOf/schema:url ?url .}
        OPTIONAL {?subj schema:datePublished|sschema:datePublished ?date_p .}
        OPTIONAL {?subj schema:publisher/schema:name|sschema:publisher/sschema:name|schema:publisher/schema:legalName|s
schema:publisher/sschema:legalName|schema:sdPublisher|sschema:sdPublisher  ?pub_name .}
        OPTIONAL {?subj schema:spatialCoverage/schema:name|sschema:spatialCoverage/sschema:name ?place_name .}
#OPTIONAL {?subj schema:spatialCoverage/schema:geo/schema:latitude|sschema:spatialCoverage/sschema:geo/schema:latitude
?lat .}
#OPTIONAL {?subj schema:spatialCoverage/schema:geo/schema:longitude|sschema:spatialCoverage/sschema:geo/schema:longitud
e ?lon .}
            OPTIONAL {?subj schema:keywords|sschema:keywords ?kwu .}
            BIND ( IF ( BOUND(?date_p), ?date_p, "No datePublished") as ?datep ) .
            BIND ( IF ( BOUND(?pub_name), ?pub_name, "No Publisher") as ?pubname ) .
            BIND ( IF ( BOUND(?place_name), ?place_name, "No spatialCoverage") as ?placename ) .
        }
#?subj ?pubname ?placename ?kwu ?datep ?url  ?name ?description  ?resourceType ?g  #was wrong
        GROUP BY ?subj ?g ?resourceType ?name ?description ?pubname ?placenames ?kw ?datep ?disurl #?score
        #?minlat ?maxlat ?minlon ?maxlon
     #  ORDER BY DESC(?score)
        """
        #using more constrained qry now in get_summary.txt * now above
#df=pd.read_csv("summary-gc1.csv") #head of summary.csv, from ec.py's get_summary("")
#df=pd.read_csv(f'{repo}.csv') #head of summary.csv, from ec.py's get_summary("")
#seeing error in csv, might be time to get it directly, as repo's are small enough, to try over
#repo="linked.earth" #get from cli now
#testing_endpoint=f'http://ideational.ddns.net:3030/{repo_name}/sparql'
#tmp_endpoint=f'http://localhost:3030/{repo}/sparql' #fnq repo
#print(f'try:{tmp_endpoint}') #if >repo.ttl, till prints, will have to rm this line &next2:
#< not IN_COLAB
#< rdf_inited,rdflib_inited,sparql_inited=True,True,True
import ec
#ec.dflt_endpoint = tmp_endpoint
#df=ec.get_summary("")
#all are tabbed after context
#a                       :Dataset ;
# then :so-keyword ;   last w/.
#column names:
# "subj" , "g" , "resourceType" , "name" , "description" , "pubname" , "placenames" , "kw" , "datep" ,
#next time just get a mapping file/have qry w/so keywords as much a possilbe
def summaryDF2ttl(df):
    urns = {}
    import json
    def is_str(v):
        return type(v) is str
    print(f'{context}')
    for index, row in df.iterrows():
        gu=df["g"][index]
        #skip the small %of dups, that even new get_summary.txt * has
        there = urns.get(gu)
        if not there:
            urns[gu]=1
        elif there: 
            #print(f'already:{there},so would break loop')
            continue #from loop
        rt=row['resourceType']
        name=json.dumps(row['name']) #check for NaN/fix
        if not name:
            name=f'""'
        if not is_str(name):
            name=f'"{name}"'
        if name=="NaN": #this works, but might use NA
            name=f'"{name}"'
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
        #if no publisher urn.split(':')
        #to use:repo in: ['urn', 'gleaner', 'summoned', 'opentopography', '58048498c7c26c7ab253519efc16df237866e8fe']
        #as of the last runs, this was being done per repo, which comes in on the CLI, so could just use that too*
        if pubname=="No Publisher":
            ul=gu.split(':')
            if len(ul)>4: #could check, for changing urn more, but for now:
                pub_repo=ul[3]
                if is_str(pub_repo):
                    pubname=pub_repo
                else: #could just use cli repo
                    global repo
                    pubname=repo
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
       #print(f'        :keyword {kw} ;') #not what schema.org &the new query uses
        print(f'        :keywords {kw} ;')
        print(f'        :publisher "{pubname}" ;')
        print(f'        :place "{placename}" ;')
        print(f'        :date "{datep}" ;') #might be: "No datePublished"
        print(f'        :subjectOf <{s}> .')
        #du= row.get("disurl") #not seeing yet
        du= row.get("url") # check now/not yet
        if is_str(du):
            print(f'        :distribution <{du}> .')
    #see abt defaults from qry or here, think dv needs date as NA or blank/check
    #old:
    #got a bad:         :subjectOf <metadata-doi:10.17882/42182> .
    #incl original subj, just in case for now
    #lat/lon not in present ui, but in earlier version

if __name__ == '__main__':
    import sys
    if(len(sys.argv)>1):
        repo = sys.argv[1]
        tmp_endpoint=f'http://localhost:3030/{repo}/sparql' #fnq repo
        print(f'try:{tmp_endpoint}') #if >repo.ttl, till prints, will have to rm this line &next2:
        ec.dflt_endpoint = tmp_endpoint
        df=ec.get_summary("")
        summaryDF2ttl(df)
