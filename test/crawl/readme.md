## parse crawl cfg -> sitemaps+graph/s -> count drop 

## use

/test/dashboard> localConfig4Counts.py --help

usage: localConfig4Counts.py [-h] [--localConfig LOCALCONFIG] [--nabu NABU] [--outputHTM OUTPUTHTM] [--outputDIR OUTPUTDIR]

options:

  -h, --help            show this help message and exit

  --localConfig LOCALCONFIG

                        localConfig.yaml is the default

  --nabu NABU           nabu is the default

  --outputHTM OUTPUTHTM

                        output html table default is count_dropoff.htm

  --outputDIR OUTPUTDIR

                        output directory, default to none right now 

  --sparkText SPARKTEXT

                        add a sparkline text plot, default to True
