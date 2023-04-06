### Examples of science-on-schema.org/[DataRepository](https://github.com/ESIPFed/science-on-schema.org/blob/master/guides/DataRepository.md) 
#### best practice

#### This is from a crawl of the top level URL for each of these repos

I used: pip3 install [extruct](https://pypi.org/project/extruct/)

then called [extruct](https://github.com/scrapinghub/extruct) on each of the URLs

this pulls out the embedded json-ld, 

along with any other valid RDF embedded in those pages

Useing [Linked-Data](https://www.ontotext.com/knowledgehub/fundamentals/linked-data-linked-open-data/) principles, you can just point to your org-URI and not have to copy the information over

This is a universal sameAs ID as the other orgIDs mentioned in the [onboarding](https://github.com/earthcube/ec/blob/master/doc/repo_onboarding.md)
