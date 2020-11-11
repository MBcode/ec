#testing re-skinning of clowder search results, so it can be placed in UX group's new CSS
 #in action probably have a flask route that calls it&along w/creating the html, 
 # might get some other metadata elts, that could be used for live filtering w/in the page
import requests
import json
import sys
import os
clowder_host = os.getenv('clowder_host')
if(len(sys.argv)>1):
    qry_str = sys.argv[1]
else:
    qry_str = "carbon"

#from assert code utils, now altered:
def first(l):
    from collections.abc import Iterable
    if isinstance(l,list):
        return l[0]
    elif isinstance(l,Iterable):
        return list(l)[0]
    else:
        return l

def httpP(str):
    #str.startswith('http')
    return str.startswith('http')

def getURLs(l):
    if isinstance(l,str):
        l=l.split()
    #filter(httpP,l)
    return filter(httpP,l)
#

def cq(qry_str):
    "clowder search query"
    r = requests.get(f"{clowder_host}/api/search?query={qry_str}")
    if(r.status_code == 200):
        #ret = json.dumps(r.json()['results'], indent=2)
        ret = r.json()['results']
        return ret
    else:
        return r.status_code

def cj2h(j):
    "clowder json ret to html"
    #if(len(j)>1)
    for r in j:
        name=r['name']
        des=r['description']
        #will want to get url
        #url=httpP(des) #bool, need actual url
        url=first(getURLs(des))
        url2= clowder_host + '/datasets/' + r['id'] #use metadata-tab for 'details'
        rh=f'<div class="rescard"><div class="resheader"><a href="{url}">{name}</a></div>'
        #rb=f'<div class="rescontiner"><a href="{url}><p>{des}</p></div>'
        #I do not see ec score from clowder  to put /\
        rb=f'<div class="rescontiner"><a href="{url}><p>{des}</p><a href={url2}>details</a><p></div>'
        rs=rh+rb
        print(rs) #for now

#I could do a getjsonLD and turn that into a jsonLD playground viz-tab url

#if I ran carrot2 dcs clustering, could just add keyword like links to the clusters that each is in
 #could generate a page for each of these clusters, that is just a filtering of these returns w/in grp

#some styling from: geodexui> view geodex/website/search.html
#contain = """ <div class="container"><vid class="row"><div class="col-12 center">  .."""
body = """<body> <div class="body-content" style="padding:0px">"""
search = """
   <div style="padding:0px;top:0px" class="container">
      <div class="row">
        <div class="col-12 center">
          <img src="../img/search.svg" style="height:25px">
          <input style="font-size:120%" type="search" id="q" name="q" aria-label="Search for samples">
          <button style="color:black;border-color:black;border-style:solid" id="update">Search</button>
          <!--   <div class="img img-website-mock"></div>  -->
          <input id="nn" type="number" min="5" max="200" step="5" value="20" />
  <div id="container1"></div>

        </div>
      </div>
    </div>
"""
contain2s = """
    <div style="padding:0px;top:0px" class="container">
      <div class="row">
        <div class="col-12">
          <div id="container2"></div>
           <div style="margin:30px">
           """
contain2e = """
           </div>
        </div>
      </div>
    </div> 
    """


#could call this externally from one of the flask routes, via: python3 fillCSS.py querystr 
rj=cq(qry_str)
#print(rj)
#ret = json.dumps(r.json()['results'], indent=2)
print("<html>")
print("<script>")
print(json.dumps(rj, indent=2))
print("</script>")
    #might need something around the table
#print("<body>")
print(body)
print(contain2s)
cj2h(rj)
print(contain2e)
print("</body>")
print("</html>")