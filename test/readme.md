# From [ingestTesting.md](https://github.com/MBcode/ec/blob/master/test/ingestTesting.md) 
### .md version derived from .ipynb version, with a focus on documentation only, and adding diagrams

Has a few parts, that the doc could be broken into:

1) How the [counts.md](https://github.com/MBcode/ec/blob/master/test/counts.md) [code](http://geocodes.ddns.net/ec/test/counts/?C=M;O=D) from the repo-sitemaps sometimes fall off in the LD-cache jsonld&ntriples, then also not getting into the endpoint
2) Then from the original cut of spot testing, but [now just new code and img below=testing.md](https://github.com/MBcode/ec/blob/master/test/testing.md); w/rewrite to just focus on that
3) How to best [sample.md](https://github.com/MBcode/ec/blob/master/test/sample.md) from the sitemaps, which has become a test set, w/the hash naming in ec/test/standard/ summoned&milled

### Got end-to-end expected [sparql](standard/qry1.txt)-to->[df](standard/queryResults1.csv)/[URNs](https://github.com/MBcode/ec/blob/master/test/standard/milled/geocodes_demo_datasets/URNs.txt), for 1st comparison below
next I use diff in df to find missing URNs, and look in LD-cache for them (bc of gleaner naming)
Check both jsonld and other rdf, with standard values
in [testing.md](https://github.com/MBcode/ec/blob/master/test/ingestTesting.md) sec 2, still have dictdiff and rdflib graph cmp
but now also have output from [blabel](https://github.com/aidhog/blabel/) that removes BlankNodes+some dups, for easier nt file comparison

## what gets passed into the Notebook
This should be read from/passed to the notebook. Suggest as a JSON structure. Needs to be short and Hashcoded url


|  Name | Description                                                           |
| ---------- |-----------------------------------------------------------------------|
| config name | name of config directory from glcon                                   |
| org        | short name or repo                                                    |
| sitemap | url of sitemap                                                        |
| s3 base | base of s3 url |
| graph base | base url of graph endpoint |
| s2 bucket | name of bucket |
| graph namespace | name of graph namespace |
| expected results | for testing we might pass in a set of (counts, etc) in json structure |
| pointer to csv | for CI testing  has queries, expected urn's |

## Data Loading 
Basic Data loading flight testing:
* Count 1.0 - Do counts match
    * Does the gleaner count match the sitemap count
    * Does the Named Graph Count match the JsonLD Count
    * urn's
```mermaid
flowchart LR
   subgraph S3Minio 
      subgraph BUCKET 
         JsonLD
         RDF(Quads or Triples)
      end
   end
  SG(sitemapgh-URLs) --> gleaner  --> JsonLD 
  gleaner  --> RDF 
  SG(sitemapgh-URLs) --> SMC( SItemap Count )
  subgraph TEST
    GLNRCOUNT(JSONLD Count)
    SMC( SItemap Count )
    GSGraphCOUNT(Named Graph count) 
    DLQUERY(Run queries from manifest ) 
  end
  JsonLD --> GLNRCOUNT
  subgraph Graphstore  
      subgraph NAMESPACE 
         QUADS
      end
   end     
  JsonLD --> Nabu --> NGRPH(Named Graphs) --> QUADS
  NGRPH --> GSGraphCOUNT
  SPARQL-Query --> DLQUERY
```

 
## Gleaner
## Gleaner Tests
* Did we get as many as expected --> Does the gleaner count match the sitemap count
* Are the UUID generated as expected - Does the UUID Match the expected
* Did is summon correctly -- JSONLD  == Golden JSONLD
* If as CI Test Dataload, Run Queries from Manifest -- Do we get expected results
## Reporting:
* Sitemap URL
* Org Information
* sitemap count
* JSONLD Count
* Bucket name
* stats on summon
    * (jsonld count/ sitemap count)
* not harvested records from sitemap
* 
```mermaid
flowchart TD
   subgraph GitHub GeocodesMetadata 
      subgraph Files 
         manifestUUID
         GoldenJSONLD
         GoldenRDF

      end
   end
   subgraph S3Minio 
      subgraph BUCKET 
         JsonLD
         RDF(Quads or Triples)
      end
   end
  SG(sitemapgh-URLs) --> gleaner  -- summon --> GenerateUUID 
  GenerateUUID -- Store-File-by_UUID --> JsonLD 
  SG(sitemapgh-URLs) --> SMC( SItemap Count )
  subgraph Test
    GLNRUUID(UUID Equals manifestUUID )
    GLNRCOUNT( Sitemap count == JSONLD count )
    GLNRJSON( JSONLD == Golden JSONLD)
  end
  JsonLD --> GLNRCOUNT
  SMC --> GLNRCOUNT
  manifestUUID --> GLNRUUID
  JsonLD --> GLNRUUID 
  gleaner  --> RDF
  GoldenJSONLD --> JsonLD
  GLNRJSON --> JsonLD
```


## Nabu
### Nabu Tests
* Did we get as many as expected --> Does the json count == named graph count
* Are the UUID generated as expected - Does the UUID Match the expected
* Did they transform as expected -- Named Graph Triples == Golden Triples
* dupes: when loaded twice are there duplicate triples
### Reporting:
* Org Information
* Converted Count
* Graph namespace and endpoint
* stats on nabu
* (named graph count/jsonld count)
* not converted records
```mermaid
flowchart TD
   subgraph GitHub GeocodesMetadata 
      subgraph Files 
         manifestUUID
         GoldenJSONLD
         GoldenRDF

      end
   end
   subgraph S3Minio 
      subgraph BUCKET 
         JsonLD
         RDF(Quads or Triples)
      end
   end
   subgraph Graphstore  
      subgraph NAMESPACE 
         QUADS
      end
   end 
  nabu --> JsonLD  
  nabu --> QUADS  
  subgraph Test
    NABUGRAPHCOUNT( JSONLD Count == Named Graph Count )
    NABUTRIPLES( TRIPLES IN NAMED GRAPH == GOLDENRDF )
    NABUNAMEDGRAPH( UUID is as expected)
    NABUNDuplicated( Load twice No Duplicates)
  end
  JsonLD --> NABUGRAPHCOUNT
  QUADS --> NABUGRAPHCOUNT
  GoldenRDF --> NABUTRIPLES
  QUADS --> NABUTRIPLES
  manifestUUID --> NABUNAMEDGRAPH
  JsonLD --> NABUNAMEDGRAPH 
  QUADS --> NABUNAMEDGRAPH
  nabu  --> RDF
```



## Functional  Conversion Testing
```mermaid
flowchart TD
U[sitemap gh-URLs] -- crawl --> J[jsonLD file] -- convert --> G[.nt or .nq version] -- load --> T[test_endpoint];
T -- query --> TR[test_results];
TR -- compare-with --> GR[gold_results] -- get --> M[missinging URNs] -- use2 --> C[check_LD_cache] -- cmp_nt --> G;
C --  cmp_jsonld --> J;
J -- compare-with --> JG[gold standard jsonLD];
G -- compare-with --> GG[gold standard triples]
```

### ./standard instances have been moved over[*](https://github.com/earthcube/GeoCODES-Metadata/tree/main/metadata/Dataset/json), but had schema testing, which will only be usefull for a repo-feedback dashboard
The current mb_ are just json, w/my naming, ec/test/standard has summoned .jsonld and milled .rdf to test against

### the expected_urls.csv or dataset_tests.csv will get finer grain, incl all the tests a dataset will go through
Right now I think most in standard will complete, but need to know which don't and why; will look at SR's look at this

We have a few test jsonld instances in 
[GeoCODES-Metadata](https://github.com/earthcube/GeoCODES-Metadatatree/main/metadata) that probably need their dataset_tests.csv to have finer grain expectations of the results of the tests; also to have the ability to have more than one test run; download, json conformance, and then to have some things that just go to a [repo-dashboard of warnings](repo-dashboard.md), like schema conformance.
 As long as it also tests well to turining into triples, and getting asserted in the triplestore, we should still do a text-bases search on it's strings.
 But even beyond conformance, the metadata has a way to go, to have better machine actionablitity.
 
### it also mentions monitoring, incl. crontab restarts and a more frequent check+log with check.py
Added slack app w/webhook url, so nagios can be sent to ecotech channel so we have more eyes on it


### other docs started [here](https://github.com/MBcode/ec/tree/master/doc)
