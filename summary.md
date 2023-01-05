## summarization workflow

```mermaid
flowchart nq2summarizedSearch
runX[loadable repo.nq files] -- load_to_repo_namespace --> F(fuseki);
tsum[cache complex query as ttl] -- reads_repo_namesapce --> F(fuseki);
tsum -- dump_ttl_triples -> ttl(per repo) -- load --> Blaze(summary namespace);
search(ui/nb) -- query --> Blaze;
Blaze -- return_same_facets --> search;
```

