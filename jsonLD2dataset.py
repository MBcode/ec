#Get my cached repo metadata asserted into a clowder dataset stub, to describe a repo's dataset-laninding-page ;mbobak
import requests
import json
import os
clowder_host = "https://earthcube.clowderframework.org"
clowder_key = os.getenv('eckey')
clowder_space = os.getenv('clowder_space') #change per repo
print(clowder_space)
#make sure the input fn's have been milled w/something like: #only iedadata, rest find w/encode utf-8
# alias dcat2i "sed -i '/http:..www.w3.org.ns.dcat#/s//dcat:/g'"

def first(l):
    if isinstance(l,list):
        return l[0]
    else:
        return l

def httpP(str):
    str.startswith('http')

def getURLs(l):
    filter(httpP,l)

#don't need strip js for internal txt, but want bs4-stripping so just use this one for now
def stripjshtm(html):
    from bs4 import BeautifulSoup
    import re
    soup = BeautifulSoup(html)
    for script in soup(["script"]):
        script.extract()
    text_wtags = soup.get_text()
    text = BeautifulSoup(text_wtags, "lxml").text #rm more tags here
    ret = re.sub(r'(\n\s*)+\n+', '\n', text.strip())
    return first(ret) #not needed


def dict2dataset(d,url=None):
    jsLD=json.dumps(d)
    name= d.get('name')
#   if not name: #for neotomadb
#       name = d['spatialCoverage']['name']
    if name:
        name=stripjshtm(name)
    else:
        name = " "
    print(name)
    #so find a way2only run for it, maybe loading a schema based cfg for nonstandard location
    #url = d['identifier'][0]['url'] #iedadata
#   idurl = d.get('identifier')
##  idurl = first(d.get('identifier'))
#   if idurl:
#       if isinstance(idurl,list):
#           url=idurl[0].get('url')
#       else:
#           url=idurl.get('url') 
#   else: #if not url: #for most repos 
#       url = d.get('url')
    if not url:
        url = d.get('url')
    if not url: #for RR
        so = d.get('subjectOf')
        if so:
           #print(len(so))
           #print(type(so))
           #print(so)
            #so = first(so)
            if isinstance(so,dict):
                url = so.get('URL')
            if isinstance(so,list):
                url = so[0].get('URL')
    if not url: #for RR
        url = d.get('@id')
    if not url:
        url = " "
    if isinstance(url,list):
        print(url)
        #url=first(getURLs(url))
        url=getURLs(url)
        print(url)

    #if not url: #should only run this if know in that repo
    #    fnb = fn.split('.')[0]
    #    url = "http://data.neotomadb.org/datasets/" + fnb
    #    print(url)
    des = d.get('description')
    if isinstance(des,list):
        des=des[0]
    print(des)
    if url:
        if des:
            sdes = stripjshtm(des) 
           #print(sdes)
           #print(url)
            du = sdes + " " + url
            #du = stripjshtm(des) + " " + url
        else:
            du = name  + " " + url
        metadata3={'name': name, 'description': du, 'url': url, 'space': [clowder_space], 'access': 'PUBLIC'}
    else:
        #metadata3={'name': name, 'description': du, 'space': [clowder_space], 'access': 'PUBLIC'}
        metadata3={'name': name, 'description': des, 'space': [clowder_space], 'access': 'PUBLIC'}
        #metadata3={'name': name, 'description': des} 
    print(metadata3)
    headers3={'X-API-Key': clowder_key,'accept': '*/*', 'Content-Type': 'application/json'}
    print(headers3)
#   rds=requests.post(f'{clowder_host}/api/datasets/createempty',headers=headers3, data=json.dumps(metadata3))
#   print(rds.json()) #check for good return before running the rest 
#   datasetID=rds.json()['id'] 
#   print(datasetID)
    headers2={'X-API-Key': clowder_key, 'Content-Type': 'application/json'}
#   URL=f'{clowder_host}/api/datasets/{datasetID}/metadata'
#   print(URL)
#    r=requests.post(URL,data=jsLD,headers=headers2)
#    print(r.json())
#   print(datasetID)
#   return datasetID
    #return "test"
    return metadata3

def jsonLD2dataset(path):
    "create clowder dataset w/title,abstract,url and assert assoc jsonLD"
    print(path)
    with open(path) as f:
        jsLD=f.read().encode("utf-8")
    if jsLD:
        d=json.loads(jsLD)
        datasetID=dict2dataset(d)
    else:
        return "jsLD is empty"
    if datasetID:
        os.system(f"mv -i {path} ldone")
        return datasetID 

#I'm not a big fan of having ~copies of the same code

def jsLD2dataset(path):
    "extruct has json-ld.."
    print(path)
    with open(path) as f:
        jsLD=f.read().encode("utf-8")
    if jsLD:
        djs=json.loads(jsLD)
        url=djs.get('url')
        d=djs.get('json-ld')
        if d:
            datasetID=dict2dataset(d[0],url)
        else:
            return "djs is empty"
    else:
        return "jsLD is empty"
    if datasetID:
        os.system(f"mv -i {path} ldone")
        return datasetID 

#jsonLD2dataset('ld/310068.jsonld')

#Then to check it was uploaded, or when get search results, &want metadata, send an 'id' to this:
def getLD(datasetID):
    "given clowder dataset id: return it's saved(altered)jsonLD"
    r = requests.get(f'{clowder_host}/api/datasets/{datasetID}/metadata', headers={'X-API-Key' : clowder_key})
    print(json.dumps(r.json(), indent=2))

def getjsonLD(datasetID):
    "given clowder dataset id: return it's saved()jsonLD"
    r = requests.get(f'{clowder_host}/api/datasets/{datasetID}/metadata.jsonld', headers={'X-API-Key' : clowder_key})
    print(json.dumps(r.json(), indent=2))

#logging
def log_dsIDs(rl):
    with open('dsIDs.txt','w') as f:
        for item in rl:
            f.write("%s\n" % item)
#w/bu reconstruction from fn's could pair w/clowder IDs

#have a fnc to ls all the jsonld in a dir, and map over that: 
# started w/: list(map(jsonLD2dataset,os.listdir('ld')))
# but path based now
def run_all_ld():
    import glob
    paths=glob.glob('./ld/*.jsonld') #this gives path, not fns so change above
    return list(map(jsonLD2dataset,paths))

def run_all_js():
    import glob
    paths=glob.glob('./js/*.js') #this gives path, not fns so change above
    rl= list(map(jsLD2dataset,paths))
    log_dsIDs(rl)
    return rl

def run_all_json():
    import glob
    #bu=os.getenv('BASE_URL') #might use w/end of paths to get url,last resort
    paths=glob.glob('./json/*.json') #this gives path, not fns so change above
    rl = list(map(jsonLD2dataset,paths))
    log_dsIDs(rl)
    return rl

# maybe returning a file w/the filename to datasetID mappings
#jsonLD2dataset('ld/609656.jsonld')
