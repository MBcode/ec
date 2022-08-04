### Repository Feedback Dashboard

If the metadata can be downloaded and turned into triples with searchable text, it should go into the index to start to be found.

Every test after that should go back to the repositories, to show them the health of their metadata, via schema/shacl tests

Later we can try some entity annotation again, and also share that.

```mermaid
flowchart TD
W[ingest workflow tests] -- insertable --> E[searchable endpoint]; 
W -- breaks --> F[fix our/their];
E -- schema-problem --> RD[repo dashboard];
F -- our --> FWF[fix workflow];
F -- their --> RD;
```
