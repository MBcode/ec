#M Bobak, for ncsa.uiuc NSF EarthCube effort, GeoCODES search&resource use w/in NoteBooks
# some on (new)direction(s) at: https://mbcode.github.io/ec
#=this is also at gitlab now, but won't get autoloaded until in github or allow for gitlab_repo
 #but for cutting edge can just get the file from the test server, so can use: get_ec()
dbg=None #can use w/logging as well soon, once there is more need&time
f_nt=None #the .nt file last downloaded
rdf_inited,rdflib_inited,sparql_inited=None,None,None
endpoint=None
#keep these more in sync ;could have a dict for each setup
#_testing: was@10
#_testing end
first_endpoint = "https://graph.geodex.org/blazegraph/namespace/nabu/sparql"
prod_endpoint = "https://graph.geocodes.earthcube.org/blazegraph/namespace/earthcube/sparql"
#dflt_endpoint = "https://graph.geocodes.earthcube.org/blazegraph/namespace/earthcube/sparql"
dflt_endpoint_old = "https://graph.geocodes.earthcube.org/blazegraph/namespace/earthcube/sparql"
mb_endpoint = "http://24.13.90.91:9999/bigdata/namespace/nabu/sparql"
ncsa_endpoint_old = "http://mbobak.ncsa.illinois.edu:9999/blazegraph/namespace/nabu/sparql"
ncsa_endpoint_ = "https://mbobak.ncsa.illinois.edu:9999/blazegraph/namespace/nabu/sparql"
ncsa_endpoint = "https://mbobak.ncsa.illinois.edu:9999/bigdata/namespace/ld/sparql"
dev_https_endpoint="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/https/sparql"
gc1_endpoint = "https://graph.geocodes-1.earthcube.org/blazegraph/namespace/earthcube/sparql"
#dflt_endpoint = ncsa_endpoint
#dflt_endpoint = "https://graph.geodex.org/blazegraph/namespace/nabu/sparql"
dflt_endpoint = gc1_endpoint
summary_endpoint = dflt_endpoint.replace("earthcube","summary") #can't always just switch


#_testing: was@40 
#_testing end

local=None
def laptop(): #could call: in_binder
    "already have libs installed"
    global rdf_inited,rdflib_inited,sparql_inited
    rdf_inited,rdflib_inited,sparql_inited=True,True,True
    print("rdf_inited,rdflib_inited,sparql_inited=True,True,True")
    return "rdf_inited,rdflib_inited,sparql_inited=True,True,True"

def local():
    "do in binder till can autoset if not in colab"
    #put in a binder version of sparql_nb template, for now
    local=laptop()

def now():
    from datetime import datetime
    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    return dt_string

def head(l, n=5):
    return l[:n]

def tail(l, n=5):
    return l[-n:]

def is_str(v):
    return type(v) is str

def is_list(v):
    return type(v) is list

#pagemil parameterized colab/gist can get this code via:
#with httpimport.github_repo('MBcode', 'ec'):   
#  import ec
#version in template used the earthcube utils
import os
import sys
import json
IN_COLAB = 'google.colab' in sys.modules
cwd = os.getcwd()

def falsep(val):
    return val == False

def not_true(val):
  return val and (val != False)

#if not_true(IN_COLAB):
if falsep(IN_COLAB):
    print("not IN_COLAB")
    #local()
    laptop()

def ndtq_(name=None,datasets=None,queries=None,tools=None):
    "force colab version, best for cli"
    n=json.loads(name)
    d=json.loads(datasets)
    t=json.loads(tools)
    Q=json.loads(queries)
    print(f'n={n},d={d},q={Q},t={t}')
    return n,d,t,Q

def ndtq(name=None,datasets=None,queries=None,tools=None):
  "get collection args for colab or binder"
  import json
  if IN_COLAB: #this has to come from top level
    n=json.loads(name)
    d=json.loads(datasets)
    t=json.loads(tools)
    Q=json.loads(queries)
  else:
    ds = ipyparams.params['collection']
    print(ds)
    dso = json.loads(ds)
    # if this cell fails the first run.
    #run a second time, and it works.
    n=dso.get('name')
    d=dso.get('datasets')
    t=dso.get('tools')
    Q=dso.get('queries')
  print(f'n={n},d={d},q={Q},t={t}')
  return n,d,t,Q

#more loging
#def install_recipy():
#    cs='pip install recipy'
#    os.system(cs)
#install_recipy()
#import recipy
def first(l):
    "get the first in an iterable"
    from collections.abc import Iterable
    if isinstance(l,list):
        return l[0]
    elif isinstance(l,Iterable):
        return list(l)[0]
    else:
        return l

def flatten(xss): #stackoverflow
    "make list of lists into 1 flat list"
    return [x for xs in xss for x in xs]

#from qry.py
def get_txtfile(fn):
    "ret str from file"
    with open(fn, "r") as f:
        return f.read()

def get_jsfile2dict(fn):
    "get jsonfile as dict"
    #s=get_txtfile(fn)
    #return json.loads(s)
    with open(fn, "r") as f:
        return json.load(f)

def put_txtfile(fn,s,wa="w"):
    "filename to dump string to"
    #with open(fn, "w") as f:
    with open(fn, "a") as f:
        return f.write(s)

def list2txtfile(fn,l,wa="w"):
    with open(fn, "a") as f:
        for elt in l:
            f.write(f'{elt}\n')
    return len(l)

def date2log(): #could use now to put on same line, but this breaks it apart
    cs="date>>log"
    os.system(cs)

def add2log(s):
    "logging" #will use lib
    date2log()
    fs=f'[{s}]\n'
    put_txtfile("log",fs,"a")

def print2log(s):
    print(s)
    add2log(s)

def os_system(cs):
    "run w/o needing ret value"
    os.system(cs)
    add2log(cs)

def os_system_(cs):
    "system call w/return value"
    s=os.popen(cs).read()
    add2log(cs)
    return s

def curl_url(url):
    cs=f'curl {url}'
    return os_system_(cs)

def whoami():
    return os_system_("whoami")

def urn_leaf(s): #like urn_tail
    "last part of : sep string" 
    leaf = s if not s else s.split(':')[-1]
    return leaf

#start adding more utils, can use to: fn=read_file.path_leaf(url) then: !head fn
def path_leaf(path):
    "everything after the last /"
    import ntpath
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def path_base_leaf(path):
    "like path_leaf but gives base 1st"
    import ntpath
    head, tail = ntpath.split(path)
    if not tail:
        tail = ntpath.basename(head)
    return head, tail

#also in:_testing: was@40 
#from 'sources' gSheet: can use for repo:file_leaf naming/printing
base_url2repo ={"https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/main/metadata/Dataset/json": "geocodes_demo_datasets",
        "https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/main/metadata/Dataset/allgood": "geocodes_demo_datasets",
        "https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/main/metadata/Dataset/bad": "geocodes_demo_bad",
                "http://mbobak.ncsa.illinois.edu/ec/minio/test3/summoned/geocodes_demo_datasets": "test3"
        } #won't match if '/' at end of key
#
def replace_base(path,mydict=base_url2repo,sep=":"): #for context like: repo:filename
    "use URI to context:, eg. repo:leaf.rdf"
    base,leaf=path_base_leaf(path)
    new_base=mydict.get(base)
    if new_base:
        return f'{new_base}{sep}{leaf}'
    else:
        return path

def file_ext(fn):
    "the ._part of the filename"
    st=os.path.splitext(fn)
    add2log(f'fe:st={st}')
    return st[-1]

def file_base(fn):
    "the base part of base.txt"
    st=os.path.splitext(fn)
    add2log(f'fb:st={st}')
    return st[0]

def file_leaf_base(path):
    "base of the leaf file"
    pl=path_leaf(path)
    return file_base(pl)

#sparql.ipynb:    "ds_url=ec.collect_ext(ds_urls,ext)\n",
def collect_ext(l,ext):
  return list(filter(lambda x: file_ext(x)==ext,flatten(l)))

def collect_ext_(l,ext):
  return list(filter(lambda x: file_ext(x)==ext,l))

def collect_pre(l,pre):
  return list(filter(lambda x: x.startswith(pre),flatten(l)))

def collect_pre_(l,pre):
  return list(filter(lambda x: x.startswith(pre),l))

def collect_str(l,s):
  return list(filter(lambda x: s in x ,flatten(l)))

def collect_str_(l,s):
  return list(filter(lambda x: s in x ,l))

#could think a file w/'.'s in it's name, had an .ext
 #so improve if possible; hopefully not by having a list of exts
  #but maybe that the ext is say 6char max,..
#only messed up filename when don't send in w/.ext and has dots, but ok w/.ext

def has_ext(fn):
    return (fn != file_base(fn))

def wget(fn):
    #cs= f'wget -a log {fn}'  #--quiet
    cs= f'wget --tries=2 -a log {fn}' 
    os_system(cs)
    return path_leaf(fn) #new

def wget2(fn,fnl): #might make optional in wget
    "wget url, save to " #eg. sitemap to repo.xml
    cs= f'wget -O {fnl} --tries=2 -a log {fn}' 
    os_system(cs) 
    return get_txtfile(fnl) #not necc,but useful

def mkdir(dir):
    cs=f'mkdir {dir}'
    return os_system(cs)

def pre_rm(url):
    "rm (possibly alredy) downloaded version of url"
    fnb=path_leaf(url)
    cs=f'rm {fnb}'
    os_system(cs)
    return fnb

def get_ec(url="http://geocodes.ddns.net/ec/nb/ec.py"):
    pre_rm(url)
    wget(url)
    return "import ec"

    #often want to get newest ec.py if debugging
    # but don't need to get qry-txt each time, but if fails will use latest download anyway

def get_ec_txt(url):
    fnb= pre_rm(url)
    wget(url)
    return get_txtfile(fnb)

jar=os.getenv("jar") #move this to top, near global endpoint
if not jar:
    if local:
        jar="~/bin/jar" #have set by local, setup will have to get otherwise
    else:
        jar="."

def blabel_l(fn): 
    "get rid of BlankNodes, needs setup_j"
    fb=file_base(fn) 
    ext=file_ext(fn)
    cs=f'java -Xmx4155M -jar {jar}/blabel.jar  LabelRDFGraph -l -i {fn} -o {fb}_l{ext}'
    os_system(cs)

def read_sd_(fn):
    "read_csv space delimited"
    import pandas as pd
    return pd.read_csv(fn,delimiter=" ")

def read_sd(fn):
    "read_file space delimited"
    fn_=fn.replace("urn:","")
    if dbg:
        print(f'read_sd:{fn_}')
    #return read_file(fn_,".txt")
    import pandas as pd
    try:
        df=pd.read_csv(fn, sep='\n',header=None,comment='#')
    except:
        df = str(sys.exc_info()[0])
    return df

def read_json_(fn):
    "read_json and flatten for df_diff"
    #import pandas as pd
    #return pd.read_json(fn) #finish or skip for:
    return read_file(fn,".json") #getting "<class 'NameError'>"

#def read_json(url):
def read_json(urn):
    "request json, ret dict"
    import urllib.request
    import json
    url=urn.replace("urn:","")
    if dbg:
        print(f'read_json:{url}')
    with urllib.request.urlopen(url) as response:
        #try:
        res = response.read()
        if res:
            return json.loads(res)
        else:
            return None

def is_df(df):
    import pandas as pd
    return isinstance(df, pd.DataFrame)

#_testing: was@427
#_testing end

def post_untar(url,uncompress="tar -zxvf "): #could be "unzip -qq "
    "uncompress downloaded version of url"
    fnb=path_leaf(url)
    cs=f'{uncompress} {fnb}'
    os_system(cs)
    return fnb

def install_url(url): #use type for uncompress later
    pre_rm(url)
    wget(url)
    fnb=post_untar(url) #
    return fnb.rstrip(".tar.gz").rstrip(".zip") #handle either type

def install_java():
    ca= "apt-get install -y openjdk-8-jdk-headless -qq > /dev/null"
    os_system(cs)  #needed for jena..
    os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
    # !java -version #check java version

def install_jena(url="https://dlcdn.apache.org/jena/binaries/apache-jena-4.5.0.tar.gz"):
    return install_url(url)

def install_fuseki(url="https://dlcdn.apache.org/jena/binaries/apache-jena-fuseki-4.5.0.tar.gz"):
    return install_url(url)

def install_any23(url="https://dlcdn.apache.org/any23/2.7/apache-any23-cli-2.7.tar.gz"):
    return install_url(url)

def setup_blabel(url="http://geocodes.ddns.net/ld/bn/blabel.jar"):
    wget(url)

def setup_j(jf=None):
    install_java()
    path=os.getenv("PATH")
    jena_dir=install_jena()
    any23_dir=install_any23()
    if jf:
        fuseki_dir=install_jena()
        addpath= f':{jena_dir}/bin:{fuseki_dir}/bin:{any23_dir}/bin'
    else:
        addpath= f':{jena_dir}/bin:{any23_dir}/bin'
    os.environ["PATH"]= path + addpath 
    setup_blabel() #which also needs java
    return addpath

##get_  _txt   fncs:
# are composed from the middle/variable word, and called in: v4qry
#def get_relateddatafilename_txt(url="https://raw.githubusercontent.com/earthcube/facetsearch/toolMatchNotebookQuery/client/src/sparql_blaze/sparql_relateddatafilename.txt"):
def get_relateddatafilename_txt(url="https://raw.githubusercontent.com/MBcode/ec/master/NoteBook/sparql_relateddatafilename.txt"):
    return get_ec_txt(url)  #need var to be {?q} so dont have to write extra logic below

def get_webservice_txt(url="https://raw.githubusercontent.com/earthcube/facetsearch/master/client/src/sparql_blaze/sparql_gettools_webservice.txt"):
    return get_ec_txt(url)

def get_download_txt(url="https://raw.githubusercontent.com/earthcube/facetsearch/master/client/src/sparql_blaze/sparql_gettools_download.txt"):
    return get_ec_txt(url)

def get_notebook_txt(url="https://raw.githubusercontent.com/MBcode/ec/master/NoteBook/sparql_gettools_notebook.txt"):
    return get_ec_txt(url)

#in feat_summary:
#def get_query_txt(url="https://raw.githubusercontent.com/earthcube/facetsearch/master/client/src/sparql_blaze/sparql_query.txt"):
def get_query_txt(url="https://raw.githubusercontent.com/MBcode/ec/master/NoteBook/sparql-query.txt"):
    return get_ec_txt(url)

#def get_summary_query_txt(url="https://raw.githubusercontent.com/earthcube/facetsearch/master/client/src/sparql_blaze/sparql_query.txt"): #had limit at end
def get_summary_query_txt(url="http://mbobak.ncsa.illinois.edu/ec/nb/sparql_blaze.txt"):
    #return get_ec_txt(url)  #start to use this in the sparql-nb txt_query
    return """PREFIX bds: <http://www.bigdata.com/rdf/search#>
 PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
 PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
 prefix schema: <https://schema.org/>
 SELECT distinct ?g ?pubname ?placenames ?kw  ?datep
        (MAX(?score1) as ?score)  ?name ?description ?resourceType
          WHERE {
            ?lit bds:search "${q}" .
            ?lit bds:matchAllTerms false .
            ?lit bds:relevance ?score1 .
            ?lit bds:minRelevance 0.14 .
            ?g ?p ?lit .
        ?g schema:name ?name .
        ?g schema:description ?description .
 BIND (IF (exists {?g a schema:Dataset .}  , "data", "tool") AS ?resourceType).
 OPTIONAL {?g schema:date ?datep .}
 OPTIONAL {?g schema:publisher ?pubname .}
 OPTIONAL {?g schema:place ?placenames .}
 OPTIONAL {?g schema:keywords ?kw .} }
 GROUP BY ?g ?pubname ?placenames ?kw ?datep ?disurl ?score ?name ?description  ?resourceType
         ORDER BY DESC(?score)"""

def get_subj2urn_txt(url="http://geocodes.ddns.net/ec/nb/sparql_subj2urn.txt"):
    #return get_ec_txt(url)
    return """prefix sschema: <https://schema.org/>
            SELECT distinct    ?g WHERE {
            graph ?g { <${g}> a schema:Dataset }}"""

def get_graphs_txt(url="http://geocodes.ddns.net/ec/nb/sparql_graphs.txt"):
    #return get_ec_txt(url)
    return "SELECT distinct ?g  WHERE {GRAPH ?g {?s ?p ?o}}"

def get_graph_txt(url="http://geocodes.ddns.net/ec/nb/get_graph.txt"):
    #return get_ec_txt(url)
    #return "SELECT distinct ?s ?p ?o  WHERE { graph ?g {?s ?p ?o} filter(?g = <${g}>)}"
    return "SELECT distinct ?s ?p ?o  WHERE { graph ?g {?s ?p ?o} filter(?g = <${q}>)}" #there will be a better way
    #return "describe <${q}>)}" #similar but can't do this    #also want where can ask for format as jsonld for ui
    #consider ret CONSTRUCT from a direct match vs filter
    #I'm ok w/filter given the changing URNs taking a subset should still return something

def get_summary_txt(url="http://geocodes.ddns.net/ec/nb/get_summary.txt"):
    "this is to make a summary, not to do a qry on the summary"
    return get_ec_txt(url)

## so/eg. this last one is where get_graph(g) calls v4qry(g,"graph")

def add_ext(fn,ft):
    if ft==None or ft=='' or ft=='.' or len(ft)<2:
        return None
    fn1=path_leaf(fn) #just the file, not it's path
    fext=file_ext(fn1) #&just it's .ext
    r=fn1
    if fext==None or fext=='':
        fnt=fn1 + ft
        #cs= f'mv {fn1} {fnt}' 
        cs= f'sleep 2;mv {fn1} {fnt}' 
        os_system(cs)
        r=fnt
    return r

def wget_ft(fn,ft):
    wget(fn)
    fnl=fn
    if ft!='.' and ft!='' and ft!=None and len(ft)>2:
        fnl=add_ext(fn,ft) #try sleep right before the mv
    #does it block/do we have2wait?, eg. time.sleep(sec)
    #fnl=path_leaf(fn) #just the file, not it's path
    if os.path.isfile(fnl):
        fs=os.path.getsize(fnl) #assuming it downloads w/that name
    else:
        fs=None
    #if fs>999 and fs<999999999: #try upper limit later
    #if fs>699:
    #    cs=f'unzip {fnl}'
    #    os.system(cs)
    #unzip even if small broken file
    if ft=='.zip': #should check if zip
        cs=f'unzip {fnl}'
        os_system(cs)
        fnb=file_base(fnl)
#       if os.path.isdir(fnb):
#           cs=f'ln -s . content' #so can put . before what you paste
#           os_system(cs)
    return fs

#rdflib_inited=None
def init_rdflib(): #maybe combine w/init_sparql
    #cs='pip install rdflib networkx'
    #cs='pip install rdflib networkx extruct' 
    #cs='pip install rdflib rdflib-jsonld networkx extruct' 
    #cs='pip install rdflib rdflib-jsonld networkx extruct python-magic' 
    cs='pip install rdflib networkx extruct python-magic pyld' 
    os_system(cs)
    rdflib_inited=cs

#-from crawlLD.py
#def crawl_LD(url) ;could get other than jsonld, &fuse
def url2jsonLD(url):
    "get jsonLD from w/in url"
    add2log(f'url2jsonLD({url})')
    if rdflib_inited==None:
        init_rdflib()
    import extruct
    import requests
    from w3lib.html import get_base_url
    r = requests.get(url)
    base_url_ = get_base_url(r.text, r.url)
    #ld = extruct.extract(r.text, base_url=base_url_ ,syntaxes=['json-ld'] )
    md = extruct.extract(r.text, base_url=base_url_ ,syntaxes=['json-ld'] )
    if md: #still geting as if all MetaData, so select out json-ld
        #ld = md.get('json-ld')
        lda = md.get('json-ld')
        #print(f'lda={lda}')
        ld=lda[0] #ret first here
        #print(f'ld={ld}')
    else: 
        ld =""
    add2log(ld)
    return ld

def url2jsonLD_fn(url,fn):
    "url2jsonLD_file w/forced filename"
    ld=url2jsonLD(url)
    LD=json.dumps(ld, indent= 2)
    fnj = fn + ".jsonld" #only if not there
    return put_txtfile(fnj,LD)

def url2jsonLD_file(url):
    "get jsonLD from w/in url, save to file"
    ld=url2jsonLD(url)
    fnb=file_leaf_base(url)
    LD=json.dumps(ld, indent= 2)
    put_txtfile(fnb,LD)
    return fnb

#def fn2jsonld(fn, base_url=None):
def fn2jsonld(fn, base_url=None):
    "url=base_url+fn save to fn"
    import re
#   if not base_url:
#       base_url = os.getenv('BASE_URL')
    #print(base_url)
    #print(fn)
#    url= base_url + fn
    url=fn
    #print(url)
    #ld=url2jsonLD(url)
    md=url2jsonLD(url)
    if md:
        ld = md.get('json-ld')
    else: 
        ld =""
    #print(len(ld))
    cfn=re.sub(r'(\n\s*)+\n+', '\n', fn.strip())
    fn = cfn + ".jsonld"
    #print(fn)
    if ld:
        with open(fn  ,'w') as f:
            #pp.pprint(ld,f)
            #f.write(pprint.pformat(ld[0]))
            f.write(json.dumps(ld[0], indent= 2))
    return ld
#-
#already done above,but take parts2fix below
def getjsonLD(url):
    "url2 .jsonld"
    import re
    import json
    ld=url2jsonLD(url) #get json
    #fnb=file_base(url)
    fnb=file_leaf_base(url)
    cfn=re.sub(r'(\n\s*)+\n+', '\n', fnb.strip())
    #fnj=fnb+".jsonld" 
    #put_txtfile(fnj,ld)
    fnj=cfn+".jsonld" 
    add2log(f'getjsonLD:{fnb},{fnj}')
    #LD=json.dumps(ld[0], indent= 2)
    LD=json.dumps(ld, indent= 2)
    put_txtfile(fnj,LD)
    #put_txtfile(fnj,LD.decode("utf-8"))
    return fnj

#get fnb + ".nt" and put_txtfile that str
#def 2nt  from any rdf frmt to a .nt file, bc easiest to concat
def xml2nt(fn,frmt="xml"):  #could also use rapper here, see: rdfxml2nt
    "turn .xml(rdf) to .nt"
    if rdflib_inited==None:
        init_rdflib()
    fnb=file_base(fn)
    from rdflib import Graph
    g = Graph()
    #g.parse(fn, format="xml")
    g.parse(fn, format=frmt) #allow for "json-ld"..
    #UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte ;fix
    #s=g.serialize(format="ntriples").decode("u8") #works via cli,nb had ntserializer prob
    s=g.serialize(format="ntriples") #try w/o ;no, but works in NB w/just a warning
    fnt=fnb+".nt" #condsider returning this
    put_txtfile(fnt,s)
    add2log(f'xml2nt:{fnt},len:{s}')
    #return len(s) 
    return fnt 

def to_nt_str(fn,frmt="json-ld"):  
    "turn .xml(rdf) to .nt"
    fnb=file_base(fn)
    from rdflib import Graph
    g = Graph()
    g.parse(fn, format=frmt) #allow for other formats
    s=g.serialize(format="ntriples") 
    return s

def jsonld2nt(fn,frmt="json-ld"):
    "turn .jsonld to .nt"
    add2log(f'jsonld2nt:{fn},{frmt}')
    return xml2nt(fn,frmt)

def url2nt(url):
    "get .jsonLD file,&create a .nt version"
    #ld=url2jsonLD(url)
    #s1=len(ld)
    fnj=getjsonLD(url)
    fnt=jsonld2nt(fnj)
    #fnt=jsonld2nt(fnb)
    #s2=jsonld2nt(fnb)
    #add2log(f'url2nt,jsonld:{s1},nt:{s2}')
    #return s2
    #add2log(f'url2nt,jsonld:{s1},{fnt}')
    add2log(f'url2nt,{fnj},{fnt}')
    return fnt

def append2everyline(fn,aptxt,fn2=None):
    with open(fn) as fp:
        lines= fp.read().splitlines()
    if(fn2==None):
        fn2=fn.replace(".nt",".nq") #main use for triples to quads
    with open(fn2, "w") as fp:
        for line in lines:
            line= line.strip('.') #get rid of this from triples
            print(line + " " + aptxt, file=fp)
    return fn2

def url2nq(url):
    "crawl url ret .jsonld .nt .nq"
    fn= url2nt(url)
    apptxt= f'<{url}> .'
    return append2everyline(fn, apptxt)

def ls(dir): #there are other py commands to do this
    cs=f'ls {dir}'
    return os_system_(cs)

def ls_(path):
    lstr=ls(path)
    return lstr.split("\n")

#_testing was@994
#_testing end

#since  no request to pull base_url from, will have to setenv it
#def nt2nq(fn,dir="nt"): #default ~hardcode, bc not sent in loop
def nt2nq(fn,dir=""): #use this dflt in ec.py in case no ./nt
    import os
    base_url= os.getenv('BASE_URL')
    if (not base_url):
        print("for now, need to: setenv BASE_URL ...")
    fnb=file_base(fn)
    #url=base_url + fnb.lstrip("nt") + "/" #hard coded 'dir'
    url=base_url + fnb.lstrip(dir) + "/"
    aptxt= f'<{url}> .'
    return append2everyline(fn,aptxt)

def all_nt2nq(dir):
    import glob
    get= dir + "/*.nt"
    ntfiles = glob.glob(get)
    for fn in ntfiles:
        #nt2nq(fn)
        print(nt2nq(fn))

#https://stackoverflow.com/questions/39274216/visualize-an-rdflib-graph-in-python
def rdflib_viz(url,ft=None): #or have it default to ntriples ;'turtle'
    if rdflib_inited==None:
        init_rdflib()
    import rdflib
    from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
    import networkx as nx
    import matplotlib.pyplot as plt 
    g = rdflib.Graph()
    if ft!=None:
        result = g.parse(url) #if didn't do mv, could send in format= 
    else:
        result = g.parse(url,format=ft)
    G = rdflib_to_networkx_multidigraph(result) 
    #stackoverflow.com/questions/3567018/how-can-i-specify-an-exact-output-size-for-my-networkx-graph
    #plt.figure(3,figsize=(12,12)) 
    plt.figure(3,figsize=(18,18)) 
    # Plot Networkx instance of RDF Graph
    pos = nx.spring_layout(G, scale=2)
    edge_labels = nx.get_edge_attributes(G, 'r')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    nx.draw(G, with_labels=True) 
    #if not in interactive mode for
    plt.show()

#still use above, although ontospy also allows for some viz
f_nt=None

#could load .nt as a tsv file, to look at if interested
def read_rdf(fn,ext=".tsv"):  #too bad no tabs though../fix?
    return read_file(fn,ext)
#consider using https://pypi.org/project/rdfpandas/

#if I ever get a chance, I'm going to go back to my more understandable /ld/repo/name format
#def urn2uri_(urn):  #looking for a more stable indicator
def urn2uri(urn): 
    "URN to backup store"
    if urn==None:
        return f'no-urn:{urn}'
    elif urn.startswith('urn:'):
        #url=urn.replace("urn:","http://141.142.218.86/",1).replace(":","/") ;gives///
        url=urn.replace(":","/").replace("urn","http://141.142.218.86",1)
        url += ".rdf"
        return url

#after ro_crate subset have all SO/dcat version 
#
def get_gID(): #could have arg that defaults to gName
  subj = "gID:" + gName.replace(".","") 
  return subj 

def get_collectionID(collectionName):
  subj=get_gID()
  collection= f'<{subj}/collection/{collectionName}>'
  return collection 

def set_collectionName(collectionName):
  rs= prefixes+ "prefix gID: https://sites.google.com/site/ \n " 
  subj = "gID:" + gName.replace(".","") #get_gID()
  search = f'<gID:search/{q}>'
  rs+= f'<{subj}> <so:searchAction> {search} \n '
  rs+= f'{search} <so:search> "{q}" \n '
  collection= f'<{subj}/collection/{collectionName}>' #get_collectionID(collectionName)
  rs+= f'<{subj}> <so:collection> {collection} \n '
  return rs 

#def set_collection_rows(collection,rows): #needs collection generated from set_collectionName right now
def set_collection_rows(collectionName,rows):
  row=rows[0] #will iterate over for all rows soon, a: row2d..
  u2=row2urn_url(row)
  urn,url=u2[0],u2[1] #will do other urls soon too
  uri=urn2uri(urn)
  collection=get_collectionID(collectionName) #if sent name vs final collection
  rs+= f'{collection} dcat:Dataset <{uri}> \n '
  rs+= f'<{uri}> dcat:Distribution <{u2[1]}> \n '
  return rs 

#This was in the gist above, but broke out parts above, so could call below w/less code
#if we want more of a breakdown, so can ask for user/agent's collections then it's ....
def rows2collection_(rows,collectionName):
  rs= prefixes+ "prefix gID: https://sites.google.com/site/ \n " 
  subj = "gID:" + gName.replace(".","") 
  search = f'<gID:search/{q}>'
  rs+= f'<{subj}> <so:searchAction> {search} \n '
  rs+= f'{search} <so:search> "{q}" \n '
  collection= f'<{subj}/collection/{collectionName}>'
  rs+= f'<{subj}> <so:collection> {collection} \n '
  row=rows[0] #will iterate over for all rows soon, a: row2d..
  u2=row2urn_url(row)
  urn,url=u2[0],u2[1] #will do other urls soon too
  uri=urn2uri(urn)
  rs+= f'{collection} dcat:Dataset <{uri}> \n '
  rs+= f'<{uri}> dcat:Distribution <{u2[1]}> \n '
  return rs 

#def rows2collection_nt(rows,collectionName): #could reuse above in parts & transform
def rows2collection(rows,collectionName): #redo above 1st
  rs1=set_collectionName(collectionName)
  rs2=set_collection_rows(collectionName,rows)
  return rs1+rs2 

#assertThese=rows2collection(rows,"my1")
#assertThese 

#
minio_backup= "http://141.142.218.86" #can also reset this global
#use w/oss
minio_prod= "https://oss.geodex.org" #minio
minio_dev_= "https://oss.geocodes.earthcube.org"
minio_dev="https://oss.geocodes-dev.earthcube.org/"
minio=minio_prod #but need to reset for amgeo in dev, would rather have all in one space, eg.just above

#summoned=jsonld milled=rdf=which is really .nt ;though gets asserted as quads /?
#def urn2uri(urn): #from wget_rdf, replace w/this call soon
def urn2urls(urn): #from wget_rdf, replace w/this call soon
    "way we map URNs ~now" #check on this w/the URN changes 
    if urn==None:
        return f'no-urn:{urn}'
    #if(urn!=None and urn.startswith('urn:')):
    elif urn.startswith('urn:'):
        #global f_nt
       #url=urn.replace(":","/").replace("urn","https://oss.geodex.org",1) #minio
        url=urn.replace(":","/").replace("urn",minio,1) #minio
      # urlroot=path_leaf(url) #file w/o path
        urlj= url + ".jsonld" #get this as well so can get_jsfile2dict the file
      # urlj.replace("milled","summoned")
        url += ".rdf"
        #cs= f'wget -a log {url}' 
        #os_system(cs)
        #cs= f'wget -a log {urlj}' 
        #os_system(cs)
        #return url, urlroot, urlj
        return url, urlj

#only urls of rdf not downloadable yet
def urn2fnt(urn):
    "urn to end of rdf url as name for .nt file"
    rdf_urls=urn2urls(urn)
    fnt=file_base(path_leaf(rdf_urls[0])) + ".nt"
    return fnt

def rdf2nt(urlroot_):
    "DFs rdf is really .nt, also regularize2dcat"
    urlroot=urlroot_.replace(".rdf","") #to be sure
    global f_nt
    fn1 = urlroot + ".rdf"
    fn2 = urlroot + ".nt" #more specificially, what is really in it
    #cs= f'mv {fn1} {fn2}' #makes easier to load into rdflib..eg: #&2 read into df
    print(f'rdf2nt,fn1:{fn1}')
    cs= f'cat {fn1}|sed "/> /s//>\t/g"|sed "/ </s//\t</g"|sed "/doi:/s//DOI:/g"|cat>{fn2}'
    os_system(cs)   #fix .nt so .dot is better ;eg. w/doi
    f_nt=fn2
    return fn2
##
def is_node(url): #not yet
    #return (url.startswith("<") or url.startswith("_:B")) #a <p> slipped in
    return (url.startswith("<ht") or url.startswith("_:B"))

#def is_tn(url):
def tn2bn(url):
    "make blaze BNs proper for .nt"
    if url.startswith("t1"):
        return url.replace("t1","_:Bt1")
    else:
        return url

def cap_http(url):
    "<url>"
    if is_http(url):
        return f'<{url}>'
    else:
        return url

def cap_doi(url):
    "<doi>"
    #if url.lower().startswith("doi:"):
    if url.startswith("doi:"):
        return f'<{url}>'
    elif url.startswith("DOI:"):
        return f'<{url}>'
    else:
        return url

def fix_url3(url):
    "cap http/doi tn2bn"
    url=tn2bn(url)
    url=cap_http(url)
    url=cap_doi(url)
    #could put is_node check here
    return url

#def fix_url_(url,obj=True): #should only get a chance to quote if the obj of the triple
def fix_url(url):
    "fix_url and quote otherwise"
    if is_node(url):
        return url
    elif url.startswith("t1"):
        return url.replace("t1","_:Bt1")
    elif is_http(url):
        return f'<{url}>'
    elif url.startswith("doi:"):
        return f'<{url}>'
    elif url.startswith("DOI:"):
        return f'<{url}>'
    #elif obj:
    else:
        import json
        return json.dumps(url)
    #else:
    #    return url

def df2nt(df,fn=None):
    "print out df as .nt file"
    import json
    nt_str=""
    if fn:
        put_txtfile(fn,"")
    for index, row in df.iterrows():
        #s=row['s']
        s=df["s"][index]
        s=fix_url(s)
        p=df["p"][index]
        p=fix_url(p)
        o=df["o"][index]
        o=fix_url(o)
        if o=="NaN":
            o=""
        str3=f'{s} {p} {o} .\n'
        if dbg:
            print(str3)
        #else:
        nt_str += str3
        if fn:
            put_txtfile(fn,str3,"a")
        #need to finish up w/dumping to a file
    return df, nt_str

def get_rdf(urn,viz=None): #get graph 
    "get_graph as df, start of replacement for wget_rdf" #that doesn't need the ld cache
    df=get_graph(urn)
    dfo,nt_str=df2nt(df)
    if viz: #should fix this below 
        fn2=urn_leaf(urn) + ".nt" #try tail
        rdflib_viz(fn2) #find out if can viz later as well via hidden .nt file
    #return df #already returns the same as wget_rdf
    return df, nt_str #now str version of the .nt file as well

def get_rdf2nt_str(urn): #get graph 
    "get_graph as nt string" #that doesn't need the ld cache
    df=get_graph(urn)
    dfo,nt_str=df2nt(df)
    return nt_str #use for get_rdf2jld _str

def get_rdf2jld_str(urn):
    "get jsonld from endpoint" #for get_graph_jld route
    nt_str= get_rdf2nt_str(urn) #only strings no files
    g= nt_str2g(nt_str) #like nt2g
    jld_str = g.serialize(format="json-ld") #from nt2jld #shouldn't need rdflib-jsonld
    return compact_jld_str(jld_str)

def compact_jld_str(jld_str):
    from pyld import jsonld
    import json
    context = { "@vocab": "https://schema.org/"}
    doc = json.loads(jld_str)
    compacted = jsonld.compact(doc, context)
    r = json.dumps(compacted, indent=2)
    return r

def get_rdf2nt(urn):
    "get and rdf2nt" #rdf2nt was getting around df's naming, will be glad to get away from that cache
    df=get_rdf(urn)
    fn2=urn_leaf(urn) # + ".nt" 
    #append2allnt(fn2) #file not made yet, done during ec.viz() call
    if not is_str(fn2):
        print(f'get_rdf2nt,warning,fn2:{fn2}, make sure to run the Parameters cell to get the urn')
        fn2=""
    fn2 = fn2 + ".nt"
    global f_nt
    f_nt = fn2
    return df2nt(df,fn2) #seems to work w/a test urn
    #return df2nt(df)
##
#added warning bc saw eval'd params that still had urn as None, so re-ran it, and was ok
##
#have a version that returns jsonld, via file, then maybe more directly for a route
 #I have versions that build something up in a str(2nq)for rdflib, can do that..
 #for file version:
  #nt2g then dump in diff version, there are a few from url/file to jsonld as well
   #xml2nt &variants have use of serialize
def nt2jld(fn):
    "load .nt and convert2 jsonld"
    g=nt2g(fn)
    s=g.serialize(format="json-ld") 
    fnb=file_base(fn)
    fnt=fnb+".jsonld" 
    put_txtfile(fnt,s)
    return fnt

def nt2ttl(fn):
    "load .nt and convert2 .ttl"
    g=nt2g(fn)
    s=g.serialize(format="ttl") 
    fnb=file_base(fn)
    fnt=fnb+".ttl" 
    put_txtfile(fnt,s)
    return fnt

def get_rdf2jld(urn):
    "get_graph 2 nt then 2 jsonld"
    df=get_rdf2nt(urn)
    #fn2=urn_leaf(urn) # + ".nt" 
    fn2=urn_leaf(urn)  + ".nt" 
    return nt2jld(fn2)

def get_rdf2ttl(urn):
    "get_graph 2 nt then 2 ttl"
    df=get_rdf2nt(urn)
    #fn2=urn_leaf(urn) # + ".nt" 
    fn2=urn_leaf(urn)  + ".nt" 
    return nt2ttl(fn2)
##
def wget_rdf(urn,viz=None):
    "new version to get_rdf from the endpoint"
    if not viz:
        #if sparql_inited==None:
        if not sparql_inited:
            init_sparql()
        print(f'get_rdf2nt({urn})')
        return get_rdf2nt(urn) #use get_graph version for now
    else:
        return wget_rdf_(urn,viz)
#take urn2uri out of this, but have to return a few vars
def wget_rdf_(urn,viz=None):
    "old version, still wget's from the urn" #as long as the mapping fnc does not change again
    if not viz:
        #if sparql_inited==None:
        if not sparql_inited:
            init_sparql()
      # print(f'get_rdf2nt({urn})') #tried new version here 1st, but want option for old too
      # return get_rdf2nt(urn) #use get_graph version for now
    if urn==None:
        return f'no-urn:{urn}'
    #if(urn!=None and urn.startswith('urn:')):
    elif urn.startswith('urn:'):
        global f_nt
 #      url=urn.replace(":","/").replace("urn","https://oss.geodex.org",1)
 #      urlroot=path_leaf(url) #file w/o path
 #      urlj= url + ".jsonld" #get this as well so can get_jsfile2dict the file
 #      urlj.replace("milled","summoned")
 #      url += ".rdf"
        #url, urlroot, urlj = urn2uri(urn) #so can reuse this, also getting sys change/fining missing in minio
        url, urlj = urn2urls(urn) #so can reuse this, also getting sys change/fining missing in minio
        urlroot=path_leaf(url) #file w/o path
        cs= f'wget -a log {url}' 
        os_system(cs)
        cs= f'wget -a log {urlj}' 
        os_system(cs)
      # fn1 = urlroot + ".rdf"
      # fn2 = urlroot + ".nt" #more specificially, what is really in it
      # #cs= f'mv {fn1} {fn2}' #makes easier to load into rdflib..eg: #&2 read into df
      # cs= f'cat {fn1}|sed "/> /s//>\t/g"|sed "/ </s//\t</g"|sed "/doi:/s//DOI:/g"|cat>{fn2}'
      # os_system(cs)   #fix .nt so .dot is better ;eg. w/doi
      # f_nt=fn2
        rdf2nt(urlroot)
        #from rdflib import Graph
        #g = Graph()
        #g.parse(fn2)
        if viz: #can still get errors
            fn2=urn_leaf(urn) #try new
            rdflib_viz(fn2) #.nt file #can work, but looks crowded now
        return read_rdf(f_nt)
    elif urn.startswith('/'):
        url=urn.replace("/","http://geocodes.ddns.net/ld/",1).replace(".jsonld",".nt",1)
        urlroot=path_leaf(url) #file w/o path
        #url += ".nt"
        cs= f'wget -a log {url}' 
        os_system(cs)
        #fn2 = urlroot + ".nt" #more specificially, what is really in it
        if viz: #can still get errors
            #rdflib_viz(fn2) #.nt file #can work, but looks crowded now
            rdflib_viz(urlroot) #.nt file #can work, but looks crowded now
        return read_rdf(f_nt)
    else:
        return f'bad-urn:{urn}'

#rdf_inited=None
def init_rdf():
    #cs='apt-get install raptor2-utils graphviz'
    cs='apt-get install raptor2-utils graphviz libmagic-dev' #can add jq yourself
    os_system(cs)  #incl rapper, can do a few rdf conversions
    rdf_inited=cs

#should just put sparql init in w/rdf _init, as not that much more work

#sparql_inited=None
def init_sparql(): #maybe combine w/init_rdflib
    #cs='pip install sparqldataframe simplejson'
    cs='pip install sparqldataframe simplejson owlready2 pyld'
    os_system(cs)
    sparql_inited=cs
    ##get_ec("http://mbobak-ofc.ncsa.illinois.edu/ext/ec/nb/sparql-query.txt")
    #get_ec("https://raw.githubusercontent.com/MBcode/ec/master/NoteBook/sparql-query.txt")
    #return get_txtfile("sparql-query.txt")
    return get_query_txt()

#-
def dfn(fn):
    "FileName or int:for:d#.nt"
    if isinstance(fn, int):
        fnt=f'd{fn}.nt'
    else:
        fnt=fn
    return fnt
#-
def sq_file(sq,fn=1):
    fnt=dfn(fn) #maybe gen fn from int
    add2log(f'dataFN={fnt}')
    add2log(f'qry={sq}')
    if sparql_inited==None:
        si= init_sparql()  #still need to init
    #global default_world
    #from owlready2 import *
    import owlready2 as o2
    #o= o2.get_ontology("d1.nt").load()
    o= o2.get_ontology(fnt).load()
    return list(o2.default_world.sparql(sq))
#-
def pp_l2s(pp,js=None):
    "predicatePath list2str"
    if(js): #["spatialCoverage" "geo" "box" ], True  -> "spatialCoverage.geo.box"
        return "." + ".".join(pp)
    else: #["spatialCoverage" "geo" "box" ]  -> ":spatialCoverage/:geo/:box"
        return ":" + "/:".join(pp)

def rget(pp,fn=1):
    "predicate path to s/o values"
    fnt=dfn(fn)
#r=sq_file("PREFIX : <http://www.w3.org/ns/dcat#> SELECT distinct ?s ?o WHERE  { ?s :spatialCoverage/:geo/:box ?o}","d1.nt")
    #s1="PREFIX : <http://www.w3.org/ns/dcat#> SELECT distinct ?s ?o WHERE  { ?s "
    s1="PREFIX : <https://schema.org/> SELECT distinct ?s ?o WHERE  { ?s " #till fix sed
    s2=" ?o}"
    #r=sq_file(s1 + ":spatialCoverage/:geo/:box" + s2,dfn)
    pps=pp_l2s(pp)
    qs=s1 + pps + s2
    print(qs)
    #add2log(f'rget:{qs}')
    add2log(f'rget:{qs},{fnt}')
    r=sq_file(qs,fnt)
    return r
#-
def grep_po_(p,fn):
  "find predicate in nt file and returns the objects"
  #cs= f"grep '{p}' {fn}|cut -f 3"
  cs= f"grep '{p}' {fn}|cut -d' ' -f 3"
  rs= os_system_(cs)
  #ra=rs.split(" .\n")
  ra=rs.split("\n")
  ra=list(map(lambda x: x.strip(".").strip(" "), ra))[:-1]
  return ra #get rid of these

def grep_po(p,fn):
  "find predicate in nt file and returns the objects"
  cs= f"egrep '{p}' {fn}|cut -f 3"
  #cs= f"grep '{p}' {fn}|cut -d' ' -f 3"
  rs= os_system_(cs)
  ra=rs.split(" .\n")
  return ra
#could ret the Predicate,Object,(lists)and pred(s) could be the 2nd return
#unless where to call it grep_p2o or grep_pred2obj
#def grep_pred2obj(p,fn):
def grep2obj(p,fn): #=f_nt): #fn could default to (global) f_nt
  "find pattern in nt file and returns the objects, of the spo lines"
  cs= f"egrep '{p}' {fn}|cut -f 3"
  rs= os_system_(cs)
  #ra=rs.split(" .\n")
  ra=rs.split(".\n")
  if ra:
      ra=list(map(lambda x: x.strip().replace('"',''), ra))
  return ra
#get pack to using a local store, to be more robust
#def urn2accessURL(urn):
def urn2accessURL(urn,fnt=None):
    "get access/content url from urn/it's .nt file"
    if not fnt:
        fnt=urn2fnt(urn) #should be same as f_nt
    print(f'grep2obj:{fnt}')
    return grep2obj('accessURL|contentUrl',fnt)
#to iterate over this could have a getDatasetURLs &either give URNs or  ROWs&dfSPARQL
def getDatasetURLs(IDs,dfS=None):
  "return the URLs from every dataset given, by URNs or df w/rows"
  d1p= not isinstance(IDs[0], int)
  ds_urls= list(map(urn2accessURL,IDs)) if d1p else list(map(lambda row: dfRow2urls(dfS,row),IDs))  #or put in another row number to get url
  #ds_url= list(map(lambda urls: urls[0],ds_urls)) if d1p else list(map(lambda urls: urls[row][1], ds_urls)) #default to 1st of the urls
  ds_url= list(map(lambda urls: urls[0],ds_urls)) #default to 1st of the urls ;need to check in 2nd/sparql_nb w/o collection
  return ds_urls, ds_url #1st of each right now
#-might want to collect/order by file types
def sparql_f2(fq,fn,r=None): #jena needs2be installed for this, so not in NB yet;can emulate though
    "files: qry,data"
    if r: #--results= Results format (Result set: text, XML, JSON, CSV, TSV; Graph: RDF serialization)
        rs=f' --results={r} '
    else:
        rs=""
    fnt=dfn(fn) #maybe gen fn from int
    #if had txt put_txtfile; if qry.txt w/var then have2replace
    cs=f'sparql --data={fnt} --query={fq} {rs}'
    return os_system_(cs)

#-
#def nt2dn(fn,n):
def nt2dn(fn=f_nt,n=1):
    ".nt to d#.nt where n=#, w/http/s schema.org all as dcat" 
    fdn= f'd{n}.nt'
    #fnd=dfn(fn) #maybe gen fn from int
    print(f'nt2nd,fn:{fn}')
    cs=f'cat {fn}|sed "/ht*[ps]:..schema.org./s//http:\/\/www.w3.org\/ns\/dcat#/g"|cat>{fdn}'  #FIX
    os_system(cs) #this makes queries a LOT easier
    return fdn

def df2URNs(df):
  return df['g']

def dfRow2urn(df,row):
  URNs=df2URNs(df)
  return URNs[row]

def urn2rdf(urn,n=1):
    df=wget_rdf(urn)
    global f_nt
    nt2dn(f_nt,n)
    return df

def dfRow2rdf(df,row):
    urn=dfRow2urn(df,row)
    return urn2rdf(urn,row)

def dfRow2urls(df,row): 
    fnt=dfn(row) #check if dfRow2rdf already done
    from os.path import exists #can check if cached file there
    if not exists(fnt):
        dfRow2rdf(df,row)
    return rget(["contentUrl"],row)

def nt2g(fnt):
    from rdflib import ConjunctiveGraph #might just install rdflib right away
    g = ConjunctiveGraph(identifier=fnt)
    data = open(fnt, "rb") #or get_textfile -no
    g.parse(data, format="ntriples")
    return g

def nt_str2g(nt_str): 
    "nt2g w/str input"
    #from rdflib import ConjunctiveGraph #might just install rdflib right away
    from rdflib import Graph 
    import io
    #g = ConjunctiveGraph(identifier=fnt)
    g = Graph()
    ##data = open(fnt, "rb") #or get_textfile -no
    #data = io.StringIO(nt_str)
    print(f'data={nt_str}') #TypeError: can't concat str to bytes
    #g.parse(data, format="ntriples")
    g.parse(data=nt_str, format="ntriples")
    return g
#get_rdf2jld_str("urn:gleaner:summoned:lipdverse:509e465d0793506b237cea8069c3cb2d276fe9c2")
#data=<_io.StringIO object at 0x104a89a60>

#def diff_nt(fn1,fn2):
def diff_nt_g(fn1,fn2):
    #import rdflib
    from rdflib.compare import to_canonical_graph, to_isomorphic, graph_diff
    g1=nt2g(fn1)
    g2=nt2g(fn2)
    iso1 = to_isomorphic(g1)
    iso2 = to_isomorphic(g2)
    if iso1 == iso2:
        return g, None, None
    else:
        in_both, in_first, in_second = graph_diff(iso1, iso2)
        #dump_nt_sorted(in_both)
        #dump_nt_sorted(in_first)
        #dump_nt_sorted(in_second)
        return in_both, in_first, in_second 

#https://github.com/RDFLib/rdflib/blob/master/rdflib/compare.py

def dump_nt_sorted(g):
    for l in sorted(g.serialize(format='nt').splitlines()):
        if l: print(l.decode('ascii'))

#fix: rdflib/plugins/serializers/nt.py:28: UserWarning: NTSerializer does not use custom encoding.
 #warnings.warn("NTSerializer does not use custom encoding.")

def diff_nt(fn1,fn2):
    in_both, in_first, in_second = diff_nt_g(fn1,fn2)
    if in_both:
        print(f'in_both:{in_both}')
        dump_nt_sorted(in_both)
    if in_first:
        print(f'in_first:{in_first}')
        dump_nt_sorted(in_first)
    if in_second:
        print(f'in_second:{in_second}')
        dump_nt_sorted(in_second)
    return in_both, in_first, in_second 


def pp2so(pp,fn): #might alter name ;basicly the start of jq via sparql on .nt files
    "SPARQL qry given a predicate-path, ret subj&obj, given nt2dn run 1st, giving fn"
    fnt=dfn(fn) #maybe gen fn from int
    #pp=":spatialCoverage/:geo/:box"
    #sq=f'PREFIX : <http://www.w3.org/ns/dcat#> \n SELECT distinct ?s ?o WHERE { ?s {pp} ?o }'
    sqpp="""PREFIX : <http://www.w3.org/ns/dcat#>
        SELECT distinct ?s ?o
        WHERE { ?s predicate-path ?o }"""
    sq=sqpp.replace("predicate-path",pp)
    add2log(f'fn={fn},sq={sq}')
    if rdf_inited==None:
        init_rdf()
    from rdflib import ConjunctiveGraph #might just install rdflib right away
    g = ConjunctiveGraph(identifier=fnt)
    data = open(fnt, "rb") #or get_textfile -no
    g.parse(data, format="ntriples")
    results = g.query(sq)
    add2log(results) #runs but still need2check output../fix
    return [str(result[0]) for result in results]

def rdfxml2nt(fnb):
    if has_ext(fnb):
        fnb=file_base(fnb)
    if rdf_inited==None:
        init_rdf()
    cs= f'rapper -i rdfxml -o ntriples {fnb}.nt|cat>{fnb}.nt'
    os_system(cs) 

def nt2svg(fnb):
    if has_ext(fnb):
        fnb=file_base(fnb)
    if rdf_inited==None:
        init_rdf()
    cs= f'rapper -i ntriples -o dot {fnb}.nt|cat>{fnb}.dot'
    os_system(cs) 
    cs= f'dot -Tsvg {fnb}.dot |cat> {fnb}.svg'
    os_system(cs)
    #could spit out nt2dot and dot2svg, and check if output file exists, so wouldn't have to make it again

#re/consider running sed "/https/s//http/g" on the .nt file, as an option, 
 #for cases were it's use as part of the namespace is inconsistent


#https://stackoverflow.com/questions/30334385/display-svg-in-ipython-notebook-from-a-function
def display_svg(fn):
    if rdf_inited==None:
        init_rdf()
    from IPython.display import SVG, display
    display(SVG(fn))

#def append2allnt(fnb): #in_colab no .all.nt to start w/
def append2allnt(fnb=None):
    "append to default viz file"
    if has_ext(fnb): #bc not switching .ext could just give full name
        fnb=file_base(fnb)
    if not fnb:
        global f_nt #the current .nt file being looked at
        fnb=file_base(f_nt)
    if dbg: 
        print(f'append2allnt,fnb:{fnb}')
    cs= f'cat {fnb}.nt >> .all.nt'
    os_system(cs) 

def nt_viz(fnb=".all.nt"):
    if fnb==".all.nt" and f_nt!=None and os.path.isfile(f_nt):
        fnb=f_nt  #if have urn .nt file, &nothing run yet, can call w/o arg&will view it
    if has_ext(fnb):
        fnb=file_base(fnb)
    nt2svg(fnb) #base(before ext)of .nt file, makes .svg version&displays
    fns= fnb + ".svg"
    display_svg(fns)
    if fnb!=".all":
        append2allnt(fnb)

def rdfxml_viz(fnb): #cp&paste (rdf)xml file paths from in .zip files
    xml2nt(fnb)
    nt_viz(fnb)

#this could be generalized further to display available views of the DataFrame as well
 #so might call this viz_rdf & the other viz_df, but still have viz that can figure that out
def viz(fn=".all.nt"): #might call this rdf_viz once we get some other type of viz going
    if has_ext(fn):
        ext=file_ext(fn)
        fnb=file_base(fn) #unused, bc they should strip the ext anyway
    else:
        return "need a file extension, to know which routines to run to show it"
    if ext==".nt":
        nt_viz(fn)
    elif ext=='.xml':
        rdfxml_viz(fn)
    else:
        return "only handle .nt and .xml (rdf) right now"

#should change os version of wget to request so can more easily log the return code
 #maybe, but this is easiest way to get the file locally to have to use
  #though if we use a kglab/sublib or other that puts right to graph, could dump from that too
#host = "http://141.142.218.86:3031"
host = "http://mbobak.ncsa.illinois.edu:3031"
#import requests

def alive():
    import requests
    r = requests.get(f'{host}/alive')
    return r

def log_msg(url): #in mknb.py logbad routed expects 'url' but can encode things
    import requests
    ##r = requests.get(f'{host}/logbad/?url={url}')
    get=f'{host}/logbad/?url={url}'
    #had old url, but should be in sync w/ui url, and don't really need this, so
    #r = requests.get(get) #skip remote logging for now, &just do locally:
    add2log(get)
    #return r 
    return "" 

#add 'rty'/error handling, which will incl sending bad-download links back to mknp.py
 #log in the except sections, below

#def check_size_(fs,df): #earlier now unused version
#    if fs:
#        if fs<300:
#            df+= "[Warn:small]"
#    else:
#        df+= "[Warn:No File]"
#    return df

def check_size(fs,df):
    "FileSize,DataFrame as ret txt"
    dfe=None
    if fs:
        if fs<300:
            dfe= "[Warn:small]"
    else:
        dfe= "[Warn:No File]"
    if dfe:
        add2log(dfe)
        log_msg(dfe) #should incl url/etc but start w/this
        df+=dfe
    return df

#considter ext2ft taking the longer-txt down to the stnd file-ext eg. .tsv ..

def nt2ft(url): #could also use rdflib, but will wait till doing other queries as well
    "path2 .nt file -> encoding~FileType"
    cs=f"grep -A4 {url} *.nt|grep encoding|cut -d' ' -f3"
    if cs:
        return os_system_(cs) 
    else:
        return None

def file_type(fn): #w/unzip it can be a dir; so fix
    from os.path import exists, isdir, isfile 
    import magic
  # if exists(fn):
  #     add2log(magic.from_file(fn))
  #     mt=magic.from_file(fn, mime = True)
    if exists(fn):
        if isfile(fn):
            add2log(magic.from_file(fn))
            mt=magic.from_file(fn, mime = True)
        elif isdir(fn):
            mt="is a dir"
        else:
            mt="exists, but not file or dir"
    else:
        mt="file not found"
    add2log(f'{fn},mime:{mt}')
    return mt
#get something that can look of header of download, before get the file, too

#def read_file(fnp, ext=nt2ft(fnp)):  $should send 'header' in
def read_file(fnp, ext=None):  #download url and ext/filetype
    "can be a url, will call pd read_.. for the ext type"
    import pandas as pd
    import re
    if rdf_inited==None: #new, going to need it
        init_rdflib()
        init_rdf()
    if(ext==None): #find filetype from .nt ecodingFormat
        ext=nt2ft(fnp)
    fn=fnp.rstrip('/') #only on right side, for trailing slash, not start of full pasted path
    fn1=path_leaf(fn) #just the file, not it's path
    fext=file_ext(fn1) #&just it's .ext
    #url = fn
    if(ext!=None):
        if ext.startswith('.'):
            ft=ext
        else:
            ft="." + ext
    else: #use ext from fn
        ft=str(fext)
        ext=ft
    df=""
    #bad_lines going away, get netcdf etc in here, even though I don't see it much
    if ext==None and len(ft)<1:
        wget(fn)
        df="no fileType info, doing:[!wget $url ],to see:[ !ls -l ] or FileExplorerPane on the left"
    elif ft=='.tsv' or re.search('tsv',ext,re.IGNORECASE) or re.search('tab-sep',ext,re.IGNORECASE):
        try:
            #df=pd.read_csv(fn, sep='\t',comment='#',warn_bad_lines=True, error_bad_lines=False)
            #df=pd.read_csv(fn, sep='\t',comment='#',warn_bad_lines=True, on_bad_lines='skip')
            df=pd.read_csv(fn, sep='\t',comment='#', on_bad_lines='skip')
            #df=pd.read_csv(fn, sep='\t',comment='#')
        except:
            df = str(sys.exc_info()[0])
            pass
    elif ft=='.csv' or re.search('csv',ext,re.IGNORECASE):
        try:
            #df=pd.read_csv(fn,comment="#",warn_bad_lines=True, error_bad_lines=False)
            df=pd.read_csv(fn,comment='#', on_bad_lines='skip')
            #df=pd.read_csv(fn,comment="#")
        except:
            df = str(sys.exc_info()[0])
            pass
    elif ft=='.txt' or re.search('text',ext,re.IGNORECASE): #want to be able to header=None here
        try:
            df=pd.read_csv(fn, sep='\n',comment='#')
        except:
            df = str(sys.exc_info()[0])
            pass
    elif ft=='.json' or re.search('js',ext,re.IGNORECASE):
        try:
            print(f'read_json({nf}')
            df=pd.read_json(fn)
        except:
            df = str(sys.exc_info()[0])
            pass
    elif ft=='.html' or re.search('htm',ext,re.IGNORECASE):
        try:
            df=pd.read_html(fn)
        except:
            df = str(sys.exc_info()[0])
            pass
    elif ft=='.zip' or re.search('zip',ext,re.IGNORECASE):
        ft='.zip'
        fs=wget_ft(fn,ft)
        #fs=os.path.getsize(fnl) #assuming it downloads w/that name
#       df=pd.read_csv(fn, sep='\t',comment='#')
        #df="can't read zip w/o knowing what is in it, doing:[!wget $url ],to see:[ !ls -l ]"
        df=f'can not read zip w/o knowing what is in it, doing:[!wget $url ],to see:[ !ls -l ]size:{fs} or FileExplorerPane on the left'
        file_type(fn1) #save2 mt and use, next
        #if fs and fs<300:
        #    df+= "[Warn:small]"
        df=check_size(fs,df)
    else:
        fs=wget_ft(fn,ft)
        #fs=os.path.getsize(fnl) #assuming it downloads w/that name
        #df="no reader, can !wget $url"
        df=f'no reader, doing:[!wget $url ],to see:[ !ls -l ]size:{fs} or FileExplorerPane on the left'
        file_type(fn1) #save2 mt and use, next
        #if fs and fs<300:
        #    df+= "[Warn:small]"
        df=check_size(fs,df)
    #look into bagit next/maybe, also log get errors, see if metadata lets us know when we need auth2get data
    #if(urn!=None): #put here for now
    #    wget_rdf(urn)
    return df

 #probably drop the [ls-l] part&just have ppl use fileBrowser, even though some CLI would still be good
#not just 404, getting small file back also worth logging
#---- sources:
def get_sources_csv(url="https://raw.githubusercontent.com/MBcode/ec/master/crawl/sources.csv"):
    return get_ec_txt(url)

def get_sources_df(url="https://raw.githubusercontent.com/MBcode/ec/master/crawl/sources.csv"):
    s= read_file(url,".csv")
    return s.loc[s['Active']] #can only crawl the active ones

#def get_sources_urls(): #could become crawl_
def crawl_sources_urls(): #work on sitemap lib to handle non-stnd ones
    import re
    s=get_sources_df()
    for url in s['URL']:
        print(f'sitemap:({url})') #dbg
        #urlb=re.sub('\/site*.xml','',url)
        urlb=re.sub('sitemap.xml','',url)
        #crawl_sitemap(urlb)
        print(f'crawl_sitemap({urlb})') #dbg
#----
def qs2graph(q,sqs):
    return sqs.replace('${q}',q)
def urn2graph(urn,sqs):
    #return sqs.replace('<${g}>',urn)
    return sqs.replace('<${g}>',f'"{urn}"')
#def sti(sqs, matchVar, replaceValue): #assume only1(replacement)right now,in the SPARQL-Qry(file)String(txt)
#    "sparql template instantiation, 2qry2df"
#    return sqs.replace(matchVar,replaceValue)
def v2iqt(var,sqs):  #does the above fncs
    if '<${g}>' in sqs: #var=urn
        #return sqs.replace('<${g}>',var)
        #return sqs.replace('<${g}>',f'"{var}"')
        return sqs.replace('<${g}>',f'<{var}>')
    if '${q}' in sqs:   #var=q
        return sqs.replace('${q}',var)
    else:
        return sqs #when nothing to replace, like in get_graphs
    #could add relatedData case, but changed to 'q' for now
    #really if only 1 var, could always just change it
    #_someday could send in dict to replace if >1

#def iqt2df(iqt,endpoint="https://graph.geodex.org/blazegraph/namespace/nabu/sparql"):
#def iqt2df(iqt,endpoint="https://graph.geocodes.earthcube.org/blazegraph/namespace/earthcube/sparql"):
#def iqt2df(iqt,endpoint=dflt_endpoint):
def iqt2df(iqt,endpoint=None):
    "instantiated-query-template/txt to df"
    if not iqt:
        return "need isntantiated query text"
    import sparqldataframe, simplejson
    if sparql_inited==None:
        si= init_sparql()  #still need to init
        #qs= iqt #or si  #need q to instantiate
    #add2log(iqt)
    global dflt_endpoint
    if not endpoint:
        endpoint=dflt_endpoint
    add2log(f'query:{iqt}')
    add2log(f'endpoint:{endpoint}')
    df = sparqldataframe.query(endpoint, iqt)
    return df

def v4qry(var,qt):
    "var + query-type 2 df"
    if not var:
        var=""
    sqs = eval("get_" + qt + "_txt()") #get_  _txt   fncs, are above
    if not is_str(sqs):
        print('f4qry get_ {qt} _txt() gave; {sqs}, so aborting')
        return ""
    iqt = v2iqt(var,sqs)
    #add2log(iqt) #logged in next fnc
    return iqt2df(iqt)

def search_query(q): #same as txt_query below
    return v4qry(q,"query")

#functionality that is see on dataset page:

def search_relateddatafilename(q):
    return v4qry(q,"relateddatafilename")

def search_download(urn):
    return v4qry(urn,"download")

def search_webservice(urn):
    return v4qry(urn,"webservice")

def search_notebook(urn):
    return v4qry(urn,"notebook")

#
def subj2urn(doi):
    "<<doi a so:Dataset>>'s graph"
    return v4qry(doi,"subj2urn")

def get_graphs():
    "return all the g URNs"
    return v4qry("","graphs")

def get_graph(g):
    "return all triples from g w/URN"
    return v4qry(g,"graph")

def get_summary(g=""): #g not used but could make a version that gets it for only 1 graph
    "return summary version of all the graphs quads"
    return v4qry(g,"summary")

#def get_summary_query(g=""): #g not used but could make a version that gets it for only 1 graph
#search_query above, should now use this
def summary_query(g=""): #this is finally used in: txt_query_summary
    "replacement txt_query of new summary namespace" #or summary2/etc check
    return v4qry(g,"summary_query") #could call this the fast_query



#summary_endpoint = dflt_endpoint.replace("earthcube","summary")
 #for now, but will have to check, at times
 #no 2nd change, all vars should be the same from the summary
#def txt_query_(q,endpoint=None):
def txt_query_(q,endpoint=None):
    "or can just reset dflt_endpoint"
    global dflt_endpoint
    if not endpoint:
        df=txt_query(q)
    elif endpoint=="summary": #1st try for summary query
        save = dflt_endpoint #but do not do till can switch the qry as well
        dflt_endpoint = dflt_endpoint.replace("/earthcube/","/summary2/")
        print(f'summary:txt_query,w/:{dflt_endpoint}')
        #df=txt_query(q)
        df=summary_query(q)
        dflt_endpoint = save
    else:
        save = dflt_endpoint
        dflt_endpoint = endpoint
        print(f'txt_query,w/:{dflt_endpoint}')
        df=txt_query(q)
        dflt_endpoint = save
    return df

def txt_query_summary(q): #might need to switch qry as well, to gs.txt
    return txt_query_(q,"summary")

#def get_graphs_list(endpoint=None):
def get_graphs_list(endpoint=None,dump_file=None):
    "get URNs as list, can send in alt endpoint"
    global dflt_endpoint
    if not endpoint:
        dfg=get_graphs()
    else:
        save = dflt_endpoint
        dflt_endpoint = endpoint
        dfg=get_graphs()
        dflt_endpoint = save
    if dump_file:
        dfg.to_csv(dump_file)
    return dfg['g'].tolist()

def get_graphs_cache(endpoint="http://ideational.ddns.net:9999/bigdata/namespace/nabu/sparql",dumpfile=None):
    print(f'get_graphs_cache:{endpoint}')
    l= get_graphs_list(endpoint)
    if dumpfile:
        list2txtfile(dumpfile,l)
    return l

def get_graphs_lon(repo=None,endpoint="http://ideational.ddns.net:3040/all/sparql"): 
    "for when I host a repo w/fuseki testing"
    endpnt= endpoint if repo==None else endpoint.replace("all",repo)
    print(f'get_graphs_lon:{endpnt}')
    return get_graphs_list(endpnt)

#def get_graph_per_repo(grep="milled",endpoint=None,dump_file="graphs.csv"): #try w/(None, ncsa_endpoint)
def get_graph_per_repo(grep="milled",endpoint="https://graph.geodex.org/blazegraph/namespace/earthcube/sparql",dump_file="graphs.csv"):
    "dump a file and sort|uniq -c out the repo counts"
    gl=get_graphs_list(endpoint,dump_file) #this needs full URN to get counts for the same 'repo:' s
    gn=len(gl)
    print(f'got:{gn} graphs')
    if grep != "milled":
        cs=f"cut -d':' -f2- {dump_file} |cut -d'/' -f1 | sort | uniq -c |sort -n" #this is for my ld-cache
    else:
        cs=f"cut -d':' -f3,4 {dump_file} | grep milled | sort | uniq -c |sort -n" #this is for gleaner milled..
    return os_system_(cs)

def urn_tail(urn):
    "like urn_leaf"
    return  urn if not urn else urn.split(':')[-1]

def urn_tails(URNs):
    return list(map(lambda s: s if not s else s.split(':')[-1],URNs))
    #return list(map(urn_tail,URNs))

def get_graphs_tails(endpoint):
    "just the UUIDs of the URNs in the graph"
    URNs=get_graphs_list(endpoint)
    return urn_tails(URNs)

#should get graph.geo.. from https://dev.geocodes.earthcube.org/#/config dynamically
 #incl the default path for each of those other queries, ecrr, ;rdf location as well
#=========append fnc from filtereSPARQLdataframe.ipynb
#def sq2df(qry_str):
#def txt_query(qry_str): #consider sending in qs=None =dflt lookup as now, or use what sent in
def txt_query(qry_str,sqs=None): #a generalized version would take pairs/eg. <${g}> URN ;via eq urn2graph
    "sparql to df"
    if sparql_inited==None:
        #qs=init_sparql()  #does: get_query_txt &libs
        si= init_sparql()  #still need to init
        #qs= sqs or init_sparql()  
        qs= sqs or si
    else:
        #qs=get_txtfile("sparql-query.txt")
        qs= sqs or get_txtfile("sparql-query.txt")
    import sparqldataframe, simplejson
    #endpoint = "https://graph.geodex.org/blazegraph/namespace/nabu/sparql"
    #endpoint = "https://graph.geocodes.earthcube.org/blazegraph/namespace/earthcube/sparql"
    global dflt_endpoint
    endpoint = dflt_endpoint
    add2log(qry_str)
    q=qs.replace('${q}',qry_str)
    add2log(q)
    #q=qs.replace('norway',qry_str) #just in case that is still around
    #q=qs
    #print(f'q:{q}')
    df = sparqldataframe.query(endpoint, q)
    #df.describe()
    return df

#==w/in-search-related-data: https://github.com/MBcode/ec/blob/master/qry/rec.py
#import pandas as pd
#import numpy as np
#import simplejson
#import sparqldataframe
#from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.metrics.pairwise import cosine_similarity
cosine_sim=None

def get_subj_from_index(index):
    return df[df.index == index]["subj"].values[0]

def get_index_from_subj(subj):
    return df[df.subj == subj]["index"].values[0]

def combine_features(row):
    try:
        return row['kw'] +" "+row['name']+" "+row["description"]+" "+row["pubname"]
    except:
        print("Error:", row)

def get_related(likes):
    global cosine_sim
    #movie_user_likes = "Avatar"
    #should pick one of the ones from the df randomly, or can do them all 
    #movie_user_likes = "https://www.bco-dmo.org/dataset/752737"
    ## Step 6: Get index of this movie from its subj
    dataset_index = get_index_from_subj(likes)
    similar_datasets =  list(enumerate(cosine_sim[dataset_index]))
    ## Step 7: Get a list of similar movies in descending order of similarity score
    sorted_similar_datasets = sorted(similar_datasets,key=lambda x:x[1],reverse=True)
    ## Step 8: Print subjs of first 50 movies
    i=0
    for element in sorted_similar_datasets:
        print(get_subj_from_index(element[0]))
        i=i+1
        if i>50:
            break
    return sorted_similar_datasets

def get_related_indices(like_index):
    "return a list of indices that are related to input index"
    global cosine_sim
    similar_indices =  list(enumerate(cosine_sim[like_index]))
    sorted_similar = sorted(similar_indices,key=lambda x:x[1],reverse=True)
    #return sorted_similar
    return list(map(first,sorted_similar))

def dfCombineFeaturesSimilary(df, features = ['kw','name','description','pubname']):
    "run only once per new sparql-df"
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    global cosine_sim
    df.insert(0,'index',range(0,len(df)))
    df.set_index('index')
    df["combined_features"] = df.apply(combine_features,axis=1)
    ##Step 4: Create count matrix from this new combined column
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df["combined_features"])
    terms=cv.get_feature_names() #new for topic-modeling
    tl=len(terms)
    print(f'topic-terms:{tl}')
    ##Step 5: Compute the Cosine Similarity based on the count_matrix
    cosine_sim = cosine_similarity(count_matrix) 

#=so after sparql-nb: df=txt_query(q)
#can dfCombineFeaturesSimilary(df)
#then get_related_indices(row)
#=I should also write other fnc to access rows of txt_query df returns, to get possible donwloads
def test_related(q,row=0): #eg "Norway"
    df=txt_query(q) #this should use summary soon too
    dfCombineFeaturesSimilary(df)
    return get_related_indices(row)
#but sparql-nd will already have the df calculated, so just do the similarity-matrix for it once, 
 #then call get_related_indices for each dataset/row you want to look at, or can now use:
def show_related(df,row):  #after dfCombineFeaturesSimilary is run on your df 'sparql results'
    #main=df['description'][row].strip() #this should be in the related-df
    #print(f'related to row={row},{main}')
    related=get_related_indices(row)
    if len(df)<4:
        print("not many to compare with")
    for ri in related:
        des=df['description'][ri].strip()
        print(f'{ri}:{des}')

#-------------------------------------------------------------
#convert a jsonld record to a minimal crate ;started in j2c.py
crate_top = """
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
crate_middle = "},"
#then all distribution records w/"@id": ... inserted  ;w/, btwn
crate_bottom = "]}"

#now given a filename, load in the jsonld, and find the distribution
# go over that array, and make the ..url into @id's that will also go w/in the hasPart

def get_distr_dicts(fn):
    "distribution dictionary/s"
    d=get_jsfile2dict(fn)
    return d.get("distribution")

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
    print(crate_top)
    #d=get_distribution(fn)
    dl=get_distr_dicts(fn)
    #for d in dl: #needs a comma btwn
    #    print(json.dumps(d))
    dl2=list(map(add_id,dl))
    ids=list(map(get_idd,dl))
    print(json.dumps(ids))
    print(crate_middle)
    print(json.dumps(dl2))
    print(crate_bottom)

def jld2crate_(fn):
    mkdir("roc") #for now
    fn_out="roc/" + fn
    put_txtfile(fn_out,crate_top)
    dl=get_distr_dicts(fn)
    dl2=list(map(add_id,dl))
    ids=list(map(get_idd,dl))
    put_txtfile(fn_out,json.dumps(ids))
    put_txtfile(fn_out,crate_middle)
    put_txtfile(fn_out,json.dumps(dl2))
    put_txtfile(fn_out,crate_bottom)

#so can take URN jsonld and make a crate, still need the URNs though
#tests on http://geocodes.ddns.net/ld/iedadata/324529.jsonld will take these out
def t1():
    jld2crate("324529.jsonld")

def t2(fn="324529.jsonld"):
    jld2crate_(fn)
#if we stay w/python /need to run on all
#I will have it put to files, w/more checks
#&use alt predicates for the @id if needed

#Still should add URN as another entry in crate
 #which is something gleaner generated
 #I wish we could use(a version of)the download url
 #and then we would all know what to expect w/o 
  #depending on some centeral rand#generator

#blabel: take a triple file w/every line ending in " ." and use filename to make a quad, needed for gleaner/testing
#potentially useful elsewhere; eg. if added repo: could use this in my workflow to make quads
#DF's gleaner uses the shah of the jsonld to name the .rdf files which are actually .nt files
# but then there are lots of .nq files that are actually .nt files, but should be able to get them w/this
#maybe someplace in nabu this is done, but by then I can't have the files to load them

#use filename to convert .rdf file to a .nq file
#▶<102 a09local: /milled/geocodes_demo_datasets> mo 09517b808d22d1e828221390c845b6edef7e7a40.rdf
#_:bcbhdkms5s8cef2c4s7j0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://schema.org/Dataset> .
#goes to:
#_:bcbhdkms5s8cef2c4s7j0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://schema.org/Dataset> "urn:09517b808d22d1e828221390c845b6edef7e7a40".
#fn = "09517b808d22d1e828221390c845b6edef7e7a40.rdf"

#https://stackoverflow.com/questions/3675318/how-to-replace-the-some-characters-from-the-end-of-a-string
def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail

#def fn2nq(fn): #from 2nq.py
def nt_fn2nq(fn): #already a nt2nq
    "take a fn.* returns a fn.nq w/4th col urn:fn"
    fnb = file_base(fn)
    fn2 = fnb + ".nq"
    replace_with = f' <urn:{fnb}> .'
    with open(fn2,'w') as fd_out:
        with open(fn,'r') as fd_in:
            for line in fd_in:
                #line_out = line.replace(" .",f' "urn:{fnb}" .')
                #replace_with = f' "urn:{fnb}" .'
                ll=len(line)
                if ll>9:
                    line_out = replace_last(line, " .", replace_with)
                    fd_out.write(line_out)
    return fn2

#could do w/read_rdf then insert fn into 4th column
 #then w/recipy could generate a shah that is tracked by it's prov like system

def riot2nq(fn):
    "process .jsonld put out .nq"
    fnb = file_base(fn)
    fn2 = fnb + ".nq"
    replace_with = f' <urn:{fnb}> .'
    nts = os_system_(f'riot --stream=nt {fn}')
    fd_in = nts.split("\n") 
    lin=len(fd_in)
    print(f'got {lin} lines')
    with open(fn2,'w') as fd_out:
        for line in fd_in:
            ll=len(line)
            if ll>9:
                line_out = replace_last(line, " .", replace_with)
                fd_out.write(line_out)
                fd_out.write('\n')
    return fn2

def to_nq(fn,prefix=None):
    "process .jsonld put out .nq"
    fnb = file_base(fn)
    fn2 = fnb + ".nq"
    if exists(fn2):
        print(f'riot2nq:{fn2} already there')
    replace_with = f' <urn:{fnb}> .'
   #nts = os_system_(f'riot --stream=nt {fn}')
    nts=to_nt_str(fn)
    fd_in = nts.split("\n") 
    lin=len(fd_in)
    print(f'got {lin} lines')
    with open(fn2,'w') as fd_out:
        for line in fd_in:
            #ll=len(line)
            if no_error(line):
                line_out = replace_last(line, " .", replace_with)
                fd_out.write(line_out)
                fd_out.write('\n')
    return fn2

#this seems to be out of sync w/2nq.py, fix
def fn2nq(fn): #if is_http wget and call self again/tranfrom input
    "output fn as .nq"
    if is_http(fn):
        fn=wget(fn)
    print(f'fn2nq on:{fn}')
    ext = file_ext(fn)
    print(f'2nq file_ext:{ext}')
    fn2="Not Found"
  # if ext==".rdf": #df's idea for .nt files
  #     #print(f'cwd:{cwd}')
  #     repo=path_leaf(cwd)
  #     #print(f'repo:{repo}')
  #     prefix=f'gleaner:summoned:{repo}'
  #     print(f'prefix:{prefix}')
  #     fn2=fn2nq(fn,prefix)
    if ext==".nt":
        fn2=fn2nq(fn)
    if ext==".jsonld":
        #fn2=riot2nq(fn)
        fn2=to_nq(fn)
    else: #it might still work:
        fn2=riot2nq(fn)
    print(f'gives:{fn2}')
    return fn2

#this gets minio buckets but could do get_htm_dir
 #or if run on machine w/crawl can do very quickly
 #_think I considered something over a part of get_oss_files
  #that could tell if minio or other html LD listing
#there is also the ability to just read it all into rdflib and query that
  #def xml2nt(fn,frmt="xml") takes json-ld as a format
  #also: def riot2nq(fn): "process .jsonld put out .nq"
 #that might be easier in the notebook, but this fuseki:3030 can be shared

def summoned2nq(s=None):
    "list of jsonld to one nq file"
    if not s:
        s=get_oss_files("summoned")
        sl=len(s)
        print(f'summoned:{sl} 2nq')
    fnout=f'{repo_name}.nq'
    #os_system(f'yes|gzip {fnout}') #complains if not there
    os_system(f'echo ""> {fnout}')
    nql=list(map(fn2nq,s))
    for nq in nql:
        print(f'summoned2nq,nq:{nq}')
        os_system(f'cat {nq}>>{fnout}')
    return fnout

def serve_nq(fn):
    "serve file w/fuseki" #could also do w/blasegraph, for txt-test/final-run
    fnb=file_base(fn)
    cs=f'nohup fuseki-server -file={fn} /{fnb} &'
    print(f'assuming no fuseki process, check for this new one:{cs}')
    os_system(cs)

def summon2serve(s=None): #~nabu like
    "get jsonld and serve the quads"
    fnout=summoned2nq(s)
    #cs=f'nohup fuseki-server -file={fnout} /{repo_name} &'
    #os_system(cs)
    serve_nq(fnout)
    return fnout

#sitemap url to LD-cache filenames
 #in mine it is BASE_URL + file_leaf(ur)
 #gleaner needs a mapping from it's PROV:

def prov2mapping(url): #use url from p above
    "read&parse 1 PROV record"
    import json
    #print(f'prov2mapping:{url}')
    j=url2json(url)
    d=json.loads(j)
    #print(d)
    g=d.get('@graph')
    if g:
        gi=list(map(lambda g: g.get("@id"), g))
        smd=g[1] #assume 1 past the context, 1st thing being from sitemap
        sm=smd.get("@id") #gi[0]
        u=collect_pre_(gi,"urn:")
        u0=u[0]
        #print(f'{sm}=>{u0}')
        #return sm, u #if expect >1
        return sm, u[0]
    else:
        return f'no graph for:{url}'

def prov2mappings(urls): #use urls from p above
    "get sitemap<->UUID in summoned,&sitemap"
    sitemap2urn={}
    urn2sitemap={} #might need this more
    for url in urls:
        key,value=prov2mapping(url)
        sitemap2urn[key]=value
        urn2sitemap[value]=key
        value2=value.split(':')[-1]   #so can also lookup form UUID w/o urn:... before it
        urn2sitemap[value2]=key #will be in same dict, so can lookup by either
    sitemap=list(sitemap2urn.keys())
    if dbg:
        print(f'prov-sitemap:{sitemap}')
    #return sitemap2urn, urn2sitemap
    return sitemap2urn, urn2sitemap, sitemap

#some bucket/gen-urls will be json(ld)
def url2json(url):
    import requests
    r=requests.get(url)
    return r.content

def get_url(url): #also in testing 
    "request.get url"
    import requests
    r=requests.get(url)
    return r.content

def is_bytes(bs):
    return isinstance(bs, bytes)

#_testing was@2672
#_testing end

def is_html(str):
    return "<html>" in str

def is_http(u):
    if not is_str(u):
        print("might need to set LD_cache") #have this where predicate called
        return None
    #might also check that the str has no spaces in it,&warn/die if it does
    return u.startswith("http")

def is_urn(u):
    if not is_str(u):
        print("might need to set LD_cache")
        return None
    return u.startswith("urn:")

def leaf(u):
    if is_http(u):
        return path_leaf(u)
    elif is_urn:
        return urn_leaf(u)
    else:
        print('no leaf:{u}')
        return u

def leaf_base(u):
    lf=leaf(u)
    if lf:
        return file_base(lf)
    else:
        print('no leaf_base:{u}')
        return lf

#_testing: was@3041
#_testing end

#extra around summary
def rcsv(fn,d=","):
    import pandas as pd
    return pd.read_csv(fn,delimiter=d)

def tgc1_(ep=None):
    "tgc1 that can use other than dflt namespace"
    if ep:
        global dflt_endpoint
        dflt_endpoint=ep
    print(f'using:{dflt_endpoint}')
    df=get_summary("")
    ln=len(df)
    print(f'got:{ln}')
    df.to_csv("summary-gc1.csv")
    return df #assume pandas

def tgc1():
    "summarize and endpoint to csv for tsum.py to turn to tll for loading into summary namespace"
    global dflt_endpoint,gc1_endpoint
    dflt_endpoint=gc1_endpoint
    print(f'using:{dflt_endpoint}')
    df=get_summary("")
    ln=len(df)
    print(f'got:{ln}')
    df.to_csv("summary-gc1.csv")
    return df #assume pandas

#might very well put tsum.py functionality here
 #will also write a similar df row mapping as 1st quick dump of sparqldataframe df to .nt file
  #though I'm sure there will be better/more build up ways
