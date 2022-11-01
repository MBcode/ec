#mbobak summarize a nq file, for quick queries, and quad now as subj to point to graph-url
 #this is almost like nq2ttl, but is sumarizing via the qry
import pandas as pd
df=pd.read_csv(fn, sep='\t',comment='#') #not filling out well yet
#subj g resourceType name description pubname placenames kw datep
context = "@prefix : <http://schema.org/> ." #might get larger, eg.incl dcat
#started by tweaking fnq of fn.nq then dump to fn.csv which could read here
# but can use ec.py utils, to just load summary.qry and get df right away
# then iterate over it  ;load ec like I do w/check.py and use
#could have summary in here, or give a get_summary_txt then get_summary(fnq)
#after this get max lat/lon and put as latitude/longnitude, then get centriod
 #consider a version of the query where the vars are already the so:keywords
 #but after changinge ResourceType to 'a', .. oh, this doesn't have : so special case anyway
qry="""
prefix schema: <https://schema.org/>
SELECT distinct ?subj ?g ?resourceType ?name ?description  ?pubname
        (GROUP_CONCAT(DISTINCT ?placename; SEPARATOR=", ") AS ?placenames)
        (GROUP_CONCAT(DISTINCT ?kwu; SEPARATOR=", ") AS ?kw) ?datep 
        #(GROUP_CONCAT(DISTINCT ?url; SEPARATOR=", ") AS ?disurl)
        WHERE {
          graph ?g {
             ?subj schema:name ?name .
             ?subj schema:description ?description .
            Minus {?subj a schema:ResearchProject } .
            Minus {?subj a schema:Person } .
 BIND (IF (exists {?subj a schema:Dataset .} ||exists{?subj a schema:DataCatalog .} , "data", "tool")
   AS ?resourceType).
             }
            optional {?subj schema:distribution/schema:url|schema:subjectOf/schema:url ?url .}
            OPTIONAL {?subj schema:datePublished ?date_p .}
            OPTIONAL {?subj schema:publisher/schema:name|schema:sdPublisher|schema:provider/schema:name ?pub_name .}
            OPTIONAL {?subj schema:spatialCoverage/schema:name ?place_name .}
            OPTIONAL {?subj schema:keywords ?kwu .}
            BIND ( IF ( BOUND(?date_p), ?date_p, "No datePublished") as ?datep ) .
            BIND ( IF ( BOUND(?pub_name), ?pub_name, "No Publisher") as ?pubname ) .
            BIND ( IF ( BOUND(?place_name), ?place_name, "No spatialCoverage") as ?placename ) .
        }
        GROUP BY ?subj ?pubname ?placenames ?kw ?datep   ?name ?description  ?resourceType ?g  """
#all are tabbed after context
#a                       :Dataset ;
# then :so-keyword ;   last w/.
#column names:
# "subj" , "g" , "resourceType" , "name" , "description" , "pubname" , "placenames" , "kw" , "datep" ,
#next time just get a mapping file/have qry w/so keywords as much a possilbe
print(f'{context}')
for g in df.rows:
    gu=g['g']
    rt=g['resourceType']
    name=g['name']
    description=g['description']
    kw=g['kw']
    pubname=g['pubname']
    datep=g['datep']
    placename=g['placename']
    print(" ")
    print(f'{gu}')
    print(f'        a {rt} ;')
    print(f'        :name {name} ;')
    print(f'        :description {description} ;')
    print(f'        :keyword {kw} ;')
    print(f'        :publisher {pubname} ;')
    print(f'        :place {placename} ;')
    print(f'        :date {datep} ;')
