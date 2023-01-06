#pulled from ec.py by mbobak@illinois.edu
#import ec #still needs refs out to ec. now for much of this part to work 
import ec2 #start ec.py w/o this file as ec2, till goes through testing
import os
import sys
import json
#_testing: was@10
repo_name="geocodes_demo_datasets" #for testing
#testing_bucket="citesting" #or bucket_name
#testing_bucket="test3" #or bucket_name
testing_bucket="mbci2" #using this vs what send in in places/fix this
ci_minio="https://oss.geocodes-dev.earthcube.org"
#ci_url=f'https://oss.geocodes-dev.earthcube.org/{testing_bucket}'
ci_url=f'{ci_minio}/{testing_bucket}' #better to have a fnc set it
bucket_url=f'https://oss.geocodes-dev.earthcube.org/{testing_bucket}' #use in oss
#testing_endpoint="http://ideational.ddns.net:3030/geocodes_demo_datasets/sparql"
testing_endpoint=f'http://ideational.ddns.net:3030/{repo_name}/sparql'
#testing_endpoint="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/{besting_bucket}/sparql"
gc1_minio = "https://oss.geocodes-1.earthcube.org/"
#_testing end


#_testing: was@40 
#from 'sources' gSheet: can use for repo:file_leaf naming/printing
base_url2repo ={"https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/main/metadata/Dataset/json": "geocodes_demo_datasets",
        "https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/main/metadata/Dataset/allgood": "geocodes_demo_datasets",
        "https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/main/metadata/Dataset/bad": "geocodes_demo_bad",
                "http://mbobak.ncsa.illinois.edu/ec/minio/test3/summoned/geocodes_demo_datasets": "test3"
        } #won't match if '/' at end of key
#can load sitemaps from gSheet, or even better github, here are a few now, in the order the get_graph_per_repo puts them out
 # https://raw.githubusercontent.com/MBcode/ec/master/test/sitemaps.csv #had to take bad ones out again
named_sitemaps={ #putting version of this in my ec/test as sitemaps.csv
"ssdb.iodp": "https://ssdb.iodp.org/dataset/sitemap.xml",
"usap-dc": "https://www.usap-dc.org/view/dataset/sitemap.xml",
#"xdomes": "https://xdomes.tamucc.edu/srr/sensorML/sitemap.xml",
"iris": "http://ds.iris.edu/files/sitemap.xml",
#"balto": "http://balto.opendap.org/opendap/site_map.txt ",
"DesignSafe": "https://www.designsafe-ci.org/sitemap.xml ",
#"neon": "https://geodex.org/neon_prodcodes_sm.xml",
"opentopography": "https://portal.opentopography.org/sitemap.xml",
"earthchem": "https://ecl.earthchem.org/sitemap.xml",
"lipidverse": "https://lipdverse.org/sitemap.xml",
"magic": "https://www2.earthref.org/MagIC/contributions.sitemap.xml",
#"neotomadb": "http://data.neotomadb.org/sitemap.xml",
"cchdo": "https://cchdo.ucsd.edu/sitemap.xml",
"unavco": "https://www.unavco.org/data/doi/sitemap.xml",
"hydroshare": "https://www.hydroshare.org/sitemap-resources.xml",
"bco-dmo": "https://www.bco-dmo.org/sitemap.xml",
"opencoredata": "http://opencoredata.org/sitemap.xml",
"iedadata": "http://get.iedadata.org/doi/xml-sitemap.php",
"ucar": "https://data.ucar.edu/sitemap.xml",
"unidata": "https://www.unidata.ucar.edu/sitemap.xml",
"linked.earth": "http://wiki.linked.earth/sitemap.xml",
"r2r": "https://service-dev.rvdata.us/api/sitemap/",
"geocodes_demo_dataset": "https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/gh-pages/metadata/Dataset/sitemap.xml",
"amgeo": "https://amgeo-dev.colorado.edu/sitemap.xml",
"rr": "https://object.cloud.sdsc.edu/v1/AUTH_85f46aa78936477d8e71b186269414e8/gleaner-summoned"
}
sitemaps=list(named_sitemaps.values())
repos=list(named_sitemaps.keys())

def test_sitemaps(sitemaps=named_sitemaps):
    sitemaps=list(named_sitemaps.values())
    print(f'getting lengths for:{sitemaps}')
    sc=sitemaps_count(sitemaps) #but needs to handle timeouts before running that full list
    return sc  #this will work w/dflt list now

def ld_ls_jsonld(repo,base_path=None):
    #if not base_path:
    #    return "go to base ld-cache dir"
    return ls_(f'{repo}/*.jsonld')

def ld_jsonld_counts(repos=repos):
    rd={}
    for repo in repos:
        l=ld_ls_jsonld(repo)
        ln=len(l)
        print(f'{repo} has {ln}')
        rd[repo]=ln
    return rd
#_testing end

#_testing: was@427
#https://stackoverflow.com/questions/48647534/python-pandas-find-difference-between-two-data-frames
def df_diff(df1,df2): #doesn't work as well as I would like in all situations, work on/fix/finish
    import pandas as pd
    if not is_df(df1):
        print("df_diff:1st arg:wrong type:{df1}")
        return pd.DataFrame() #False
    if not is_df(df2):
        print("df_diff:2nd arg:wrong type:{df2}")
        return pd.DataFrame() #False
    if dbg:
        print(f'df_diff:{df1},{df2}')
    return pd.concat([df1,df2]).drop_duplicates(keep=False)

def diff_sd(fn1,fn2):
    "df_diff 2 space delimited files"
    df1=read_sd(fn1)
    df2=read_sd(fn2)
    dfdiff=df_diff(df1,df2)
    if dfdiff.empty:
        return True
    else:
        return dfdiff

def diff_flat_json(fn1,fn2):
    "df_diff 2 space delimited files"
    df1=read_json(fn1)
    df2=read_json(fn2)
    return df_diff(df1,df2) #or skip for:

def get_json_eq(fn1,fn2):
    print(f'get_json_eq:{fn1},{fn2}') #dbg
    d1=read_json(fn1)
    d2=read_json(fn2)
    if not d1:
        print("d1 missing")
    if not d2:
        print("d2 missing")
    return d1 == d2

def get_json_diff(fn1,fn2):
    d1=read_json(fn1)
    d2=read_json(fn2)
    #(https://pypi.org/project/deepdiff/)  or (https://dictdiffer.readthedocs.io/en/latest/)
    return d1 == d2 #finish, as will have to install in NBs too

#def list_diff(li1,li2):
def list_diff_not_in(li1,li2):
    "those in l1 not in l2"
    s = set(li2)
    return [x for x in li1 if x not in s]
#>>> list_diff_not_in(["a","b","c"],["a","b"])
#['c']
def list_diff_dropoff(li1,li2):
    ldiff= list_diff_not_in(li1,li2)
    #print(f'li1={li1}')
    #print(f'li2={li2}')
    #print(f'ldiff={ldiff}')
    return ldiff
    #return list_diff_not_in(li1,li2)

#testing cmp w/gold-stnd should now comes from github 
 #also can send alt bucket ..., now citesting, but be able to set: testing_bucket
#now endpoint loaded from ld-cache to work out mechanics of these fncs, 
 #will get from live workflow one we are sure it will be up during testing ;can be reset from script

def find_urn_diffs(endpoint="http://ideational.ddns.net:3030/geocodes_demo_datasets/sparql", 
        gold="https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/mb_sample/metadata/Dataset/standard/milled/geocodes_demo_datasets/URNs.txt"):
       #gold="https://raw.githubusercontent.com/MBcode/ec/master/test/standard/milled/geocodes_demo_datasets/URNs.txt"):
    "get_graphs_list and saved gold-list, and diff" #~do a set diff
    print("in find_urn_diffs,read_sd gold")
    #df_gold=read_sd(gold)
    df_gold=read_file(gold,".txt")
    print(f'gold:{df_gold}')
    #get_graphs w/convience gives list
    #return df_diff(df_gold, )
    global testing_endpoint
    if endpoint == testing_endpoint:
        test_endpoint=endpoint
    else: #use global so can set by script
        test_endpoint=testing_endpoint
    #test_list=get_graphs_list(test_endpoint)
    test_list=get_graphs_tails(test_endpoint)
    print(f'test:{test_list}')
    gold_list=df_gold['g'].tolist()
    print(f'gold:{gold_list}')
    tl=len(test_list)
    tg=len(gold_list)
    print(f'got:{tl},expected:{tg}') #consider also listing sitmap counts
    #return list_diff(test_list,gold_list)
    return list_diff_not_in(gold_list,test_list)

#if have url for gold-stnd bucket, and have missing urn
#milled_bucket="" #either the test milled, or from production then from diff buckets, ;still missing URNs from end2end start it off

#check_urn_ rdf|jsonld look up from LD-cache of latest run, and compare w/gold-stnd in github
  #tested separately, &ok on 1st pass;  ret True if ok=the same as gold-stnd
  #if the file was not there, might send whole file back as diff, or fail/check, but would like it2say not there/finish
   #might also call from spot_crawl_dropoff, which would already know that the file was there for sure

def check_urn_rdf(urn,
        test_bucket="https://oss.geocodes-dev.earthcube.org/citesting/milled/geocodes_demo_datasets/",
        gold="https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/mb_sample/metadata/Dataset/standard/milled/geocodes_demo_datasets/"):
       #gold="https://raw.githubusercontent.com/MBcode/ec/master/test/standard/milled/geocodes_demo_datasets/"):
    "check a URNs milled-rdf diff btw urls for current+gold-stnd buckets"
    import pandas as pd
    #gold_rdf=f'{test_bucket}{urn}.rdf' #test_rdf=f'{milled_bucket}{urn}.rdf'
    gold_rdf=f'{gold}{urn}.rdf'
    test_rdf=f'{test_bucket}{urn}.rdf'
    #could blabel_l them both if need be
    #df_gold=pd.read_csv(gold_rdf)
    #df_test=pd.read_csv(test_rdf)
    #return df_diff(df_gold,df_test)
    return diff_sd(gold_rdf,test_rdf) #the read should skip the header

def check_urn_jsonld(urn,
     #test_bucket="https://oss.geocodes-dev.earthcube.org/citesting/summoned/geocodes_demo_datasets/", ;use testing_bucket fix
                     #test_bucket="https://oss.geocodes-dev.earthcube.org/test3/summoned/geocodes_demo_datasets/",
        test_bucket=f'https://oss.geocodes-dev.earthcube.org/{testing_bucket}/summoned/geocodes_demo_datasets/',
        gold="https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/mb_sample/metadata/Dataset/standard/summoned/geocodes_demo_datasets/"):
       #gold="https://raw.githubusercontent.com/MBcode/ec/master/test/standard/summoned/geocodes_demo_datasets/"):
    "check a URNs summonded-jsonld diff btw urls for current+gold-stnd buckets"
    #rm urn: if necessary
    gold_rdf=f'{gold}{urn}.jsonld'
    test_rdf=f'{test_bucket}{urn}.jsonld'
    print(f'check_urn_jsonld:{urn}')
    #return diff_sd(gold_rdf,test_rdf)
    #return diff_flat_json(gold_rdf,test_rdf)
    return get_json_eq(gold_rdf,test_rdf) #if not= then use dict-diff lib to show the diffs

#might make a check_urn_ld_cache(urn,bucket=,test_set=,test_base=): #and it knows summoned .jsonld, milled .rdf
def check_urn_ld_cache(urn,bucket="citesting",test_set="geocodes_demo_datasets",test_base="https://oss.geocodes-dev.earthcube.org/"):
    "given URN, compare latest run LD_cache with gold-std" #check_urn_ fncs hold default gold url
    global testing_bucket
    if(testing_bucket != "citesting"): #to change test_bucket ...
        test_bucket=test_bucket.replace("citesting",testing_bucket)
    else:
        test_bucket=bucket
    test_rdf=f'{test_base}{test_bucket}/milled/{test_set}/' #{urn}.rdf added later
    print(f'new rdf:{test_rdf}')
    #rdf_check= list(check_urn_rdf(urn,test_rdf)) #bool not iterable
    rdf_check= check_urn_rdf(urn,test_rdf)
    test_jsonld=f'{test_base}{test_bucket}/summoned/{test_set}/' #{urn}.jsonld added later
    print(f'new jsonld:{test_jsonld}')
    jsonld_check= check_urn_jsonld(urn,test_jsonld) 
    #return rdf_check.append(jsonld_check) #mapping over these, they would come back in pairs
    return rdf_check, jsonld_check 

#endpoint loaded like nabu, to work on all this functionality, then can make sure it keeps it up like the ld-cache
def get_urn_diffs(endpoint="http://ideational.ddns.net:3030/geocodes_demo_datasets/sparql", 
        gold="https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/mb_sample/metadata/Dataset/standard/milled/geocodes_demo_datasets/"):
       #gold="https://raw.githubusercontent.com/MBcode/ec/master/test/standard/milled/geocodes_demo_datasets/"):
    "see which URN/graphs are in endpoint, and compare with expected"
    gold_URNs= gold + "URNs.txt"
    print(f'find_urn_diffs:{endpoint},{gold_URNs}')
    dfu=find_urn_diffs(endpoint,gold_URNs)
    return dfu

#spot_ crawl_dropoff below, will use new LD_cache_ .. files and call these helper functions in the end
 #non spot will still need integrity checks like in original ingestTesting.md &some shacl

#'validation'  ;check consituent fncs before switch over to this one
def check_urn_diffs(endpoint="http://ideational.ddns.net:3030/geocodes_demo_datasets/sparql", 
        test_bucket="https://oss.geocodes-dev.earthcube.org/citesting/milled/geocodes_demo_datasets/",
        gold="https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/mb_sample/metadata/Dataset/standard/milled/geocodes_demo_datasets/"):
       #gold="https://raw.githubusercontent.com/MBcode/ec/master/test/standard/milled/geocodes_demo_datasets/"):
       "looks at endpoint for missing URNs, then check LD-cache for each"
       dfu=get_urn_diffs(endpoint,gold)
       #ld_checks= list(map(lambda urn: check_urn_ld_cache(urn,test_bucket),dfu)) #could send more or less:
       ld_checks= list(map(check_urn_ld_cache,dfu))
       return ld_checks
#vs
#'validation'
def check_urn_diffs_(endpoint="http://ideational.ddns.net:3030/geocodes_demo_datasets/sparql", 
        test_bucket="https://oss.geocodes-dev.earthcube.org/citesting/milled/geocodes_demo_datasets/",
        gold="https://raw.githubusercontent.com/earthcube/GeoCODES-Metadata/mb_sample/metadata/Dataset/standard/milled/geocodes_demo_datasets/"):
       #gold="https://raw.githubusercontent.com/MBcode/ec/master/test/standard/milled/geocodes_demo_datasets/"):
    "find_urn_diffs and for each missing check_urn_rdf|jsonld" #get_graphs diff w/expected URNs, then check each missing
    gold_URNs= gold + "URNs.txt"
    print(f'find_urn_diffs:{endpoint},{gold_URNs}')
    dfu=find_urn_diffs(endpoint,gold_URNs)
    #dfu=find_urn_diffs(endpoint) #use it's default for a bit, bc read_sd prob w/github raw right now ;change2 read_file
    global testing_bucket
    if(testing_bucket != "citesting"): #to change test_bucket ...
        use_test_bucket=test_bucket.replace("citesting",testing_bucket)
        print(f'need2setup2pass changed test_bucket:{use_test_bucket}')
        #maybe have test_ url made of test_base + bucket + (summonde4.jsonld,milled4.rdf) + test_set
        test_base="https://oss.geocodes-dev.earthcube.org/"
        test_set="geocodes_demo_datasets" #could set this as a global as well
        test_rdf=f'{test_base}{use_test_bucket}/milled/{test_set}/'
        print(f'new rdf:{test_rdf}')
        test_jsonld=f'{test_base}{use_test_bucket}/summoned/{test_set}/'
        print(f'new jsonld:{test_jsonld}')
        #rdf_checks= list(map(lambda urn: check_urn_rdf(urn,endpoint,rdf_checks),dfu))
        rdf_checks= list(map(lambda urn: check_urn_rdf(urn,test_rdf),dfu))
        #jsonld_checks= list(map(lambda urn: check_urn_jsonld(urn,endpoint,jsonld_checks),dfu)) 
        jsonld_checks= list(map(lambda urn: check_urn_jsonld(urn,test_jsonld),dfu)) 
    else: # the other way   #got similar output w/missing bucket,so needs more test situations/closer look
        #will need lambdas if want to pass any change to the defaults on
        print(f'check_urn_rdf of:{dfu}')
        rdf_checks= list(map(check_urn_rdf,dfu))
        jsonld_checks= list(map(check_urn_jsonld,dfu)) #could do after, only if a problem, or just check them all now
        print(f'get:{rdf_checks}')
    return rdf_checks.append(jsonld_checks) 
    #return rdf_checks #test the check fncs w/any (array of) URNs that exist

#=merge using:
def merge_dict_list(d1,d2):
    from collections import defaultdict
    dd = defaultdict(list)
    for d in (d1, d2): # you can list as many input dicts as you want here
        for key, value in d.items():
            dd[key].append(value)
    return dd

def repos2counts(repos):
    "from cached sitemaps,etc"
    repo_df_loc={}
    for repo in repos:
        repo_df_loc[repo]=repo2site_loc_df(repo)
    repo_counts={}
    #for repo in repos:
    for repo in repo_df_loc:
        repo_counts[repo]=len(repo_df_loc[repo])
    #for now on ld-cache-counts:
    repo_ld_counts={}
    repo_fnum=wget2("http://geocodes.ddns.net/ec/test/repo_fnum.txt","summoned.txt")
    repo_fnum_list=repo_fnum.split('\n')
    for repo_num in repo_fnum_list:
        repo_num_list=repo_num.split(' ')
        if len(repo_num_list)>1:
            #print(repo_num_list)
            repo_=repo_num_list[0]
            fnum=repo_num_list[1]
            rl=repo_.split('/')
            if len(rl)>2:
                #print(rl)
                rn=rl[2]
                repo_ld_counts[rn]=fnum
    #for now on final-counts: #next from graph.csv and run system cmd on it,then strip extra spaces
    repoCounts=wget2("http://geocodes.ddns.net/ec/test/graph_counts.txt","graph.txt")
    final_counts={}
    rl2_list=repoCounts.split('\n')
    for  rl2 in rl2_list:
        num_repo=rl2.split(' ')
        if len(num_repo)>1:
            #print(num_repo)
            count=num_repo[0]
            repo=num_repo[1].lstrip('milled:').lstrip('summoned:') #in case either
            final_counts[repo]=count
    return repo_counts,repo_ld_counts,final_counts,      repo_df_loc 
#_testing end


#_testing was@994
def setup_s3fs(): #do this by hand for now
    #cs='pip install s3fs' #assume done rarely, once/session 
    #cs='pip install s3fs xmltodict' #want to switch to just request of url&parse xml:bucket_files.py
    cs='pip install s3fs xmltodict htmllistparse' #last for rehttpfs
    os_system(cs)

#if mounted minio like htm, that could have some benefits, incl getting over maxkeys, see what lib/s needed

#def mount_htm(ld_url=f'http://mbobak.ncsa.illinois.edu/ld/{repo_name}'):
def mount_htm(ld_url="http://mbobak.ncsa.illinois.edu/ld",repo=None):
    "mount any htm url, but default to current repo"
    if not repo:
        global repo_name
        repo = repo_name
    repo_cache=f'{ld_url}/{repo}'
    os_system(f'mkdir {repo}') #could mount higher so can mix repos
    cs=f'nohup rehttpfs {repo_cache} {repo} &' #macfuse has a problem but works on linux
    print(cs) #dbg
    os_system(cs)
    l=ls(repo)
    print(f'ls:{l}')
    return repo
    
def mount_repo(repo=None,ld_url="http://mbobak.ncsa.illinois.edu/ld"):
    "mount repo from my ld_cache"
    return mount_htm(ld_url,repo)

def mount_ld(repo="ld",ld_url="http://mbobak.ncsa.illinois.edu"):
    "mount ld_cache for all repos"
    return mount_htm(ld_url,repo)

def get_oss_(minio_endpoint_url="https://oss.geocodes-dev.earthcube.org/"): #old version
    import s3fs
    oss = s3fs.S3FileSystem( anon=True, key="", secret="",
          client_kwargs = {"endpoint_url": minio_endpoint_url})
    return oss
#def get_oss(minio_endpoint_url="https://oss.geocodes-dev.earthcube.org/"):
#def get_oss(minio_endpoint_url="https://oss.geocodes-dev.earthcube.org/",login=False):
def get_oss(minio_endpoint_url="https://oss.geocodes-dev.earthcube.org/",anon=True):
    import s3fs
    global S3KEY,S3SECRET
    #if login:
    if not anon:
        s3key=S3KEY
        s3secret=S3SECRET
    else:
        s3key=""
        s3secret=""
    oss = s3fs.S3FileSystem(
            #anon=True,
          anon=anon,
          key=s3key,
          secret=s3secret,
          #client_kwargs = {"endpoint_url":"https://oss.geodex.org"}
          #client_kwargs = {"endpoint_url":"https://oss.geocodes-dev.earthcube.org/"}
          client_kwargs = {"endpoint_url": minio_endpoint_url}
       )
    return oss
#in nb got: 
#ImportError: cannot import name 'PROTOCOL_TLS' from 'urllib3.util.ssl_' (/usr/local/lib/python3.7/dist-packages/urllib3/util/ssl_.py)
#but mostly run on machine where crawl/insert is done w/ spot_test.py for reports

#if not: fs = s3fs.S3FileSystem(anon=True), anon=False:
#def get_oss_login(minio_endpoint_url="https://oss.geodex.org", login=True):
def get_oss_login(minio_endpoint_url="https://oss.geodex.org", anon=False):
    #return get_oss(minio_endpoint_url,login)
    return get_oss(minio_endpoint_url,anon)


#def oss_ls(path='test3/summoned'):
def oss_ls(path='test3/summoned',full_path=True,minio_endpoint_url="https://oss.geocodes-dev.earthcube.org/"):
    oss=get_oss(minio_endpoint_url) #global oss
    import s3fs
    epl= oss.ls(path)
    if full_path:
        return list(map(lambda ep: f'{minio_endpoint_url}{ep}', epl))
    else:
        return epl
#>>> oss_ls('test3/summoned',False) #now need false to get this output
#['test3/summoned/geocodes_demo_datasets', 'test3/summoned/opentopography']
#>>> oss_ls('test3/summoned/geocodes_demo_datasets') #did not have base of url, so fixed w/map above, as default output type
#['test3/summoned/geocodes_demo_datasets/257108e0760f96ef7a480e1d357bcf8720cd11e4.jsonld', 'test3/summoned/geocodes_demo_datasets/261c022db9edea9e4fc025987f1826ee7a704f06.jsonld', 'test3/summoned/geocodes_demo_datasets/7435cba44745748adfe80192c389f77d66d0e909.jsonld', 'test3/summoned/geocodes_demo_datasets/9cf121358068c7e7f997de84fafc988083b72877.jsonld', 'test3/summoned/geocodes_demo_datasets/b2fb074695be7e40d5ad5d524d92bba32325249b.jsonld', 'test3/summoned/geocodes_demo_datasets/c752617ea91a725643d337a117bd13386eae3203.jsonld', 'test3/summoned/geocodes_demo_datasets/ce020471830dc75cb1639eae403a883f9072bb60.jsonld', 'test3/summoned/geocodes_demo_datasets/fcc47ef4c3b1d0429d00f6fb4be5e506a7a3b699.jsonld', 'test3/summoned/geocodes_demo_datasets/fe3c7c4f7ca08495b8962e079920c06676d5a166.jsonld']
#>>> 

def wget_oss_repo(repo=None,path="gleaner/milled",bucket=gc1_minio):
    "download all the rdf from a gleaner bucket"
    if not repo:
        global cwd  #I like having it go from the dirname, so files don't get mixed up
        repo=path_leaf(cwd)
        print(f'using, repo:{repo}=path_leaf({cwd})') #as 2nq.py will use cwd for repo, if it runs .rdf files
    files=oss_ls(f'{path}/{repo}',True,bucket)
    #print(f'will wget:{files}')
    for f in files:
        fl=path_leaf(f)
        from os.path import exists #can check if cached file there
        if not exists(fl):
            print(f'will wget:{f}')
            wget(f)
        else:
            print(f'have:{fl} already')
    if dbg: #might dump this all time, or by arg
        list2txtfile("l1h",files)
    return files

def setup_sitemap(): #do this by hand for now
    cs='pip install ultimate_sitemap_parser' #assume done rarely, once/session 
    os_system(cs) #get rid of top one soon
    cs='pip install advertools' #assume done rarely, once/session 
    os_system(cs)

def sitemap_tree(url): #will depricate
    "len .all_pages for count"
    #print("assume: setup_sitemap()")
    from usp.tree import sitemap_tree_for_homepage
    tree = sitemap_tree_for_homepage(url)
    return tree

#switch over libs from tree to df

def sitemap_df(url):
    import  advertools as adv
    df=adv.sitemap_to_df(url)
    return df

def sitemap_all_pages(url):
    #tree=sitemap_tree(url)
    #return tree.all_pages()
    df=sitemap_df(url)
    return df['loc']

def repo2site_loc_df(repo):
    "get df[loc] from repos sitemap" #use cached sitemap
    base_url="http://geocodes.ddns.net/ec/crawl/sitemaps/"
    url=f'{base_url}{repo}.xml'
    return sitemap_all_pages(url)

def sitemaps_all_loc(sitemaps):
    "list(iterable) to get all DFs of LOCs"
    return map(sitemap_all_pages,sitemaps)
    #also be able to work w/dictionaries,  repo_name sitmap in, count out

def sitemap_list_(url):
    pages=sitemap_all_pages(url)
    pl=list(pages)
    return pl #get rid of need for these libs

def sitemap_list(url):
    "use fast xml lib"
    return sitemap_urls(url)

def sitemap_len(url):
    "try fast xml version"
    ul=sitemap_urls(url)
    return len(ul)
#now using this over https://github.com/MBcode/ec/blob/master/test/counts.md named_sitemaps
#sitemaps=list(named_sitemaps.values())
#counts=list(map(sitemap_len_,sitemaps)) #now resistent to errors, get:
#[25226, 18634, 704, 28, 5654, 17654, 0, 4263, 920, 0, 211, 45159, 0, 910, 2522, 0]
#can also run: that prints them out as it goes along
#sc=sitemaps_count(sitemaps)

def sitemap_len_(url):
    "for counts" # maybe allow filtering types later
    pages=sitemap_all_pages(url)
    pl=list(pages)
    return len(pl)

def sitemaps_count(sitemaps):
    sitemap_count = {}
    for sitemap in sitemaps:
        count=sitemap_len(sitemap)
        print(f'{sitemap} has {count} records')
        sitemap_count[sitemap]=count
    return sitemap_count

def crawl_sitemap(url):
    "url w/o sitemap.xml, might try other lib"
    #tree=sitemap_tree(url)
    pages=sitemap_all_pages(url)
    #for page in tree.all_pages():
    for page in pages:
        url2nq(page)
        #url2nq(page.url)
        #print(f'url2nq({page.url})') #dbg

#if already crawled and just need to convert
#_testing end

#_testing was@2672
#testing, where we look at gleaner's mino ld-cache via web
 #so it can be swapped out for my web LD-cache when missing
#==bucket_files.py to get (minio) files list from a bucket path
#ci_url="https://oss.geocodes-dev.earthcube.org/citesting"
#ci_url="https://oss.geocodes-dev.earthcube.org/test3"
ci_url2="https://oss.geocodes-dev.earthcube.org/citesting2"

#https://pypi.org/project/htmllistparse/ rehttpfs does a fuse mount of a html dir
#which allows for reading any of it like a file

def get_url(url): 
    "request.get url"
    import requests
    r=requests.get(url)
    return r.content
#for LD_cache_files ..;if file_ext(url)==".xml" ret xmltodict, ;could d for htm but list nicer:
#s=get_url(url) st=s.decode("utf-8"); if "<html>" in st: parse_html, w/listFD
#from stackoverflow ;so can get ~bucket_files from each dir separately
#url = 'http://mbobak.ncsa.illinois.edu/ec/minio/test3/summoned/geocodes_demo_datasets/'
#ext = 'nq' ;might start using my ld_cache too; it seems more consistent
def listFD(url, ext=''):
    from bs4 import BeautifulSoup
    import requests
    page = requests.get(url).text
    if(dbg):
        print(page)
    soup = BeautifulSoup(page, 'html.parser')
    r= [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]
    #ftd=get_file_types(r)
    #return r,ftd
    return r

def get_htm_dir(url,ext=None):
    from bs4 import BeautifulSoup
    import requests
    page = requests.get(url).text
    if(dbg):
        print(page)
    soup = BeautifulSoup(page, 'html.parser')
    if ext:
        return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]
    else:
        return [url + '/' + node.get('href') for node in soup.find_all('a')]
#eg:
#>>> files=get_htm_dir("http://mbobak.ncsa.illinois.edu/ec/minio/test3/summoned/geocodes_demo_datasets")
#>>> get_file_ext_types(files)
#{'': 5, '.jsonld': 9, '.nq': 9, '.nt': 9}
#then can: 
#>>> fj=get_htm_dir("http://mbobak.ncsa.illinois.edu/ec/minio/test3/summoned/geocodes_demo_datasets",".jsonld")
#>>> len(fj)
#9
#>>> list(map(replace_base,fj)) #will replace the base above w/'test3' ;if not in global lambda w/{"base": "repo"}

def url_xml(url): #could just be get_url
    "given bucket url ret raw xml listing"
    import requests
    #r=requests.get(url)
    try:
        r=requests.get(url, timeout=(15, 45)) #used in check.py
    except:
        print(f'url_xml:req-execpt on:{url}')
        return None
    test_xml=r.content
    #print(test_xml) #check if 200
    status=r.status_code 
    if(status == 200):
        return test_xml
    else:
        print(f'url_xml,bad:{status},for:{url}')
        return None

def is_bytes(bs):
    return isinstance(bs, bytes)

def xmltodict_parse(test_xml):
    import xmltodict
    if not is_bytes(test_xml):
        print(f'xml_parse no str')
        return None
    try:
        d=xmltodict.parse(test_xml)
    except:
        lx=len(test_xml)
        print(f'xml_parse exception')
        d=None
    return d

def sitemap_xml2dict(test_xml): #libs don't work in diff places
    #import xmltodict
    #d=xmltodict.parse(test_xml)
    d=xmltodict_parse(test_xml)
    if(dbg):
        print(d)
    if not d:
        print(f'sitemap_xml2 not found')
        return None
    lbr=d.get("urlset")
    if lbr:
        c=lbr.get("url")
        return c
    else:
        print(f'no urlset, for:{test_xml}')
        return None

def sitemap_urls(url):
    "faster way of getting urls w/just xml lib"
    test_xml=url_xml(url)
    if not test_xml:
        return []
    c=sitemap_xml2dict(test_xml)
    if c:
        urls=list(map(lambda kd: kd.get('loc'), c))
        return urls
    else:
        print(f'no sitemap_urls xml for urls:{url}')
        #return None
        return [] #hope to still work


def bucket_xml(url):
    return url_xml(url)

def bucket_xml2dict(test_xml):
    "bucket url to list of dicts, w/file in key"
    #import xmltodict
    #d=xmltodict.parse(test_xml)
    d=xmltodict_parse(test_xml)
    #print(d)
    lbr=d.get("ListBucketResult")
    if lbr:
        c=lbr.get("Contents")
        return c
    else:
        print(f'no ListBucketResult, for:{test_xml}')
        return None

def bucket_files(url): #need to get past: <MaxKeys>1000</MaxKeys>
    "bucket_url to file listing"
    test_xml=bucket_xml(url)
    c=bucket_xml2dict(test_xml)
    if c:
        files=map(lambda kd: kd.get('Key'), c)
        dates=map(lambda kd: kd.get('LastModified'), c) #or when get prov look at file dates before the parse?
         #AttributeError: 'int' object has no attribute 'get' #had taken this out
        return list(files),list(dates)
    else:
        print(f'no bucket xml for files:{url}')
        return None, None


def endpoint_xml2dict(test_xml):
    #import xmltodict
    #d=xmltodict.parse(test_xml)
    d=xmltodict_parse(test_xml)
    if(dbg):
        print(d)
    #lbr=d.get("rdf:Description")
    #if not lbr:
    #    lbr=d.get('rdf:RDF')
    lbr=d.get('rdf:RDF')
    return lbr

def endpoint_description(url="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/citesting2/sparql"):
    "get/test if endpoint ok, description xml to see that it is healthy"
    test_xml=url_xml(url)
    ts=test_xml.decode("utf-8")
    if is_html(ts):
        return "html"
    if ts.startswith("Service"):
        return "service_description"
    c=endpoint_xml2dict(test_xml)
    lc=len(c) #2keys
    print(f'endpoint w/{lc} descriptions')
    des=c.get('rdf:Description')
    return des
#c.get('@xmlns:rdf')
#'http://www.w3.org/1999/02/22-rdf-syntax-ns#'

#once I need this for >1 bucket I will turn it into a class, and make instances
LD_cache_base=None
LD_cache_files=None
LD_cache_dates=None #Might use, or as we query the file, also want to get files metadata
LD_cache_types=None
#output: {'milled/geocodes_demo_datasets': 25, 'orgs': 1, 'prov/geocodes_demo_datasets': 31, 'results/runX': 1, 'summoned/geocodes_demo_datasets': 25}
#{'orgs': 4, 'prov/geocodes_demo_datasets': 45, 'prov/magic': 951} #so key prov/bucket_name
 #so much prov here that get _files doesn't seem to have summoned though there/fix


def get_file_ext_types(file_list):
    file_types={}
    for fn in file_list:
        base,leaf = path_base_leaf(fn)
        ext=file_ext(leaf)
        count=file_types.get(ext)
        if count:
            count += 1
        else:
            count = 1
        file_types[ext] = count
    return file_types #use w/get_htm_dir

def get_file_leaf_types(file_list): 
    "use to find duplicate files in a dir"
    file_types={}
    for fn in file_list:
        base,leaf = path_base_leaf(fn)
        #count=file_types.get(base)
        count=file_types.get(leaf)
        if count:
            count += 1
        else:
            count = 1
        #file_types[base] = count
        file_types[leaf] = count
    return file_types 

def get_file_base_types(file_list):
    file_types={}
    for fn in file_list:
        base,leaf = path_base_leaf(fn)
        count=file_types.get(base)
        if count:
            count += 1
        else:
            count = 1
        file_types[base] = count
    return file_types #can use just below/?, and w/get_htm_dir

#if folders where different, maybe layer that over for different buckets, someday
def set_bucket_files(bucket=None):
    "get+set LD_cache_ files array and types dict"
    if not bucket:
        global ci_url
        bucket=ci_url
    global LD_cache_base, LD_cache_files, LD_cache_types
    LD_cache_base=bucket
    LD_cache_files,LD_cache_dates=bucket_files(bucket)
    LD_cache_types={}
    for fn in LD_cache_files:
        base,leaf = path_base_leaf(fn)
        count=LD_cache_types.get(base)
        if count:
            count += 1
        else:
            count = 1
        LD_cache_types[base] = count
    return LD_cache_types

def get_full_key(partial_key,mydict):
    "get key that has str in it"
    #fk = next(k for k,v in LD_cache_types.items() if base_type in k) #full key
    fk = next(k for k,v in mydict.items() if partial_key in k) #full key
    return fk

#conider getting listing from repo_name/base_type ;for bucket_files

def get_bucket_files(base_type):
    "ask for base_type= summoned,milled,prov,.. get all full file paths"
    global LD_cache_base, LD_cache_files, LD_cache_types
    if not LD_cache_files:
        set_bucket_files()
    print(f'get_bucket_files:{base_type}')
  # fk = next(k for k,v in LD_cache_types.items() if base_type in k) #full key
   #ks=LD_cache_types.keys()
   #fkl=collect_pre_(ks,base_type)
   #print(f'get:{base_type} has {fk}')
    fe=collect_pre_(LD_cache_files,base_type) #end of file paths
    lfe=len(fe)
    if lfe>0:
        ff=list(map(lambda f: f'{LD_cache_base}/{f}', fe)) #full file paths
    else:
        print(f'WARN:no {base_type} in {LD_cache_base}:{fe}')
        #ff=[]
        ff=None
    return ff

#if my cache has to go into a bucket it will be extruct/repo
#also I want a put_oss_files, so get key/secret from env-vars
# S3ADDRESS  S3KEY S3SECRET get.env
S3ADDRESS=os.getenv("S3ADDRESS")
S3KEY=os.getenv("S3KEY")
S3SECRET=os.getenv("S3SECRET")

#>>> oss_ls('test3/summoned/geocodes_demo_datasets') == get_bucket_files
  #not replacing yet, bc get error, even though doesn't get drowned out
#repo_name="geocodes_demo_datasets" #for testing
#testing_bucket="test3" #or bucket_name
#def get_oss_files_(path=None, base_type=None, bucket=None, minio_endpoint_url="https://oss.geodex.org/" ,full_path=True,):
def get_oss_files_(repo=None, base_type=None, bucket="gleaner", path=None, minio_endpoint_url="https://oss.geodex.org/" ,full_path=True,): #usually do not use version ending in _
    if not bucket:
        global testing_bucket
        bucket= testing_bucket
    if not base_type:
        base_type="summonded"
    if not repo:
        global repo_name
        repo= repo_name
    if not path:
        #path=f'{testing_bucket}/{base_type}/{repo_name}'
        path=f'{bucket}/{base_type}/{repo}'
    print(f'get_oss_files_:{path}') #dbg
    #oss_ls("gleaner/summoned", True, "https://oss.geodex.org/")
    return oss_ls(path, full_path, minio_endpoint_url)
#default getting access-denied, though get xml, and from:, but was for mbci2
#oss_ls("gleaner/summoned", True, "https://oss.geodex.org/")

def get_oss_files(base_type):
    path=f'{testing_bucket}/{base_type}/{repo_name}'
    return oss_ls(path)
#>>> get_oss_files("summoned")
#['test3/summoned/geocodes_demo_datasets/257108e0760f96ef7a480e1d357bcf8720cd11e4.jsonld', 'test3/summoned/geocodes_demo_datasets/261c022db9edea9e4fc025987f1826ee7a704f06.jsonld', 'test3/summoned/geocodes_demo_datasets/7435cba44745748adfe80192c389f77d66d0e909.jsonld', 'test3/summoned/geocodes_demo_datasets/9cf121358068c7e7f997de84fafc988083b72877.jsonld', 'test3/summoned/geocodes_demo_datasets/b2fb074695be7e40d5ad5d524d92bba32325249b.jsonld', 'test3/summoned/geocodes_demo_datasets/c752617ea91a725643d337a117bd13386eae3203.jsonld', 'test3/summoned/geocodes_demo_datasets/ce020471830dc75cb1639eae403a883f9072bb60.jsonld', 'test3/summoned/geocodes_demo_datasets/fcc47ef4c3b1d0429d00f6fb4be5e506a7a3b699.jsonld', 'test3/summoned/geocodes_demo_datasets/fe3c7c4f7ca08495b8962e079920c06676d5a166.jsonld']

site_urls2UUIDs=None
urn2site_urls=None
UUIDs2site_urls={} #uuid part of urn as key
prov_sitemap=None

#def URLsUUID(url):
def urn2uuid(url):
    "pull out the UUID from w/in the URL" 
    s=urn_leaf(url)
    leaf_base = s if not s else file_base(s)
    return leaf_base

def uuid2url(uuid):
    "map from uuid alone to crawl url"
    url=UUIDs2site_urls.get(uuid)
    if not url:
        print(f'bad uuid2url:{uuid}')
        return uuid
    return url

def uuid2repo_url(uuid):
    "uuid2url w/shorter repo:leaf.json"
    url=uuid2url(uuid)
    if url:
        return replace_base(url)
    else:
        print(f'bad uuid2repo_url:{uuid}')
        return uuid
#not getting this below now
#uuid2repo_url("09517b808d22d1e828221390c845b6edef7e7a40")
#'geocodes_demo_datasets:MB_amgeo_data-01-06-2013-17-30-00.json'
#_testing end


#_testing: was@3041
def to_repo_url(u):
    uuid=leaf_base(u)
    return uuid2repo_url(uuid)

def to_repo_url_(u):
    "uuid or urn to repo_url"
    if is_urn(u):
        u=urn2uuid(u)
    return uuid2repo_url(u)
#this isn't ret anything
#there are UUIDs from graph that should just go through
 #though might want get.graphs w/ urn: returns

def fill_repo_url(url,mydict,val="ok"):
    "url w/uuid ->repo:leaf as key in dict"
    key=to_repo_url(url) 
    mydict[key]=val
    print(mydict)
    return mydict
#skip these, as not by ref/rm soon
def fill_repo_urls(urls,mydict,val="ok"):
    ul=len(urls)
    print(f'frus:{ul}')
    map(lambda u: fill_repo_url(u,mydict,val), urls)
    print(mydict)
    return mydict

def urls2idict(urls,val="ok"):
    mydict={}
    if not urls:
        print(f'urls2idict:no urls')
        return mydict
    ul=len(urls) if urls else 0
    print(f'u2d:{ul}')
    for url in urls:
        key=to_repo_url(url) 
        mydict[key]=val
    if(dbg):
        print(mydict)
    return mydict
#better, but not getting the key/find/fix that

def get_vals(key,dl):
    "lookup key in a list of dicts"
    rl= list(map(lambda d: d.get(key), dl))
    rl.insert(0,key)
    return rl
#[['geocodes_demo_datasets:MB_amgeo_data-01-06-2013-17-30-00.json', 'ok', 'ok', None], ['geocodes_demo_datasets:MB_iris_syngine.json', 'ok', 'ok', None], ['geocodes_demo_datasets:MB_lipdverse_HypkanaHajkova2016.json', None, None, None], ['geocodes_demo_datasets:argo-20220707.json', 'ok', 'ok', None], ['geocodes_demo_datasets:argoSimple-v1Shapes.json', None, None, None], ['geocodes_demo_datasets:bcodmo1-20220707.json', 'ok', 'ok', None], ['geocodes_demo_datasets:bcodmo1.json', 'ok', 'ok', None], ['geocodes_demo_datasets:earthchem_1572.json', None, None, None], ['geocodes_demo_datasets:opentopo1.json', 'ok', 'ok', None]]


#use this as the key for a dict for every saved state of the workflow
 #so can put out a csv, starting w/this, as it is made from the starting sitemap-url
 #but then for summoned, and if there milled, and then quads in the graph
 #for the ones that don't get filled in, just ret a comma
#So from the processed sitemap-url's xml, get the long form, then make short if possible
 #use this as the 1st column, and iterate over the list the same way; 
  #after that states dict has been filled up as much as possilbe
#have s m, then get_graphs  for the other saved states ;can do list-diff but csv will show missing already
#def csv_dropoff(sitemap_url): #maybe add spot test output later
#this needs LD_cache full 1st, can run bucket_files3 or..
csv_out=None

#def cmp_expected_results(df=None,df2="http://mbobak.ncsa.illinois.edu/ec/test/expected_results.csv"):
def cmp_expected_results(df=None,df2="https://raw.githubusercontent.com/MBcode/ec/master/test/expected_results.csv"):
    "just show where not expected" #so bad things can still be ok
    global csv_out
    if not is_df(df) and csv_out:
        df=csv_out
    if is_http(df2):
        import pandas as pd
        df2=pd.read_csv(df2)
    print(f'df1={df},df2={df2}')
    return df_diff(df,df2)
#check/fix: ValueError: The truth value of a DataFrame is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().

#def csv_dropoff(sitemap_url="https://earthcube.github.io/GeoCODES-Metadata/metadata/Dataset/allgood/sitemap.xml",
def csv_dropoff(sitemap_url="https://raw.githubusercontent.com/MBcode/ec/master/test/sitemap.xml", #start expecte bad cases
        bucket_url=None, endpoint="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/citesting2/sparql",cmp=False):
    global csv_out
    print(f'==sitemap:{sitemap_url}')
    print(f'==graph_endpoint:{endpoint}')
    if is_df(csv_out):
        print("already have a csv_out")
        return csv_out
    if bucket_url:
        global ci_url
        if bucket_url != ci_url:
            print(f'reset from:{ci_url} to:{bucket_url}')
            ci_url = bucket_url 
    print(f'==s3_endpoint:{bucket_url}')
    #print(f'csv_dropoff,bucket:{bucket_url}')
    if not urn2site_urls:
        set_prov2site_mappings()
    sm=sitemap_list(sitemap_url) #can now use sitemap2urn to get sitemap into same ID space
    #sm_ru=list(map(to_repo_url,sm)) #acts as key for each dict #this goes2uuid but sm doens't have that
    #sm_ru=list(map(replace_base,sm)) #acts as key for each dict ;need v of replace_base w/base_url2repo, but for url
    sm_ru=list(map(replace_base,sm)) #acts as key for each dict ;need v of replace_base w/base_url2repo, but for url
    #s=get_bucket_files("summoned")
    s=get_oss_files("summoned")
    #m=get_bucket_files("milled")
    m=get_oss_files("milled")
    #p=get_bucket_files("prov")
    #g=get_graphs_tails(endpoint)
    print(f'check,endpoint:{endpoint}')
    ep_ok=endpoint_description(endpoint)
    if ep_ok:
        g=get_graphs_list(endpoint) #will strip ..urn: to uuid anyway
    else:
        print(f'cd:enpoing not ok:{endpoint}')
        g=None
    #print(f'csv_ states,sm:{sm},s:{s},m:{m},g:{g}')
    print(f'sm:{sm}')
    #print(f'sm:{sm_ru}')
    print(f's:{s}')
    print(f'm:{m}')
    print(f'g:{g}')
    sml=len(sm_ru)
    sl=len(s) if s else 0
    ml=len(m) if m else 0
    gl=len(g) if g else 0
    print(f'csv_ states,sm:{sml},s:{sl},m:{ml},g:{gl}')
    sd=urls2idict(s)
    md=urls2idict(m)
    gd=urls2idict(g)
    #these are getting set w/uuid keys, and want to_repo_url keys
     #though UUIDs2site_urls should help map them ;whatever2 uuid, to_repo_url
    print(f'sd:{sd}')
    print(f'md:{md}')
    print(f'gd:{gd}') #this needs repo:file keys instead of uuids
    dl=[sd,md,gd]
    print(f'now lookup by:{sm_ru}')
    r= list(map(lambda k: get_vals(k, dl), sm_ru))
    lr=len(r)
    print(f'{sml}={lr}')
    import pandas as pd
    df = pd.DataFrame.from_dict(r)
    #csv_out=df #so we don't rerun uncessesarily
    csv_out=df.set_axis(["repo:file_name",  "summoned", "milled", "graph"], axis=1, inplace=False)
    if cmp or dbg:
        diff=cmp_expected_results(csv_out)
        print(f'diff w/expected:{diff}')
    return csv_out
#turn this into html-table &/or dataframe
  #see what is up w/graph's comparison/fix that; bad uuid2url: 
   #so might have other crawl in graph? look for similar name/urls there
#9=9  aslo check on 3 that didn't summon
#                                                   0     1     2     3
#0  geocodes_demo_datasets:MB_amgeo_data-01-06-201...    ok    ok  None
#1        geocodes_demo_datasets:MB_iris_syngine.json    ok    ok  None
#2  geocodes_demo_datasets:MB_lipdverse_HypkanaHaj...  None  None  None
#3          geocodes_demo_datasets:argo-20220707.json    ok    ok  None
#4    geocodes_demo_datasets:argoSimple-v1Shapes.json  None  None  None
#5       geocodes_demo_datasets:bcodmo1-20220707.json    ok    ok  None
#6                geocodes_demo_datasets:bcodmo1.json    ok    ok  None
#7         geocodes_demo_datasets:earthchem_1572.json  None  None  None
#8              geocodes_demo_datasets:opentopo1.json    ok    ok  None

#def prov2site_mappings():
def set_prov2site_mappings():  #make sure it is run, to get mappings
    "use cached PROV to make mappings"
    #global LD_cache_base, LD_cache_files, LD_cache_types
    #pu=get_bucket_files("prov") #only the ones for the repo_name being run
    pu=get_bucket_files(f'prov/{repo_name}') #only the ones for the repo_name being run
    #would be great to only send the (sitemap len) newest files
    if pu:
        global site_urls2UUIDs, urn2site_urls, UUIDs2site_urls, prov_sitemap
        #return prov2mappings(pu)
        #sitemap2urn,urn2sitemap,sitemap=prov2mappings(pu)
        #site_urls2UUIDs,UUIDs2site_urls,prov_sitemap=prov2mappings(pu)
        site_urls2UUIDs,urn2site_urls,prov_sitemap=prov2mappings(pu)
       #UUIDs2site_urls from urn2site_urls ;needs is_urn
       #UUIDs2site_urls=list(map(urn2uuid,urn2site_urls));needs is_urn ;use next/or
        for k,v in urn2site_urls.items(): #=list(map(urn2uuid,urn2site_urls));needs is_urn
            k2=urn2uuid(k)
            if k2:
                UUIDs2site_urls[k2]=v
            else:
                print('bad k2 for:{k},{v}')
        l1=len(site_urls2UUIDs)
        #l2=len(UUIDs2site_urls)
        l2=len(urn2site_urls)
        l3=len(prov_sitemap)
        ss=f'set:{l1} site_urls2UUIDs,{l2} UUIDs2site_urls,{l3} prov_sitemap'
        print(ss)
        return ss
    else:
        print(f'no prov for site_mappings')
        return None #so can skip out of dependcies

#def prov2sitemap(bucket_url,pu=None):
def prov2sitemap(bucket_url=None,pu=None): #backward compat4a bit
    "return prov_sitemap, parse prov if not there"
    if not prov_sitemap:
        set_prov2site_mappings()
    return prov_sitemap

#def prov2sitemap(bucket_url):
#def prov2sitemap(bucket_url,pu=None):
def prov2sitemap_(bucket_url,pu=None): #do not use
    "parse bucket prov2get sitemap&it's mappings"
    fi=bucket_files(bucket_url)
    if not fi:
        print(f'prov2sitemap, no bucket_files:{bucket_url}')
        return None
    p=collect_pre_(fi,"prov") #only the ones for the repo_name being run
    pu=list(map(lambda fp: f'{bucket_url}/{fp}', p))
    sitemap=None
    try:
        pul=len(pu)
        #print(f'prov2mapping for:{pul}')
        print(f'prov2sitemap_mapping for:{pul}')
        sitemap2urn,urn2sitemap,sitemap=prov2mappings(pu)
        #print("got the mappings")
    except:
        #print("bad prov2mappings sitemap")
        print("bad prov2sitemap_mappings, on the:{pul}")
    return sitemap #for now

#if ret more could use in fnc/s below

#spot_ crawl_dropoff fnc below, ~being sucseeded by csv_dropoff fncs above
#want2check on: =Graph-count:9, Error count:-9, missing:[]  ;but from older way
 #I setup the old to get LD_cache info from the new; but might be better focusing on df grid a bit more now
 #so can get some more bad data through that is expected and catch it
 #s14 output mostly good, except 2not ok, not in summary../check

#will not need these other bucket_ fncs soon
 #will make spot_ crawl_dropoff something that could more easily fit
 #into a workflow check, alongside each stage, just accessing the state
 #on each side and getting the diff, for a report
 #incl. a (dbg) version aligned as a csv/spreadsheet ;algo above

def bucket_files2(url):
    "url to tuple of summoned+milled lists"
    fi=bucket_files(url)
    s=collect_pre_(fi,"summoned")
    m=collect_pre_(fi,"milled")
    return s,m

def bucket_files3(url=None): #might try using above w/this for just a bit
    if url: 
        global ci_url
        ci_url=url
    #s=get_bucket_files("summoned")
    s=get_oss_files("summoned")
    #m=get_bucket_files("milled")
    m=get_oss_files("milled")
    #p=get_bucket_files("prov")
    p=get_bucket_files(f'prov/{repo_name}') #only the ones for the repo_name being run
    #pu=list(map(lambda fp: f'{url}/{fp}', p))
    global site_urls2UUIDs, UUIDs2site_urls, prov_sitemap
    if not prov_sitemap:
        #prov_sitemap=prov2sitemap()
        prov2sitemap()
    psl=len(prov_sitemap)
    print(f'bf3,prov_sitemap:{psl}')
    sitemap2urn=site_urls2UUIDs
    urn2sitemap=UUIDs2site_urls
    if not s:
        print("bf3:no summoned")
    if not m:
        print("bf3:no milled")
    return s,m,sitemap2urn,urn2sitemap #not sending prov_sitemap yet

#going fwd, focus on being able2keep each stage in assoc, so after list_diff still know which original url started it off
 #this is in the metadata for the file, but also in the prov mappings

#def bucket_files3(url=None):
def bucket_files3_(url=None): #do not use
    "url to summoned+milled,prov lists"
    if not url:
        global ci_url
        url = ci_url
    fi=bucket_files(url)
    if not fi:
        print(f'bucket_files 3,nothings for:{url}')
        return None, None, None, None
    #s=collect_pre_(fi,"summoned") #use other ;as fix
    s=get_oss_files("summoned")
    m=collect_pre_(fi,"milled")
    p=collect_pre_(fi,"prov")
    pu=list(map(lambda fp: f'{url}/{fp}', p))
    sitemap2urn=None
    try:
        pul=len(pu)
        print(f'prov2mapping for:{pul}')
        #sitemap2urn,urn2sitemap=prov2mappings(pu)
        sitemap2urn,urn2sitemap,sitemap=prov2mappings(pu)
        #print("got the mappings")
    except:
        print("bad prov2mappings")
    if sitemap2urn: 
        return s,m,sitemap2urn,urn2sitemap
    else:
        #return s,m,p #mostly expect mappings below, &not prov
        print(f'bucket_files3 no map so send Nones, for:{url}')
        return s,m, None, None

#could also pass sitemap, in case used later from:

def bucket_files2diff(url,URNs=None):
    "list_diff_dropoff summoned milled, URNs"
    #summoned,milled=bucket_files2(url) #now have bucket_files3
    summoned,milled,sitemap2urn,urn2sitemap=bucket_files3(url) 
    if not summoned:
        print(f'bucket_files3 2diff, nones for bad:{url}') 
        return None, None, None, None, None
    su=list(map(lambda f: file_base(path_leaf(f)),summoned))
    if not milled:
        print(f'bucket_files3 2diff, no milled for bad:{url}') 
        mu=[]
    else:
        mu=list(map(lambda f: file_base(path_leaf(f)),milled))
    if dbg:
        print(f'summoned-URNs:{su}')
        print(f'milled-URNs:{mu}')
    sl=len(su)
    ml=len(mu)
    dsm=sl-ml #diff summoned&milled= datasets lost in this step
    lose_s2m=list_diff_dropoff(su,mu)
    if URNs:
        ul=len(URNs)
        dmu=ml-ul
        print(f'dmu:{dmu}=ml:{ml} - ul:{ul}') #dbg, negative if no milled
        #print(f'=Summoned-count:{sl}, Error count:{dsm}, missing:{lose_s2s}') #below
        print(f'=Milled-count:{ml}, Error count:{dmu}, missing:{lose_s2m}')
        #print(f'expected-URNs:{URNs}')
        if dbg:
            print(f'endpoint-URNs:{URNs}')
        #dropoff=f's:{sl}/m:{ml}/u:{ul} diff:{dmu}'
        dropoff=f'summoned:{sl}-{dsm}=>milled:{ml}-{dmu}=>graph:{ul}'
        if dbg:
            print(dropoff)
        lose_m2u=list_diff_dropoff(mu,URNs) 
        print(f'=Graph-count:{ul}, Error count:{dmu}, missing:{lose_m2u}')
        #return lose_s2m, lose_m2u
        #return dropoff,lose_s2m, lose_m2u
        #return dropoff,lose_s2m, lose_m2u , sitemap2urn
        return dropoff,lose_s2m, lose_m2u , sitemap2urn, su #last is summoned
    else:
        #dropoff=f's:{sl}/m:{ml} diff:{dsm}')
        dropoff=f'summoned:{sl}-{dsm}=>milled:{ml}'
        if dbg:
            print(dropoff)
        #return lose_s2m
        #return dropoff,lose_s2m
        return dropoff,lose_s2m, None, None, None

#don't need to have a diff version, bc bucket_files3 looks up PROV even w/o a sitemap
#def bucket_files3diff(sitemap,url,URNs=None):

#break out all the code in crawl_dropoff that deals w/sitemap to summoned w/mapping
#def drop1mapping(sm,sitemap2urn):
def drop1mapping(sm,sitemap2urn,su): #want to but not used yet; still in crawl_dropoff
    "break out all the code in crawl_dropoff that deals w/sitemap to summoned w/mapping"
    sml=len(sm)
    #print(f'will get:{sml} urn2urn w/:{sitemap2urn}') #dbg
    #smu=list(map(lambda s: sitemap2urn[s], sm))
    smu=list(map(lambda s: sitemap2urn.get(s), sm)) #used prov mapping to gen test sitemap
    if dbg:
        print(f'URN/UUIDs for sitemaps:{smu}')             #need to get same sitemap, &use map for cmp:
    #smu2=list(map(lambda s: s.split(':')[-1],smu))
    smu2=list(map(lambda s: s if not s else s.split(':')[-1],smu)) #=urn_tails(smu)
    if dbg:
        print(f'URN/UUIDs for sitemaps:{smu2}')             #need to get same sitemap, &use map for cmp:
    lose_s2s=list_diff_dropoff(smu2,su) 
    lsl=len(lose_s2s) #should= sml- ml from above
    print(f'lose_s2s:{lose_s2s}') #will need to map this back to the sitemap url ;if it was in prov
    ##lose_s2m=list_diff_dropoff(su,mu), from above
    #dropoff=f'sitemap:{sml} =>{dropoff2}'  #pull sl, to calc dss=sml-sl
    #dropoff=f'sitemap:{sml}-{lsl}:{lose_s2s} =>{dropoff2}'  
  # print(f'=Summoned-count:{sl}, Error count:{ls1}, missing:{lose_s2s}')
    dropoff=f'sitemap:{sml}-{lsl}:{lose_s2s} =>'  
    #dropoff=f'sitemap:{sml}-{dss}=>{dropoff2}' #can't get lose_s2s w/o PROV sitemap URLs to UUID mapping  
    #return dropoff,lose_s2m, lose_m2u
    #return dropoff,lose_s2s, lose_s2m, lose_m2u
    return dropoff,lose_s2s

def crawl_dropoff_(sitemap,bucket_url,endpoint): #do not use
    "show counts at each stage, and URN diffs when can"
    #URNs=get_graphs_list(endpoint)  #that are in the endpoint, not the expected
    URNs=get_graphs_tails(endpoint)  #that are in the endpoint, not the expected
    #dropoff2,lose_s2m, lose_m2u = bucket_files2diff(bucket_url,URNs)
    #dropoff2,lose_s2m, lose_m2u, sitemap2urn = bucket_files2diff(bucket_url,URNs)
    dropoff2,lose_s2m, lose_m2u, sitemap2urn, su = bucket_files2diff(bucket_url,URNs)
    #sml=sitemap_len(sitemap) #can now use sitemap2urn to get sitemap into same ID space
    sm=sitemap_list(sitemap) #can now use sitemap2urn to get sitemap into same ID space
    #print(f'sitemap:{sm}')
    sml=len(sm)
    if sitemap2urn:
        dropoff1,lose_s2s=drop1mapping(sm,sitemap2urn,su)
        dropoff=f'{dropoff1} =>{dropoff2}'  
        return dropoff,lose_s2s, lose_s2m, lose_m2u
    else:
        return dropoff2, lose_s2m, lose_m2u
    #print(f'will get:{sml} urn2urn w/:{sitemap2urn}') #dbg
    #smu=list(map(lambda s: sitemap2urn[s], sm))
    #rest in drop1mapping now

#should be setup w/o sitemap, to get it from PROV ;no bc won't necc have mapping for something that didn't parse

#Will want to send in sitemap(url) and compare w/that gleaned from prov, so whatever prov didn't get was is a url to be checked
def sitemap_dropoff(sitemap_url=None,bucket_url=None): #bucket to get prov's version
    "figure out which sitemap URLs that need checking"
    if sitemap_url:
        sm=sitemap_list(sitemap_url) #can now use sitemap2urn to get sitemap into same ID space
    else:
        print(f'sitemap_dropoff no sitemap_url:{sitemap_url}')
        sm=[]
    if bucket_url:
        sitemap_l=prov2sitemap(bucket_url) #this gives the list of them, which most fncs expect the sitemap_url
    else:
        print(f'sitemap_dropoff no bucket_url:{bucket_url}')
        sitemap_l=[]
    if dbg: #if sitemap is malformed can get non flat list
        print(f'sitemap_dropoff,_l:{sitemap_l},sm:{sm}') #dbg
    lose_s2s=list_diff_dropoff(sitemap_l,sm) #check_sm_urls
    sml=len(sm)
    lsl=len(lose_s2s) #should= sml- ml from above
    dropoff1=f'sitemap:{sml}-{lsl}:{lose_s2s}'  
    if dbg:
        print(f'use this dropoff1:{dropoff1}')
    return sitemap_l, sm, dropoff1

def crawl_dropoff(sitemap,bucket_url,endpoint):
    "show counts at each stage, and URN diffs when can"
    if not sitemap:
        sitemap=prov2sitemap(bucket_url) #this gives the list of them, which most fncs expect the sitemap_url
    #URNs=get_graphs_list(endpoint)  #that are in the endpoint, not the expected
    URNs=get_graphs_tails(endpoint)  #that are in the endpoint, not the expected
    print(f'crawl_dropoff:URNs:{URNs}')
    #dropoff2,lose_s2m, lose_m2u = bucket_files2diff(bucket_url,URNs)
    #dropoff2,lose_s2m, lose_m2u, sitemap2urn = bucket_files2diff(bucket_url,URNs)
    dropoff2,lose_s2m, lose_m2u, sitemap2urn, su = bucket_files2diff(bucket_url,URNs)
    #sml=sitemap_len(sitemap) #can now use sitemap2urn to get sitemap into same ID space
    #if not sitemap: #could warn here
    if not sitemap: 
        print(f'crawl_dropoff, no sitemap for:{bucket_url}')
        return None
    #elif is_str(sitemap): #could be a sep if
    if is_str(sitemap): 
        if dbg:
            print(f'=using sitemap str:{sitemap}')
        else:
            print(f'using sitemap str')
        sm=sitemap_list(sitemap) #can now use sitemap2urn to get sitemap into same ID space
    else:
        if dbg:
            print(f'using sitemap list:{sitemap}')
        else:
            smul=len(sitemap)
            print(f'using sitemap list:{smul}')
        sm=sitemap #if from prov2sitemap
    #print(f'sitemap:{sm}')
    sml=len(sm)
    if sitemap2urn: #was able to get PROV..
      # dropoff,lose_s2s=drop1mapping(sm,sitemap2urn) #only call in variant above where code below goes away
        #print(f'will get:{sml} urn2urn w/:{sitemap2urn}') #dbg
        #smu=list(map(lambda s: sitemap2urn[s], sm))
        smu=list(map(lambda s: sitemap2urn.get(s), sm)) #used prov mapping to gen test sitemap
        if dbg:
            print(f'URN/UUIDs for sitemaps:{smu}')             #need to get same sitemap, &use map for cmp:
        #smu2=list(map(lambda s: s.split(':')[-1],smu))
        smu2=list(map(lambda s: s if not s else s.split(':')[-1],smu))
        if dbg:
            print(f'URN/UUIDs for sitemaps:{smu2}')             #need to get same sitemap, &use map for cmp:
        lose_s2s=list_diff_dropoff(smu2,su) 
        lsl=len(lose_s2s) #should= sml- ml from above
        if dbg:
            print(f'lose_s2s:{lose_s2s}') #will need to map this back to the sitemap url ;if it was in prov
        ##lose_s2m=list_diff_dropoff(su,mu), from above
        #dropoff=f'sitemap:{sml} =>{dropoff2}'  #pull sl, to calc dss=sml-sl
        #print(f'=Sitemap-count:{sml}, Error count:{ls1}, missing:{loose_s2s}') #dropoff should be in the next one
        print(f'=Sitemap-count:{sml}') #dropoff should be in the next one
        sl=len(smu) #url we get from prov are once it gets run into summoned
        print(f'=Summoned-count:{sl}, Error count:{lsl}, missing:{lose_s2s}')
        dropoff=f'sitemap:{sml}-{lsl}:{lose_s2s} =>{dropoff2}'  
        #dropoff=f'sitemap:{sml}-{dss}=>{dropoff2}' #can't get lose_s2s w/o PROV sitemap URLs to UUID mapping  
        #return dropoff,lose_s2m, lose_m2u
        return dropoff,lose_s2s, lose_s2m, lose_m2u
    else:
        #return dropoff2, lose_s2m, lose_m2u
        return dropoff2, None, lose_s2m, lose_m2u

#could then take these loss lists, and map over w/ check_urn_ jsonld|rdf
 #lose_s2m would only still have summoned, so could check_urn_jsonld
 #lose_m2u would only still have milled, so could check_urn_rdf
def spot_crawl_dropoff(sitemap,bucket_url,endpoint):
    "when have spot gold stnd, can also check on that"
    print("csv_ then spot_crawl_ dropoffs")
    df=csv_dropoff(sitemap,bucket_url,endpoint)
    print(df)
    #dropoff,lose_s2m, lose_m2u = crawl_dropoff(sitemap,bucket_url,endpoint)
    dropoff,lose_s2s,lose_s2m, lose_m2u = crawl_dropoff(sitemap,bucket_url,endpoint)
    if not is_list(lose_s2m): #empty list would trip this off
        print(f'spot_ crawl_dropoff, none4lose, bad:{bucket_url}')
        return None, None, None, None, None, None
    s_check=list(map(check_urn_jsonld,lose_s2m))
    if not lose_m2u:
        print(f'scd:no milled:{lose_m2u}')
        m_check=[] #..
    else:
        m_check=list(map(check_urn_rdf,lose_m2u)) #can't do this if no milled,  can try the transformation though
    #return dropoff,lose_s2m, s_check, lose_m2u, m_check 
    #return dropoff,lose_s2s, lose_s2m, s_check, lose_m2u, m_check 
    return dropoff,lose_s2s, lose_s2m, s_check, lose_m2u, m_check, df
    #could have map interleave URN w/True=ok or diff
    #return dropoff,lose_s2m, lose_m2u

#turns out reading PROV to get sitemap<->UUID's in summoned, also gives us the sitemap run
#def tsc(sitemap=None,bucket_url=None,endpoint=None):
def tsc(sitemap=None,bucket_url=None,endpoint="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/citesting/sparql"):
    "test spot_crawl_dropoff"
    if not endpoint:
        global testing_endpoint
        endpoint = testing_endpoint
    if not bucket_url:
        global ci_url
        bucket_url = ci_url
    print(f'=s3_endpoint:{bucket_url}')
    print(f'=graph_endpoint:{endpoint}')
    sitemap_l, sm, dropoff1 = sitemap_dropoff(sitemap,bucket_url) #will still get sitemap_l if no sitemap url given
    if not sitemap: #moved into crawl_dropoff, keep here/in case
        ##sitemap2urn, urn2sitemap, sitemap=prov2mappings(..)
        #sitemap=prov2sitemap(bucket_url) #this gives the list of them, which most fncs expect the sitemap_url
        sitemap=sitemap_l
    if not sitemap:
        print("did not get sitemap from prov so go w/deflt")
        sitemap="http://geocodes.ddns.net/ec/test/sep/sitemap.xml"
    print(f'=sitemap:{sitemap}')
    return spot_crawl_dropoff(sitemap,bucket_url,endpoint)

def tsc2__(sitemap2="http://geocodes.ddns.net/ec/test/sitemap.xml",bucket_url2=None,endpoint2=None):
    "same test but send in sitemap vs get it from prov"
    tsc(sitemap=sitemap2,bucket_url=bucket_url2,endpoint=endpoint2)
#old get rid of
def tsc2_(bucket_url=None,endpoint2="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/citesting2/sparql"):
    "for mb_ci setup which uses unused citesting2 bucket&endpoint"
    if not bucket_url:
        global ci_url2
        bucket_url = ci_url2
    tsc(None,bucket_url,endpoint=endpoint2)

def tsc2(sitemap=None,bucket_url=None,endpoint="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/citesting2/sparql"):
    "as is being used in spot_test/report on geocodes-dev now" #still need to deal w/milled dissapearing in a few places
    return tsc(sitemap,bucket_url,endpoint)

#def tsc3(sitemap="http://geocodes.ddns.net/ec/test/sep/sitemap.xml",bucket_url=None,
def tsc3(sitemap="https://raw.githubusercontent.com/MBcode/ec/master/test/sitemap.xml",bucket_url=None,
        endpoint="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/citesting2/sparql"):
    "as is being used in spot_test/report on geocodes-dev now" #still need to deal w/milled dissapearing in a few places
    return tsc(sitemap,bucket_url,endpoint)

#this has the sitemap from the gSpreadsheet 'sources'
def tsc4_(sitemap="https://earthcube.github.io/GeoCODES-Metadata/metadata/Dataset/allgood/sitemap.xml",bucket_url=None,
        endpoint="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/citesting2/sparql"):
    "as is being used in spot_test/report on geocodes-dev now" #still need to deal w/milled dissapearing in a few places
    return tsc(sitemap,bucket_url,endpoint)

#this has the sitemap from the gSpreadsheet 'sources'  ;keep bucket in sync w/endpnt etc #bucket_url=ci_url2,
def tsc4(sitemap="https://earthcube.github.io/GeoCODES-Metadata/metadata/Dataset/allgood/sitemap.xml", 
        bucket_url="https://oss.geocodes-dev.earthcube.org/citesting2",
        endpoint="http://ideational.ddns.net:3030/geocodes_demo_datasets/sparql"):
       #endpoint="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/citesting2/sparql"): #nabu was not run here
    "as is being used in spot_test/report on geocodes-dev now" #still need to deal w/milled dissapearing in a few places
    return tsc(sitemap,bucket_url,endpoint)
#9=9 #this got the graph to show up, milled was skiped by gleaner, &had similar summoned
#0  geocodes_demo_datasets:MB_amgeo_data-01-06-201...    ok  None    ok
#1        geocodes_demo_datasets:MB_iris_syngine.json    ok  None    ok
#2  geocodes_demo_datasets:MB_lipdverse_HypkanaHaj...  None  None  None
#3          geocodes_demo_datasets:argo-20220707.json    ok  None    ok
#4    geocodes_demo_datasets:argoSimple-v1Shapes.json    ok  None    ok
#5       geocodes_demo_datasets:bcodmo1-20220707.json    ok  None    ok
#6                geocodes_demo_datasets:bcodmo1.json    ok  None    ok
#7         geocodes_demo_datasets:earthchem_1572.json  None  None  None
#8              geocodes_demo_datasets:opentopo1.json    ok  None    ok
#get_oss_files now gets summoned, but getting check_urn_jsonld error, that is new/but getting good urls from this fnc
#it was the test data coming from citesting vs test3 fix above/and all works
def tscg(sitemap="https://earthcube.github.io/GeoCODES-Metadata/metadata/Dataset/allgood/sitemap.xml"): #rest are global
    global bucket_url,testing_endpoint
    endpoint=testing_endpoint
    print(f'tscg:{sitemap},{bucket_url},{endpoint}')
    return tsc(sitemap,bucket_url,endpoint)

#def mb_ci2(sitemap="https://earthcube.github.io/GeoCODES-Metadata/metadata/Dataset/allgood/sitemap.xml",
#made cp of sitemap, so could add bad tests, eg. a 404
def mb_ci2(sitemap="https://raw.githubusercontent.com/MBcode/ec/master/test/sitemap.xml",
   #def mb_ci2(sitemap="http://mbobak.ncsa.illinois.edu/ec/test/sitemap.xml", #before pushing to github
          #endpoint="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/mb_ci2/sparql", #not being filled/fix
           endpoint="http://ideational.ddns.net:3030/geocodes_demo_datasets/sparql",
           bucket_url="https://oss.geocodes-dev.earthcube.org/mbci2"): 
          #bucket_url="https://oss.geocodes-dev.earthcube.org/mb_ci2"): #can't name bucket this way 
    print(f'mb_ci2:{sitemap},{bucket_url},{endpoint}')
    print(" ") #spot_crawl_dropoff has .. w/df at end, that needs a newline
    return tsc(sitemap,bucket_url,endpoint)

def test5(sitemap="https://earthcube.github.io/GeoCODES-Metadata/metadata/Dataset/allgood/sitemap.xml",
           endpoint="http://localhost:9999/blazegraph/namespace/nabu/sparql",
           bucket_url="https://oss.geocodes-dev.earthcube.org/test5"): 
    print(f'test5:{sitemap},{bucket_url},{endpoint}')
    return tsc(sitemap,bucket_url,endpoint)
#_testing end
