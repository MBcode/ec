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

def httpP(str):
    #str.startswith('http')
    return str.startswith('http')

def getURLs(l):
    if isinstance(l,str):
        l=l.split()
    #filter(httpP,l)
    return filter(httpP,l)

#csq2.py go back to the clowder ID's so don't have to change html gen much right now
cs=f'/usr/bin/python3 sq2.py {qry_str}|curl $dcs_url -F "dcs.output.format=JSON" -F "dcs.c2stream=@-"'
#cs=f'/usr/bin/python3 sq1.py {qry_str}|curl $dcs_url -F "dcs.output.format=JSON" -F "dcs.c2stream=@-"'
#would like to go back to sq2.py and use the cID's, but 
 #also want to keep from being clowder centric
#sq1 has list indecies for id's
s=os.popen(cs).read()
#d=xmltodict.parse(s)
#print(s) #origninal
dct=json.loads(s)
docs=dct['documents']
nd=len(docs)
#print(f'got {nd} hits')
cls=dct['clusters']
nc=len(cls)
#print(f'got {nc} clusters')
#
#i2dj ={}
i2d ={} #id to doc info,  docs already looks good, but want like original js but w/tags in it
i2j ={} #ld
i2t ={} #tags

#def cls2docs(cls)
def cls2docs():
    for c in cls:
        phr=first(c['phrases'])
        ds=c['documents']
        ncd=len(ds)
    #   print(f'{ncd} docs for:{phr}')
        for d in ds:
#           print(f'{d}')
     #      id=int(d) #check for off by 1 error
    #       print(f'{id}<{nd}')
            #if sq2.py used i for id instead of cid, then this would work,now have2 lookup
            # difficult2init the dict2 = collections.defaultdict(list)   #consider just add while converting to html anyway
     #      did=docs[id]
            #oldprh=i2t[d]
            oldphr=i2t.get(d)
            if oldphr:
                oldphr=[oldphr]
                i2t[d]=oldphr.append(phr)
            else:
                i2t[d]=phr
            #print(did) #should rename to tags
    #       dc=did.get("clusters") #put phrases here
    #       if not dc:
    #           #did['clusters']= collections.defaultdict(list)
    #           did['clusters']= [phr]
    #           print(f'add clusters key to:{did}')
    #       else:
    #           did['clusters']= dc.append(phr)
            #docs[id]['clusters'].append(phr)
#print(s)
#-
def getjsonLD(datasetID):
    "given clowder dataset id: return it's saved()jsonLD"
    r = requests.get(f'{clowder_host}/api/datasets/{datasetID}/metadata.jsonld')
    return  first(r.json())
#-
ids=[]
#w/sq1 vs sq2 which has cID,  not sure if the clowder lookup (c)id is being stored anywhere
 #tried in sq1.py put the cID at the end, last/d4d line of the snippet
def doc2dcts():
    for h in docs:
        id=h['id']
        url=h['url']
        snip=h['snippet']
        #nd=url.split("\n")   #check
        nd=snip.split("\n")   #check
        name=nd[0] 
        description=nd[1] 
        #cid=nd[2]  #back w/sq2 w/cid and didn't need to put in snippet anymore
        cid=id
#       print(f'cid={cid}') #need to index by this so I can fill tags by this lookup
        ids.append(cid)
        #ld=len(description)
        #print(f'{id}:{name}:ldes={ld}') #now turn into a dict, w/name,description&LD
        i2d[id]=nd
        #i2d[id]['id']=cid
    #   i2d[id]['name']=name
    #   i2d[id]['description']=description
        #i2d[id]['tags']=h['clusters']
#       ld=getjsonLD(id)
#       nld=len(ld)
#       print(f'{id}:{nd}:ldes={nld}') #now turn into a dict, w/name,description&LD
#       i2j[id]=ld

#print("_doc2dcts")
doc2dcts()
#print("_cls2docs")
cls2docs()

#from ff.py
def cj1h(r):
    "clowder(1)json ret to html"
    name=r['name']
    des=r['description']
    url=first(getURLs(des))
    url2= clowder_host + '/datasets/' + r['id'] #use metadata-tab for 'details'
    rh=f'<div class="rescard"><div class="resheader"><a href="{url}">{name}</a></div>'
    rb=f'<div class="rescontiner"><a href="{url}"><p>{des}</p><a href="{url2}">details</a><p></div></div>'
    rs=rh+rb
    print(rs) #for now

def i2h(i):
    "cid to html for the hit"
    nd=i2d[i]
    name=nd[0]
    des=nd[1]
    tags=i2t[i]
    url=first(getURLs(des))
    url2= clowder_host + '/datasets/' + i #use metadata-tab for 'details'
    rh=f'<div class="rescard"><div class="resheader"><a href="{url}">{name}</a></div>'
    #rb=f'<div class="rescontiner"><a href="{url}"><p>{des}</p><a href="{url2}">details</a><p></div></div>'
    rb=f'<div class="rescontiner"><a href="{url}"><p>{des}</p><a href="{url2}">details</a>'
    rc=f'<a href="#clusters">subtopic:{tags}</a><p></div></div>' #might link to specific cluster and have those have links to all hits
    rs=rh+rb
    print(rs) #for now

#get the fillSearch cj2h function to be running off this new json vs the direct clowder json returns
 #or could get something just like those rets w/the extra info
  #&/or keep more like sparql returns which is what we will be using for the most part
#think cluster loop alters s, by putting the tags in each doc-hit
#print(s)
#print(docs)
#print(json.dumps(docs, indent=2))
#want these together to do it

#print("_i2d")
#print(json.dumps(i2d, indent=2))
#print("_i2t")
#print(json.dumps(i2t, indent=2))
#print("_now-by-ids")
for i in ids:
    i2h(i)
#    print(i)
#    print(i2d[i])
#    tags=i2t[i]
#    print(f'tags:{tags}')
