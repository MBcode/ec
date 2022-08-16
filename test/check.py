#!/usr/bin/env python3
#mike b, check endpoint and restart it, if it times out
import requests
import json
import os
import logging
#logger = logging.getLogger(__name__)
#at the moment this won't make any difference, but can use soon
cs="restart_triplestore.sh" #fixed to _ once it is working
#cs="restart-triplestore.sh" #use during testing
url="https://graph.geodex.org/blazegraph/namespace/earthcube/sparql"
url2="http://graph.geocodes.earthcube.org"

def restart_endpoint(cs="restart_triplestore.sh"):
    os.system(cs)

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
    #logger.warning(s) #would differentiate

def os_system(cs):
    os.system(cs)
    add2log(cs)
#=
def add2slack(s):
    cs='source ~/mb/.ssh/.ck'
    os.system(cs)
    key=os.getenv("nagioslack") #make sure works for su/crontab too
    #change to requests, and use getenv, if I actually use this part
    if key:
        cs="curl -X POST -H ‘Content-type: application/json’ --data '{\"text\":{s}}' https://hooks.slack.com/services/{key}"
        os_system(cs)
    else:
        print("no key for logging")

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

#got different results from ec.py bc default endpoint is different, 
 #so either send in, or use local version w/change
#def get_query_time(local=None):
def get_query_time(local=True):
    if local:
        import httpimport
        with httpimport.github_repo('MBcode', 'ec'):
          import ec
    #ec.get_ec() #work from scratch version for a bit
    else:
        import ec
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
    return elapse


#not using signal version, as wasn't caught properly
def handler(signum, frame):
    print("handler")
    add2log("norway query > 35 sec")
    raise Exception("norway query > 35 sec")

def try_query_time(local=None):
    import signal
    #signal.alarm(35)
    signal.alarm(35) #for testing
    try:
        elapse=get_query_time(local)
        print(elapse)
    except Exception as exc:
        add2log("norway query > 35 sec")
        print(exc)
        add2log(exc) #pass str
        #add2slack(exc) #pass str
        add2slack("norway query > 35 sec, so auto-restarting")
    print("post try")

#try_query_time(True) #use local version w/diff endpoint for now

def query_timeout(local=None):
    from func_timeout import func_timeout, FunctionTimedOut
    try:
        #elapse=get_query_time(local)
        #elapse=func_timeout(5,get_query_time,args=(local))
        #elapse=func_timeout(5,get_query_time,args=())
        elapse=func_timeout(45,get_query_time)
        print(elapse)
        add2log(f'elapse={elapse}') 
    except FunctionTimedOut:
        add2log("norway query > 45 sec, so restart_endpoint")
        restart_endpoint()
    except Exception as exc:
        add2log("norway query > 35 sec")
        print(exc)
        add2log(exc) #pass str
        #add2slack(exc) #pass str #don't have to tell us on slack if had to restart, just log it
    print("post try")

#right now the timings are hourly, strange the diff in endpoints, will be good to see
 #and even better finally getting the time to work on it, which it is being tracked(for timing..)

query_timeout(True) #use local version w/diff endpoint for now
