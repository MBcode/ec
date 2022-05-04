#generate a sitemap for all the datasets, via the clowder api
# http://isda.ncsa.uiuc.edu/~mbobak
import requests
import json
import sys
top= """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
   """ 

#could do this w/in the loop
def put_txtfile(fn,s,wa="w"):
    with open(fn, "a") as f:
        return f.write(s)

def datasetlist2sitemap(url,sm="sitemap.xml"):
    r=requests.get(url)
    put_txtfile(sm,top)
    URLb = url.strip("api/datasets")
    ja=json.loads(r.text)
    for ds in ja:
        id=ds.get('id')
        if(id):
            put_txtfile(sm,f'<url><loc>{URLb}/datasets/{id}</loc></url>')

if __name__ == '__main__':
    #if >2 could set alt sitemap name
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "http://localhost:9000/api/datasets" 
    datasetlist2sitemap(url)
