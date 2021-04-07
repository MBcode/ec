import os

def flatten_list(_2d_list):
    "https://stackabuse.com/python-how-to-flatten-list-of-lists/"
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list

#fl=flatten_list([[1, 2, 3, 4], [5, 6, 7], [8, 9, 10]])
#print(fl)
#[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

repos=["balto","bco-dmo","earthchem","edi","hydroshare","iedadata","iris","magic","neotomadb","opencoredata","opentopography","rr","ssdb.iodp","ucar","unavco"]

qryb=  'hydrologic|extremes'

def matchesInRepo(repo): 
    cs=f"ag -c '{qryb}' {repo}/*.jsonld"
    s=os.popen(cs).read()
    print(s)
    return s

def matches(): 
    lol=list(map(matchesInRepo,repos))
    arl=flatten_list(lol)
    ll=len(arl)
    print(arl)
    print(ll)

matches()

;still needed txt broken apart, and sorting that list by the #of matches
 ;since most likely throw away, faster2do list minip in lisp, so agr.cl
