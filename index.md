## This is an [EarthCube](https://www.earthcube.org/) [GeoCODES](https://www.earthcube.org/geocodes) staging ground

I [edit these markdown file here](https://github.com/MBcode/ec/edit/gh-pages/index.md) 

Much of this is how to improve the MetaData for better harmonization, discoverablity, &machine-useablity
![Image](http://141.142.218.86/ec/m4m/m4m.png)

Much of what is below is about making the metadata we crawl better, but we could also consider having people author better metadata via [tools](https://www.researchobject.org/ro-crate/tools/) like [describo](https://arkisto-platform.github.io/describo-online/) who's shared-ID-lookup could someday be folded in to our [jsonLD_forms-editor](https://ecjsonforms.netlify.app/#/)

The early doc started with the main [ReadMe](https://github.com/MBcode/ec#readme) &then topical sub-dirs

These latest (but waylaid) thoughts started [in these diagrams](https://github.com/MBcode/ec/tree/master/crawl#readme), now below

One of the most lasting effects on the community is the use of [ScienceOnSchema.org](https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/GETTING-STARTED.md) [metadata](http://isda.ncsa.uiuc.edu/~mbobak/sd/) [(superset)](https://www.w3.org/TR/vocab-dcat-3/)

Yet that often ends in text/**string** vs interconnected graph URI/**[thing](https://blog.google/products/search/introducing-knowledge-graph-things-not/)** descriptions

So I want to start improving this situation by:

_deduplicating_, giving _URI IDs,_ & then using _[NER](https://en.wikipedia.org/wiki/Named-entity_recognition)_ for annotation, to get a healthy graph of connections

By using even more of the [FAIR principles](https://www.go-fair.org/fair-principles/)[,](https://phaidra.univie.ac.at/download/o:1246343) we can improve the machine action-ablility&general capabilities

![Image](https://github.com/MBcode/ec/raw/master/crawl/etl.svg)

The *checking* could also be done from the [gleaner](https://gleaner.io/) generated quads.

The _dedup_ could even be done via [openrefine](https://guides.library.illinois.edu/openrefine/duplicates), if not [py](https://pypi.org/project/dedupe/) [lib](https://pypi.org/project/pandas-dedupe/)/[s](https://pypi.org/project/sparqldataframe/)

_[Generating](https://notes.knowledgefutures.org/pub/ic0grz58/release/3) an @id_ for (especially repeated) blank-nodes

[Then](https://github.com/MBcode/is/wiki) [lookup](https://github.com/WDscholia/scholia/blob/master/scholia/api.py)/[find](https://opensource.ncsa.illinois.edu/bitbucket/projects/CATS/repos/extractors-dbpedia/browse) (the shared) Name (of) the entities (_NER_), 
incl [linking](https://en.wikipedia.org/wiki/Entity_linking) [relations](https://lhncbc.nlm.nih.gov/ii/tools/SemRep_SemMedDB_SKR.html) 

which can then be [shown](https://lhce-brat.nlm.nih.gov/index.xhtml#/SKR/Factuality/Reconcile_50/10048237) w/the txt, &[generated](https://lhncbc.nlm.nih.gov/ii/tools/MetaMap/Docs/CreatingTheEFODataSetForMetaMap.html) from an ontology

This ([iSchool](https://ischool.illinois.edu/people/halil-kilicoglu)) part is [described](https://github.com/MBcode/is/wiki) in these early [slides](https://docs.google.com/presentation/d/1hPkhgtFMYjKwesR_WVtMeA7ACHtAtTBo/edit?usp=sharing&ouid=112141946798542182515&rtpof=true&sd=true)

Breakdown of present/future matching:

![Image](https://raw.githubusercontent.com/MBcode/ec/master/NoteBook/mLD.svg)

[sparql-NB](https://gist.github.com/MBcode/1fe85b1a87677968ea7c8804d56933d2) allows for cross-dataset queries, can do the dataset-page queries, & allows for more(deeper/finer):

After 1st resource-tool match will want to use other local+remote [LinkedData](https://patterns.dataincubator.org/book/follow-your-nose.html)/triples (incl eg. variable descriptions) to make better matches/kick off services

The 2nd-[toolmatch](https://docs.google.com/document/d/1ZIrr7Pwy2T5Ts5k7iRHfrdKhKPTPBmgTaPGnnNIdBmc/edit?usp=sharing)-query might be where you know which type of NB/workflow you want, but need to use some local-linked(meta)data to finish off, say a webservice call in that NoteBook

There [is work out there](https://twitter.com/txkuhn/status/1455449860652548097) that has already gone in a similar direction:
![Image](https://pbs.twimg.com/media/FDLL57oWEAMuhhS.jpg)

[FAIR-WorkFlows](https://fairworkflows.readthedocs.io/en/latest/)
