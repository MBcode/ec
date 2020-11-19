#cp sc.py sca.py #leta see if we can getjsonLD and add a few keys from it  to each record returned
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

def full(l):
    return (len(l) > 0)
#from fillSearch.py but most of this will be going in there anyway
def first(l):
    from collections.abc import Iterable
    if isinstance(l,list):
        if(full (l)):
            return l[0]
        else: 
            #return l
            return None
    elif isinstance(l,Iterable):
        return list(l)[0]
    else:
        return l

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
    return  first(r.json())

#qry_str = "multibeam sonar" 
if len(sys.argv)>1:
    qry_str=sys.argv[1]
else:
    #qry_str="carbon" #2many4test
    qry_str="multibeam sonar"

#r = requests.get(f"{clowder_host}/api/search?query={qry_str}", headers={'X-API-Key': clowder_key}) 
r = requests.get(f"{clowder_host}/api/search?query={qry_str}") 
#print(json.dumps(r.json(), indent=2))  #maybe not print here, and only print after the new keys are added

#https://gist.github.com/douglasmiranda/5127251
def find(key, dictionary):
    for k, v in dictionary.iteritems():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result

#lots of bad DDS dates, ..

def LD2re(LD,result):
  LDc=LD.get("content") 
  #LDc0=LD.get("content")
  #LDc=LDc0.get("details")
  LDd=LDc.get("details")
  publ=LDc.get("publisher")
# publ=find("publisher",LDc)
  date=first(LDc.get("datePublished"))
  #if not date:
  if( not date or len(date)<2):
      print("details")
      details=first(LDc.get("details"))
      print(details)
      if details:
          date=first(details.get("datePublished"))
          print(date)
# date=find("datePublished", LDc)
  if(date):
      print(f'==================date:{date}')
      result['date']=date
  pub = LDc.get("publisher")
  #print(f'===================pub:{pub}')
  #if(publ):
  #if(isinstance(publ, list)):
  if(isinstance(publ, dict)):
      #print("===================pub:")
      pub = publ.get("name")
   #  pub = find("name", publ)
      if(not pub): 
          #pub=first(publ)
          publ=publ['']
          pub = publ.get("name")
      if(not pub): 
          pub = LDd.get("publisher")
      print(f'===================pub:{pub}')
      result['publisher']=pub
      print("=======================")
  else:
      print(f'==========pub:{pub}')
      print("=--==--==--==--==--==--")
      #print(type(LD))
      #print(LD)
      #for key in LD:
      for key in LDc:
          print(key)
      ##print(json.dumps(LD, indent=2))
      #print(json.dumps(LDc, indent=2))
      print("=--==--==--==--==--==--")
# result['details']=LD  #not getting back to r.json
  result['details']=LDc 
  return result

#getLD the 'details' for each search result, and put (link?) back in search results
for result in r.json()["results"]:
  dataset=result['id']
  print(f'=========dataset:{dataset}====')
  #print(dataset) #only print after altering now
  LD=getjsonLD(dataset)
  #print(LD) #maybe not print it all(unless err)&just print new keys added
  #print(result) #lets just see the record w/the new keys
# print(json.dumps(result, indent=2)) #but w/formatting so easier to see
  #could turn into jsonl-ld playground viz tab url here
  #-
  if(LD):
      re = LD2re(LD, result)
  else:
      re = result
  #-
  #this won't be seen in print, unless moved down here
  print(json.dumps(re, indent=2))
  #if func: return result #&if print wasn't being scooped up

#could just be txt-dumping this, since fillSearch is taking a qry, getting this json, this should be put there
 #and can have the html have other elts not seen, not necc RDFa, but whatever is easy to facet on the page


#I'm ok w/going w/an API based approach where the above search once open (as was advertised)
 #can replace the present geodex.org one: https://geocodes.earthcube.org/?q=carbon&n=200
 #I still just need the 'url' key to appear, so might include it in the description as a link
 
 #Interesting someone else asked about doing this just today on #general

 #I still just need the 'url' key to appear, so might include it in the description as a link
  #it can be had from the metadata:    but needs to be up top

#Turns out several of the search results already do have the metadata tab filled out
 #if clicking on a result went to the metadata tab, it would be like our 'details' page

#ps. the login time-outs are still driving me crazy, the really have to be lengthened.
