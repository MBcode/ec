#try converting a jsonld record to a minimal crate
import os
import json
top = """
{ "@context": "https://w3id.org/ro/crate/1.1/context",
  "@graph": [
    {
        "@type": "CreativeWork",
        "@id": "ro-crate-metadata.json",
        "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"},
        "about": {"@id": "./"}
  },  
  {
    "@id": "./",
    "@type": [
      "Dataset"
    ],
    "hasPart":  
    """
#then all "@id": ...  ;w/, btwn
middle = "},"
#then all distribution records w/"@id": ... inserted  ;w/, btwn
bottom = "]}"

#now given a filename, load in the jsonld, and find the distribution
# go over that array, and make the ..url into @id's that will also go w/in the hasPart

#in this 1st pass, could try: jq .distribution filename, and read that in to process
def os_sys_(cs):
    return os.popen(cs).read()

#later take in full jsonld&alter in plc
def get_jsfile2dict(fn):
    s=get_textfile(fn)
    return json.loads(s)

def put_txtfile(fn,s,wa="w"):
    #with open(fn, "w") as f:
    with open(fn, "a") as f:
        return f.write(s)

def get_distribution(fn):
    cs=f'jq .distribution {fn}'
    return os_sys_(cs)

def get_distr_dicts(fn):
    "distribution dictionary"
    s=get_distribution(fn)
    return json.loads(s)

def add_id(d): #there will be other predicates to check
    "set @id as (access)url"
    u=d.get("dcat:accessURL")
    d["@id"]=u
    return d

def get_id(d):
    return d.get("@id")

def get_idd(d):
    "dict of @id value, for hasPart[]"
    id=d.get("@id")
    dr={}
    dr["@id"]=id
    return dr

#jsonld to minimal ro-crate
#started by iterativly changing the distribution, then get IDs out for hasPart
def jld2crate(fn):
    print(top)
    #d=get_distribution(fn)
    dl=get_distr_dicts(fn)
    #for d in dl: #needs a comma btwn
    #    print(json.dumps(d))
    dl2=list(map(add_id,dl))
    ids=list(map(get_idd,dl))
    print(json.dumps(ids))
    print(middle)
    print(json.dumps(dl2))
    print(bottom)

def jld2crate_(fn):
    fn_out="roc/" + fn
    put_txtfile(fn_out,top)
    dl=get_distr_dicts(fn)
    dl2=list(map(add_id,dl))
    ids=list(map(get_idd,dl))
    put_txtfile(fn_out,json.dumps(ids))
    put_txtfile(fn_out,middle)
    put_txtfile(fn_out,json.dumps(dl2))
    put_txtfile(fn_out,bottom)

#tests
def t1():
    jld2crate("324529.jsonld")

def t2(fn="324529.jsonld"):
    jld2crate_(fn)
#if we stay w/python /need to run on all
#I will have it put to files, w/more checks
#&use alt predicates for the @id if needed

#Still need to add URN as another entry
 #which is something gleaner generated
 #I wish we could use(a version of)the download url
 #and then we would all know what to expect w/o 
  #depending on some centeral rand#generator
