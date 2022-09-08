#!/usr/bin/env python3
#mike bobak, getting used to clowder v2 api
import os
import requests
#api_url='http://localhost:8000/api/v2/login'
api_base_url='http://localhost:8000/api/v2/'
c2passwd=os.getenv("c2passwd")
jd={ "email": "mbobak@illinois.edu"}
jd["passwd"]=c2passwd
s = requests.Session()

def c2post(route):
    api_url=api_base_url + route
    print(f'post to:{api_url}')
    r=s.post(api_url, json=jd)
    print(r.status_code)
    print(f'content:{r.content}')
    #return r.json() #vs content
    return r.content

#token=r.json() #vs content
token=c2post("login")
print(token) 

#next use token in next calls
 #session should deal w/cookies 
  #to help w/fast changeover

def c2get(route):
    api_url=api_base_url + route
    print(f'post to:{api_url}')
    r=s.get(api_url, json=jd)
    print(r.status_code)
    print(f'content:{r.content}')
    #return r.json() #vs content
    return r.content

 
#I started w/curl, was able to make a user and get a token
 #but it didn't work in swagger, so starte to write this
