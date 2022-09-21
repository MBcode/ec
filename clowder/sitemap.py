#!/usr/bin/env python3
#generate a sitemap for all the datasets, via the clowder api
# http://isda.ncsa.uiuc.edu/~mbobak
import requests
import json
import sys
import os
from os.path import exists
import subprocess
top= """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
   """ 

#could do this w/in the loop
def put_txtfile(fn,s,wa="a"): 
    "default of add to textfile" #so should compress previous
    with open(fn, wa) as f: 
        return f.write(s)

def datasetlist2sitemap(url,sm="sitemap.xml"):
    r=requests.get(url)
    if r.status_code != 200:
        print(r.status_code)
        return r.status_code
    URLb = url.strip("api/datasets")
    ja=json.loads(r.text)
    if not ja:
        print("no text")
        return 0
    if exists('sitemap.xml.gz'):
        os.remove("sitemap.xml.gz")
    if exists('sitemap.xml'):
        cs=f'yes|gzip {sm}'
        cr=subprocess.call(cs,shell=True)
        if cr != 0:
            print(f'cr={cr}')
    put_txtfile(sm,top)
    for ds in ja:
        id=ds.get('id')
        if(id):
            put_txtfile(sm,f'<url><loc>{URLb}/datasets/{id}</loc></url> ')
    put_txtfile(sm,"</urlset>")
    return os.stat('sitemap.xml').st_size 

if __name__ == '__main__':
    #if >2 could set alt sitemap name
    if len(sys.argv) > 1:
        url = sys.argv[1]
        if not "datasets" in url: 
            url = url + "/api/datasets" #so can just send in clowderurl
    else:
        url = "http://localhost:9000/api/datasets" 
    datasetlist2sitemap(url)
