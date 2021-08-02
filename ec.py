#pagemil parameterized colab/gist can get this code via:
#with httpimport.github_repo('MBcode', 'ec'):
#  import ec
import os

#start adding more utils, can use to: fn=read_file.path_leaf(url) then: !head fn
def path_leaf(path):
    import ntpath
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def file_ext(fn):
    st=os.path.splitext(fn)
    return st[-1]

def wget(fn):
    cs= f'wget -a log {fn}' 
    os.system(cs)

def add_ext(fn,ft):
    fn1=path_leaf(fn) #just the file, not it's path
    fext=file_ext(fn1) #&just it's .ext
    if fext==None or fext=='':
        fnt=fn1 + ft
        cs= f'mv {fn1} {fnt}' 
        os.system(cs)

def wget_ft(fn,ft):
    wget(fn)
    add_ext(fn,ft)

def wget_rdf(urn):
    if(urn.startswith('urn:')):
        url=urn.replace(":","/").replace("urn","https://oss.geodex.org",1)
        url += ".rdf"
        cs= f'wget -a log {url}' 
        os.system(cs)
        urlroot=path_leaf(url)
        fn1 = urlroot + ".rdf"
        fn2 = urlroot + ".nt" #more specificially, what is really in it
        cs= f'mv {fn1} {fn2}' #makes easier to load into rdflib..eg: 
        os.system(cs)
        #from rdflib import Graph
        #g = Graph()
        #g.parse(fn2)
    else:
        return f'bad-urn:{urn}'

#should change os version of wget to request so can more easily log the return code
 #maybe, but this is easiest way to get the file locally to have to use
  #though if we use a kblab/sublib or other that puts right to graph, could dump from that too

def read_file(fnp, ext=None):
    "can be a url, will call pd read_.. for the ext type"
    import pandas as pd
    import re
    fn=fnp.strip('/')
    fn1=path_leaf(fn) #just the file, not it's path
    fext=file_ext(fn1) #&just it's .ext
    #url = fn
    if(ext!=None):
        ft="." + ext
    else: #use ext from fn
        ft=fext
    df=""
    if ft=='.tsv' or re.search('tsv',ext,re.IGNORECASE) or re.search('tab-sep',ext,re.IGNORECASE):
        df=pd.read_csv(fn, sep='\t',comment='#')
    elif ft=='.csv' or re.search('csv',ext,re.IGNORECASE):
        df=pd.read_csv(fn)
    elif ft=='.txt' or re.search('text',ext,re.IGNORECASE):
        df=pd.read_csv(fn, sep='\n',comment='#')
    elif ft=='.zip' or re.search('zip',ext,re.IGNORECASE):
        ft='.zip'
        wget_ft(fn,ft)
#       df=pd.read_csv(fn, sep='\t',comment='#')
        df="can't read zip w/o knowing what is in it, doing:[!wget $url ],to see:[ !ls -l ]"
    else:
        wget_ft(fn,ft)
        #df="no reader, can !wget $url"
        df="no reader, doing:[!wget $url ],to see:[ !ls -l ]"
    #look into bagit next/maybe, also log get errors, see if metadata lets us know when we need auth2get data
    #if(urn!=None): #put here for now
    #    wget_rdf(urn)
    return df
