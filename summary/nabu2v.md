## what you call to run summarization

#### from getting (gleaner) crawler's runX fix quads through making the summary triples, and loading both of them w/nabu2v

```mermaid
flowchart TD;
R2S[repo_to_summary.sh]  -- calls --> G[1: fix_runX.sh];
G -- calls --> r2n[run2nq.py];
R2S -- calls --> SR[2: summarize_repo.sh];
SR -- calls --> F2[2: tsum.py] -- produces --> RT(repo.ttl);
r2n -- produces --> nq(repo.nq);
nabu2v[nabu2v.py] -- loads --> RT;
nabu2v -- can_load --> nq; 
nabu2v -- ttl_into --> Bs[blaze_summary];
nabu2v -- nq_into --> Bm[blaze_main];
```
#### Since the runX fix has to make the main repo.nq files to create the repo.ttl summary, they are both available to upload in a sync'd manner

##### there is a simplification of this, that would skip a server and just query a file, [here](https://github.com/MBcode/dc/blob/main/call-summary.md)

as soon as the [system](https://github.com/MBcode/ec/blob/master/system.md) is made more modular, the repo.nq can come from my [crawl](https://github.com/MBcode/ec/tree/master/crawl) as well
