#!/usr/bin/env python3
#mbobak, parse crawl cfg, to get sitemap+graph to get counts from them
#can be done from cli, dagster wf-elt, or notebook
import pandas as pd
#dbg=True
dbg=False
cache=True
#cache=False
import logging as log   #can switch print's to log.info's but Readme expects it to the stdout
log.basicConfig(filename='parseConfig.log', encoding='utf-8', level=log.DEBUG,
                format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

#from mb.py part of utils, for now
def path_leaf(path):
    "everything after the last /"
    import ntpath
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def put_txtfile(fn,s,wa="a"): #or w
    "filename to dump string to"
    with open(fn, wa) as f:
        return f.write(s)

#=merge using:
def merge_dict_list(d1,d2):
    from collections import defaultdict
    dd = defaultdict(list)
    for d in (d1, d2): # you can list as many input dicts as you want here
        for key, value in d.items():
            dd[key].append(value)
    return dd

def len_gt1(l):
    "len >1 predicate"
    b=(len(l) > 1)
    if dbg:
        print(f'l={l},b={b}')
    return b

def val_len_gt1(p):
    "len_gt1 on value of a pair"
    v=p[1]
    return len_gt1(v)

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
            log.warning(e) 
            return None

def df_cols2dict(df,c1,c2):
    "make a dict from 2 df cols"
    #d={}
    log.info(f'will pull out, c1={c1},c2={c2}')
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
    log.info(f'reposP={reposP}')
    #reposP=['summoned/opentopography', 'summoned/iris', 'summoned/hydroshare', 'summoned/iedadata', 'summoned/opentopography', 'summoned/iris', 'summoned/magic', 'summoned/earthchem', 'summoned/usap-dc']
    repos=list(map(path_leaf,reposP))
    log.info(f'repos={repos}')
    #could use this Path version for intermediate summoned counts next; see ec testing file
    sD=d['sparql']
    endpoint=sD['endpoint']
    log.info(f'endpoint={endpoint}')
    #endpoint=https://graph.geocodes.ncsa.illinois.edu/blazegraph/namespace/earthcube2/sparql
    endpoint2=sD.get('summary')
    if endpoint2:
        print(f'got summary endpoint:{endpoint2}')
    else:
        endpoint2="https://graph.geocodes.ncsa.illinois.edu/blazegraph/namespace/earthcube2/sparql"
        print(f'this is where I could alter the main endpoint to look more like: {endpoint2}')
    return repos, endpoint, endpoint2

def crawl_cfg2counts(lc_fn="localConfig.yaml",nabu_fn="nabu",outputHTM="count_dropoff.htm",outputDIR=None):
    "use crawl cfg to pull out counts: sitemaps+graph"
    #import ec
    import sitemap as ec #need put txtfile
    import query as q
    log.info("====crawl_cfg2counts===")
    repo2url = parse_localConfig(lc_fn)
    log.info(f'repo2url={repo2url}')
    repos, endpoint, endpoint2 = parse_nabu(nabu_fn)  #want to get summary endpoint, right now using hard-coded;will make issue
    #then map repo2url on repos -> sitemaps
    urls=list(map(lambda r: repo2url[r], repos)) #or just use values/no
    log.info(f'urls={urls}') #might need to make repo:url dict
    #map ec sitemap_counts over that -> output1 
    if not cache: #need a version of this that is repo-name: num,  so can merge w/graph_per_repo dict
        #sitemaps_count = ec.sitemaps_count(urls) #only ec fnc used, so will pull out
        sitemaps_count = ec.sitemaps_d_count(repo2url) #only ec fnc used, so will pull out
    else: #so don't have to pull each time we test
       #sitemaps_count={'https://opentopography.org/sitemap.xml': 780, 'http://ds.iris.edu/files/sitemap.xml': 28, 'https://www.hydroshare.org/sitemap-resources.xml': 13932, 'http://get.iedadata.org/doi/xml-sitemap.php': 10099, 'https://www2.earthref.org/MagIC/contributions.sitemap.xml': 4332, 'https://ecl.earthchem.org/sitemap.xml': 650, 'https://www.usap-dc.org/view/dataset/sitemap.xml': 963}
        sitemaps_count={'balto': 0, 'neotomadb': 45936, 'decade': 0, 'renci': 0, 'c4rsois': 0, 'resource_registry': 0, 'datadiscoverystudio': 0, 'unidata': 211, 'aquadocs': 0, 'opentopography': 780, 'iris': 28, 'edi': 0, 'bco-dmo': 0, 'hydroshare': 13935, 'iedadata': 10099, 'unavco': 5693, 'ssdb.iodp': 26156, 'linked.earth': 18634, 'lipdverse': 27, 'ucar': 17696, 'opencoredata': 0, 'magic': 4332, 'earthchem': 650, 'xdomes': 0, 'neon': 0, 'designsafe': 0, 'r2r': 47462, 'geocodes_demo_datasets': 9, 'usap-dc': 962, 'cchdo': 2523, 'amgeo': 0, 'wifire': 0, 'cresis': 0}
    log.info(f'sitemaps_count={sitemaps_count}') #need to get this usable by merge_dict_list
    #ec graph_counts as 2nd part of final jina2/streamlit template
    #gpr=ec.get_graph_per_repo("milled",endpoint) #setting off/so fix
    log.info(f'q.get_graph_per_repo {endpoint2}')  #this is from summary, might also do from main
    gpr=q.get_graph_per_repo("",endpoint2) #setting off/so fix
    log.info(f'gpr={gpr}') #get this into a dict, in rev order, now: 6084 hydroshare ...
    #gt=type(gpr)
    #print(f'gpr={gpr},type:{gt}') 
    rc_d=df_cols2dict(gpr,"g","1")
    log.info(f'rc_d={rc_d}') #so this is useable w/merge_dict_list
    #def repos2counts(repos): does some of this splitting the lines/etc
    count_dropoff=merge_dict_list(sitemaps_count,rc_d)
    log.info(f'count_dropoff={count_dropoff}')
    import pprint
    pretty_dict_str = pprint.pformat(count_dropoff)
    log.info(pretty_dict_str)
    #next jina2/streamlit #here we could even start a dynamic info page, 
    #even w/the pygal.sparktext, but for now only pull out repo-s w/a dropoff,eg.len(value)>1
    #        'cchdo': [2523, 2517],
    #        'designsafe': [0, 458],
    #        'earthchem': [650, 917],
    #        'edi': [0, 8303],
    #        'hydroshare': [13935, 6084],
    #        'iedadata': [10099, 6455],
    #        'iris': [28, 43],
    #        'linked.earth': [18634, 698],
    #        'opentopography': [780, 773],
    #        'r2r': [47462, 1],
    #        'ssdb.iodp': [26156, 25225],
    #        'unavco': [5693, 7377],
    #        'usap-dc': [962, 912],
    #should change the dicts or merge_dict_list, so a placeholder is put if not in one of them
    # though for sparkline/plotting can only show numeric, so set to 0 even if missing
  # result=count_dropoff
  # import jinja2
  # template= """<table> <thead> <tr> <th>Key</th> <th>Value</th> </tr> </thead>
  #           <tbody>
  #           {% for key, value in result.items() %}
  #            <tr> <td> {{ key }} </td> <td> {{ value }} </td> </tr>
  #           {% endfor %} </tbody> </table>"""
  # #print(template.render(result))
  # print(template)
    #probably easier w/pd: 
    #stackoverflow.com/questions/41671436/how-can-i-convert-a-python-dictionary-to-an-html-table
    #raise ValueError("All arrays must be of the same length") #just have to filter as above
    result=dict(filter(val_len_gt1,count_dropoff.items()))
    log.info(f'result={result}')
    df = pd.DataFrame(data=result)
    df = df.fillna(' ').T
    #df_=df.rename(columns={'0': 'sitemap', '1': 'graph'}) #not there so:
    df.columns =['sitemap','graph']
    #dfh=df.to_html() #easier than jinja right now
    dfh=df.to_html() 
    if dbg:
        print(f'df={df}')
        print(f'dfh={dfh}')
    #ec.put_txtfile("count_dropoff.htm",dfh) #appending right now, can send in 3rd are to Replace
    #ec.put_txtfile(outputHTM,dfh) #appending right now, can send in 3rd are to Replace
    if outputDIR:
        outputHTM= outputDIR + "/" + outputHTM
    put_txtfile(outputHTM,dfh) #appending right now, can send in 3rd are to Replace
    return result

def t1():
    "test:could pass through lc&nabu file names if they change"
    return crawl_cfg2counts()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--localConfig",  help='localConfig.yaml is the default', default='localConfig.yaml')
    parser.add_argument("--nabu",  help='nabu is the default', default='nabu')
    parser.add_argument("--outputHTM",  help='output html table default is count_dropoff.htm', default='count_dropoff.htm')
    parser.add_argument("--outputDIR",  help='output directory, default to none right now', default=None)
    args = parser.parse_args()
    crawl_cfg2counts(args.localConfig,args.nabu,args.outputHTM,args.outputDIR)
