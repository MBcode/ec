#get output from sq.py which does a free-text search of triplestore &returns output in format ready for carro2 clustering
#setenv dcs_url "http://localhost:8080/dcs/rest"
# curl $dcs_url -F "dcs.c2stream=@c2.xml"
#dcs_url =  "http://10.0.0.34:8080/"
#dcs_url =  "http://10.0.0.34:8080/dcs/rest"
dcs_url =  "http://localhost:8080/dcs/rest"
#curl $dcs_url -F "dcs.c2stream=@
#similar to sending the jsonld2clowder but sending the xml to cluster-service
import os
import json
#dcs_url = os.getenv('dcs_url')

def search2dcs(searchfile = 'search.xml'):
    "search output in carrot2 input format2 qry srvc"
    import xmltodict
    import requests
    with open(searchfile) as f:
        xml=f.read()
    hits = xmltodict.parse(xml)
    header1={'Content-Type': 'application/json'}
    header2={'Content-Type': 'application/json', 'dcs.output.format': 'JSON'}
    header3={'Content-Type': 'application/json', 'dcs.output.format': 'JSON', 'dcs.c2stream': searchfile}
    r=requests.post(dcs_url,data=hits,headers=header2)
    if r:
        print(r.json())
        return r.json()
    else: 
        return hits

#don't want from input file, want from direct output from sq.py call, try2avoid tmp file
#cat c2.xml | curl $dcs_url -F "dcs.c2stream=@-"
 #works, 
# python3 sq.py carbon | curl $dcs_url -F "dcs.c2stream=@-"


def csearch2dcs(searchfile = 'search.xml'):
    "search output in carrot2 input format2 qry srvc"
    #cs=f'out=$(curl {dcs_url} -F "dcs.c2stream=@{searchfile}"); echo $out'
    #cs=f'curl $dcs_url -F "dcs.c2stream=@{searchfile}"'
    cs=f'curl {dcs_url} -F "dcs.c2stream=@{searchfile}"'
    #cs=f'dcs.sh {searchfile}' #works 
    print(cs)
    s=os.popen(cs).read()
    return s

def t2(sf='c2.xml'):
    #hits=search2dcs(sf)
    hits=csearch2dcs(sf)
    print(hits)
