#fillSearch.py is a simple templated fill of search results
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
        #if len(l)>0:
        #    return list(l)[0]
        #else:
        #    return l
    else:
        return l

def first_(l):
    from collections.abc import Iterable
    if isinstance(l,list):
        #return l[0]
        if len(l)>0:
            return list(l)[0]
        else:
            return l
    elif isinstance(l,Iterable):
        #return list(l)[0]
        if len(l)>0:
            return list(l)[0]
        else:
            return l
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

def cj2h_(j): #split this in parts
    "clowder(all)json ret to html"
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
        rb=f'<div class="rescontiner"><a href="{url}"><p>{des}</p><a href="{url2}">details</a><p></div></div>'
        rs=rh+rb
        print(rs) #for now

def cj1h(r):
    "clowder(1)json ret to html"
    name=r['name']
    des=r['description']
    url=first(getURLs(des))
    url2= clowder_host + '/datasets/' + r['id'] #use metadata-tab for 'details'
    rh=f'<div class="rescard"><div class="resheader"><a href="{url}">{name}</a></div>'
    rb=f'<div class="rescontiner"><a href="{url}"><p>{des}</p><a href="{url2}">details</a><p></div></div>'
    rs=rh+rb
    print(rs) #for now

def cj1hf(j):
    "wrap so filterable"
    print(f'<div class="item"><p class="tags">1993</p>')
    cj1h(j)
    print(f'</div>')

def cj2h(j):
    "clowder(all)json ret to html"
    for r in j:
        #cj1h(r)
        cj1hf(r)

#I could do a getjsonLD and turn that into a jsonLD playground viz-tab url
 #right now this file:fillSearch.py is called from sc2.py which has those functions
  #we are still getting the json back &now converting to html, so this is a  place we could call getjsonLD 
  #then how much do we do here vs sending the array of jsonLD on the page to be filtered there
  #I've seen some flask based faceted search so have hope that as much as possible can be done here

#if I ran carrot2 dcs clustering, could just add keyword like links to the clusters that each is in
 #could generate a page for each of these clusters, that is just a filtering of these returns w/in grp

#----this was 1st templating, but only using 'top' and 'bottom' below now
##some styling from: geodexui> view geodex/website/search.html
#    ...
#--above unused now

#could call this externally from one of the flask routes, via: python3 fillCSS.py querystr 
rj=cq(qry_str) #converted to html at very bottom now
##print(rj)
##ret = json.dumps(r.json()['results'], indent=2)
#print("<html>")
#print("<script>")
#print(json.dumps(rj, indent=2))   #this is where the jsonLD array could be put, but below now
#print("</script>")
#    #might need something around the table
##print("<body>")
#print(body)
#print(contain2s)
#cj2h(rj)
#print(contain2e)
#print("</body>")
#print("</html>")

#-now just simple top&bottom template, that has it's table filled by taking clowder search json returns and turnign to html
#  <title>GeoDex: JS-SPARQL search</title>
#now clowder backed, though sparql was what we had going in beginning and could still use
top = """
<!DOCTYPE html>
<html>

<head>
  <title>GeoCODES: resource search</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="shortcut icon" href="http://mbobak-ofc.ncsa.illinois.edu/img/earthcubeicon.png">

  <link rel="stylesheet" href="http://mbobak-ofc.ncsa.illinois.edu/css/reset.css">
  <link rel="stylesheet" href="http://mbobak-ofc.ncsa.illinois.edu/css/simple-grid.css">
  <link rel="stylesheet" href="http://mbobak-ofc.ncsa.illinois.edu/css/zc-grid.css">
  <link rel="stylesheet" href="http://mbobak-ofc.ncsa.illinois.edu/css/card.css">

    <style>
    .facetsearch {
        display: inline-block;
        width: 200px;
        vertical-align: top;
      }
      .activeorderby,
      .activefacet { color: red; }
       #showmorebutton {
        border: 1px solid #AAA;
        border-radius: 15px;
        background-color: #DDD;
        margin: 0 0 10px 0;
        padding: 10px;
        width: 100%;
        display: block;
        text-align: center;
        cursor: pointer;
      }
      </style>
</head>

<body>
  <div class="jumbotron" style="background-image: linear-gradient(#7391ff, #625354);">
    <div class="container">
      <div class="row">
        <div class="col-12 center">
          <a href=http://earthcube.org/><img src="http://mbobak-ofc.ncsa.illinois.edu/img/earthcubeicon.png"></a>
					<h3 style="margin:5px;color:white"><a href=https://geocodes.earthcube.org/>GeoCODES</a></h3>
          <h3 style="margin:5px;color:white" class="font-light">a schema.org/metadata backed Dataset/resource search</h3>
        </div>

      </div>
      <div class="row">
        <div class="col-12 center">
          <p>
            <a style="margin:5px;color:white "href="https://geocodes.earthcube.org/">home</a>
            <a style="margin:5px;color:white "href="http://mbobak-ofc.ncsa.illinois.edu/search.htm">search</a>
            <a style="margin:5px;color:white "href="http://mbobak-ofc.ncsa.illinois.edu/about.htm">about</a>
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
      <div slot="header"> Header Title </div>
      This card has a header. You can put all sorts of things in it!
    </sl-card> -->

    <form action="http://mbobak-ofc.ncsa.illinois.edu:5000/search" method="GET">
    <div style="padding:0px;top:0px" class="container">
      <div class="row">
        <div class="col-12 center">
          <img src="http://mbobak-ofc.ncsa.illinois.edu/img/search.svg" style="height:25px">
          <input style="font-size:120%" type="search" id="q" name="q" aria-label="Search for samples">
          <button style="color:black;border-color:black;border-style:solid" id="update">Search</button>
          <!--   <div class="img img-website-mock"></div>  -->
          <input id="nn" type="number" min="5" max="200" step="5" value="80" />
          <!-- <label> <input type="hidden" size="10" id="n"> </label>
            <label> <input type="hidden" size="10" value="0" id="s"> </label>
            <label> <input type="hidden" size="10" id="i"> </label> -->
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
  """

footer = """
  <footer style="padding-bottom:5px;background-image: linear-gradient(#7391ff, #625354);">
    <div class="container">
      <div class="row">
        <div class="col-12">
          <h6 style="color:grey">Work on this site is supported by NSF EarthCube</h6>
          <h6 style="color:grey">prototype <a href=https://github.com/MBcode/ec/tree/master/search>code available</a>,
            other search versions: 
            <a href=https://geocodes.earthcube.org/>geocodes</a>, 
            <a href=https://geocodes.earthcube.org/geocodes/textSearch.html>text</a>, 
            <a href=https://earthcube.clowderframework.org/>clowder</a>, 
            <a href=https://search.dataone.org/portals/earthcubedemo/Data >dataone</a>
          </h6>
        </div>
      </div>
    </div>
  </footer>
</body>
</html>
"""
#so can put script at very bottom for a bit
#getting bad mid-section and there was a possible div error that might have snuch in cj2h, so check

def getjsonLD(datasetID):
    "given clowder dataset id: return it's saved()jsonLD"
    r = requests.get(f'{clowder_host}/api/datasets/{datasetID}/metadata.jsonld')
    return  first_(r.json())

def cj2ld(j):
    "json ld /clowder dataset"
    #if(len(j)>1)
    LDl = []
    for r in j:
        dataset=r['id']
        LD=getjsonLD(dataset)
        #LDc=LD['content'] #unless need clowder-uri still for metadata
        LDl.append(LD)
        #print(json.dumps(LD, indent=2)) #this is where the jsonLD array could be put, but below now
    #need to put ',' between the elts; so could append to a list then dump that ;should have len =to #of search hits, not sure have that now
    print(json.dumps(LDl, indent=2)) 


# datePublished as a start
#check on start,and if div needed/ok
#might loose this style or mv ;also 1of:
      #'<h4><%= obj.description %></h4>'
      #'<h4><%= obj.@id %></h4>'
facetScripts0 = """
  <div id=wrapper>
    <div id=description> </div>
    <h4>Demo</h4>
      <div id=facets></div>
      """
#     <!--- <div id=results></div> --->
facetScripts_ = """
  </div>
    <script src="http://mbobak-ofc.ncsa.illinois.edu/js/jquery-1.6.2.js"></script>
    <script src="http://mbobak-ofc.ncsa.illinois.edu/js/underscore-1.1.7.js"></script>
    <script src="http://mbobak-ofc.ncsa.illinois.edu/js/facetedsearch.js"></script>
    """
facetScripts = """
  </div>
    <script src="http://mbobak-ofc.ncsa.illinois.edu/js/jquery-1.6.2.js"></script>
    <script src="http://mbobak-ofc.ncsa.illinois.edu/js/underscore-1.1.7.js"></script>
    <script src="http://mbobak-ofc.ncsa.illinois.edu/js/facetedsearch.js"></script>
  <script>
  $(function(){
      var item_template =
       '<div class="item">' +
       '<h4><%= obj.@id %></h4>'
       '<p class="tags">' +
       '<% if (obj.citation) {  %>, <%= obj.citation %><% } %>' +
       '</p>' +
       '<p class="desc"><%= obj.description %></p>' +
       '</div>';
       settings = {
       items            : example_items,
      facets           : { 'datePublished'     : 'Year published' },
      resultSelector   : '#results',
          facetSelector    : '#facets',
          resultTemplate   : item_template,
          paginationCount  : 50,
          }
          $.facetelize(settings);
      });
  </script>
"""
#do i need: orderByOptions facetSortOption
#then need script w/var example_items =

def cj2lds(j):
    "wrap LD array in case need w/script"
    print(facetScripts)
    print("<script>")
    #print("[")
    #print("var example_items = [") #put in list now already
    print("var example_items = ")
    cj2ld(j)
    #print("]")
    print("</script>")

#thought I wanted jsonLD array at top, but also want results out quickly
 #though filter-componets need to be there&will wait for this, maybe dump the main divs, then array then filter components

#print(top0)
#print("<script>")
##print(json.dumps(rj, indent=2))   #this is where the jsonLD array could be put, but below now
#cj2ld(rj)
#print("</script>")
#print(top1)

print(top)
#-
print(facetScripts0)
print(f'<div id=results>') #just this makes the reusults dissapear, I'd rather try a filter table w/o js
 #I could try to get rid of the js that is resetting it, but not the js that lets you filter live
cj2h(rj) #table filled by taking clowder search json returns and turnign to html
print(f'</div>')
print(facetScripts_)
#-
print(bottom)
#cj2lds(rj)  #right now just putting fake elts in results, &will try to not overwrite
print(footer)
