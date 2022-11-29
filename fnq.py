#!/usr/bin/env python3
#mbobak, fnq.py an extention of my fuseki-server of a .nq file, alias
#_will be used w/ tsum.py to have that repo available on:
#   tmp_endpoint=f'http://localhost:3030/{repo}/sparql' #fnq repo
#-more from n18 notes:
#will also run the other summaries now even to get sense of what it would be w/more repos
# for that, have a: Catupcwdext  to: cat *.ttl > ../$cwd.ttl
#_and have tsum.py or script above it, also run the fnq repo.ttl ;till do it w/rdflib internally
# alias fnq "nohup fuseki-server --file \!*.nq /\!* &"
# _if do one repo at a time, and want to re-use the port, then, kill-all fuseki-server before running it
#try a py fnc, to add to tsum.py, that would do above, or w/just the os call, could be in it's own fnq.py 
import os
#from ec.py
def os_system(cs):
    "run w/o needing ret value"
    os.system(cs)
    #add2log(cs)

def os_system_(cs):
    "system call w/return value"
    s=os.popen(cs).read()
    #add2log(cs)
    return s

def is_str(v):
    return type(v) is str

def is_list(v):
    return type(v) is list

#=

def ps_fuseki():
    "kill fuseki server"
    #return os_system_("psgrep fuseki-server")
    #s= os_system_("ps -ef|grep fuseki-server")
    s= os_system_("ps -ef|grep fuseki-server|grep -v grep")
    #sl=s.split(' ').remove('')
    sl=s.split(' ')
    #print(f'ps:{sl}')
    #sl=sl.remove('') #destroys list
    sl = [i for i in sl if i]
    print(f'ps:{sl}')
    if is_list(sl):
        if len(sl) >1:
            pid=sl[1]
            print(f'pid:{pid}')
            return pid
    return sl

def kill_fuseki():
    old=ps_fuseki()
    pid=old
    print(f'will kill server, from:{old}')
    if old: #wait to make sure dead
        ks=f'kill -9 {pid}'
        print(ks)
        os_system(ks)
        os_system("sleep 5")
    #os_system("killall fuseki-server")

def run_fuseki(repo):
    kill_fuseki() #vs a new port
    print(f'will start fuseki-server, for:{repo}') #no nohup as it's temporary
    os_system(f'fuseki-server --file {repo}.nq /{repo} &')

if __name__ == '__main__':
    import sys
    if(len(sys.argv)>1):
        repo = sys.argv[1]
        tmp_endpoint=f'http://localhost:3030/{repo}/sparql' #fnq repo
        print(f'try:{tmp_endpoint}') #if >repo.ttl, till prints, will have to rm this line &next2:
        #next3lines from tsum.py, _but_
        #ec.dflt_endpoint = tmp_endpoint
        #df=ec.get_summary("")
        #summaryDF2ttl(df) 
        #_but_ here we are just getting that server going:
        from os.path import exists #check if have the file to serve
        fn=f'{repo}.nq'
        if not exists(fn):
            print(f'no:{fn} to server')
        else:
            run_fuseki(repo)
            os_system("sleep 9")

#how it is run:
#==> summarize_repo.sh <==
#fnq.py $1
#tsum.py $1 |egrep -v "not IN_COLAB|rdf_inited|try:http"|cat>$1.ttl

#if you get an error, where the sleep above wasn't enough, the server is running, but you just need tsum.py part, run:
#==> tsum.sh <==
#tsum.py $1 |egrep -v "not IN_COLAB|rdf_inited|try:http"|cat>$1.ttl