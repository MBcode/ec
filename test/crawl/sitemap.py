#mbobak sitemap parts of the utils that where orginally more notebook focused

def setup_sitemap(): #do this by hand for now
    cs='pip install ultimate_sitemap_parser' #assume done rarely, once/session 
    os_system(cs) #get rid of top one soon
    cs='pip install advertools' #assume done rarely, once/session 
    os_system(cs)

def sitemap_tree(url): #will depricate
    "len .all_pages for count"
    #print("assume: setup_sitemap()")
    from usp.tree import sitemap_tree_for_homepage
    tree = sitemap_tree_for_homepage(url)
    return tree

#switch over libs from tree to df

def sitemap_df(url):
    import  advertools as adv
    df=adv.sitemap_to_df(url)
    return df

def sitemap_all_pages(url):
    #tree=sitemap_tree(url)
    #return tree.all_pages()
    df=sitemap_df(url)
    return df['loc']

def repo2site_loc_df(repo):
    "get df[loc] from repos sitemap" #use cached sitemap
    base_url="http://mbobak.ncsa.illinois.edu/ec/crawl/sitemaps/"
    url=f'{base_url}{repo}.xml'
    return sitemap_all_pages(url)

def sitemaps_all_loc(sitemaps):
    "list(iterable) to get all DFs of LOCs"
    return map(sitemap_all_pages,sitemaps)
    #also be able to work w/dictionaries,  repo_name sitmap in, count out

def sitemap_list_(url):
    pages=sitemap_all_pages(url)
    pl=list(pages)
    return pl #get rid of need for these libs

def sitemap_list(url):
    "use fast xml lib"
    return sitemap_urls(url)

def sitemap_len(url):
    "try fast xml version"
    ul=sitemap_urls(url)
    return len(ul)
#now using this over https://github.com/MBcode/ec/blob/master/test/counts.md named_sitemaps
#sitemaps=list(named_sitemaps.values())
#counts=list(map(sitemap_len_,sitemaps)) #now resistent to errors, get:
#[25226, 18634, 704, 28, 5654, 17654, 0, 4263, 920, 0, 211, 45159, 0, 910, 2522, 0]
#can also run: that prints them out as it goes along
#sc=sitemaps_count(sitemaps)

def sitemap_len_(url):
    "for counts" # maybe allow filtering types later
    pages=sitemap_all_pages(url)
    pl=list(pages)
    return len(pl)

def sitemaps_count(sitemaps):
    "send in urls, get url: count"
    sitemap_count = {}
    for sitemap in sitemaps:
        count=sitemap_len(sitemap)
        print(f'{sitemap} has {count} records')
        sitemap_count[sitemap]=count
    return sitemap_count
#---
def sitemaps_d_count(sitemaps_d):
    "send in repo:url get back repo:count"
    sitemap_count = {}
    #for sitemap in sitemaps:
    for repo,sitemap in sitemaps_d.items():
        count=sitemap_len(sitemap)
        print(f'{sitemap} has {count} records')
        #sitemap_count[sitemap]=count
        sitemap_count[repo]=count
    return sitemap_count
#---
def crawl_sitemap(url):
    "url w/o sitemap.xml, might try other lib"
    #tree=sitemap_tree(url)
    pages=sitemap_all_pages(url)
    #for page in tree.all_pages():
    for page in pages:
        url2nq(page)
        #url2nq(page.url)
        #print(f'url2nq({page.url})') #dbg

#if already crawled and just need to convert
#_testing end



#---- sources:
def get_sources_csv(url="https://raw.githubusercontent.com/MBcode/ec/master/crawl/sources.csv"):
    return get_ec_txt(url)

def get_sources_df(url="https://raw.githubusercontent.com/MBcode/ec/master/crawl/sources.csv"):
    s= read_file(url,".csv")
    return s.loc[s['Active']] #can only crawl the active ones

#def get_sources_urls(): #could become crawl_
def crawl_sources_urls(): #work on sitemap lib to handle non-stnd ones
    import re
    s=get_sources_df()
    for url in s['URL']:
        print(f'sitemap:({url})') #dbg
        #urlb=re.sub('\/site*.xml','',url)
        urlb=re.sub('sitemap.xml','',url)
        #crawl_sitemap(urlb)
        print(f'crawl_sitemap({urlb})') #dbg
#----



#sitemap url to LD-cache filenames
 #in mine it is BASE_URL + file_leaf(ur)
 #gleaner needs a mapping from it's PROV:

def prov2mapping(url): #use url from p above
    "read&parse 1 PROV record"
    import json
    #print(f'prov2mapping:{url}')
    j=url2json(url)
    d=json.loads(j)
    #print(d)
    g=d.get('@graph')
    if g:
        gi=list(map(lambda g: g.get("@id"), g))
        smd=g[1] #assume 1 past the context, 1st thing being from sitemap
        sm=smd.get("@id") #gi[0]
        u=collect_pre_(gi,"urn:")
        u0=u[0]
        #print(f'{sm}=>{u0}')
        #return sm, u #if expect >1
        return sm, u[0]
    else:
        return f'no graph for:{url}'

def prov2mappings(urls): #use urls from p above
    "get sitemap<->UUID in summoned,&sitemap"
    sitemap2urn={}
    urn2sitemap={} #might need this more
    for url in urls:
        key,value=prov2mapping(url)
        sitemap2urn[key]=value
        urn2sitemap[value]=key
        value2=value.split(':')[-1]   #so can also lookup form UUID w/o urn:... before it
        urn2sitemap[value2]=key #will be in same dict, so can lookup by either
    sitemap=list(sitemap2urn.keys())
    if dbg:
        print(f'prov-sitemap:{sitemap}')
    #return sitemap2urn, urn2sitemap
    return sitemap2urn, urn2sitemap, sitemap





def url_xml(url): #could just be get_url
    "given bucket url ret raw xml listing"
    import requests
    #r=requests.get(url)
    try:
        r=requests.get(url, timeout=(15, 45)) #used in check.py
    except:
        print(f'url_xml:req-execpt on:{url}')
        return None
    test_xml=r.content
    #print(test_xml) #check if 200
    status=r.status_code 
    if(status == 200):
        return test_xml
    else:
        print(f'url_xml,bad:{status},for:{url}')
        return None

def is_bytes(bs):
    return isinstance(bs, bytes)

def xmltodict_parse(test_xml):
    import xmltodict
    if not is_bytes(test_xml):
        print(f'xml_parse no str')
        return None
    try:
        d=xmltodict.parse(test_xml)
    except:
        lx=len(test_xml)
        print(f'xml_parse exception')
        d=None
    return d

def sitemap_xml2dict(test_xml): #libs don't work in diff places
    #import xmltodict
    #d=xmltodict.parse(test_xml)
    d=xmltodict_parse(test_xml)
    if(dbg):
        print(d)
    if not d:
        print(f'sitemap_xml2 not found')
        return None
    lbr=d.get("urlset")
    if lbr:
        c=lbr.get("url")
        return c
    else:
        print(f'no urlset, for:{test_xml}')
        return None

def sitemap_urls(url):
    "faster way of getting urls w/just xml lib"
    test_xml=url_xml(url)
    if not test_xml:
        return []
    c=sitemap_xml2dict(test_xml)
    if c:
        urls=list(map(lambda kd: kd.get('loc'), c))
        return urls
    else:
        print(f'no sitemap_urls xml for urls:{url}')
        #return None
        return [] #hope to still work

