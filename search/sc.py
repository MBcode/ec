#early example of augmenting search results
#taken from the colab NB that I've shared
import requests
import json
import os 
clowder_host = "https://earthcube.clowderframework.org" 
clowder_key = os.getenv('eckey') #I can use locally w/new instance till it is fixed 

#To check it was uploaded, or when get search results, &want metadata, send an 'id' to this:
def getLD(datasetID):
    r = requests.get(f'{clowder_host}/api/datasets/{datasetID}/metadata', headers={'X-API-Key' : clowder_key})
    #print(json.dumps(r.json(), indent=2)) 
    #print(r.json()) 
    return r.json() 

def getjsonLD(datasetID):
    "given clowder dataset id: return it's saved()jsonLD"
    r = requests.get(f'{clowder_host}/api/datasets/{datasetID}/metadata.jsonld', headers={'X-API-Key' : clowder_key})
    print(json.dumps(r.json(), indent=2))

qry_str = "multibeam sonar" 

r = requests.get(f"{clowder_host}/api/search?query={qry_str}", headers={'X-API-Key': clowder_key}) 
print(json.dumps(r.json(), indent=2))

#getLD the 'details' for each search result, and put (link?) back in search results
for result in r.json()["results"]:
  dataset=result['id']
  print(dataset)
  LD=getjsonLD(dataset)
  print(LD)
# #could turn into jsonl-ld playground viz tab url here
  result['details']=LD  #not getting back to r.json


#I'm ok w/going w/an API based approach where the above search once open (as was advertised)
 #can replace the present geodex.org one: https://geocodes.earthcube.org/?q=carbon&n=200
 #I still just need the 'url' key to appear, so might include it in the description as a link
 
 #Interesting someone else asked about doing this just today on #general

 #I still just need the 'url' key to appear, so might include it in the description as a link
  #it can be had from the metadata:    but needs to be up top

#Turns out several of the search results already do have the metadata tab filled out
 #if clicking on a result went to the metadata tab, it would be like our 'details' page

#ps. the login time-outs are still driving me crazy, the really have to be lengthened.
