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
We could also make some fixes for their breaks (eg. I've made context fixes), and inform them

#### Validation by data of the workflow software
Had a mockup [here](https://github.com/earthcube/geocodes_documentation/wiki/DataValidationReportMockup)
Which is mostly in the utils that can be called by [spot_test.py](https://github.com/MBcode/ec/blob/master/test/spot_test.py#L62) and just needs a little cleaning up


## want to reuse this for reporting
![oih dashboard](oih-dashboard.png)

#### should start with simple count drop off that is [in sync with crawl's cfg](localConfigCounts.py)


### can get sparklines in info [page](https://geocodes.ncsa.illinois.edu/#/about)

#### count-droppoff numbers should go into the org info, so can be presented easily in the info-page

[sitemap, summonded, graph]

[13]
import pygal
chart = pygal.Line()
chart.add('', [13221, 12902, 12484])
chart.render_sparktext(relative_to=12484)
█▄▁
#### the info page could have this right next to the number that made it in the graph

[14]
chart.render_sparktext(relative_to=0)
█▇▇
#### workflow counts could be done in thirds, toptop=green, middle=yellow, bottom=red


##### numbers for example come from original [counts.md](https://github.com/earthcube/ec/blob/master/test/counts.md)
