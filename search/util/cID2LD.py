#======================cID2LD.py
#want to step towards really not just being tied2clowder, but will start w/also caching it's cache
 #nice2have utils, but settle on what should be ret, &maybe just test4that
import requests
import json
import sys
import os
clowder_host = os.getenv('clowder_host')

#sq.py
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
    #return filter(httpP,l)
    #return list(filter(httpP,l))
    ret= list(filter(httpP,l))
    if len(ret)<1:
        return ""
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

def get_txtfile(fn):
    with open(fn, "r") as f:
        return f.read()

def get_jsonfile(fn):
    t=get_txtfile(fn)
    return json.loads(t)

def getContent(ld):
    if isinstance(ld,dict):
        LDc= ld.get("content")
        #lldc=len(LDc)
        #print(f'content:{lldc}') #dbg
        return LDc
    else:
        return ld

def cID2LD(cID):  
    ccf = "cc/" + cID + ".jsonld"
    if os.path.exists(ccf) and os.stat(ccf).st_size >0:
        #with open(ccf, "r") as rf:
        #    d=json.loads(rf)
        LD=get_jsonfile(ccf)
        LD=getContent(LD)
        return LD
    else:
        LD = getjsonLD(cID)
        if LD:
            LD=getContent(LD)
            #should try, bc more important to ret than aave
            try:
                with open(ccf, "w") as of:
                    of.write(json.dumps(LD))
            except:
                raise Warning(f'can not write:{ccf}')
            return LD
        else:
            raise Warning(f'no LD for:{ccf}')
            return None

def gd(id):
    print(cID2LD(id))
#======================new:
def first(l):
    from collections.abc import Iterable
    if isinstance(l,list):
        return l[0]
    elif isinstance(l,Iterable):
        return list(l)[0]
    else:
        return l

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
    #print(f'd={d},kl={kl}')
    ret= getif(d,first(kl))
    #ret= getif1(d,first(kl))
    #print(f'=ret={ret}')
    if isinstance(kl, list):
        if len(kl)>1:
            return rgetif(ret,rest(kl))
        else:
            return ret
    else:
        return ret

#======================new:
#from csq2.py /gm.py
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

def pLDs2f(LD):
    "print more terse version of LDs2f" #use instead of pLD
    LDc=LD.get("content")
    m3=deep_search(["publisher", "spatialCoverage", "datePublished"], LDc)
    pub1=getif(m3["publisher"],'')
    m3s=""
    pub=getif1(pub1,'name')
    if pub:
        m3s += f'publisher:{pub},'
    plc=m3["spatialCoverage"]['geo']
    if plc:
        box=plc.get('box')
        if box:
            plc=box
    if plc:
        m3s += f'place:{plc},'
    datep=m3["datePublished"]
    if datep:
        m3s += f'date:{datep}'
    #print(m3s) #dbg
    return m3s

#new
def LD2md(LD):   #based on pLDs2f(LD):
    "search LD content for keys&ret in dict"
    if isinstance(LD,list): #check
        LD= first_(LD) 
    md={} #like m3s str
    #print(LD) #dbg
    #LDc=LD.get("content")
    LDc=getContent(LD)
    if not LDc:
        return None
    m3=deep_search(["publisher", "spatialCoverage", "datePublished"], LDc)
    #=publisher
    pub1=getif(m3["publisher"],'')
    pub=getif1(pub1,'name')
    if pub:
        md['pub']=pub
    #=place
    #plc=m3["spatialCoverage"]['geo']
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
        md['plc']=plc
    #=datePublished
    #datep=m3["datePublished"]
    m3d=m3.get("datePublished")
    if m3d:
        datep=m3d
    else:
        datep = None
    if datep:
        md['datep']=datep
    #print(md) #dbg
    return md

#from sq2.py

def cq(qry_str):
    "clowder search query"
    clowder_host = os.getenv('clowder_host')
    r = requests.get(f"{clowder_host}/api/search?query={qry_str}")
    if(r.status_code == 200):
        #ret = json.dumps(r.json()['results'], indent=2)
        ret = r.json()['results']
        rl=len(ret)
        #print(f'cq:{rl}') #dbg
        return ret
    else:
        #return r.status_code
        #print(f'cq:bad:{rs}') #dbg
        rs= r.status_code
        return rs

def cHit2d(r):   #from inside def qc2dcs(qry_str):'s loop
    "one clowder search hit, to a dict usable on after"
    d={}          #also like: defun phit (ds)  in sca.cl
    cID=r['id']
    name=r['name'].replace("&","_and_").replace("<"," _lt_ ")
    description=r['description'].replace("&","_and_").replace("<"," _lt_ ")
    try:
        #url=first(getURLs(description))
        url=first_(getURLs(description))
    except:
        #print(f'dbg:{description}')
        url=""
    #would print out the xml hit at this point in gc2dcs, but dict 1st
    d['id']=cID
    d['url']=url
    #would have a snippet now, w/name \n description, but will keep separate now
    d['name']=name
    d['description']=description
    #LD=cID2LD(cID) #I'd like to use this, but for now:
    #print(d) #dbg
    LD= getjsonLD(cID)
    #print(LD) #dbg
    md=LD2md(LD)
    d['metadata']=md
    return d

def cq2dl(qry_str):   #from def qc2dcs(qry_str):'s loop
    "clowder-qry to dict-list"
    rj=cq(qry_str)
    dl= list(map(cHit2d,rj))
    #print(dl) #dbg
    return dl

def cq2js(qry_str):   
    "clowder-qry to json"
    dl=cq2dl(qry_str)
    js=json.dumps(dl, indent=2)
    print(js)
    ##return js
    #return dl
