#want to step towards really not just being tied2clowder, but will start w/also caching it's cache
 #nice2have utils, but settle on what should be ret, &maybe just test4that
import requests
import json
import sys
import os
clowder_host = os.getenv('clowder_host')

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
