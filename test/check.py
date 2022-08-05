#!/usr/bin/env python3
#mike b, check endpoint and restart it, if it times out
import requests
import json
import os
cs="restart_triplestore.sh" #fixed to _ once it is working
#cs="restart-triplestore.sh" #use during testing
url="https://graph.geodex.org/blazegraph/namespace/earthcube/sparql"
url2="http://graph.geocodes.earthcube.org"

#from ec.py:
def put_txtfile(fn,s,wa="w"):
    #with open(fn, "w") as f:
    with open(fn, "a") as f:
        return f.write(s)

def date2log():
    #cs="date>>log"
    cs="date>>check.log"
    os.system(cs)

def add2log(s):
    date2log()
    fs=f'[{s}]\n'
    #put_txtfile("log",fs,"a") 
    put_txtfile("check.log",fs,"a") 

def os_system(cs):
    os.system(cs)
    add2log(cs)
#=
key =  "too/secret"
def add2slack(s):
    #change to requests, and use getenv, if I actually use this part
    cs="curl -X POST -H ‘Content-type: application/json’ --data '{\"text\":{s}}' https://hooks.slack.com/services/{key}"
    os_system(cs)

def get_sc(url):
    try:
        print(f'checking:{url}')
        #rds=requests.post(url)
        #rds=requests.get(url, timeout=(15, 45))
        rds=requests.get(url2, timeout=(15, 45))
        #print(rds.json()) #check for good return before running the rest 
        print(rds.status_code)
    #except:
    except Exception as e:
        print(cs)
        add2log(cs)
        add2log(e) #pass str
        #add2slack(e) #pass str
        os.system(cs)

get_sc(url2)
#getting ok while it is having problems, bc not hitting that part of the store?
#might load ec.py and do an actual query, and start to log timings as well

def get_query_time():
    import httpimport
    with httpimport.github_repo('MBcode', 'ec'):
      import ec
    #ec.get_ec() #work from scratch version for a bit
    #import ec
    q="norway"
    ec.local() #don't load lots of libs for the notebook
    import time
    start=time.time()
    df=ec.txt_query(q)
    end=time.time()
    elapse=end - start
    #print(df)
    print(elapse)
    add2log(elapse)

get_query_time()
