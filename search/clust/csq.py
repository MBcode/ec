#this supercedes csq.sh, but still uses sq2.py to do the search and cluster it
#import xmltodict #prefer to have curl below dump in json format
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

cs=f'/usr/bin/python3 sq2.py {qry_str}|curl $dcs_url -F "dcs.output.format=JSON" -F "dcs.c2stream=@-"'
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
    p=first(c['phrases'])
    ds=c['documents']
    ncd=len(ds)
    print(f'{ncd} docs for:{p}')
    for d in ds:
        print(f'{d}')
        #if sq2.py used i for id instead of cid, then this would work,now have2 lookup
        #docs[d]['clusters'].append(p)
#print(s)
