# From [ingestTesting.md](https://github.com/MBcode/ec/blob/master/test/ingestTesting.md) 
### .md version derived from .ipynb version, with a focus on documentation only, and adding diagrams

Has a few parts, that the doc could be broken into:

1) How the [counts](https://github.com/MBcode/ec/blob/master/test/counts.md) from the repo-sitemaps sometimes fall off in the LD-cache jsonld&ntriples, then also not getting into the endpoint
2) Then from the original cut of spot testing, but [now just new code and img below](https://github.com/MBcode/ec/blob/master/test/testing.md)=this page, is getting a rewrite to just focus on that
3) How to best [sample](https://github.com/MBcode/ec/blob/master/test/sample.md) from the sitemaps, which has become a test set, w/the hash naming in ec/test/standard/ summoned&milled

### Got end-to-end expected [sparql](standard/qry1.txt)-to->[df](standard/queryResults1.csv)/[URNs](https://github.com/MBcode/ec/blob/master/test/standard/milled/geocodes_demo_datasets/URNs.txt), for 1st comparison below
next I use diff in df to find missing URNs, and look in LD-cache for them (bc of gleaner naming)
Check both jsonld and other rdf, with standard values
in [testing.md](https://github.com/MBcode/ec/blob/master/test/ingestTesting.md) sec 2, still have dictdiff and rdflib graph cmp
but now also have output from [blabel](https://github.com/aidhog/blabel/) that removes BlankNodes+some dups, for easier nt file comparison
```mermaid
flowchart TD
U[sitemap gh-URLs] -- crawl --> J[jsonLD file] -- convert --> G[.nt or .nq version] -- load --> T[test_endpoint];
T -- query --> TR[test_results];
TR -- compare-with --> GR[gold_results] -- get --> M[missinging URNs] -- use2 --> C[check_LD_cache] -- cmp_nt --> G;
C --  cmp_jsonld --> J;
J -- compare-with --> JG[gold standard jsonLD];
G -- compare-with --> GG[gold standard triples]
```

#now we have the new spot check code, for each missing graph in the endpoint
#that looks at latest run's LD_cache and compare with gold-standard in github


```python
#new version that looks to github for gold-stnd and ld-cache bucket from latest run:
jld_eq=ec.check_urn_jsonld("11316929f925029101493e8a05d043b0ae829559") #for each URN that might be missing
jld_eq
```

    read_json:https://raw.githubusercontent.com/MBcode/ec/master/test/standard/summoned/geocodes_demo_datasets/11316929f925029101493e8a05d043b0ae829559.jsonld
    read_json:https://oss.geocodes-dev.earthcube.org/citesting/summoned/geocodes_demo_datasets/11316929f925029101493e8a05d043b0ae829559.jsonld





    True




```python
#now can also do this for ld-cache of the ntriples
nt_eq=ec.check_urn_rdf("11316929f925029101493e8a05d043b0ae829559") #fix so skips header
nt_eq
```

    read_sd:https://raw.githubusercontent.com/MBcode/ec/master/test/standard/milled/geocodes_demo_datasets/11316929f925029101493e8a05d043b0ae829559.rdf
    read_sd:https://oss.geocodes-dev.earthcube.org/citesting/milled/geocodes_demo_datasets/11316929f925029101493e8a05d043b0ae829559.rdf





    True




```python
#q=ec.init_sparql()
#can do for all the URNs that don't make it to the end of the workflow
missing_URNs=ec.get_urn_diffs()
missing_URNs
```

    find_urn_diffs:http://ideational.ddns.net:3030/geocodes_demo_datasets/sparql,https://raw.githubusercontent.com/MBcode/ec/master/test/standard/milled/geocodes_demo_datasets/URNs.txt
    in find_urn_diffs,read_sd gold
    gold:                                               g
    0   urn:ed2951175523219d05de578b6065cea156c68545
    1   urn:ed2951175523219d05de578b6065cea156c68545
    2   urn:d8e168385b0f8e0c562af2c185d804e6a35aa248
    3   urn:9a17d3fe8da1fe10866333f856986df012bff341
    4   urn:11316929f925029101493e8a05d043b0ae829559
    5   urn:261c022db9edea9e4fc025987f1826ee7a704f06
    6   urn:b2fb074695be7e40d5ad5d524d92bba32325249b
    7   urn:ce020471830dc75cb1639eae403a883f9072bb60
    8   urn:509e465d0793506b237cea8069c3cb2d276fe9c2
    9   urn:ed2951175523219d05de578b6065cea156c68545
    10  urn:8d045db20860bef9ddb33e856f95c31d6eca8206
    11  urn:8e590ac37fd8ff4442522304057a328fad5f5098
    12  urn:fe3c7c4f7ca08495b8962e079920c06676d5a166
    13  urn:7435cba44745748adfe80192c389f77d66d0e909
    14  urn:261c022db9edea9e4fc025987f1826ee7a704f06
    15  urn:b2fb074695be7e40d5ad5d524d92bba32325249b
    16  urn:40d84a8722ddae799976a0714a7af73576d7f8c0
    17  urn:bcc801ddac04636689f5bcca5dd6910ae4f548d7
    18  urn:4af74d8dd359a14000f48c3f6a1309d39d5142ce
    19  urn:1c1d4cefef851335a3311a6e3f964deaab6098e6
    20  urn:09517b808d22d1e828221390c845b6edef7e7a40
    21  urn:f4752b57d0e5434c4452136725294f755700313c
    test:['urn:7b72dec10f2359b1ab72fa3b409b4f8e691cb699', 'urn:b2fb074695be7e40d5ad5d524d92bba32325249b', 'urn:11316929f925029101493e8a05d043b0ae829559', 'urn:9a17d3fe8da1fe10866333f856986df012bff341', 'urn:40d84a8722ddae799976a0714a7af73576d7f8c0', 'urn:4af74d8dd359a14000f48c3f6a1309d39d5142ce', 'urn:fe897ff59f2f8478c24e6d17ea28df48c3bc8f69', 'urn:b62d103d4812ac2df9f2f148d9f4a3933b51abb3', 'urn:09517b808d22d1e828221390c845b6edef7e7a40', 'urn:ce020471830dc75cb1639eae403a883f9072bb60', 'urn:f4752b57d0e5434c4452136725294f755700313c', 'urn:d8e168385b0f8e0c562af2c185d804e6a35aa248', 'urn:1c1d4cefef851335a3311a6e3f964deaab6098e6', 'urn:bcc801ddac04636689f5bcca5dd6910ae4f548d7', 'urn:67e446d6f86ce88ead6335842a7a9d610a03b071', 'urn:509e465d0793506b237cea8069c3cb2d276fe9c2', 'urn:44999966af64df27587cae4aec4a744e51ad852b', 'urn:8e590ac37fd8ff4442522304057a328fad5f5098', 'urn:8d045db20860bef9ddb33e856f95c31d6eca8206', 'urn:fe3c7c4f7ca08495b8962e079920c06676d5a166', 'urn:23006491dd1bec061f6ab39e43278123ed59e359', 'urn:5288b5aa49d11829c5ab6777bb769cba4f40bd03', 'urn:ed2951175523219d05de578b6065cea156c68545', 'urn:7435cba44745748adfe80192c389f77d66d0e909', 'urn:2a328e672986c936715c52e82c519b9c34c6fafa', 'urn:261c022db9edea9e4fc025987f1826ee7a704f06']
    gold:['urn:ed2951175523219d05de578b6065cea156c68545', 'urn:ed2951175523219d05de578b6065cea156c68545', 'urn:d8e168385b0f8e0c562af2c185d804e6a35aa248', 'urn:9a17d3fe8da1fe10866333f856986df012bff341', 'urn:11316929f925029101493e8a05d043b0ae829559', 'urn:261c022db9edea9e4fc025987f1826ee7a704f06', 'urn:b2fb074695be7e40d5ad5d524d92bba32325249b', 'urn:ce020471830dc75cb1639eae403a883f9072bb60', 'urn:509e465d0793506b237cea8069c3cb2d276fe9c2', 'urn:ed2951175523219d05de578b6065cea156c68545', 'urn:8d045db20860bef9ddb33e856f95c31d6eca8206', 'urn:8e590ac37fd8ff4442522304057a328fad5f5098', 'urn:fe3c7c4f7ca08495b8962e079920c06676d5a166', 'urn:7435cba44745748adfe80192c389f77d66d0e909', 'urn:261c022db9edea9e4fc025987f1826ee7a704f06', 'urn:b2fb074695be7e40d5ad5d524d92bba32325249b', 'urn:40d84a8722ddae799976a0714a7af73576d7f8c0', 'urn:bcc801ddac04636689f5bcca5dd6910ae4f548d7', 'urn:4af74d8dd359a14000f48c3f6a1309d39d5142ce', 'urn:1c1d4cefef851335a3311a6e3f964deaab6098e6', 'urn:09517b808d22d1e828221390c845b6edef7e7a40', 'urn:f4752b57d0e5434c4452136725294f755700313c']
    got:26,expected:22





    []




```python
#none missing, but could pretend one was
missing_URNs=["11316929f925029101493e8a05d043b0ae829559"]
ld_checks= list(map(check_urn_ld_cache,missing_URNs))
ld_checks
```

    new rdf:https://oss.geocodes-dev.earthcube.org/citesting/milled/geocodes_demo_datasets/
    read_sd:https://raw.githubusercontent.com/MBcode/ec/master/test/standard/milled/geocodes_demo_datasets/11316929f925029101493e8a05d043b0ae829559.rdf
    read_sd:https://oss.geocodes-dev.earthcube.org/citesting/milled/geocodes_demo_datasets/11316929f925029101493e8a05d043b0ae829559.rdf
    new jsonld:https://oss.geocodes-dev.earthcube.org/citesting/summoned/geocodes_demo_datasets/
    read_json:https://raw.githubusercontent.com/MBcode/ec/master/test/standard/summoned/geocodes_demo_datasets/11316929f925029101493e8a05d043b0ae829559.jsonld
    read_json:https://oss.geocodes-dev.earthcube.org/citesting/summoned/geocodes_demo_datasets/11316929f925029101493e8a05d043b0ae829559.jsonld





    [(True, True)]



#all the above is wrapped into one validation function, 
#that will be called with papermill to make sure workflow stages still ok=True



### the expected_urls.csv or dataset_tests.csv will get finer grain, incl all the tests a dataset will go through
Right now I think most in standard will complete, but need to know which don't and why; will look at SR's look at this

We have a few test jsonld instances in 
[GeoCODES-Metadata](https://github.com/earthcube/GeoCODES-Metadatatree/main/metadata) that probably need their dataset_tests.csv to have finer grain expectations of the results of the tests; also to have the ability to have more than one test run; download, json conformance, and then to have some things that just go to a [repo-dashboard of warnings](repo-dashboard.md), like schema conformance.
 As long as it also tests well to turining into triples, and getting asserted in the triplestore, we should still do a text-bases search on it's strings.
 But even beyond conformance, the metadata has a way to go, to have better machine actionablitity.
 

### other docs started [here](https://github.com/MBcode/ec/tree/master/doc)
