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

def first__(l):
    from collections.abc import Iterable
    if isinstance(l,list):
        return l[0]
    elif isinstance(l,Iterable):
        return list(l)[0]
    else:
        return l

def first(l):
    from collections.abc import Iterable
    if isinstance(l,list):
        #return l[0]
        if len(l)>0:
            #return list(l)[0]
            return l[0]
        else:
            return l
#   elif isinstance(l,Iterable):
#       return list(l)[0]
    else:
        return l

def first_(l):
    from collections.abc import Iterable
    if isinstance(l,list):
        #return l[0]
        if len(l)>0:
            return list(l)[0]
        else:
            return l
    elif isinstance(l,Iterable):
        #return list(l)[0]
        if len(l)>0:
            return list(l)[0]
        else:
            return l
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
#----------------------
#-from sca2.py for csq2.py
import requests
clowder_host = "https://earthcube.clowderframework.org" 

#https://stackoverflow.com/questions/14048948/how-to-find-a-particular-json-value-by-key 
import json 
def deep_search(needles, haystack):
    found = {}
    if type(needles) != type([]):
        needles = [needles]

    if type(haystack) == type(dict()):
        for needle in needles:
            if needle in haystack.keys():
                found[needle] = haystack[needle]
            elif len(haystack.keys()) > 0:
                for key in haystack.keys():
                    result = deep_search(needle, haystack[key])
                    if result:
                        for k, v in result.items():
                            found[k] = v
    elif type(haystack) == type([]):
        for node in haystack:
            result = deep_search(needles, node)
            if result:
                for k, v in result.items():
                    found[k] = v
    return found

#print(deep_search(["P1", "P3"], json.loads(json_string)))
#{'P1': 'ss', 'P3': [{'P1': 'aaa'}]}
clowder_host = "https://earthcube.clowderframework.org" 
#clowder_key = os.getenv('eckey') #I can use locally w/new instance till it is fixed 
 #no longer needed

def full(l): #not used here now
    return (len(l) > 0)
#from fillSearch.py but most of this will be going in there anyway

def getif(dl,k):
    d=first(dl) #
    if isinstance(d, dict):
        #return d.get(k)
        ret= d.get(k)
        if ret:
            return ret
        else: return d
    else:
        return d

def getif1(d,k):
    if isinstance(d, dict):
        ret= d.get(k)
        if ret:
            return ret
        else: return d
    elif isinstance(d, list):
        getif(first(d),k)
    else:
        return d

def rgetif(d,kl): #not used here now
    print(f'd={d},kl={kl}')
    ret= getif(d,first(kl)) 
    #ret= getif1(d,first(kl)) 
    print(f'=ret={ret}')
    if isinstance(kl, list):
        if len(kl)>1:
            return rgetif(ret,rest(kl))
        else:
            return ret
    else:
        return ret

def get_jsonLD(datasetID):
    "given clowder dataset id: return it's saved()jsonLD"
    r = requests.get(f'{clowder_host}/api/datasets/{datasetID}/metadata.jsonld')
    return  first_(r.json())

def getjsonLD(datasetID):
    "given clowder dataset id: return it's saved()jsonLD"
    try: 
        r = requests.get(f'{clowder_host}/api/datasets/{datasetID}/metadata.jsonld')
    except:
        r=None
    if r:
        return  first_(r.json())
    else:
        return None

def pLDs2f(LD):
    "print more terse version of LDs2f" #use instead of pLD
    LDc=LD.get("content") 
    #m3=deep_search(["publisher", "spatialCoverage", "datePublished"], LDc) 
    #m3=deep_search(["publisher", "spatialCoverage", "Place", "datePublished"], LDc) 
    m3=deep_search(["publisher", "spatialCoverage", "geo", "datePublished"], LDc) 
    #pub1=getif(m3["publisher"],'')
    m3p=m3.get("publisher")
    #if m3p:
    if isinstance(m3p,dict):
        pub1=getif(m3p,'')
        pub=getif1(pub1,'name')
    else:
        pub=None
    m3s=""
    if pub:
        m3s += f'publisher:{pub},'
        #pub_tc[pub]+=1
        incrKeyCount(pub,pub_tc)
    #plc=m3["spatialCoverage"]['geo']
    #sc=m3["spatialCoverage"]
    #sc=m3.get("spatialCoverage")
    sc=first(m3.get("spatialCoverage"))
    if not sc:
        #sc=m3.get("geo")
        sc=first(m3.get("geo"))
    if isinstance(sc,dict):
        #plc=sc.get('geo')
        plc=first(sc.get('geo'))
    else:
        plc=sc
    #if plc:
    if isinstance(plc,dict):
        box=plc.get('box')
        if box:
            plc=box
    if plc:
        m3s += f'place:{plc},'
    #datep=m3["datePublished"]
    m3d=m3.get("datePublished")
    if m3d:
        datep=m3d
    else:
        datep = None
    if datep:
        m3s += f'date:{datep}'
        #date_tc[date]+=1
        datepy=datep.split('-')[0]
        incrKeyCount(datepy,date_tc)
    #print(m3s)
    return m3s

#I will also just be going from ID to LD, w/getjsonLD
 #in csq2/fillSearch, will have ID, and would like to get rest w/o needing result, so rewrite above to handle that
  #result wasn't needed/used, so removed
   #pLD is just filler right now to look at it, will be returning something going to html/filter-widgets soon
    #instead of pLD, might actually need varient of LDs2f, to get the format to get back to rescard/divs/etc
    #get just that, &pull out that handfull of fncs, in one file, and have either fillSearh|csq2 using it,load&call as needed

def i2f(id):
    "clowderID to facets2filter on"
    LD=getjsonLD(id)
    #pLD(LD, None)
    if LD:
        return pLDs2f(LD)
    else:
        return ""
#-
#i2f("5f827886e4b0b81250da6018")
#publisher:PANGAEA - Data Publisher for Earth & Environmental Science,place:-7.8801, 60.9205 -7.8787, 60.9249,date:2014
#----------------------
#csq2.py go back to the clowder ID's so don't have to change html gen much right now
cs=f'/usr/bin/python3 sq2.py {qry_str}|curl $dcs_url -F "dcs.output.format=JSON" -F "dcs.c2stream=@-"'
#cs=f'/usr/bin/python3 sq1.py {qry_str}|curl $dcs_url -F "dcs.output.format=JSON" -F "dcs.c2stream=@-"'
#would like to go back to sq2.py and use the cID's, but 
 #also want to keep from being clowder centric
#sq1 has list indecies for id's
s=os.popen(cs).read()
#d=xmltodict.parse(s)
#print(s) #origninal

#try:
#    dct=json.loads(s)
#except:
#    print(f'error w/json.loads:{s}')

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
i2tn ={} #tag(cluster)number, or better break out, index by tag-txt &get counts sort later
pub_tc = {}  
date_tc = {}  
plc_tc = {}  
#---
def d2htm(d):
    print(f'<TABLE border="1" style="border: 1px solid #000000; border-collapse: collapse;" cellpadding="4">')
    for k, v in d.items():
        print(f'<tr><td>{k}</td><td>{v}</td></tr>')
    print("</table>")

def d2html(d,title):
    dl=len(d)
    print(f'{title}:{dl}')
    d2htm(d)

def printFacetCounts2htm(): #new
    d2html(pub_tc,"Publications")
    d2html(date_tc,"DatePublished")
    d2html(plc_tc,"Place")
#---
 #only problem is it should default to 0
def incrKeyCount(key,d):
    v=d.get(key)
    if not v:
        d[key] = 0
    d[key] += 1

#def cls2docs(cls)
def cls2docs():
    for c in cls:
        phr=first(c['phrases'])
        ds=c['documents']
        ncd=len(ds)
        tn=c['id'] #tagnum,so can get cluster# later
    #   print(f'{ncd} docs for:{phr}')
        for d in ds:
#           print(f'{d}')
     #      id=int(d) #check for off by 1 error
    #       print(f'{id}<{nd}')
            #if sq2.py used i for id instead of cid, then this would work,now have2 lookup
            # difficult2init the dict2 = collections.defaultdict(list)   #consider just add while converting to html anyway
     #      did=docs[id]
            #oldprh=i2t[d]
            #I would expect to get more doubles at least, not all single tags, so check ;maybe not take 1st as well
            oldphr=i2t.get(d)
            if oldphr:
                oldphr=[oldphr]
                i2t[d]=oldphr.append(phr)
            else:
                i2t[d]=phr
                i2tn[d]=tn
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
#def getjsonLD(datasetID):
def getjson_LD(datasetID):
    "given clowder dataset id: return it's saved()jsonLD"
    r = requests.get(f'{clowder_host}/api/datasets/{datasetID}/metadata.jsonld')
    return  first_(r.json())
#-
ids=[]
#w/sq1 vs sq2 which has cID,  not sure if the clowder lookup (c)id is being stored anywhere
 #tried in sq1.py put the cID at the end, last/d4d line of the snippet
def doc2dcts():
    for h in docs:
        id=h['id']
        #url=h['url']
        url=h.get('url')
        if not url:
            url=""
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

def i2name(id):
    nd=i2d[id]
    name=nd[0] 
    return name

#when a cluster has a set of IDs can map over and get set of names, &turn to a comma sep list of links to id-anchors

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
    "cid to html for the hit" #consider .get(i), &skip if not there
    nd=i2d[i]
    name=nd[0]
    des=nd[1]
    tags=i2t[i] #i2t.get(i)
    tn=i2tn[i]
    #ctags=','.join(tags) #wanted commas in format v print, but that works below
    url=first(getURLs(des))
    url2= clowder_host + '/datasets/' + i #use metadata-tab for 'details'
    #rh=f'<div class="rescard"><div class="resheader"><a href="{url}">{name}</a></div>' #mved id to top of record
    rh=f'<div class="rescard" id="{i}"><div class="resheader"><a href="{url}">{name}</a></div>'
    ##rb=f'<div class="rescontiner"><a href="{url}"><p>{des}</p><a href="{url2}">details</a><p></div></div>'
    rb=f'<div class="rescontiner"><a href="{url}"><p>{des}</p><a href="{url2}">details</a> '
    #rb=f'<div class="rescontiner" id="{i}"><a href="{url}"><p>{des}</p><a href="{url2}">details</a> '
    #rc=f' subtopic:<a href="#clusters">{tags}</a><p></div></div>' #might link to specific cluster and have those have links to all hits
    #rs=rh+rb+rc
    rs=rh+rb   #above get an id= anchor in there so can jump to it from the cls2h/i2h_ links
    print(rs) #for now
    if tags: #if could have cluster# w/tags, then could ref2it directly
        if tn: #if had specific cluster id/anchor could link right to it, in a bit
            print(f' in_subtopic:<a href="#cluster{tn}">') 
        else:
            print(f' in_subtopic:<a href="#clusters">')  
        #print(' in_subtopic:<a href="#clusters">')  
        print(tags, sep=", ")
        print('</a><p>')
    f=i2f(i)
    if f:
        print(f'<small>{f}</small>')
    #next if: publisher, place, time-period
    print('</div></div>')

def i2h_(i):
    "short version of i2h for cluster links"
    nd=i2d[i]
    name=nd[0]
    rn=f'<a href="#{i}">{name}</a><br>'
    print(rn)
#probable-todo:
#will get a footer rescard, done w/look like in cls2docs, but for every doc-id get the name part of nd, so can display a list
 #cluster-phrase, then the name-link2anchor-id list for all docs in the cluster
 #might be best to have a rescard per cluster then
def cls2h():
    print(f'<a id="clusters">')
    for c in cls:
        i=c['id']
        ci='cluster'+str(i)
        phr=first(c['phrases'])
        ds=c['documents']
        sc=int(c['score'])
        #rh=f'<div class="rescard" id="{ci}"><div class="resheader">{phr}</a></div>'
        #rh=f'<div class="rescard" id="{ci}"><div class="resheader">{phr}  score:{sc}</a></div>'
        rh=f'<div class="rescard" id="{ci}"><div class="resheader">{phr}</a>  <i><small>score:{sc}</small></i></div>'
        rb=f'<div class="rescontiner">'
        print(rh+rb)
        for d in ds:
            i2h_(d)
        print('</div></div></div>')

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
printFacetCounts2htm() #new, might have to try here to start bc calc when html generated
cls2h() #get a few more rescards w/the cluster info, and links back up
