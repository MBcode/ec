#this is the NB/cli code that can be used w/o an auth-key
#"http://mbobak-ofc.ncsa.illinois.edu:5000/search/carbon"
earthcube_host="http://mbobak-ofc.ncsa.illinois.edu:5000"
earthcube_host="http://localhost:5000"
#on this machine they are the same
import requests
import json
import sys
if len(sys.argv)>1:
    qry_str=argv[1]
else:
    qry_str="carbon"
r = requests.get(f"{earthcube_host}/search/{qry_str}")
print(json.dumps(r.json(), indent=2)) 
