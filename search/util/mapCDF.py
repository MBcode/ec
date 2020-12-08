#more py usable mapCDF
#should have first, then use that for the return of this
def assoc_v(key, d):
    if isinstance(d,dict):
        r= d.get(key)
        print(r) #dbg
        return r
#======mapping things, from data from CDF_Sites gSpreadsheet
 #could have loaded directly, but ok w/this snapshot, as shouldn't change
  #well if clowder db not backed up the all thos guid's go away
#=bu2r
bu2r_d ={ #"base_url to repo-name" 
    "https://portal.edirepository.org/nis/mapbrowse?scope=ecotrends&amp;identifier= https://portal.edirepository.org/nis/mapbrowse?packageid=": "edi",
    "http://www.bco-dmo.org/dataset": "bco-dmo",
    "https://www.hydroshare.org/resource": "hydroshare",
    "http://get.iedadata.org/doi": "iedadata",
    "https://portal.opentopography.org/lidarDataset?opentopoID=": "opentopography",
    "https://www.unavco.org/data/doi": "unavco",
    "https://ssdb.iodp.org/dataset": "ssdb.iodp",
    "http://balto.opendap.org/opendap/data": "balto",
    "http://wiki.linked.earth": "linked.earth",
    "http://ds.iris.edu/ds": "iris",
    "https://data.ucar.edu/dataset": "ucar",
    "http://opencoredata.org/id/dataset": "opencoredata",
    "ttps://earthref.org/MagIC ?_escaped_fragment_=": "magic",
    "http://data.neotomadb.org/datasets ?_escaped_fragment_=": "neotomadb",
    "http://datadiscoverystudio.org/geoportal/rest/metadata/item": "datadiscoverystudio",
    "http://earthcube.org/resource_registry": "resource_registry",
    "https://ecl.earthchem.org/view.php?id=": "earthchem",
    "https://xdomes.tamucc.edu/srr/sensorML": "xdomes",
    "https://data.neonscience.org/data-products": "neon"}

#could also have a assoc :test fnc that uses prefixp, who when given a full url
 #it returns the repo that has the base_url part
#start w/an exact match lookup, &can keep this name more obscure right now
def bu2r(bu):
  "base_url to repo dir-name"
  return assoc_v(bu, bu2r_d)
#-
#=would do url2r next using :test #'prefixp but it
#turns out that the base_url used for the crawl and the doi/desurl in t.qry might not
# always be the same
#-
#=s2r
#this is clowder specific mapping,  the other one can work from a url&get the repo/filname
 #so will be needed anyway, this just does clowder spaceID to the repo part, which can be used
 #as a check on the other
s2r_d ={ #"space to repo" 
    "5f7cb835e4b018b1752f2b8c": "edi",
    "5f7cb7c5e4b018b1752f2b78": "bco-dmo",
    "5f72574fe4b01e808c79c162": "hydroshare",
    "5f73a800e4b044a97a381ed9": "iedadata",
    "5f732bdbe4b01e808c8230f4": "opentopography",
    "5f7266e3e4b01e808c7a56c8": "unavco",
    "5f728495e4b01e808c7dc040": "ssdb.iodp",
    "5f7cb9d5e4b018b1752f2bf2": "balto",
    "5f7cba71e4b018b1752f2c07": "linked.earth",
    "5f734863e4b01e808c823533": "iris",
    "5f727055e4b01e808c7b0b01": "ucar",
    "5f72a8ace4b01e808c7f0dcd": "opencoredata",
    "5f72ae06e4b01e808c802269": "magic",
    "5f727997e4b01e808c7ca6c4": "neotomadb",
    "5f7f8bb2e4b0b812d24b0e53": "datadiscoverystudio",
    "5f87c52ee4b0a4d76fb2c3ce": "resource_registry",
    "5f89c5f8e4b0f4e0c0d9e773": "earthchem",
    "5fa30539e4b097cab4a00169": "xdomes",
    "5f9aefcee4b0511722cd7be7": "neon"} #s2r

#defun sID2repo (sID)
def s2r (sID):
  "clowder spaceID to the repo dirname"
  return assoc_v(sID, s2r_d)

#at minimum, when using clowder&not using the file-cache could still more easily look up the 
 #assoc logo's,  see repo2logo
#-
#=r2l
r2l_d = { #"reponame to logo" 
    "edi": "https://portal.edirepository.org/nis/images/EDI-logo-300DPI_5.png",
    "bco-dmo": "https://www.bco-dmo.org/sites/all/themes/bcodmo/logo.png",
    "hydroshare": "https://www.hydroshare.org/static/img/logo-lg.png",
    "iedadata": "https://www.iedadata.org/wp-content/themes/IEDA/assets/img/logo.png",
    "opentopography": "https://opentopography.org/sites/opentopography.org/files/ot_transp_logo_2.png",
    "unavco": "https://www.unavco.org/lib/images/banner/uv-logo.png",
    "ssdb.iodp": "http://ssdb.iodp.org/images/head_logo_PRO.gif",
    "balto": "http://balto.opendap.org/opendap/docs/images/logo.png",
    "linked.earth": "http://wiki.linked.earth/wiki/images/thumb/5/51/EarthLinked_Banner_blue_NoShadow.jpg/440px-EarthLinked_Banner_blue_NoShadow.jpg",
    "iris": "http://ds.iris.edu/static/img/layout/logos/iris_logo_shadow.png",
    "ucar": "https://opensky.ucar.edu/islandora/object/opensky%3Aucommunity/datastream/TN/view",
    "opencoredata": "https://opencoredata.org/img/logo22small.png",
    "magic": "http://mbobak-ofc.ncsa.illinois.edu/ext/ec/magic/MagIC.png",
    "neotomadb": "https://www.neotomadb.org/images/site_graphics/Packrat.png",
    "datadiscoverystudio": "http://datadiscoverystudio.org/geoportal/images/DataDiscoveryStudioBufferedWhite.png",
    "resource_registry": "https://www.earthcube.org/sites/default/files/doc-repository/logo_earthcube_full_horizontal.png",
    "earthchem": "http://www.earthchem.org/sites/default/files/files/EC_0-1.png",
    "xdomes": "https://xdomes.tamucc.edu/images/xdomes_logo.png",
    "neon": "https://www.neonscience.org/themes/custom/neon/logo.svg"}

def r2l(rn):
  "repo-name to logo-url"
  return assoc_v(rn, r2l_d)
#-
#since not sure I'll use this much, kick out quickly in lisp, &see how much use it gets 1st
 #it is easy enough to translate, in fact I could write a few lines to get the py dicts..
def s2l (sID):
  "spaceID to logo-url"
  r=s2r(sID)
  return r2l(r)

def ts(): # (&optional (sID "5f7cb835e4b018b1752f2b8c"))
    sID = "5f7cb835e4b018b1752f2b8c"
    t=s2l(sID)
    print(t) 
ts()
#"https://portal.edirepository.org/nis/images/EDI-logo-300DPI_5.png"
