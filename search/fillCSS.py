import requests
import json
import sys
import os
clowder_host = os.getenv('clowder_host')
if(len(sys.argv)>1):
    qry_str = sys.argv[1]
else:
    qry_str = "carbon"

#from assert code utils:
def first(l):
    if isinstance(l,list):
        return l[0]
    else:
        return l

def httpP(str):
    str.startswith('http')

def getURLs(l):
    filter(httpP,l)
#

def cq(qry_str):
    "clowder search query"
    r = requests.get(f"{clowder_host}/api/search?query={qry_str}")
    if(r.status_code == 200):
        #ret = json.dumps(r.json()['results'], indent=2)
        ret = r.json()['results']
        return ret
    else:
        return r.status_code

def cj2h(j):
    "clowder json ret to html"
    #if(len(j)>1)
    for r in j:
        name=r['name']
        des=r['description']
        #will want to get url
        url=httpP(des) #bool, need actual url
        rh=f'<div class="rescard"><div class="resheader"><a href="{url}">{name}</a></div>'
        rb=f'<div class="rescontiner"><a href="{url}><p>{des}</p></div>'
        #I do not see ec score from clowder  to put /\
        rs=rh+rb
        print(rs) #for now

#if I ran carrot2 dcs clustering, could just add keyword like links to the clusters that each is in
 #could generate a page for each of these clusters, that is just a filtering of these returns w/in grp

rj=cq(qry_str)
print(rj)
#ret = json.dumps(r.json()['results'], indent=2)
print(json.dumps(rj, indent=2))
cj2h(rj)
