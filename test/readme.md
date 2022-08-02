# From ingestTesting.md

We have a few test jsonld instances in 
[GeoCODES-Metadata](https://github.com/earthcube/GeoCODES-Metadatatree/main/metadata) that probably need their dataset_tests.csv to have finer grain expectations of the results of the tests; also to have the ability to have more than one test run; download, json conformance, and then to have some things that just go to a repo-dashboard of warnings, like schema conformance.
 As long as it also tests well to turining into triples, and getting asserted in the triplestore, we should still do a text-bases search on it's strings.
 But even beyond conformance, the metadata has a way to go, to have better machine actionablitity.

## .md version derived from .ipynb version, with a focus on documentation only, and adding diagrams
## ./standard instances have been moved over, but had schema testing, which will only be usefull for a repo-feedback dashboard
## the expected_urls.csv or dataset_tests.csv will get finer grain, incl all the tests a dataset will go through
