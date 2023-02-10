#!/usr/bin/env python3
#started as sh file, now  python ;M Bobak ;was going to call present sh files, but could do it all here
#Expect namespaces have been made, and are empty, if not making an addition
#this uploads the .ttl and .nq that we have from the summarization process, to https://graph.{$HOST}
#can just give the version to upload that will be appended to the default namespaces 'summary'&'earthcube'
#call: nabu-v.sh ""  ;the 1st time , and can use: nabu-v.sh 2  
 #2 etc after/as long as summary{namespace_version} & earthcube{namespace_version} exist
import logging as log
log.basicConfig(filename='nabu2v.log', encoding='utf-8', level=log.DEBUG,
                format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
import sys
import os
dbg=False
#dbg=True
import click #1st day, I'd like it just to call and fill them, so I can say search works/waiting2long4automation/s
GRAPH_HOST = "https://graph.geocodes.ncsa.illinois.edu"
SUMMARY_V = "summary"
BIG_V = "earthcube"
log.info(f'default GRAPH_HOST= {GRAPH_HOST}, summary={SUMMARY_V}, main={BIG_V}')
#will want to at least check that namespace exist, and inhibit trying to fill if not there
gh= os.getenv("GRAPH_HOST")
if gh:
    GRAPH_HOST=gh
    log.warning(f'using env-var for GRAPH_HOST= {GRAPH_HOST}')

#from ec.py
def os_system_(cs):
    "system call w/return value"
    s=os.popen(cs).read()
    log.info(f'will run: {cs}')
    return s


#get util fncs to get dir listings filtered by file type, and then do a requsts version of what shell file was doing
 #though for 1st shot could just call the upload shell files we have been using
 #will do this now, incl click agrparse, and py-logging ;will update nabu2v.md to show use of requests
 #_could still allow upload of repo.nq to make sure sync'd w/summary.ttl, but go nabu can do that as well

#get util fncs to get dir listings filtered by file type, and then do a requsts version of what shell file was doing
#from ec.py
def flatten(xss): #stackoverflow
    "make list of lists into 1 flat list"
    return [x for xs in xss for x in xs]

def file_ext(fn):
    "the ._part of the filename"
    st=os.path.splitext(fn)
    #log.info(f'fe:st={st}')
    return st[-1]

def collect_ext(l,ext):
  return list(filter(lambda x: file_ext(x)==ext,l))
  #return list(filter(lambda x: file_ext(x)==ext,flatten(l)))
#>>> l=ls_()  ;dbg
#>>> collect_ext(l,".ttl")
#['earthchem.ttl', 'hydroshare.ttl', 'iedadata.ttl', 'iris.ttl', 'magic.ttl', 'opentopography.ttl', 'usap-dc.ttl']

def ls(dir): #there are other py commands to do this
    cs=f'ls {dir}'
    return os_system_(cs)
    
def ls_(path="."):
    lstr=ls(path)
    return lstr.split("\n")

#and some new/different from in utils
#https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
def ls_b(mypath="."):
    "list files"
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

def ls_ext(dir=None,ext=None):
    "file in . w/ext"
    l=ls_()
    log.debug(f'ls={len(l)}')
    ret = collect_ext(l,ext)
    log.debug(f'ls_ext={ret}')
    return ret

#tmp_endpoint=f'https://graph.geocodes.ncsa.illinois.edu/{namespace}/sparql'

#other than getting rid of the scripts we used to use, want to:
#https://github.com/blazegraph/database/wiki/REST_API#create-data-set
#https://github.com/blazegraph/database/wiki/REST_API#destroy-data-set
#maybe some from: https://github.com/blazegraph/blazegraph-python vs all by hand

def ttl2blaze(endpoint=GRAPH_HOST, summary_namespace=SUMMARY_V):
    "end of summarization upload the triples"
    log.info(f'ttl2blaze using endpoint={endpoint}, summary_ns={summary_namespace}')
    #cs=f'ttl2blaze.sh {endpoint}/{summary_namespace}/sparql'
    #os_system_(cs)
    cs=f'{endpoint}/{summary_namespace}/sparql'
    l=ls_ext(".ttl")
    log.debug(f'would upload {l} to summary namespace at {cs}')

def nq2blaze(endpoint=GRAPH_HOST, big_namespace=BIG_V):
    "also have quads from this, so can upload here too"
    log.info(f'nq2blaze using endpoint={endpoint}, big_ns={big_namespace}')
    #cs=f'nq2blaze.sh {endpoint}/{big_namespace}/sparql'
    #os_system_(cs)
    cs=f'{endpoint}/{big_namespace}/sparql'
    l=ls_ext(".nq")
    log.debug(f'would upload {l} as an option, to {cs}')

#like kglab might: from icecream import ic 
@click.command()
@click.option('--endpoint', default="https://graph.geocodes.ncsa.illinois.edu", help='url of triplestore we load to.')
@click.option('--summary_namespace', default="summary", help='namespace repo.ttl is uploaded to')
@click.option('--big_namespace', default="earthcube", help='namespace repo.nq could be uploaded to')
@click.option('--namespace_version', default=None, help='potential number to append to namespaces')
def nabu2v(endpoint, summary_namespace, big_namespace, namespace_version):
    "will use requests/lib to upload to namespace/s"
    if namespace_version:
        log.warning(f'will append {namespace_version} to both namespaces')
        summary_namespace += namespace_version
        big_namespace += namespace_version
    log.info(f'using endpoint={endpoint}, summary_ns={summary_namespace}, big_ns={big_namespace},v={namespace_version}')
    ttl2blaze(endpoint, summary_namespace) #rework/fix these
    nq2blaze(endpoint, big_namespace)
    log.info(f'check {endpoint} to see if loaded')
    #ttl2blaze(endpoint, SUMMARY_V)
    #nq2blaze(endpoint, BIG_V)

if __name__ == '__main__':
    nabu2v()
