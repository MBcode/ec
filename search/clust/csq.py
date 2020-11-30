#this supercedes csq.sh, but still uses sq2.py to do the search and cluster it
#import xmltodict #prefer to have curl below dump in json format
import collections
import json
import sys
import os
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
        #print(did)
        dc=did.get("clusters")
        if not dc:
            did['clusters']= collections.defaultdict(list)
            print(f'add clusters key to:{did}')
        #docs[id]['clusters'].append(phr)
#print(s)

#AttributeError: 'collections.defaultdict' object has no attribute 'append'

#get the fillSearch cj2h function to be running off this new json vs the direct clowder json returns
 #or could get something just like those rets w/the extra info
  #&/or keep more like sparql returns which is what we will be using for the most part
