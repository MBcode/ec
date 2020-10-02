import extruct
import requests
from w3lib.html import get_base_url
import pprint
import xmltodict
import os
import json
pp = pprint.PrettyPrinter(indent=2) 
#is what I used when I did scripted run(w/alias)to create cached filenames
#1st I striped it from that sitemap list, used as fn, and recreated full url to crawl
#but here per repo could give 'n' for url.split("/")[n] from the url; eg, ideadata n=3
# though for eg.opentopograph url.split("=")[1]

#-get the sitmap urls:
#have a yaml of all the sitemaps, but start by just read&parsing one of them:

#fn = "sites/xml/get.iedadata.org.xml" #better to start from cdf_sites sitemapurls &use lib below
#with open(fn) as f:
#    urls=f.read()

#url[n]['url']['loc']
#turns out there are sitemap libs: 
# mediacloud/ultimate-sitemap-parser #see: tu.py
# daveoconnor/site-map-parser 
 #smapper, pip ver broken, but works in gh


#-get the metadata in jsonld only for now
#def print_data(url):
def url2metadata(url):
    r = requests.get(url)
    base_url_ = get_base_url(r.text, r.url)
    data = extruct.extract(r.text, base_url=base_url_) #,syntaxes=['json-ld'] if was ok to throw others away
    #pp.pprint(data)
    return data

def url2jsonld(url):
    md =  url2metadata(url)
    if md:
        ld = md.get('json-ld')
    else: 
        ld ="" 
    return ld

def fn2jsonld(fn):
    "url=base_url+fn save to fn"
    import re
    base_url = os.getenv('BASE_URL') 
    #print(base_url)
    url= base_url + fn
    ld=url2jsonld(url)
    print(len(ld))
    cfn=re.sub(r'(\n\s*)+\n+', '\n', fn.strip())
    fn = cfn + ".jsonld"
    print(fn)
    with open(fn  ,'w') as f:
        #pp.pprint(ld,f)
        #f.write(pprint.pformat(ld[0]))
        f.write(json.dumps(ld[0], indent= 2))
    return ld

def test(): #use a optional here
    url2jsonld("http://get.iedadata.org/doi/111486")

def t2(ns="101000"): #works
    fn2jsonld(ns)

def run_IDs(fn='l1'):
    with open(fn) as f:
        IDs = f.readlines()
    return list(map(fn2jsonld,IDs))


#considering if any of: 'microdata': [], 'microformat': [], 'opengraph': [], 'rdfa': []}
#then save as .js w/them all
#otherwize &/or anyway save: 'json-ld' as .jsonld
#=for now just: url2jsonld, but have it take it from a call to: url2metadata


#print_data("http://get.iedadata.org/doi/111486")
#setenv BASE_URL http://get.iedadata.org/doi
# is not necc exaclty the base_url above, but is realated to the filenames I use to cache this
