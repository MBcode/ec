#cat fillCSS.py search.htm >fillSearch.py
#replaces fillCSS.py
#start w/run.sh runs sc2.py which calls this now, from a form submission from a search.htm like below

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
##print(rj)
##ret = json.dumps(r.json()['results'], indent=2)
#print("<html>")
#print("<script>")
#print(json.dumps(rj, indent=2))
#print("</script>")
#    #might need something around the table
##print("<body>")
#print(body)
#print(contain2s)
#cj2h(rj)
#print(contain2e)
#print("</body>")
#print("</html>")

top= """
<!DOCTYPE html>
<html>

<head>
  <title>GeoDex: JS-SPARQL search</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="shortcut icon" href="/img/earthcubeicon.png">

  <!---
  <script type="module" src="/js/geodex.js"></script>
  ---->

  <link rel="stylesheet" href="/css/reset.css">
  <link rel="stylesheet" href="/css/simple-grid.css">
  <link rel="stylesheet" href="/css/zc-grid.css">
  <link rel="stylesheet" href="/css/card.css">

</head>

<body>
  <div class="jumbotron" style="background-image: linear-gradient(#7391ff, #625354);">
    <div class="container">
      <div class="row">
        <div class="col-12 center">
          <img src="/img/earthcubeicon.png">
					<h3 style="margin:5px;color:white"><a href=https://geocodes.earthcube.org/>GeoCODES</a></h3>
          <h3 style="margin:5px;color:white" class="font-light">a schema.org/metadata backed Dataset/resource search</h3>
            <!-- 
          <div class="img img-logo center"></div>
          <h1>Simple Grid is a CSS grid for your website.</h1>
          <h2 class="font-light">Responsive, light, simple.</h2>
          <a href="simple-grid.zip" download>
            <button>Download</button>
          </a>
            -->
        </div>

      </div>
      <div class="row">
        <div class="col-12 center">
          <p>
            <a style="margin:5px;color:white "href="/index.html">home</a>
            <a style="margin:5px;color:white "href="/search.htm">search</a>
            <a style="margin:5px;color:white "href="/about.htm">about</a>
          </p>
        </div>
      </div>

      <div class="row">
        <div class="col-2 hidden-sm"></div>
      </div>
    </div>
  </div>


  <div class="body-content" style="padding:0px">

    <details>
      <summary>Search suggestions</summary>
      <p>
        Some search ideas for example resutls:
      <ul>
        <li>ross sea</li>
        <li>acidification</li>
        <li> CO2</li>
        <li> basalt</li>
        <li>IPCC models</li>
        <li>seismic</li>
        <li>sea ice</li>
      </ul>
      </p>
      <p>
        Note: fuzzy searching and stemming search is supported but I think my current search short circuits those.
      </p>
    </details>

    <!-- <sl-card class="card-header">
      <div slot="header">
        Header Title
      </div>
    
      This card has a header. You can put all sorts of things in it!
    </sl-card> -->

		<form action="http://mbobak-ofc.ncsa.illinois.edu:5000/search" method="GET">
    <div style="padding:0px;top:0px" class="container">
      <div class="row">
        <div class="col-12 center">
          <img src="/img/search.svg" style="height:25px">
          <input style="font-size:120%" type="search" id="q" name="q" aria-label="Search for samples">
          <button style="color:black;border-color:black;border-style:solid" id="update">Search</button>
          <!--   <div class="img img-website-mock"></div>  -->
          <input id="nn" type="number" min="5" max="200" step="5" value="80" />
          <!-- <label>
		<input type="hidden" size="10" id="n">
	</label>
	<label>
		<input type="hidden" size="10" value="0" id="s">
	</label>
	<label>
		<input type="hidden" size="10" id="i">
  </label> -->
  <div id="container1"></div>

        </div>
      </div>
    </div>
		</form>

    <div style="padding:0px;top:0px" class="container">
      <div class="row">
        <div class="col-12">
          <div id="container2"></div>
          """
bottom="""
        </div>
      </div>
    </div>

  </div>


  <footer style="padding-bottom:5px;background-image: linear-gradient(#7391ff, #625354);">
    <div class="container">
      <div class="row">
        <div class="col-12">
          <h6 style="color:white">Work on this site is supported by NSF EarthCube</h6>
          <h6 style="color:grey">Simple Grid by <a style="color:grey" href="http://zcole.me" target="_blank">Zach
              Cole</a>
            Open source under the <a style="color:grey" href="https://opensource.org/licenses/MIT" target="_blank">MIT
              License</a>
          </h6>
        </div>
      </div>
    </div>
  </footer>
</body>

</html>
"""
print(top)
cj2h(rj)
print(bottom)

