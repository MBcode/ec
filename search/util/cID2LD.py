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


def cID2LD(cID):
    ccf = "cc/" + cID + ".jsonld"
    if os.path.exists(ccf):
        #with open(ccf, "r") as rf:
        #    d=json.loads(rf)
        d=get_jsonfile(ccf)
    else:
        d = getjsonLD(ccf)
        if d:
            with open(ccf, "w") as of:
                of.write(d)
    return d

def gd(id):
    print(cID2LD(id))
