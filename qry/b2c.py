#all the code in ../assert & ../search as clowder at least as a backup, this finally breaks free&be small like these early queris I wante to finish
import os
import sys
import json
#import requests

if(len(sys.argv)>1):
    qry_str=sys.argv[1]
else:
    qry_str = "Tectonophysics Seymour Island"

#here can focus on bindings dict, bs the clowder search dict, which was limited; 
 #should have at least returned the url I sent in, as promoted data, if not more

def get_txtfile(fn):
    with open(fn, "r") as f:
        #return f.read().encode("utf-8").replace("�","_")
        return f.read().encode("utf-8")

#--below/next functions are for clustering in_subtopic facet
 #will probably break out into a separate d2c.py file soon
  #and could send the sq bindings-dict as js2it similarly
   #b2hs fnc will get bindings as-is w/all optionals in
    #so nothing extra to to there, except on the html-gen side

def b1xs_(result): #original version
    "one binding to xml str"
    rl=len(result)
    #print(f'b1xs,result:{result}') #dbg
    #print(f'{result}') #dbg
    if rl<2:
        #print(f'b1xs,result-len:{rl}') #dbg
        return ""
    rs=""
    doi=result["subj"]["value"]
    ds=f'\n<document id=\"{doi}\">'
#   print(ds) #dbg
    rs+=ds
    url=result["disurl"]["value"]
    us=f'<url>{url}</url>\n'
#   print(us) #dbg
    rs+=us
    description=result["description"]["value"]
    description=description.replace("&","_and_").replace("<"," _lt_ ")
    ss=f'<snippet>{description}</snippet></document>'
#   print(ss) #dbg
    rs+=ss
    return rs

def b1xs(result): #use changed dict, 2compress keys together
    "one binding to xml str"
    rl=len(result)
    #print(f'b1xs,result:{result}') #dbg
    #print(f'{result}') #dbg
    if rl<2:
        #print(f'b1xs,result-len:{rl}') #dbg
        return ""
    rs=""
    #doi=result["subj"]["value"]
    doi=result["subj"]
    ds=f'\n<document id=\"{doi}\">'
#   print(ds) #dbg
    rs+=ds
    #url=result["disurl"]["value"]
    url=result["disurl"]
    us=f'<url>{url}</url>\n'
#   print(us) #dbg
    rs+=us
    #description=result["description"]["value"]
    description=result["description"]
    description=description.replace("&","_and_").replace("<"," _lt_ ")
    ss=f'<snippet>{description}</snippet></document>'
#   print(ss) #dbg
    rs+=ss
    return rs

def b2xs(b):
    "var bindings2xml(str)4 clowder2 dcs service"
    rs = """<?xml version="1.0" encoding="UTF-8"?>
        <searchresult>"""   #when in file only gets up to here
    xml_qry=f'<query>{qry_str}</query>\n'  #gotten from global
    print(xml_qry) #dbg
    rs += xml_qry
    for result in b:
        #if isinstance(result,dict):
        #    rs+= b1xs(result)
        #print(f'result={result}')
        rs+= b1xs(result)
    rs += "</searchresult>"
    return rs 
#dicts are off

def b2xs_(b):
    "cache around bindings2xml-str"
    ccf = "cc/" + qry_str.replace(" ", "_")  + ".xml" #from global
    if os.path.exists(ccf) and os.stat(ccf).st_size >199:
        print(f'already have file:{ccf}')
        x=get_txtfile(ccf) #actually need to read as file for now
        lx=len(x)
        print(f'len:{lx}')
    else:
        x=b2xs(b)
        print(f'xml:{x}') #dbg, not as full as returned below
        xl=len(x)
        print(f'writing xml of len{xl}')
        #write, then use
        with open(ccf, "w") as of:
            of.write(x)
    return x
#-or: now using
def q2xs_(qry_str):
    "cache around bindings2xml-str"
    ccf = "cc/" + qry_str.replace(" ", "_")  + ".xml" #from global
    if os.path.exists(ccf) and os.stat(ccf).st_size >199:
        print(f'already have file:{ccf}')
        x=get_txtfile(ccf) #actually need to read as file for now
        lx=len(x)
        print(f'len:{lx}')
    else:
        b=q2b(qry_str)   
        x=b2xs(b)
        print(f'xml:{x}') #dbg, not as full as returned below
        xl=len(x)
        print(f'writing xml of len{xl}')
        #write, then use
        with open(ccf, "w") as of:
            of.write(x)
    return x

#getting: java.lang.IllegalArgumentException  Identifiers must be unique, duplicated identifier: DOI:10.15784/601208 [existing: [DOI:10.15784/601208]]
#before sending the xml, consider looking at dict/fixing, or before saving;rigth from sparql
#distinct should have kept this from happening
def xs2c(x):  
    "dcs-xml(str-cache-file)call to get clusters only in json" 
    #just needs b2xs_ check/setting the xml file to load, till can send via requests
    ccf = "cc/" + qry_str.replace(" ", "_")  + ".xml" #from global
    cs= f'curl $dcs_url -F "dcs.clusters.only=true" -F "dcs.output.format=JSON" -F "dcs.c2stream=@{ccf}"'
    s=os.popen(cs).read().encode("utf-8")
    sl=len(s)
    print(f'curl dcs w/:{ccf},has-ret-len:{sl}')
    try:
        dct=json.loads(s)
    except:
        print(s) 
        dct={"clusters": ""}
 #  sl=len(s)
 #  print(f'sx2c,sl={sl}')
 #  dct=json.loads(s) 
    #docs=dct['documents'] #this fnc just abt clusters, but still make sure  original binidngs, make2html2
    cls=dct['clusters']
    nc=len(cls)
    print(f'got {nc} clusters') #dbg
    if nc<1:
        print(f'nc=0 for cls={cls}')
    return cls 


#bindings will have the optional filterable md-elts now, but have2see how used by filter widgets
 #sounds like it just needs the range of values w/counts, ;which can get from sparql-qry too
  #along w/more optional to normalize the publisher, which varies, so will look into that
#--

def add2dict(key,v,d):
    #d.add(k,v) #more internal to class
    d[key]=v

def ld1js(d):  #thought abt mapping, but could append2new dict like I do w/incrKeyCount
    "jsonld to just js, for one search hit"
    tmp={}
    for k, v in d.items():
        v2 = v['value']
        #add k,v2  to the .js version of this hit, just below/finsh
        add2dict(k,v2,tmp)
    return tmp

def ld2js(d):
    "jsonld to just js"
    tmpa=[]
    for hit in d:
        d=ld1js(hit)
        tmpa.append(d)
    return tmpa
#--
#def sq2b_(qry_str): "cache around sparql-qry2binding"
#def b2b(qry_str):
def q2b(qry_str):
    "read in binding cache"
    #ccf = "cc/" + qry_str.replace(" ", "_")  + ".js" #from global
    ccf = "cc/" + qry_str.replace(" ", "_")  + ".jsonld" #from global
    #ccf = "cc/" + qry_str.replace(" ", "_")  + ".jsonld" #from global
    if os.path.exists(ccf) and os.stat(ccf).st_size >199:
        b_=get_txtfile(ccf) #actually need to read as file for now
        print(f'already have file:{ccf}')
        b=json.loads(b_)
        b=ld2js(b) #new #hopefully collapses dup key as well
        return b
    else:
        print("called out of order") #could call qry.py here though if need be
#--

#---qry+fill middle of search page
#w/this don't actually have to read in the bindings if have already cached the clusters
#so when get to reading clusters if not there could read in bindings then
 #could keep as is, till dbg done &get request calls in w/o cache files;or could mv back
#def sq2(qry_str): 
#def b2c(qry_str):  
def q2c(qry_str):  
    "take bindings from cache & cache the related clusters" 
    #get the filter-facet metadata through optional lines in sparql qry
    #b=sq2b(qry_str)   
  # b=q2b(qry_str)   
  # x=b2xs_(b) #binding to dcs-xml
    x=q2xs_(qry_str)   
    #jb=json.dumps(b, indent=2)
    #-can skip below if don't need clusters, but still need other metadata-put in
    c=xs2c(x) #dcs-xml(file)to clusters
 #  print(f'clusters:{c}') #dbg
    #if c, then can put in the html
    #h=b2hs(b) #binding to html
    #print(f'html:{h}') #dbg  #would print down here if putting cluters as part of metadata
    # at end, had rescards w/cluster info, incl links back2id's in html
    print(f'clusters:{c}') #dbg
      #this is from csq2's cls2h, ..

#sq2(qry_str)
#b2c(qry_str)
q2c(qry_str)
