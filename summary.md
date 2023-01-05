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
tsum -- dump_ttl_triples --> T[ttl per repo]  -- load --> B[blaze:summary namespace];;
search[ui/nb] -- 1:query --> B -- 2:return_same_facets --> search;
```


