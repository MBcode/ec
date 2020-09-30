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

#don't need strip js for internal txt, but want bs4-stripping so just use this one for now
def stripjshtm(html):
    from bs4 import BeautifulSoup
    import re
    soup = BeautifulSoup(html)
    for script in soup(["script"]):
        script.extract()
    text = soup.get_text()
    return re.sub(r'(\n\s*)+\n+', '\n', text.strip())

def jsonLD2dataset(path):
    "create clowder dataset w/title,abstract,url and assert assoc jsonLD"
    print(path)
    with open(path) as f:
        jsLD=f.read().encode("utf-8")
    if jsLD:
        d=json.loads(jsLD)
    else:
        return "jsLD is empty"

    name= d.get('name')
    if not name: #for neotomadb
        name = d['spatialCoverage']['name']
    if name:
        name=stripjshtm(name)
    #so find a way2only run for it, maybe loading a schema based cfg for nonstandard location
    #url = d['identifier'][0]['url'] #iedadata
    idurl = d.get('identifier')
    if idurl:
        if isinstance(idurl,list):
            url=idurl[0].get('url')
        else:
            url=idurl.get('url') 
    else: #if not url: #for most repos 
        url = d.get('url')
    #if not url: #should only run this if know in that repo
    #    fnb = fn.split('.')[0]
    #    url = "http://data.neotomadb.org/datasets/" + fnb
    #    print(url)
    des = d.get('description')
    if url:
        if des:
            du = stripjshtm(des) + " " + url
        else:
            du = name  + " " + url
        metadata3={'name': name, 'description': du, 'url': url, 'space': [clowder_space], 'access': 'PUBLIC'}
    else:
        metadata3={'name': name, 'description': des} 
    print(metadata3)
    headers3={'X-API-Key': clowder_key,'accept': '*/*', 'Content-Type': 'application/json'}
    print(headers3)
    rds=requests.post(f'{clowder_host}/api/datasets/createempty',headers=headers3, data=json.dumps(metadata3))
    print(rds.json()) #check for good return before running the rest 
    datasetID=rds.json()['id'] 
    print(datasetID)
    headers2={'X-API-Key': clowder_key, 'Content-Type': 'application/json'}
    URL=f'{clowder_host}/api/datasets/{datasetID}/metadata'
    print(URL)
    r=requests.post(URL,data=jsLD,headers=headers2)
    print(r.json())
    #os.system(f"mv {path} ldone")
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

#have a fnc to ls all the jsonld in a dir, and map over that: 
# started w/: list(map(jsonLD2dataset,os.listdir('ld')))
# but path based now
def run_all():
    import glob
    paths=glob.glob('./ld/*.jsonld') #this gives path, not fns so change above
    return list(map(jsonLD2dataset,paths))

# maybe returning a file w/the filename to datasetID mappings
#jsonLD2dataset('ld/609656.jsonld')
