#mbobak, parse crawl cfg, to get sitemap+graph to get counts from them
import pandas as pd
dbg=True

#from mb.py part of utils, for now
def path_leaf(path):
    "everything after the last /"
    import ntpath
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

# https://www.golinuxcloud.com/python-convert-yaml-file-to-dictionary/
def yml2d(fn):
    "yml file to dict"
    import yaml
    from yaml.loader import BaseLoader
    # opening a file
    with open(fn, 'r') as stream:
        try:
            # Converts yaml document to python object
            d=yaml.load(stream, Loader=BaseLoader)
            if dbg:
                for key, val in d.items():
                    print(key, " : ", val,"\n")       
                return d
        except yaml.YAMLError as e:
            print(e)
            return None

def df_cols2dict(df,c1,c2):
    "make a dict from 2 df cols"
    #d={}
    print(f'will pull out, c1={c1},c2={c2}')
    d=df.set_index(c1).to_dict()[c2]
    if dbg:
        print(f'd={d}')
    return d

def parse_localConfig(fn='localConfig.yaml'):
    "parse gleaner cfg, ret: name2url dict .."
    d=yml2d(fn)
    sgD=d['sourcesSource']
    loc=sgD['location']
    if dbg: #where the Sources csv is
        print(f'loc={loc}')
    df=pd.read_csv(loc)
    if dbg:
        print(df)
    #really want to pull out repo-name&sitemap cols, to make a mapping dict
    d=df_cols2dict(df,"Name","URL")
    #d={'balto': 'http://balto.opendap.org/opendap/site_map.txt ' ...
    return d

def parse_nabu(fn='nabu'):
    "get prefix=sites crawled,&endpoint"
    d=yml2d(fn)
    obD=d['objects']
    reposP=obD['prefix']
    print(f'reposP={reposP}')
    #reposP=['summoned/opentopography', 'summoned/iris', 'summoned/hydroshare', 'summoned/iedadata', 'summoned/opentopography', 'summoned/iris', 'summoned/magic', 'summoned/earthchem', 'summoned/usap-dc']
    repos=list(map(path_leaf,reposP))
    print(f'repos={repos}')
    #could use this Path version for intermediate summoned counts next; see ec testing file
    sD=d['sparql']
    endpoint=sD['endpoint']
    #endpoint=https://graph.geocodes.ncsa.illinois.edu/blazegraph/namespace/earthcube2/sparql
    print(f'endpoint={endpoint}')
    return repos, endpoint


def crawl_cfg2counts():
    "use crawl cfg to pull out counts: sitemaps+graph"
    import ec
    repo2url = parse_localConfig()
    repos, endpoint = parse_nabu()
    #then map repo2url on repos -> sitemaps
    urls=list(map(lambda r: repo2url[r], repos))
    print(f'urls={urls}')
    #map ec sitemap_counts over that -> output1 
    sitemaps_count = ec.sitemaps_count(urls)
    print(f'sitemaps_count={sitemaps_count}')
    #sitemaps_count={'https://opentopography.org/sitemap.xml': 780, 'http://ds.iris.edu/files/sitemap.xml': 28, 'https://www.hydroshare.org/sitemap-resources.xml': 13932, 'http://get.iedadata.org/doi/xml-sitemap.php': 10099, 'https://www2.earthref.org/MagIC/contributions.sitemap.xml': 4332, 'https://ecl.earthchem.org/sitemap.xml': 650, 'https://www.usap-dc.org/view/dataset/sitemap.xml': 963}
    #ec graph_counts as 2nd part of final jina2/streamlit template
    gpr=ec.get_graph_per_repo("milled",endpoint) #setting off/so fix
    #next jina2/streamlit

def t1():
    "test:could pass through lc&nabu file names if they change"
    crawl_cfg2counts()
