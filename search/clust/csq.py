#this supercedes csq.sh, but still uses sq2.py to do the search and cluster it
#import xmltodict #prefer to have curl below dump in json format
import collections
import requests
import json
import sys
import os
clowder_host = os.getenv('clowder_host')
if(len(sys.argv)>1):
    qry_str=sys.argv[1]
else:
    qry_str = "organic"

def first(l):
    from collections.abc import Iterable
    if isinstance(l,list):
        return l[0]
    elif isinstance(l,Iterable):
        return list(l)[0]
    else:
        return l

#cs=f'/usr/bin/python3 sq2.py {qry_str}|curl $dcs_url -F "dcs.output.format=JSON" -F "dcs.c2stream=@-"'
cs=f'/usr/bin/python3 sq1.py {qry_str}|curl $dcs_url -F "dcs.output.format=JSON" -F "dcs.c2stream=@-"'
#sq1 has list indecies for id's
s=os.popen(cs).read()
#d=xmltodict.parse(s)
print(s)
dct=json.loads(s)
docs=dct['documents']
nd=len(docs)
print(f'got {nd} hits')
cls=dct['clusters']
nc=len(cls)
print(f'got {nc} clusters')
for c in cls:
    phr=first(c['phrases'])
    ds=c['documents']
    ncd=len(ds)
    print(f'{ncd} docs for:{phr}')
    for d in ds:
        #print(f'{d}')
        id=int(d)
        print(f'{id}<{nd}')
        #if sq2.py used i for id instead of cid, then this would work,now have2 lookup
        # difficult2init the dict2 = collections.defaultdict(list)   #consider just add while converting to html anyway
        did=docs[id]
        #print(did) #should rename to tags
        dc=did.get("clusters") #put phrases here
        if not dc:
            #did['clusters']= collections.defaultdict(list)
            did['clusters']= [phr]
            print(f'add clusters key to:{did}')
        else:
            did['clusters']= dc.append(phr)
        #docs[id]['clusters'].append(phr)
#print(s)
#-
def getjsonLD(datasetID):
    "given clowder dataset id: return it's saved()jsonLD"
    r = requests.get(f'{clowder_host}/api/datasets/{datasetID}/metadata.jsonld')
    return  first(r.json())
#-
#i2dj ={}
i2d ={}
i2j ={}
for h in docs:
    id=h['id']
    url=h['url']
    nd=url.split("\n")   #check
    #name=nd[0] 
    #description=nd[1] 
    #ld=len(description)
    #print(f'{id}:{name}:ldes={ld}') #now turn into a dict, w/name,description&LD
    i2d[id]=nd
    ld=getjsonLD(id)
    nld=len(ld)
    print(f'{id}:{nd}:ldes={nld}') #now turn into a dict, w/name,description&LD
    i2j[id]=ld

#AttributeError: 'collections.defaultdict' object has no attribute 'append'

#get the fillSearch cj2h function to be running off this new json vs the direct clowder json returns
 #or could get something just like those rets w/the extra info
  #&/or keep more like sparql returns which is what we will be using for the most part
#think cluster loop alters s, by putting the tags in each doc-hit
#print(s)
print(docs)
