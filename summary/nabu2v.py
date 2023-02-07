#!/bin/env python3
#started as sh file, now  python ;M Bobak ;was going to call present sh files, but could do it all here
#Expect namespaces have been made, and are empty, if not making an addition
#this uploads the .ttl and .nq that we have from the summarization process, to https://graph.{$HOST}
#can just give the version to upload that will be appended to the default namespaces 'summary'&'earthcube'
#call: nabu-v.sh ""  ;the 1st time , and can use: nabu-v.sh 2  ;etc after as long as summary{$V} & earthcube{$V} exist
import sys
import os
dbg=False
#import click #1st day, I'd like it just to call and fill them, so I can say search works/waiting2long4automation/s
GRAPH_HOST = "https://geocodes.ncsa.illinois.edu"
SUMMARY_V = "summary"
BIG_V = "earthcube"
print(f'default GRAPH_HOST= {GRAPH_HOST}, summary={SUMMARY_V}, main={BIG_V}')
#will want to at least check that namespace exist, and inhibit trying to fill if not there
gh= os.getenv("GRAPH_HOST")
if gh:
    GRAPH_HOST=gh
    print(f'using env-var for GRAPH_HOST= {GRAPH_HOST}')

#from ec.py
def os_system_(cs):
    "system call w/return value"
    s=os.popen(cs).read()
    #add2log(cs)
    return s

#@click.command()
#@click.option('--endpoint', default=GRAPH_HOST, help='url of triplestore we load to.')
#@click.option('--endpoint', default="https://geocodes.ncsa.illinois.edu", help='url of triplestore we load to.')
#@click.option('--endpoint',  help='url of triplestore we load to.')
#Error: Got unexpected extra arguments (h t t p s : / / g e o c o d e s . n c s a . i l l i n o i s . e d u) 

#get util fncs to get dir listings filtered by file type, and then do a requsts version of what shell file was doing
 #though for 1st shot could just call the upload shell files we have been using

def ttl2blaze(endpoint=GRAPH_HOST, summary_namespace=SUMMARY_V):
    "end of summarization upload the triples"
    cs=f'ttl2blaze.sh {endpoint}/blazegraph/namespace/{summary_namespace}/sparql'
    print(f'will run: {cs}')
    if not dbg:
        os_system_(cs)

def nq2blaze(endpoint=GRAPH_HOST, big_namespace=BIG_V):
    "also have quads from this, so can upload here too"
    cs=f'nq2blaze.sh {endpoint}/blazegraph/namespace/{big_namespace}/sparql'
    print(f'will run: {cs}')
    if not dbg:
        os_system_(cs)

def nabu2v(endpoint=GRAPH_HOST, summary_namespace=SUMMARY_V, big_namespace=BIG_V):
    print(f'using GRAPH_HOST= {GRAPH_HOST}, summary={SUMMARY_V}, main={BIG_V}')
    #print(f'using GRAPH_HOST= {endpoint}, summary={summary_namespace}, main={big_namespace}')
    #ttl2blaze(endpoint, summary_namespace) #rework/fix these
    #nq2blaze(endpoint, big_namespace)
    ttl2blaze(endpoint, SUMMARY_V)
    nq2blaze(endpoint, BIG_V)

if __name__ == '__main__':
    if(len(sys.argv)>1): #will go back to click once I see it work
        namespace_version= sys.argv[1]
        print(f'got {namespace_version} to append to namespaces')
        #global SUMMARY_V, BIG_V
        SUMMARY_V += namespace_version
        BIG_V += namespace_version
    nabu2v()
