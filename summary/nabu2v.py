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

#tmp_endpoint=f'https://graph.geocodes.ncsa.illinois.edu/{namespace}/sparql'

def ttl2blaze(endpoint=GRAPH_HOST, summary_namespace=SUMMARY_V):
    "end of summarization upload the triples"
    #cs=f'ttl2blaze.sh {endpoint}/blazegraph/namespace/{summary_namespace}/sparql'
    cs=f'ttl2blaze.sh {endpoint}/{summary_namespace}/sparql'
    if not dbg:
        os_system_(cs)

def nq2blaze(endpoint=GRAPH_HOST, big_namespace=BIG_V):
    "also have quads from this, so can upload here too"
    #cs=f'nq2blaze.sh {endpoint}/blazegraph/namespace/{big_namespace}/sparql'
    cs=f'nq2blaze.sh {endpoint}/{big_namespace}/sparql'
    if not dbg:
        os_system_(cs)

#like kglab might: from icecream import ic 
#@click.option('--endpoint',  help='url of triplestore we load to.')
#@click.option('--endpoint', default=GRAPH_HOST, help='url of triplestore we load to.')
#def nabu2v(endpoint=GRAPH_HOST, summary_namespace=SUMMARY_V, big_namespace=BIG_V):
    #print(f'using GRAPH_HOST= {endpoint}, summary={summary_namespace}, main={big_namespace}')
    #log.info(f'using GRAPH_HOST= {GRAPH_HOST}, summary={SUMMARY_V}, main={BIG_V}')
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
    #ttl2blaze(endpoint, SUMMARY_V)
    #nq2blaze(endpoint, BIG_V)

if __name__ == '__main__':
#   #if(len(sys.argv)>1): #will go back to click once I see it work
#   #    namespace_version= sys.argv[1]
#   #    log.info(f'got {namespace_version} to append to namespaces')
#   #    #global SUMMARY_V, BIG_V
#   #    SUMMARY_V += namespace_version
#   #    BIG_V += namespace_version
    nabu2v()
