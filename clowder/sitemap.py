#generate a sitemap for all the datasets, via the clowder api
import requests
import json
top= """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
   """ 

#do this w/in the loop, next
def put_txtfile(fn,s,wa="w"):
    #with open(fn, "w") as f:
    with open(fn, "a") as f:
        return f.write(s)

sm = "sitemap.xml"
url = "http://localhost:9000/api/datasets" #have as cli arg next
URLb = "http://localhost:9000/" #ame as url.remove("api/datasets")

r=requests.get(url)
#print(f'r={r}')
#print(f'txt={r.text}')
#print(f'url={r.url}')

#print(top)
put_txtfile(sm,top)

ja=json.loads(r.text)

for ds in ja:
    id=ds.get('id')
    if(id):
        #print(f'{URLb}{id}')
        #print(f'<url><loc>{URLb}{id}</loc></url>')
        put_txtfile(sm,f'<url><loc>{URLb}{id}</loc></url>')
