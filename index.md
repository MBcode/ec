## This is an [EarthCube](https://www.earthcube.org/) [GeoCODES](https://www.earthcube.org/geocodes) staging ground

Just starting to [edit](https://github.com/MBcode/ec/edit/gh-pages/index.md) the Markdown files.

The early doc started with the main [ReadMe](https://github.com/MBcode/ec#readme) &then topical sub-dirs

These latest (but waylaid) thoughts started [in these diagrams](https://github.com/MBcode/ec/tree/master/crawl#readme) now below

One of the most lasting effects on the community is the use of [ScienceOnSchema.org](https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/GETTING-STARTED.md) [metadata](http://isda.ncsa.uiuc.edu/~mbobak/sd/)

Yet that often ends in text/**string** vs interconnected graph URI/**[thing](https://blog.google/products/search/introducing-knowledge-graph-things-not/)** descriptions

So I want to start improving this situation by:

_deduplicating_, giving _URI IDs,_ & then using _[NER](https://en.wikipedia.org/wiki/Named-entity_recognition)_ for annotation, to get a healthy graph of connections

By using even more of the [FAIR principles](https://www.go-fair.org/fair-principles/) we can improve the machine action-ablility&general capabilities

![Image](https://github.com/MBcode/ec/raw/master/crawl/etl.svg)

The checking could also be done from the [gleaner](https://gleaner.io/) generated quads.

The _dedup_ could even be done via [openrefine](https://guides.library.illinois.edu/openrefine/duplicates), if not [py](https://pypi.org/project/dedupe/) [lib](https://pypi.org/project/pandas-dedupe/)/[s](https://pypi.org/project/sparqldataframe/)

_[Generating](https://notes.knowledgefutures.org/pub/ic0grz58/release/3) an @id_ for (especially repeated) blank-nodes

Then [lookup](https://github.com/WDscholia/scholia/blob/master/scholia/api.py) (the shared) Name (of) the entities (_NER_), 
incl [linking](https://en.wikipedia.org/wiki/Entity_linking) [relations](https://lhncbc.nlm.nih.gov/ii/tools/SemRep_SemMedDB_SKR.html) which can then be [shown](https://lhce-brat.nlm.nih.gov/index.xhtml#/SKR/Factuality/Reconcile_50/10048237) w/the txt
