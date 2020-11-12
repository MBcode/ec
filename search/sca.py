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

#from fillSearch.py but most of this will be going in there anyway
def first(l):
    from collections.abc import Iterable
    if isinstance(l,list):
        return l[0]
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
    qry_str="carbon"

#r = requests.get(f"{clowder_host}/api/search?query={qry_str}", headers={'X-API-Key': clowder_key}) 
r = requests.get(f"{clowder_host}/api/search?query={qry_str}") 
#print(json.dumps(r.json(), indent=2))  #maybe not print here, and only print after the new keys are added

#getLD the 'details' for each search result, and put (link?) back in search results
for result in r.json()["results"]:
  dataset=result['id']
  #print(dataset) #only print after altering now
  LD=getjsonLD(dataset)
  #print(LD) #maybe not print it all(unless err)&just print new keys added
  #print(result) #lets just see the record w/the new keys
# print(json.dumps(result, indent=2)) #but w/formatting so easier to see
  #could turn into jsonl-ld playground viz tab url here
  LDc=LD.get("content")
  publ=LDc.get("publisher")
  date=first(LDc.get("datePublished"))
  if(date):
      print("=======================")
      print(date)
      result['date']=date
  if(publ):
      print("=======================")
      pub=first(publ)
      print(pub)
      result['publisher']=pub
      print("=======================")
  else:
      print("=--==--==--==--==--==--")
      print(type(LD))
      #print(LD)
      for key in LD:
          print(key)
      print(json.dumps(LD, indent=2))
      print("=--==--==--==--==--==--")
# result['details']=LD  #not getting back to r.json
  #this won't be seen in print, unless moved down here
  print(json.dumps(result, indent=2))

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
