#cat sc.py ss2sq.py > sc2.py
#use the jsonLD for a search?q=  that might incl facet/filters
#===
#return all the jsonLD for each of the search results

#early example of augmenting search results
#taken from the colab NB that I've shared
import requests
import json
import sys 
import os 
clowder_host = "https://earthcube.clowderframework.org" 
#clowder_key = os.getenv('eckey') #I can use locally w/new instance till it is fixed 
 #no longer needed

#To check it was uploaded, or when get search results, &want metadata, send an 'id' to this:
def getLD(datasetID):
    #r = requests.get(f'{clowder_host}/api/datasets/{datasetID}/metadata', headers={'X-API-Key' : clowder_key})
    r = requests.get(f'{clowder_host}/api/datasets/{datasetID}/metadata')
    #print(json.dumps(r.json(), indent=2)) 
    #print(r.json()) 
    return r.json() 

def getjsonLD(datasetID):
    "given clowder dataset id: return it's saved()jsonLD"
    #r = requests.get(f'{clowder_host}/api/datasets/{datasetID}/metadata.jsonld', headers={'X-API-Key' : clowder_key})
    r = requests.get(f'{clowder_host}/api/datasets/{datasetID}/metadata.jsonld')
    print(json.dumps(r.json(), indent=2))

##qry_str = "multibeam sonar" 
#if len(sys.argv)>1:
#    qry_str=sys.argv[1]
#else:
#    qry_str="carbon"

##r = requests.get(f"{clowder_host}/api/search?query={qry_str}", headers={'X-API-Key': clowder_key}) 
#r = requests.get(f"{clowder_host}/api/search?query={qry_str}") 
#print(json.dumps(r.json(), indent=2))

##getLD the 'details' for each search result, and put (link?) back in search results
#for result in r.json()["results"]:
#  dataset=result['id']
#  print(dataset)
#  LD=getjsonLD(dataset)
#  print(LD)
## #could turn into jsonl-ld playground viz tab url here
#  result['details']=LD  #not getting back to r.json

#this (just above) will be needed for a faceted search on these metadata elts


#I'm ok w/going w/an API based approach where the above search once open (as was advertised)
 #can replace the present geodex.org one: https://geocodes.earthcube.org/?q=carbon&n=200
 #I still just need the 'url' key to appear, so might include it in the description as a link
 
 #Interesting someone else asked about doing this just today on #general

 #I still just need the 'url' key to appear, so might include it in the description as a link
  #it can be had from the metadata:    but needs to be up top

#Turns out several of the search results already do have the metadata tab filled out
 #if clicking on a result went to the metadata tab, it would be like our 'details' page

#ps. the login time-outs are still driving me crazy, the really have to be lengthened.
#Search main or backup clowder or search3 sparql endpoint(&get all metadata at once)
#ss.py + dev4c.py,  then took sparql part out into sq.py, and call it from this: ss2sq.py
#code below is from the colab NoteBook that I shared awhile ago
# can be more than a shim to get non-auth clowder search
#since it's an API shim/augmentation, will assume called from NB or other code,
 #but as I get html returns could just call it from a txt-box or directly
# for which I will give the qry.py example
# which already falls over to sq.py sparql query, should do that here for /search
#then make sure all output is close/useable for final html search results
#&add something like /cluster to produce the carrot2 clustering results
from flask import Flask
from markupsafe import escape
app = Flask(__name__)
import requests
import json
import os
#./ld holds links to full LinkedData cache

@app.route('/agrep/<qry>')
def agrep(qry):
    "agrep jsonld, get as html"
    qry_str=escape(qry) #tre-agrep is preferred
    #cs=f"agrep -d'^\{' {qry_str} ld/edi/* |sed '/^ld\//s//<p>/'"
    cs=f"getLD.sh {qry_str} "
    htm=os.popen(cs).read()
    #s=os.popen(cs).read()
    #htm= '<html>' + s + '</html>'
    return htm

@app.route('/ag/<qry>')
def ag(qry):
    "grep jsonld, get as html"
    qry_str=escape(qry) 
    cs=f"ag {qry_str} ld/* |sed '/^ld\//s//<p>/'"
    s=os.popen(cs).read()
    htm= '<html>' + s + '</html>'
    return htm

def sq(qry_str):
    "sparql query"
    #cs=f"python3 sq.py {qry_str}"
    cs=f"python3 sq.py {qry_str}|sed '/^</s//<br></'"
    s=os.popen(cs).read()
    if len(s)<8:
        print("<!--nothing from triplestore backup2grep-->")
        ag(qry_str)
    #return s 
    htm= '<html>' + s + '</html>'
    return htm

@app.route('/search3/<qry>')
def search3(qry):
    "sparql text search"
    qry_str=escape(qry) 
    #cs=f"python3 sq.py {qry_str}"
    #s=os.popen(cs).read()
    #if len(s)<8:
    #    print("<!--nothing from triplestore backup2grep-->")
    #    ag(qry)
    s = sq(qry)
    return s 

#@app.route('/search/<qry>')
#def search(qry):
@app.route('/search')
def search():
    "text search of clowder then sparql if down"
    #was setup to fallback from earthcube to ncsa clowder at one point
    #clowder_key = os.getenv('testkey')
    # clowder_key = os.getenv('eckey')
    clowder_host = os.getenv('clowder_host')
    #if not clowder_host:
    #    clowder_host = "https://earthcube.clowderframework.org"
    #    clowder_key = os.getenv('testkey')
    print(clowder_host)
#    qry_str=escape(qry) 
    from flask import request
    qry_str = request.args.get("q")
    print(qry_str)
    #print(f'host:{clowder_host},qry:{qry_str}')
    ret=" " #shouldn't need to do this
    try:
        #r = requests.get(f"{clowder_host}/api/search?query={qry_str}", headers={'X-API-Key': clowder_key})
        #cs=f"python3 fillCSS.py {qry_str}"
        cs=f"python3 fillSearch.py {qry_str}"
        r=os.popen(cs).read()
        if(not r):
            r = requests.get(f"{clowder_host}/api/search?query={qry_str}")
        else:
            return r
        #could either call fillCSS.py or it's fnc that turn the ret json just above into the final html
    except:
        print("<!--exception so used backup-->")
        #ret=search3(qry)
        ret=sq(qry)
    else:
        sc=r.status_code
        ret=f'<!--status-code:{sc}-->'
        print(ret)
        #if r:
        #if(r.status_code == requests.codes.ok):
        if(r.status_code == 200):
            ret = json.dumps(r.json()['results'], indent=2)
            return ret
        else:
            ret=sq(qry)
    return ret

#qry.py falls over when clowder down to search3, I'd like that try/excpt..to happen here next
 #is is a cli that calls the /search route but then backs up to the /search3 route
  #but I could just have search that right here went clowder->sparql->grep

#next get search json.. in html format, for now; 
 #bc I can't get geodex api returns, to see what they are like to match them yet
