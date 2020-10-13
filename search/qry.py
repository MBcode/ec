#this is the NB/cli code that can be used w/o an auth-key
#"http://mbobak-ofc.ncsa.illinois.edu:5000/search/carbon"
#earthcube_host="http://mbobak-ofc.ncsa.illinois.edu:5000"
#earthcube_host="http://localhost:5000"
import requests
import json
import sys
import os
earthcube_host=os.getenv('earthcube_host')
if len(sys.argv)>1:
    qry_str=argv[1]
else:
    qry_str="carbon"
print(qry_str)
try:
    r = requests.get(f"{earthcube_host}/search/{qry_str}")
except:
    print("exception so used backup")

print(r.status_code)
#if(r.status_code == requests.codes.ok):
if(r.status_code == 200):
    print(json.dumps(r.json(), indent=2)) 
else:
    print("going for triplestore backup")
    #r = requests.get(f"{earthcube_host}/search3/{qry_str}")
    cs=f"python3 sq.py {qry_str}" #can qry w/sq=sparql-query
    r=os.popen(cs).read()
    print(r) 

#above runs off ss.py and now: ss2.py, which adds:
#r = requests.get(f"{earthcube_host}/search3/{qry_str}")
 #which just calls a sparql-query to to a text-search
#if I make the return the same, will put both under /search
 #which is essentially what the above code does
# break out any search clustering to /cluster
#Also get add 'try' everywhere
