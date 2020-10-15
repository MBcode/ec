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
    try:
        data = extruct.extract(r.text, base_url=base_url_) #,syntaxes=['json-ld'] if was ok to throw others away
    except:
        data = None
    #pp.pprint(data)
    return data

def url2jsonld(url):
    md =  url2metadata(url)
    if md:
        ld = md.get('json-ld')
    else: 
        ld ="" 
    return ld

#def fn2jsonld(fn):
def fn2jsonld(fn, base_url=None):
    "url=base_url+fn save to fn"
    import re
    if not base_url:
        base_url = os.getenv('BASE_URL') 
    #print(base_url)
    #print(fn)
    url= base_url + fn
    #print(url)
    ld=url2jsonld(url)
    #print(len(ld))
    cfn=re.sub(r'(\n\s*)+\n+', '\n', fn.strip())
    fn = cfn + ".jsonld"
    #print(fn)
    if ld:
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
    "file of FNs to append to base_url"
    with open(fn) as f:
        IDs = f.readlines()
    return list(map(fn2jsonld,IDs))

def site2buFNs(sitesfile = 'sitemap.xml'):
    "sitemap-> base_url & FileNames"
    import xmltodict
    import json

    with open(sitesfile) as f:
        xml=f.read()
    sites = xmltodict.parse(xml)
    urls=sites['urlset']['url']
    for url in urls:
        loc=(url['loc'])
    #generalize by finding last possible split char
    splitchar = '='
    url2pair = lambda url : url['loc'].split(splitchar)
    base_url = url2pair(urls[0])[0] + splitchar
    print(base_url) #return this
    url2fn = lambda url : url2pair(url)[1]
    #pairs = map(url2pair,urls)
    FNs = map(url2fn,urls) #return this too
    #for fn in FNs:
    #    print(fn)
    return base_url, FNs

def run_site(fn='sitemap.xml'):
    #import site2urls
    base_url, FNs = site2buFNs(fn)
    print(base_url)
    for fn in FNs:
        print(fn)
        fn2jsonld(fn,base_url)
    #return list(map(fn2jsonld,FNs,base_url))


#considering if any of: 'microdata': [], 'microformat': [], 'opengraph': [], 'rdfa': []}
#then save as .js w/them all
#otherwize &/or anyway save: 'json-ld' as .jsonld
#=for now just: url2jsonld, but have it take it from a call to: url2metadata


#print_data("http://get.iedadata.org/doi/111486")
#setenv BASE_URL http://get.iedadata.org/doi
# is not necc exaclty the base_url above, but is realated to the filenames I use to cache this
