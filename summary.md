## summarization workflow

### summarize_repo.sh runs:
#### fnq.py on a repo, to load the quads into repo namespace in fuseki
#### tsum.py for repo, to read that namesapce and dump summary ttl triples
```mermaid
flowchart TD;
runX[runX w/loadable repo.nq files] -- fnq:load_to_repo_namespace --> F[fuseki_repo_namespace];
tsum[tsum: cache complex query as ttl] -- reads_repo_namesapce --> F;
tsum -- dump_ttl_triples --> T[repo_ttl];

```


