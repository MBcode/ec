## - 1:make summary triples

### [summarize_repo.sh](https://github.com/MBcode/ec/blob/master/summarize_repo.sh) runs:
#### [fnq.py](https://github.com/MBcode/ec/blob/master/fnq.py) on a repo, to load the quads into repo namespace in fuseki
#### [tsum.py](https://github.com/MBcode/ec/blob/master/tsum.py) for repo, to read that namespace and dump summary ttl triples
```mermaid
flowchart TD;
runX[runX w/loadable repo.nq files] -- fnq:load_to_repo_namespace --> F[fuseki_repo_namespace];
tsum[tsum: cache complex query as ttl] -- reads_repo_namesapce --> F;
tsum -- dump_ttl_triples --> T[repo_ttl];
```
  
  
  
## - 2:use for fast sparql on summary namespace
```mermaid
flowchart TD;
T[ttl per repo]  -- load --> B[blaze:summary namespace];
search[ui/nb] -- 1:query --> B -- 2:return_same_facets --> search;
```
  
## - also: get RDF from endpoint
### which gets rid of need for a duplicate cache
```mermaid
flowchart TD;
B[blaze] -- query_ret_facets_incl_g --> U[ui/nb]; 
U -- use_g_to_get_rdf --> B;
``` 



## - ps. triples from a crawl/s
### [runX](https://github.com/gleanerio/gleaner/issues/126) 'quads' could come from gleaner or extruct crawls, now
