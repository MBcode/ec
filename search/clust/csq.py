#this supercedes csq.sh, but still uses sq2.py to do the search and cluster it
#import xmltodict #prefer to have curl below dump in json format
import json
import sys
import os
if(len(sys.argv)>1):
    qry_str=sys.argv[1]
else:
    qry_str = "organic"
cs=f'/usr/bin/python3 sq2.py {qry_str} | curl $dcs_url -F "dcs.output.format=JSON" -F "dcs.c2stream=@-"'
s=os.popen(cs).read()
#d=xmltodict.parse(s)
d=json.loads(s)
#print(json.dumps(s, indent=2))
print(s)
#print(type(d))
