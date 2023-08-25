
head <- function(l, n=5) {
    return(l[1:n])
}

tail <- function(l, n=5) {
    return(l[(length(l)-n+1):length(l)])
}

is_str <- function(v) {
    return(class(v) == "character")
}

is_list <- function(v) {
    return(class(v) == "list")
}

is_tuple <- function(v) {
    return(class(v) == "list")
}


first <- function(l) {
    if (is.list(l)) {
        return(l[[1]])
    } else if (is.vector(l) || is.matrix(l)) {
        return(l[1])
    } else {
        return(l)
    }
}

flatten <- function(xss) {
    return(unlist(xss))
}

get_txtfile <- function(fn) {
    return(readLines(fn))
}


os_system <- function(cs) {
    # run w/o needing ret value
    system(cs)
    add2log(cs)
}

os_system_ <- function(cs) {
    # system call w/return value
    s <- system(cs, intern = TRUE)
    add2log(cs)
    return(s)
}

curl_url <- function(url) {
    cs <- paste0("curl ", url)
    return(os_system_(cs))
}

whoami <- function() {
    return(os_system_("whoami"))
}

urn_leaf <- function(s) {
    # last part of : sep string
    leaf <- ifelse(s == "", s, tail(strsplit(s, ":")[[1]], 1))
    return(leaf)
} 

path_leaf <- function(path) {
    # everything after the last /
    library(ntpath)
    split_path <- ntpath::ntpath.split(path)
    tail <- split_path[2]
    if (tail == "") {
        tail <- ntpath::ntpath.basename(split_path[1])
    }
    return(tail)
}

path_base_leaf <- function(path) {
    # like path_leaf but gives base 1st
    library(ntpath)
    split_path <- ntpath::ntpath.split(path)
    head <- split_path[1]
    tail <- split_path[2]
    if (tail == "") {
        tail <- ntpath::ntpath.basename(head)
    }
    return(list(head, tail))
}

replace_base <- function(path, mydict = base_url2repo, sep = ":") {
    # use URI to context:, eg. repo:leaf.rdf
    split_path <- path_base_leaf(path)
    base <- split_path[[1]]
    leaf <- split_path[[2]]
    new_base <- mydict[[base]]
    if (!is.null(new_base)) {
        return(paste0(new_base, sep, leaf))
    } else {
        return(path)
    }
}

file_ext <- function(fn) {
    # the ._part of the filename
    st <- base::file_ext(fn)
    add2log(paste0("fe:st=", st))
    return(st[length(st)])
}

file_base <- function(fn) {
    # the base part of base.txt
    st <- base::file_ext(fn)
    add2log(paste0("fb:st=", st))
    return(st[1])
}

file_leaf_base <- function(path) {
    # base of the leaf file
    pl <- path_leaf(path)
    return(file_base(pl))
}

collect_ext <- function(l, ext) {
  return(Filter(function(x) file_ext(x) == ext, unlist(l)))
}

collect_ext_ <- function(l, ext) {
  return(Filter(function(x) file_ext(x) == ext, l))
}

collect_pre <- function(l, pre) {
  return(Filter(function(x) startsWith(x, pre), unlist(l)))
}

collect_pre_ <- function(l, pre) {
  return(Filter(function(x) startsWith(x, pre), l))
}

collect_str <- function(l, s) {
  return(Filter(function(x) s %in% x, unlist(l)))
}

collect_str_ <- function(l, s) {
  return(Filter(function(x) s %in% x, l))
}

has_ext <- function(fn) {
  return(fn != file_base(fn))
}

wget <- function(fn) {
  cs <- paste0('wget --tries=2 -a log ', fn)
  os_system(cs)
  return(path_leaf(fn))
}

wget2 <- function(fn, fnl) {
  cs <- paste0('wget -O ', fnl, ' --tries=2 -a log ', fn)
  os_system(cs)
  return(get_txtfile(fnl))
}

mkdir <- function(dir) {
  cs <- paste0('mkdir ', dir)
  return(os_system(cs))
}

pre_rm <- function(url) {
  fnb <- path_leaf(url)
  cs <- paste0('rm ', fnb)
  os_system(cs)
  return(fnb)
}

get_ec <- function(url = "http://mbobak.ncsa.illinois.edu/ec/nb/ec.py") {
    pre_rm(url)
    system(paste("wget", url))
    return("import ec")
}

get_ec_txt <- function(url) {
    fnb <- pre_rm(url)
    system(paste("wget", url))
    return(get_txtfile(fnb))
}

jar <- Sys.getenv("jar")
if (is.null(jar)) {
    if (local) {
        jar <- "~/bin/jar"
    } else {
        jar <- "."
    }
}

blabel_l <- function(fn) {
    fb <- file_base(fn)
    ext <- file_ext(fn)
    cs <- paste("java -Xmx4155M -jar", jar, "/blabel.jar LabelRDFGraph -l -i", fn, "-o", paste(fb, "_l", ext, sep = ""))
    system(cs)
}

read_sd_ <- function(fn) {
    return(read.csv(fn, sep = " "))
}

read_sd <- function(fn) {
    fn_ <- gsub("urn:", "", fn)
    if (dbg) {
        print(paste("read_sd:", fn_))
    }
    tryCatch({
        df <- read.csv(fn, sep = "\n", header = FALSE, comment.char = "")
    }, error = function(e) {
        df <- as.character(e)
    })
    return(df)
}

read_json_ <- function(fn) {
    return(read_file(fn, ".json"))
}

```python
read_json <- function(urn) {
    url <- gsub("urn:", "", urn)
    res <- jsonlite::fromJSON(url)
    if (!is.null(res)) {
        return(res)
    } else {
        return(NULL)
    }
}

is_df <- function(df) {
    return(class(df) == "data.frame")
}

df_diff <- function(df1, df2) {
    if (!is_df(df1)) {
        print(paste("df_diff:1st arg:wrong type:", deparse(substitute(df1))))
        return(data.frame())
    }
    if (!is_df(df2)) {
        print(paste("df_diff:2nd arg:wrong type:", deparse(substitute(df2))))
        return(data.frame())
    }
    return(dplyr::anti_join(dplyr::bind_rows(df1, df2), df1))
}

diff_sd <- function(fn1, fn2) {
    df1 <- read_sd(fn1)
    df2 <- read_sd(fn2)
    dfdiff <- df_diff(df1, df2)
    if (nrow(dfdiff) == 0) {
        return(TRUE)
    } else {
        return(dfdiff)
    }
}

diff_flat_json <- function(fn1, fn2) {
    df1 <- read_json(fn1)
    df2 <- read_json(fn2)
    return(df_diff(df1, df2))
}

get_json_eq <- function(fn1, fn2) {
    print(paste("get_json_eq:", fn1, ",", fn2))
    d1 <- read_json(fn1)
    d2 <- read_json(fn2)
    if (is.null(d1)) {
        return(NULL)
    }
}




merge_dict_list <- function(d1, d2) {
  dd <- list()
  for (d in list(d1, d2)) {
    for (key in names(d)) {
      dd[[key]] <- c(dd[[key]], d[[key]])
    }
  }
  return(dd)
}

repos2counts <- function(repos) {
  repo_df_loc <- list()
  for (repo in repos) {
    repo_df_loc[[repo]] <- repo2site_loc_df(repo)
  }
  repo_counts <- list()
  for (repo in names(repo_df_loc)) {
    repo_counts[[repo]] <- length(repo_df_loc[[repo]])
  }
  repo_ld_counts <- list()
  repo_fnum <- wget2("http://mbobak.ncsa.illinois.edu/ec/test/repo_fnum.txt", "summoned.txt")
  repo_fnum_list <- strsplit(repo_fnum, "\n")[[1]]
  for (repo_num in repo_fnum_list) {
    repo_num_list <- strsplit(repo_num, " ")[[1]]
    if (length(repo_num_list) > 1) {
      repo_ <- repo_num_list[1]
      fnum <- repo_num_list[2]
      rl <- strsplit(repo_, "/")[[1]]
      if (length(rl) > 2) {
        rn <- rl[3]
        repo_ld_counts[[rn]] <- fnum
      }
    }
  }
  repoCounts <- wget2("http://mbobak.ncsa.illinois.edu/ec/test/graph_counts.txt", "graph.txt")
  final_counts <- list()
  rl2_list <- strsplit(repoCounts, "\n")[[1]]
  for (rl2 in rl2_list) {
    num_repo <- strsplit(rl2, " ")[[1]]
    if (length(num_repo) > 1) {
      count <- num_repo[1]
      repo <- gsub("milled:|summoned:", "", num_repo[2])
      final_counts[[repo]] <- count
    }
  }
  return(list(repo_counts, repo_ld_counts, final_counts, repo_df_loc))
}

post_untar <- function(url, uncompress = "tar -zxvf ") {
  fnb <- tools::file_path_sans_ext(basename(url))
  cs <- paste0(uncompress, " ", fnb)
  system(cs)
  return(fnb)
}

install_url <- function(url) {
  pre_rm(url)
  wget(url)
  fnb <- post_untar(url)
  return(gsub(".tar.gz|.zip", "", fnb))
}

install_java <- function() {
  ca <- "apt-get install -y openjdk-8-jdk-headless -qq > /dev/null"
  system(ca)
  Sys.setenv(JAVA_HOME = "/usr/lib/jvm/java-8-openjdk-amd64")
}

install_jena <- function(url = "https://dlcdn.apache.org/jena/binaries/apache-jena-4.5.0.tar.gz") {
  return(install_url(url))
}

install_fuseki <- function(url = "https://dlcdn.apache.org/jena/binaries/apache-jena-fuseki-4.5.0.tar.gz") {
  return(install_url(url))
}

install_any23 <- function(url = "https://dlcdn.apache.org/any23/2.7/apache-any23-cli-2.7.tar.gz") {
  return(install_url(url))
}

setup_blabel <- function(url = "http://mbobak.ncsa.illinois.edu/ld/bn/blabel.jar") {
  wget(url)
}

setup_j <- function(jf = NULL) {
  install_java()
  path <- Sys.getenv("PATH")
  jena_dir <- install_jena()
  any23_dir <- install_any23()
  if (!is.null(jf)) {
    fuseki_dir <- install_jena()
    addpath <- paste0(":", jena_dir, "/bin:", fuseki_dir, "/bin:", any23_dir, "/bin")
  } else {
    addpath <- paste0(":", jena_dir, "/bin:", any23_dir, "/bin")
  }
  Sys.setenv(PATH = paste0(path, addpath))
  setup_blabel()
  return(addpath)
}

get_relateddatafilename_txt <- function(url = "https://raw.githubusercontent.com/MBcode/ec/master/NoteBook/sparql_relateddatafilename.txt") {
  return(get_ec_txt(url))
}

get_webservice_txt <- function(url = "https://raw.githubusercontent.com/earthcube/facetsearch/master/client/src/sparql_blaze/sparql_gettools_webservice.txt") {
  return(get_ec_txt(url))
}

get_download_txt <- function(url = "https://raw.githubusercontent.com/earthcube/facetsearch/master/client/src/sparql_blaze/sparql_gettools_download.txt") {
  return(get_ec_txt(url))
}

get_notebook_txt <- function(url = "https://raw.githubusercontent.com/MBcode/ec/master/NoteBook/sparql_gettools_notebook.txt") {
  return(get_ec_txt(url))
}

get_query_txt <- function(url = "https://raw.githubusercontent.com/MBcode/ec/master/NoteBook/sparql-query.txt") {
  return(get_ec_txt(url))
}

get_subj2urn_txt <- function(url = "http://mbobak.ncsa.illinois.edu/ec/nb/sparql_subj2urn.txt") {
  # Add code here
}

get_graphs_txt <- function(url = "http://mbobak.ncsa.illinois.edu/ec/nb/sparql_graphs.txt") {
  return("SELECT distinct ?g  WHERE {GRAPH ?g {?s ?p ?o}}")
}

get_graphs_txt <- function(url = "http://mbobak.ncsa.illinois.edu/ec/nb/sparql_graphs.txt") {
  return("SELECT distinct ?g  WHERE {GRAPH ?g {?s ?p ?o}}")
}

get_graph_txt <- function(url = "http://mbobak.ncsa.illinois.edu/ec/nb/get_graph.txt") {
    return("SELECT distinct ?s ?p ?o  WHERE { graph ?g {?s ?p ?o} filter(?g = <${q}>)}")
}

get_summary_query_txt <- function(url = "http://mbobak.ncsa.illinois.edu/ec/nb/sparql_blaze.txt") {
    return()
}

get_summary_txt <- function(url = "https://raw.githubusercontent.com/earthcube/ec/master/summary/get_summary.txt") {
    "this is to make a summary, not to do a qry on the summary"
    return(get_ec_txt(url))
}

add_ext <- function(fn, ft) {
  if (is.null(ft) || ft == '' || ft == '.' || nchar(ft) < 2) {
    return(NULL)
  }
  fn1 <- path_leaf(fn)
  fext <- file_ext(fn1)
  r <- fn1
  if (is.null(fext) || fext == '') {
    fnt <- paste0(fn1, ft)
    cs <- paste0('sleep 2;mv ', fn1, ' ', fnt)
    system(cs)
    r <- fnt
  }
  return(r)
}

wget_ft <- function(fn, ft) {
  wget(fn)
  fnl <- fn
  if (ft != '.' && ft != '' && !is.null(ft) && nchar(ft) > 2) {
    fnl <- add_ext(fn, ft)
  }
  if (file.exists(fnl)) {
    fs <- file.size(fnl)
  } else {
    fs <- NULL
  }
  if (ft == '.zip') {
    cs <- paste0('unzip ', fnl)
    system(cs)
    fnb <- file_base(fnl)
  }
  return(fs)
}

init_rdflib <- function() {
  cs <- 'pip install rdflib networkx extruct python-magic pyld'
  system(cs)
  rdflib_inited <- cs
}

url2jsonLD <- function(url) {
  add2log(paste0('url2jsonLD(', url, ')'))
  if (is.null(rdflib_inited)) {
    init_rdflib()
  }
  library(extruct)
  library(requests)
  library(w3lib)
  r <- requests::get(url)
  base_url_ <- get_base_url(r$text, r$url)
  md <- extruct::extract(r$text, base_url = base_url_, syntaxes = c('json-ld'))
  if (!is.null(md)) {
    lda <- md[['json-ld']]
    ld <- lda[[1]]
  } else {
    ld <- ""
  }
  add2log(ld)
  return(ld)
}

url2jsonLD_fn <- function(url, fn) {
  ld <- url2jsonLD(url)
  LD <- jsonlite::toJSON(ld, pretty = TRUE)
  fnj <- paste0(fn, ".jsonld")
  return(put_txtfile(fnj, LD))
}

url2jsonLD_file <- function(url) {
  ld <- url2jsonLD(url)
  fnb <- file_leaf_base(url)
  LD <- jsonlite::toJSON(ld, pretty = TRUE)
  put_txtfile(fnb, LD)
  return(fnb)
}

fn2jsonld <- function(fn, base_url = NULL) {
  url <- fn
  md <- url2jsonLD(url)
  if (!is.null(md)) {
    ld <- md$json-ld
  } else {
    ld <- ""
  }
  cfn <- gsub("(\\n\\s*)+\\n+", "\\n", fn)
  fn <- paste0(cfn, ".jsonld")
  if (ld != "") {
    write(jsonlite::toJSON(ld[1], pretty = TRUE), file = fn)
  }
  return(ld)
}

getjsonLD <- function(url) {
  ld <- url2jsonLD(url)
  fnb <- file_leaf_base(url)
  cfn <- gsub("(\\n\\s*)+\\n+", "\\n", fnb)
  fnj <- paste0(cfn, ".jsonld")
  add2log(paste0("getjsonLD:", fnb, ",", fnj))
  LD <- jsonlite::toJSON(ld, pretty = TRUE)
  put_txtfile(fnj, LD)
  return(fnj)
}

xml2nt <- function(fn, frmt = "xml") {
  if (is.null(rdflib_inited)) {
    init_rdflib()
  }
  fnb <- file_base(fn)
  g <- rdflib::Graph()
  g$parse(fn, format = frmt)
  s <- g$serialize(format = "ntriples")
  fnt <- paste0(fnb, ".nt")
  put_txtfile(fnt, s)
  return(fnt)
}

to_nt_str <- function(fn,frmt="json-ld"){
  "turn .xml(rdf) to .nt"
  fnb <- file_base(fn)
  library(rdflib)
  g <- Graph()
  g <- parse(fn, format=frmt) #allow for other formats
  s <- serialize(g, format="ntriples")
  return(s)
}

jsonld2nt <- function(fn,frmt="json-ld"){
  "turn .jsonld to .nt"
  add2log(paste0('jsonld2nt:',fn,',',frmt))
  return(to_nt_str(fn,frmt))
}

url2nt <- function(url){
  "get .jsonLD file,&create a .nt version"
  fnj <- getjsonLD(url)
  fnt <- jsonld2nt(fnj)
  add2log(paste0('url2nt,',fnj,',',fnt))
  return(fnt)
}


append2everyline <- function(fn, aptxt, fn2 = NULL){
  lines <- readLines(fn)
  if(is.null(fn2)){
    fn2 <- gsub(".nt", ".nq", fn) #main use for triples to quads
  }
  writeLines(paste0(lines, " ", aptxt), fn2)
  return(fn2)
}

url2nq <- function(url){
  "crawl url ret .jsonld .nt .nq"
  fn <- url2nt(url)
  apptxt <- paste0("<", url, "> .")
  return(append2everyline(fn, apptxt))
}

ls_ <- function(path){
  lstr <- system(paste0("ls ", path), intern = TRUE)
  return(strsplit(lstr, "\n")[[1]])
}

nt2nq <- function(fn, dir = ""){
  base_url <- Sys.getenv("BASE_URL")
  if(is.null(base_url)){
    print("for now, need to: setenv BASE_URL ...")
  }
  fnb <- basename(fn)
  url <- paste0(base_url, gsub(dir, "", fnb), "/")
  aptxt <- paste0("<", url, "> .")
  return(append2everyline(fn, aptxt))
}

all_nt2nq <- function(dir){
  ntfiles <- list.files(path = dir, pattern = "*.nt", full.names = TRUE)
  for(fn in ntfiles){
    print(nt2nq(fn))
  }
}

rdflib_viz <- function(url, ft = NULL){
  if(is.null(rdflib_inited)){
    init_rdflib()
  }
  library(rdflib)
  library(networkx)
  library(matplotlib)
  
  g <- rdflib::rdflib_graph()
  if(!is.null(ft)){
    result <- g$parse(url)
  } else {
    result <- g$parse(url, format = ft)
  }
  G <- rdflib::rdflib_to_networkx_multidigraph(result)
  matplotlib::plt.figure(3, figsize = c(18, 18))
  pos <- networkx::spring_layout(G, scale = 2)
  edge_labels <- networkx::get_edge_attributes(G, 'r')
  networkx::draw_networkx_edge_labels(G, pos, edge_labels = edge_labels)
  networkx::draw(G, with_labels = TRUE)
  matplotlib::plt.show()
}

read_rdf <- function(fn, ext = ".tsv"){
  return read_file(fn, ext)
}

urn2uri <- function(urn){
  if(is.null(urn)){
    return(paste0("no-urn:", urn))
  } else if(grepl("urn:", urn)){
    url <- gsub(":", "/", urn)
    url <- gsub("urn", "http://141.142.218.86", url, fixed = TRUE)
    url <- paste0(url, ".rdf")
    return(url)
  }
}

get_gID <- function(){
  subj <- paste0("gID:", gsub(".", "", gName))
  return(subj)
}

urn2urls <- function(urn){ #from wget_rdf, replace w/this call soon
  "way we map URNs ~now" #check on this w/the URN changes 
  if (is.null(urn)){
    return(paste0("no-urn:", urn))
  } else if (is_http(urn)){
    urlj <- gsub(".nt", ".jsonld", url)
    return(c(urn, urlj))
  } else if (startsWith(urn, "urn:")){
    #global f_nt
    #url <- gsub(":", "/", urn, fixed = TRUE)
    #url <- gsub("urn", "https://oss.geodex.org", url, fixed = TRUE, ignore.case = TRUE) #minio
    url <- gsub(":", "/", urn, fixed = TRUE)
    url <- gsub("urn", minio, url, fixed = TRUE, ignore.case = TRUE) #minio
    urlj <- paste0(url, ".jsonld") #get this as well so can get_jsfile2dict the file
    url <- paste0(url, ".rdf")
    #cs <- paste0("wget -a log ", url)
    #os_system(cs)
    #cs <- paste0("wget -a log ", urlj)
    #os_system(cs)
    #return(c(url, urlroot, urlj))
    return(c(url, urlj))
  }
}

urn2fnt <- function(urn){
  "urn to end of rdf url as name for .nt file"
  rdf_urls <- urn2urls(urn)
  fnt <- paste0(file_base(path_leaf(rdf_urls[1])), ".nt")
  return(fnt)
}


rdf2nt <- function(urlroot_){
  #DFs rdf is really .nt, also regularize2dcat
  urlroot <- gsub(".rdf","",urlroot_) #to be sure
  fn1 <- paste0(urlroot,".rdf")
  fn2 <- paste0(urlroot,".nt") #more specificially, what is really in it
  print(paste0("rdf2nt,fn1:",fn1))
  cs <- paste0("cat ",fn1,"|sed \"/> /s//>\t/g\"|sed \"/ </s//\t</g\"|sed \"/doi:/s//DOI:/g\"|cat>",fn2)
  system(cs)   #fix .nt so .dot is better ;eg. w/doi
  f_nt <- fn2
  return(fn2)
}

is_node <- function(url){ #not yet
  return(startsWith(url,"<ht") | startsWith(url,"_:B"))
}

tn2bn <- function(url){
  #make blaze BNs proper for .nt
  if(startsWith(url,"t1")){
    return(gsub("t1","_:Bt1",url))
  } else {
    return(url)
  }
}

cap_http <- function(url){
  #"<url>"
  if(is_http(url)){
    return(paste0("<",url,">"))
  } else {
    return(url)
  }
}

cap_doi <- function(url){
  #"<doi>"
  #if url.lower().startswith("doi:"):
  if(startsWith(url,"doi:")){
    return(paste0("<",url,">"))
  } else if(startsWith(url,"DOI:")){
    return(paste0("<",url,">"))
  } else {
    return(url)
  }
}

fix_url3 <- function(url){
  "cap http/doi tn2bn"
  url <- tn2bn(url)
  url <- cap_http(url)
  url <- cap_doi(url)
  return(url)
}

fix_url <- function(url){
  "fix_url and quote otherwise"
  if(is_node(url)){
    return(url)
  } else if(startsWith(url, "t1")){
    return(gsub("t1", "_:Bt1", url))
  } else if(is_http(url)){
    return(paste0("<", url, ">"))
  } else if(startsWith(url, "doi:")){
    return(paste0("<", url, ">"))
  } else if(startsWith(url, "DOI:")){
    return(paste0("<", url, ">"))
  } else {
    return(toJSON(url))
  }
}

get_rdf <- function(urn, viz = NULL){
  #get graph
  df <- get_graph(urn)
  dfo <- df2nt(df)
  if(!is.null(viz)){
    fn2 <- urn_leaf(urn) + ".nt" #try tail
    rdflib_viz(fn2) #find out if can viz later as well via hidden .nt file
  }
  return(list(df, dfo))
}

df2nt <- function(df_, fn = NULL){
  #print out df as .nt file
  nt_str <- ""
  if(!is.null(fn)){
    put_txtfile(fn, "")
  }
  if(dbg){
    print(paste0("df2nt:", df))
  }
  for(index in 1:nrow(df)){
    s <- df$s[index]
    s <- fix_url(s)
    p <- df$p[index]
    p <- fix_url(p)
    o <- df$o[index]
    o <- fix_url(o)
    if(o == "NaN"){
      o <- ""
    }
    str3 <- paste0(s, " ", p, " ", o, " .")
    if(dbg){
      print(str3)
    }
    nt_str <- paste0(nt_str, str3)
    if(!is.null(fn)){
      put_txtfile(fn, str3, "a")
    }
  }
  return(list(df, nt_str))
}

get_rdf2nt_str <- function(urn){
  #get graph
  "get_graph as nt string" #that doesn't need the ld cache
  df <- get_graph(urn)
  dfo,nt_str <- df2nt(df)
  return (nt_str) #use for get_rdf2jld _str
}

get_rdf2jld_str <- function(urn){
  #get jsonld from endpoint
  "get jsonld from endpoint" #for get_graph_jld route
  nt_str <- get_rdf2nt_str(urn) #only strings no files
  g <- nt_str2g(nt_str) #like nt2g
  jld_str <- g$serialize(format="json-ld") #from nt2jld #shouldn't need rdflib-jsonld
  return (compact_jld_str(jld_str))
}

compact_jld_str <- function(jld_str){
  library(jsonld)
  library(jsonlite)
  context <- '{"@vocab": "https://schema.org/"}'
  doc <- fromJSON(jld_str)
  compacted <- jsonld::compact(doc, context)
  r <- toJSON(compacted, indent=2)
  return (r)
}

get_rdf2nt <- function(urn){
  #get and rdf2nt
  "get and rdf2nt" #rdf2nt was getting around df's naming, will be glad to get away from that cache
  df <- get_rdf(urn)
  fn2 <- urn_leaf(urn) # + ".nt"
  #append2allnt(fn2) #file not made yet, done during ec.viz() call
  if (!is_str(fn2)){
    print(paste0('get_rdf2nt,warning,fn2:',fn2,', make sure to run the Parameters cell to get the urn'))
    fn2 <- ""
  }
  fn2 <- paste0(fn2, ".nt")
  #global f_nt #finish
  # f_nt = fn2
  # return df2nt(df,fn2) #seems to work w/a test urn

nt2jld <- function(fn){
  #load .nt and convert2 jsonld
  g <- nt2g(fn)
  s <- serialize(g, format="json-ld")
  fnb <- file_base(fn)
  fnt <- paste0(fnb, ".jsonld")
  put_txtfile(fnt,s)
  return(fnt)
}

nt2ttl <- function(fn){
  #load .nt and convert2 .ttl
  g <- nt2g(fn)
  s <- serialize(g, format="ttl")
  fnb <- file_base(fn)
  fnt <- paste0(fnb, ".ttl")
  put_txtfile(fnt,s)
  return(fnt)
}

get_rdf2jld <- function(urn){
  #get_graph 2 nt then 2 jsonld
  df <- get_rdf2nt(urn)
  #fn2 <- urn_leaf(urn) # + ".nt" 
  fn2 <- paste0(urn_leaf(urn), ".nt")
  return(nt2jld(fn2))
}

get_rdf2ttl <- function(urn){
  #get_graph 2 nt then 2 ttl
  df <- get_rdf2nt(urn)
  #fn2 <- urn_leaf(urn) # + ".nt" 
  fn2 <- paste0(urn_leaf(urn), ".nt")
  return(nt2ttl(fn2))
}

wget_rdf_ <- function(urn, viz=NULL){
  #new version to get_rdf from the endpoint
  if(is.null(viz)){
    #if(sparql_inited == NULL){
    if(!sparql_inited){
      init_sparql()
    }
    print(paste0("get_rdf2nt(", urn, ")"))
    return(get_rdf2nt(urn)) #use get_graph version for now
  } else {
    return(wget_rdf_(urn,viz)

iwget_rdf <- function(urn, viz = NULL){
  # old version, still wget's from the urn
  if(is.null(viz)){
    if(!sparql_inited){
      init_sparql()
    }
  }
  if(is.null(urn)){
    return(paste0("no-urn:", urn))
  } else if(is_http(urn)){
    cs <- paste0("wget -a log ", urn)
    os_system(cs)
    urlroot <- path_leaf(urn) # file w/o path
    rdf2nt(urlroot)
    return(read_rdf(urn))
  } else if(startsWith(urn, "urn:")){
    url <- urn2urls(urn)$url
    urlj <- urn2urls(urn)$urlj
    urlroot <- path_leaf(url) # file w/o path
    cs <- paste0("wget -a log ", url)
    os_system(cs)
    cs <- paste0("wget -a log ", urlj)
    os_system(cs)
    #if viz: #finish
    rdf2nt(urlroot)
    #      return read_rdf(f_nt)
    #else:
    #    return f'bad-urn:{urn}'

  }
}

d_fn <- function(fn){
  "FileName or int:for:d#.nt"
  if(is.integer(fn)){
    fnt <- paste0("d", fn, ".nt")
  } else {
    fnt <- fn
  }
  return(fnt)
}

sq_file <- function(sq, fn = 1){
  fnt <- d_fn(fn) #maybe gen fn from int
  add2log(paste0("dataFN=", fnt))
  add2log(paste0("qry=", sq))
  if(sparql_inited == NULL){
    si <- init_sparql()  #still need to init
  }
  #global default_world
  #from owlready2 import *
  library(owlready2)
  #o= o2.get_ontology("d1.nt").load()
  o <- o2.get_ontology(fnt).load()
  return(list(o2.default_world.sparql(sq)))
}

pp_l2s <- function(pp, js = NULL){
  "predicatePath list2str"
  if(js){ #["spatialCoverage" "geo" "box" ], True  -> "spatialCoverage.geo.box"
    return(paste0(".", paste(pp, collapse = ".")))
  } else { #["spatialCoverage" "geo" "box" ]  -> ":spatialCoverage/:geo/:box"
    return(paste0(":", paste(pp, collapse = "/:")))
  }
}

rget <- function(pp, fn = 1){
  # predicate path to s/o values
  fnt <- dfn(fn)
  s1 <- "PREFIX : <https://schema.org/> SELECT distinct ?s ?o WHERE  { ?s " #till fix sed
  s2 <- " ?o}"
  pps <- pp_l2s(pp)
  qs <- paste0(s1, pps, s2)
  print(qs)
  #add2log(f'rget:{qs}')
  add2log(paste0("rget:", qs, ",", fnt))
  r <- sq_file(qs, fnt)
  return(r)
}

grep_po_ <- function(p, fn){
  # find predicate in nt file and returns the objects
  #cs= f"grep '{p}' {fn}|cut -f 3"
  cs <- paste0("grep '", p, "' ", fn, "|cut -d' ' -f 3")
  rs <- os_system_(cs)
  #ra=rs.split(" .\n")
  ra <- strsplit(rs, "\n")[[1]]
  ra <- trimws(ra, "both", ".")[-length(ra)]
  return(ra)
}

grep_po <- function(p,fn){
  #find predicate in nt file and returns the objects
  cs <- paste0("egrep '",p,"' ",fn,"|cut -f 3")
  #cs= f"grep '{p}' {fn}|cut -d' ' -f 3"
  rs <- os_system_(cs)
  ra <- strsplit(rs, " .\n")
  return(ra)
  #could ret the Predicate,Object,(lists)and pred(s) could be the 2nd return
  #unless where to call it grep_p2o or grep_pred2obj
  #def grep_pred2obj(p,fn):
}

grep2obj <- function(p,fn){ #=f_nt){ #fn could default to (global) f_nt
  #find pattern in nt file and returns the objects, of the spo lines
  cs <- paste0("egrep '",p,"' ",fn,"|cut -f 3")
  rs <- os_system_(cs)
  #ra=rs.split(" .\n")
  ra <- strsplit(rs, ".\n")
  if(length(ra) > 0){
    ra <- lapply(ra, function(x) gsub("\"","",str_trim(x)))
  }
  return(ra)
  #get pack to using a local store, to be more robust
  #def urn2accessURL(urn):
}

urn2accessURL <- function(urn,fnt=NULL){
    #get access/content url from urn/it's .nt file
    if(is.null(fnt)){
        fnt <- urn2fnt(urn) #should be same as f_nt
    }
    print(paste0("grep2obj:",fnt))
    return(grep2obj('accessURL|contentUrl',fnt))
}

getDatasetURLs <- function(IDs, dfS = NULL){
  #return the URLs from every dataset given, by URNs or df w/rows
  d1p <- !is.numeric(IDs[1])
  ds_urls <- if(d1p) {
    lapply(IDs, urn2accessURL)
  } else {
    lapply(IDs, function(row) dfRow2urls(dfS, row))
  }
  #ds_url <- if(d1p) {
  #  lapply(ds_urls, function(urls) urls[1])
  #} else {
  #  lapply(ds_urls, function(urls) urls[row][1])
  #}
  ds_url <- lapply(ds_urls, function(urls) urls[1]) #default to 1st of the urls ;need to check in 2nd/sparql_nb w/o collection
  return(list(ds_urls, ds_url)) #1st of each right now
}

sparql_f2 <- function(fq, fn, r = NULL){ #jena needs2be installed for this, so not in NB yet;can emulate though
  #files: qry,data
  if(!is.null(r)){ #--results= Results format (Result set: text, XML, JSON, CSV, TSV; Graph: RDF serialization)
    rs <- paste0(" --results=", r, " ")
  } else {
    rs <- ""
  }
  fnt <- dfn(fn) #maybe gen fn from int
  #if had txt put_txtfile; if qry.txt w/var then have2replace
  cs <- paste0("sparql --data=", fnt, " --query=", fq, rs)
  return(os_system_(cs))
}

#nt2dn <- function(fn = f_nt, n = 1){
#  #.nt to d#.nt where n=#, w/http/s schema.org all as dcat
#  fdn

nt2g <- function(fnt){
  library(rdflib)
  g <- ConjunctiveGraph(identifier = fnt)
  data <- readBin(fnt, "raw", n = file.info(fnt)$size)
  g <- parse(g, data, format = "ntriples")
  return(g)
}

nt_str2g <- function(nt_str){
  library(rdflib)
  g <- Graph()
  g <- parse(g, data = nt_str, format = "ntriples")
  return(g)
}

diff_nt_g <- function(fn1, fn2){
  library(rdflib)
  g1 <- nt2g(fn1)
  g2 <- nt2g(fn2)
  iso1 <- to_isomorphic(g1)
  iso2 <- to_isomorphic(g2)
  if (iso1 == iso2){
    return(list(g1, NULL, NULL))
  } else {
    in_both <- graph_diff(iso1, iso2)[[1]]
    in_first <- graph_diff(iso1, iso2)[[2]]
    in_second <- graph_diff(iso1, iso2)[[3]]
    return(list(in_both, in_first, in_second))
  }
}

dump_nt_sorted <- function(g){
  for (l in sort(serialize(g, format = "nt") %>% strsplit("\n")[[1]])){
    if (l != ""){
      print(l)
    }
  }
}

diff_nt <- function(fn1, fn2){
  in_both, in_first, in_second <- diff_nt_g(fn1, fn2)
  if (length(in_both) > 0){
    print(paste("in_both:", in_both))
    dump_nt_sorted(in_both)
  }
  if (length(in_first) > 0){
    print(paste("in_first:", in_first))
    dump_nt_sorted(in_first)
  }
  if (length(in_second) > 0){
    print(paste("in_second:", in_second))
    dump_nt_sorted(in_second)
  }
  return(list(in_both, in_first, in_second))
}

pp2so <- function(pp, fn){
  fnt <- dfn(fn)
  sqpp <- "PREFIX : <http://www.w3.org/ns/dcat#>
        SELECT distinct ?s ?o
        WHERE { ?s predicate-path ?o }"
  sq <- gsub("predicate-path", pp, sqpp)
  add2log(paste("fn=", fn, "sq=", sq))
  if (is.null(rdf_inited)){
    init_rdf()
  }
  library(rdflib)
  g <- ConjunctiveGraph(identifier = fnt)
  data <- open(fnt, "rb")
  g <- parse(data, format = "ntriples")
  results <- query(g, sq)
  add2log(results)
  return(str(result[1]) for result in results)
}

rdfxml2nt <- function(fnb){
  if (has_ext(fnb)){
    fnb <- file_base(fnb)
  }
  if (rdf_inited == NULL){
    init_rdf()
  }
  cs <- paste0("rapper -i rdfxml -o ntriples ", fnb, ".nt|cat>", fnb, ".nt")
  os_system(cs)
}

nt2svg <- function(fnb){
  if (has_ext(fnb)){
    fnb <- file_base(fnb)
  }
  if (rdf_inited == NULL){
    init_rdf()
  }
  cs <- paste0("rapper -i ntriples -o dot ", fnb, ".nt|cat>", fnb, ".dot")
  os_system(cs)
  cs <- paste0("dot -Tsvg ", fnb, ".dot |cat> ", fnb, ".svg")
  os_system(cs)
}

display_svg <- function(fn){
  if (rdf_inited == NULL){
    init_rdf()
  }
  library(IPython)
  display(SVG(fn))
}

append2allnt <- function(fnb = NULL){
  "append to default viz file"
  if (has_ext(fnb)){ #bc not switching .ext could just give full name
    fnb <- file_base(fnb)
  }
  if (!fnb){
    global f_nt #the current .nt file being looked at
    fnb <- file_base(f_nt)
  }
  if (dbg){
    print(paste0("append2allnt,fnb:", fnb))
  }
  cs <- paste0("cat ", fnb, ".nt >> .all.nt")
  os_system(cs)
}

nt_viz <- function(fnb = ".all.nt"){
  if(fnb == ".all.nt" && !is.null(f_nt) && file.exists(f_nt)){
    fnb <- f_nt #if have urn .nt file, &nothing run yet, can call w/o arg&will view it
  }
  if(has_ext(fnb)){
    fnb <- file_base(fnb)
  }
  nt2svg(fnb) #base(before ext)of .nt file, makes .svg version&displays
  fns <- paste0(fnb, ".svg")
  display_svg(fns)
  if(fnb != ".all"){
    append2allnt(fnb)
  }
}

rdfxml_viz <- function(fnb){ #cp&paste (rdf)xml file paths from in .zip files
  xml2nt(fnb)
  nt_viz(fnb)
}

viz <- function(fn = ".all.nt"){ #might call this rdf_viz once we get some other type of viz going
  if(has_ext(fn)){
    ext <- file_ext(fn)
    fnb <- file_base(fn) #unused, bc they should strip the ext anyway
  } else {
    return("need a file extension, to know which routines to run to show it")
  }
  if(ext == ".nt"){
    nt_viz(fn)
  } else if(ext == '.xml'){
    rdfxml_viz(fn)
  } else {
    return("only handle .nt and .xml (rdf) right now")
  }
}

alive <- function(){
  library(requests)
  r <- requests::get(paste0(host, "/alive"))
  return(r)
}

log_msg <- function(url){
  get <- paste0(host, "/logbad/?url=", url)
  add2log(get)
  return("")
}

check_size <- function(fs, df){
  dfe <- NULL
  if(fs){
    if(fs < 300){
      dfe <- "[Warn:small]"
    }
  } else {
    dfe <- "[Warn:No File]"
  }
  if(!is.null(dfe)){
    add2log(dfe)
    log_msg(dfe)
    df <- paste0(df, dfe)
  }
  return(df)
}

nt2ft <- function(url){
  cs <- paste0("grep -A4 ", url, " *.nt|grep encoding|cut -d' ' -f3")
  if(cs){
    return(os_system_(cs))
  } else {
    return(NULL)
  }
}

file_type <- function(fn){
  if(file.exists(fn)){
    if(file.info(fn)$isdir){
      mt <- "is a dir"
    } else if(file.info(fn)$isfile){
      add2log(magic.from.file(fn))
      mt <- magic.from.file(fn, mime = TRUE)
    } else {
      mt <- "exists, but not file or dir"
    }
  } else {
    mt <- "file not found"
  }
  add2log(paste0(fn, ",mime:", mt))
  return(mt)
}

read_file <- function(fnp, ext=NULL){
  #download url and ext/filetype
  "can be a url, will call pd read_.. for the ext type"
  if(is.null(rdf_inited)){ #new, going to need it
    init_rdflib()
    init_rdf()
  }
  if(is.null(ext)){ #find filetype from .nt ecodingFormat
    ext <- nt2ft(fnp)
  }
  fn <- rstrip(fnp, "/") #only on right side, for trailing slash, not start of full pasted path
  fn1 <- path_leaf(fn) #just the file, not it's path
  fext <- file_ext(fn1) #&just it's .ext
  #url = fn
  if(!is.null(ext)){
    if(startsWith(ext, ".")){
      ft <- ext
    } else {
      ft <- paste0(".", ext)
    }
  } else { #use ext from fn
    ft <- as.character(fext)
    ext <- ft
  }
  df <- ""
  #bad_lines going away, get netcdf etc in here, even though I don't see it much
  if(is.null(ext) && nchar(ft) < 1){
    wget(fn)
    df <- "no fileType info, doing:[!wget $url ],to see:[ !ls -l ] or FileExplorerPane on the left"
  } else if(ft == ".tsv" || grepl("tsv", ext, ignore.case = TRUE) || grepl("tab-sep", ext, ignore.case = TRUE)){
    tryCatch({
      #df=pd.read_csv(fn, sep='\t',comment='#',warn_bad_lines=True, error_bad_lines=False)
      #df=pd.read_csv(fn, sep='\t',comment='#',warn_bad_lines=True, on_bad_lines='skip')
      df <- read.csv(fn

read_file <- function(fnp, ext=NULL){
  #download url and ext/filetype
  "can be a url, will call pd read_.. for the ext type"
  if(is.null(rdf_inited)){ #new, going to need it
    init_rdflib()
    init_rdf()
  }
  if(is.null(ext)){ #find filetype from .nt ecodingFormat
    ext <- nt2ft(fnp)
  }
  fn <- str_trim(fnp, side = "right", "/") #only on right side, for trailing slash, not start of full pasted path
  fn1 <- basename(fn) #just the file, not it's path
  fext <- file_ext(fn1) #&just it's .ext
  if(!is.null(ext)){
    if(startsWith(ext, ".")){
      ft <- ext
    } else {
      ft <- paste0(".", ext)
    }
  } else { #use ext from fn
    ft <- as.character(fext)
    ext <- ft
  }
  df <- ""
  if(is.null(ext) && nchar(ft) < 1){
    wget(fn)
    df <- "no fileType info, doing:[!wget $url ],to see:[ !ls -l ] or FileExplorerPane on the left"
  } else if(ft == ".tsv" || grepl("tsv", ext, ignore.case = TRUE) || grepl("tab-sep", ext, ignore.case = TRUE)){
    tryCatch({
      df <- read.csv(fn, sep = "\t", comment = "#", on_bad_lines = "skip")
    }, error = function(e){
      df <- e
    })
  } else if(ft == ".csv" || grepl("csv", ext, ignore.case = TRUE)){
    tryCatch({
      df <- read.csv(fn, comment = "#", on_bad_lines = "skip")
    }, error = function(e){
      df <- e
    })
  } else if(ft == ".txt"){
    tryCatch({
      df <- read.csv(fn, sep = "\n", comment = "#")
    }, error = function(e){
      df <- e
    })
  } else if(ft == ".json" || grepl("js", ext, ignore.case = TRUE)){
    tryCatch({
      print(paste0("read_json(", nf, ")"))
      df <- read.json(fn)
    }, error = function(e){
      df <- e
    })
  } else if(ft == ".html" || grepl("htm", ext, ignore.case = TRUE)){
    tryCatch({
      df <- read.html(fn)
    }, error = function(e){
      df <- e
    })
  } else if(ft == ".zip" || grepl("zip", ext, ignore.case = TRUE)){
    ft <- ".zip"
    fs <- wget_ft(fn, ft)
    df <- paste0("can not read zip w/o knowing what is in it, doing:[!wget $url ],to see:[ !ls -l ]size:", fs, " or FileExplorerPane on the left")
    file_type(fn1)
    df <- check_size(fs, df)
  } else {
    fs <- wget_ft(fn, ft)
    df <- paste0("no reader, doing:[!wget $url ],to see:[ !ls -l ]size:", fs, " or FileExplorerPane on the left")
    file_type(fn1)
    df <- check_size(fs, df)
  }
  return(df)
}


get_sources_csv <- function(url="https://raw.githubusercontent.com/MBcode/ec/master/crawl/sources.csv"){
  return(get_ec_txt(url))
}

get_sources_df <- function(url="https://raw.githubusercontent.com/MBcode/ec/master/crawl/sources.csv"){
  s <- read_file(url,".csv")
  return(s[s$Active,]) #can only crawl the active ones
}

crawl_sources_urls <- function(){ #work on sitemap lib to handle non-stnd ones
  library(regex)
  s <- get_sources_df()
  for (url in s$URL){
    print(paste0("sitemap:(",url,")")) #dbg
    urlb <- gsub("sitemap.xml","",url)
    print(paste0("crawl_sitemap(",urlb,")"))
  }
}

iqt2df <- function(iqt, endpoint = NULL){
  #instantiated-query-template/txt to df
  if(!iqt){
    return("need isntantiated query text")
  }
  if(sparql_inited == NULL){
    si <- init_sparql() #still need to init
    #qs <- iqt #or si  #need q to instantiate
  }
  #add2log(iqt)
  if(!endpoint){
    endpoint <- dflt_endpoint
  }
  add2log(paste0("query:", iqt))
  add2log(paste0("endpoint:", endpoint))
  df <- sparqldataframe::query(endpoint, iqt)
  return(df)
}

v4qry <- function(var, qt){
  #var + query-type 2 df
  if(!var){
    var <- ""
  }
  sqs <- eval(paste0("get_", qt, "_txt()")) #get_  _txt   fncs, are above
  if(!is_str(sqs)){
    print(paste0("f4qry get_ ", qt, "_txt() gave; ", sqs, ", so aborting"))
    return("")
  }
  iqt <- v2iqt(var, sqs)
  #add2log(iqt) #logged in next fnc
  return(iqt2df(iqt))
}

search_query <- function(q){ #same as txt_query below
  return(v4qry(q, "query"))
}

#functionality that is see on dataset page:

search_relateddatafilename <- function(q){
  return(v4qry(q, "relateddatafilename"))
}

search_download <- function(urn){
  return(v4qry(urn, "download"))
}

search_webservice <- function(urn){
  return(v4qry(urn, "webservice"))
}

subj2urn <- function(doi){
  "<<doi a so:Dataset>>'s graph"
  return(v4qry(doi,"subj2urn"))
}

get_graphs <- function(){
  "return all the g URNs"
  return(v4qry("","graphs"))
}

get_graph <- function(g){
  "return all triples from g w/URN"
  return(v4qry(g,"graph"))
}

get_summary <- function(g=""){ #g not used but could make a version that gets it for only 1 graph
  "return summary version of all the graphs quads"
  return(v4qry(g,"summary"))
}

summary_query <- function(g=""){ #this is finally used in: txt_query_summary
  "replacement txt_query of new summary namespace" #or summary2/etc check
  return(v4qry(g,"summary_query")) #could call this the fast_query
}

txt_query_ <- function(q,endpoint=NULL){
  "or can just reset dflt_endpoint"
  if(is.null(endpoint)){
    df <- txt_query(q)
  } else if(endpoint == "summary"){ #1st try for summary query
    save <- dflt_endpoint #but do not do till can switch the qry as well
    dflt_endpoint <- gsub("/earthcube/","/summary2/",dflt_endpoint)
    print(paste("summary:txt_query,w/:",dflt_endpoint))
    #df <- txt_query(q)
    df <- summary_query(q)
    dflt_endpoint <- save
  } else {
    save <- dflt_endpoint
    dflt_endpoint <- endpoint
    print(paste("txt_query,w/:",dflt_endpoint))
    df <- txt_query(q)
    dflt_endpoint <- save
  }
  return(df)
}

txt_query_summary <- function(q){
  return(txt_query_(q, "summary"))
}

get_graphs_list <- function(endpoint = NULL, dump_file = NULL){
  dflt_endpoint <<- endpoint
  if(is.null(endpoint)){
    dfg <- get_graphs()
  } else {
    save <- dflt_endpoint
    dflt_endpoint <<- endpoint
    dfg <- get_graphs()
    dflt_endpoint <<- save
  }
  if(!is.null(dump_file)){
    write.csv(dfg$g, dump_file)
  }
  return(dfg$g)
}

get_graphs_cache <- function(endpoint = "http://ideational.ddns.net:9999/bigdata/namespace/nabu/sparql", dump_file = NULL){
  print(paste("get_graphs_cache:", endpoint))
  l <- get_graphs_list(endpoint)
  if(!is.null(dump_file)){
    list2txtfile(dump_file, l)
  }
  return(l)
}

get_graphs_lon <- function(repo = NULL, endpoint = "http://ideational.ddns.net:3040/all/sparql"){
  endpnt <- ifelse(is.null(repo), endpoint, gsub("all", repo, endpoint))
  print(paste("get_graphs_lon:", endpnt))
  return(get_graphs_list(endpnt))
}

get_graph_per_repo <- function(grep="milled",endpoint="https://graph.geocodes.ncsa.illinois.edu/blazegraph/namespace/earthcube/sparql",dump_file="graphs.csv"){
  gl <- get_graphs_list(endpoint,dump_file) #this needs full URN to get counts for the same 'repo:' s
  gn <- length(gl)
  print(paste0("got:",gn,"graphs"))
  if (grep != "milled"){ #used -f5- on latest&a few still off; shows the mess of dep on URN syntax
    cs <- paste0("cut -d':' -f2- ",dump_file," |cut -d'/' -f1 | sort | uniq -c |sort -n") #this is for my ld-cache
  } else {
    cs <- paste0("cut -d',' -f2- graphs.csv | cut -d':' -f5 | cut -d'/' -f1 | sortucn|gred -v ' 1 '")
  }
  return os_system_(cs)
}

urn_tail <- function(urn){
  #like urn_leaf
  if (urn == ""){
    return(urn)
  } else {
    return(strsplit(urn, ":")[[1]][length(strsplit(urn, ":")[[1]])])
  }
}

urn_tails <- function(URNs){
  return(lapply(URNs, function(s){
    if (s == ""){
      return(s)
    } else {
      return(strsplit(s, ":")[[1]][length(strsplit(s, ":")[[1]])])
    }
  }))
}

get_graphs_tails <- function(endpoint){
  #just the UUIDs of the URNs in the graph
  URNs <- get_graphs_list(endpoint)
  return(urn_tails(URNs))
}

txt_query <- function(qry_str, sqs = NULL){
  #a generalized version would take pairs/eg. <${g}> URN ;via eq urn2graph
  "sparql to df"
  if (is.null(sparql_inited)){
    si <- init_sparql()  #still need to init
    qs <- ifelse(is.null(sqs), si, sqs)
  } else {
    qs <- ifelse(is.null(sqs), get_txtfile("sparql-query.txt"), sqs)
  }
  library(sparqldataframe)
  library(jsonlite)
  dflt_endpoint <- endpoint
  add2log(qry_str)
  q <- gsub("${q}", qry_str, qs)
  add2log(q)
  df <- sparqldataframe::query(endpoint, q)
  return(df)
}

get_subj_from_index <- function(index){
  return(df[df$index == index, "subj"])
}

get_index_from_subj <- function(subj){
  return(df[df$subj == subj, "index"])
}

combine_features <- function(row){
  tryCatch({
    return(paste(row$kw, row$name, row$description, row$pubname, sep = " "))
  }, error = function(e){
    print(paste("Error:", row))
  })
}

cosine_sim <- NULL

get_related <- function(likes){
  dataset_index <- get_index_from_subj(likes)
  similar_datasets <-  list(enumerate(cosine_sim[dataset_index]))
  ## Step 7: Get a list of similar movies in descending order of similarity score
  sorted_similar_datasets <- sort(similar_datasets,key=function(x)x[1],decreasing=TRUE)
  ## Step 8: Print subjs of first 50 movies
  i <- 0
  for (element in sorted_similar_datasets){
    print(get_subj_from_index(element[0]))
    i <- i + 1
    if (i > 50){
      break
    }
  }
  return(sorted_similar_datasets)
}

get_related_indices <- function(like_index){
  "return a list of indices that are related to input index"
  similar_indices <-  list(enumerate(cosine_sim[like_index]))
  sorted_similar <- sort(similar_indices,key=function(x)x[1],decreasing=TRUE)
  #return sorted_similar
  return(list(map(first,sorted_similar)))
}

dfCombineFeaturesSimilary <- function(df, features = c('kw','name','description','pubname')){
  "run only once per new sparql-df"
  library(tm)
  df <- cbind(index=seq_len(nrow(df)), df)
  df <- df[,c('index',features)]
  df$combined_features <- apply(df, 1, function(x) paste(x, collapse=" "))
  ##Step 4: Create count matrix from this new combined column
  cv <- CountVectorizer()
  count_matrix <- cv$fit_transform(df$combined_features)
  terms <- cv$get_feature_names() #new for topic-modeling
  tl <- length(terms)
  print(paste("topic-terms:",tl))
      #Step 5: Compute the Cosine Similarity based on the count_matrix
      cosine_sim <- cosine(cv)
}

test_related <- function(q, row = 0){
  df <- txt_query(q)
  dfCombineFeaturesSimilary(df)
  return(get_related_indices(row))
}

show_related <- function(df, row){
  related <- get_related_indices(row)
  if(nrow(df) < 4){
    print("not many to compare with")
  }
  for(ri in related){
    des <- df$description[ri]
    print(paste(ri, ":", des))
  }
}

get_distr_dicts <- function(fn){
  d <- get_jsfile2dict(fn)
  return(d$distribution)
}

add_id <- function(d){
  u <- d$`dcat:accessURL`
  d$`@id` <- u
  return(d)
}

get_id <- function(d){
  return(d$`@id`)
}

jld2crate <- function(fn){
  print(crate_top)
  dl <- get_distr_dicts(fn)
  dl2 <- lapply(dl, add_id)
  ids <- lapply(dl, get_idd)
  print(toJSON(ids))
  print(crate_middle)
  print(toJSON(dl2))
  print(crate_bottom)
}

jld2crate_ <- function(fn){
  dir.create("roc") #for now
  fn_out <- paste0("roc/", fn)
  put_txtfile(fn_out, crate_top)
  dl <- get_distr_dicts(fn)
  dl2 <- lapply(dl, add_id)
  ids <- lapply(dl, get_idd)
  put_txtfile(fn_out, toJSON(ids))
  put_txtfile(fn_out, crate_middle)
  put_txtfile(fn_out, toJSON(dl2))
  put_txtfile(fn_out, crate_bottom)
}

replace_last <- function(source_string, replace_what, replace_with){
  head <- strsplit(source_string, split = replace_what)[[1]][1]
  tail <- strsplit(source_string, split = replace_what)[[1]][3]
  return (paste(head, replace_with, tail, sep = ""))
}

nt_fn2nq <- function(fn){
  fnb <- file_base(fn)
  fn2 <- paste(fnb, ".nq", sep = "")
  replace_with <- paste0(" <urn:", fnb, "> .")
  fd_out <- file(fn2, open = "w")
  fd_in <- file(fn, open = "r")
  for (line in fd_in){
    ll <- nchar(line)
    if (ll > 9){
      line_out <- replace_last(line, " .", replace_with)
      writeLines(line_out, fd_out)
    }
  }
  close(fd_in)
  close(fd_out)
  return (fn2)
}

riot2nq <- function(fn){
  fnb <- file_base(fn)
  fn2 <- paste(fnb, ".nq", sep = "")
  replace_with <- paste0(" <urn:", fnb, "> .")
  nts <- system(paste("riot --stream=nt", fn), intern = TRUE)
  lin <- length(nts)
  print(paste("got", lin, "lines"))
  fd_out <- file(fn2, open = "w")
  for (line in nts){
    ll <- nchar(line)
    if (ll > 9){
      line_out <- replace_last(line, " .", replace_with)
      writeLines(line_out, fd_out)
    }
  }
  close(fd_out)
  return (fn2)
}

to_nq <- function(fn, prefix = NULL){
  #process .jsonld put out .nq
  fnb <- file_base(fn)
  fn2 <- paste0(fnb, ".nq")
  if (file.exists(fn2)){
    print(paste0("riot2nq:", fn2, " already there"))
  }
  replace_with <- paste0(" <urn:", fnb, "> .")
  #nts <- os_system_(paste0("riot --stream=nt ", fn))
  nts <- to_nt_str(fn)
  fd_in <- strsplit(nts, "\n")[[1]]
  lin <- length(fd_in)
  print(paste0("got ", lin, " lines"))
  fd_out <- file(fn2, "w")
  for (line in fd_in){
    #ll <- length(line)
    if (no_error(line)){
      line_out <- replace_last(line, " .", replace_with)
      writeLines(line_out, fd_out)
    }
  }
  close(fd_out)
  return(fn2)
}

fn2nq <- function(fn){
  #output fn as .nq
  if (is_http(fn)){
    fn <- wget(fn)
  }
  print(paste0("fn2nq on:", fn))
  ext <- file_ext(fn)
  print(paste0("2nq file_ext:", ext))
  fn2 <- "Not Found"
  if (ext == ".nt"){
    fn2 <- fn2nq(fn)
  }
  if (ext == ".jsonld"){
    #fn2 <- riot2nq(fn)
    fn2 <- to_nq(fn)
  } else {
    #it might still work:
    fn2 <- riot2nq(fn)
  }
  print(paste0("gives:", fn2))
  return(fn2)
}

summoned2nq <- function(s = NULL){
  #list of jsonld to one nq file
  if(is.null(s)){
    s <- get_oss_files("summoned")
    sl <- length(s)
    print(paste0("summoned:", sl, " 2nq"))
  }
  fnout <- paste0(repo_name, ".nq")
  #os_system(paste0("yes|gzip ", fnout)) #complains if not there
  os_system(paste0("echo \"\"> ", fnout))
  nql <- lapply(s, fn2nq)
  for(nq in nql){
    print(paste0("summoned2nq,nq:", nq))
    os_system(paste0("cat ", nq, ">>", fnout))
  }
  return(fnout)
}

serve_nq <- function(fn){
  #serve file w/fuseki #could also do w/blasegraph, for txt-test/final-run
  fnb <- file_base(fn)
  cs <- paste0("nohup fuseki-server -file=", fn, " /", fnb, " &")
  print(paste0("assuming no fuseki process, check for this new one:", cs))
  os_system(cs)
}

summon2serve <- function(s = NULL){
  #get jsonld and serve the quads
  fnout <- summoned2nq(s)
  #cs <- paste0("nohup fuseki-server -file=", fnout, " /", repo_name, " &")
  #os_system(cs)
  serve_nq(fnout)
  return(fnout)
}

prov2mapping <- function(url){
  #use url from p above
  "read&parse 1 PROV record"
  library(jsonlite)
  #print(f'prov2mapping:{url}')
  j <- get_url(url)
  d <- fromJSON(j)
  #print(d)
  g <- d$`@graph`
  if(!is.null(g)){
    gi <- sapply(g, function(g) g$`@id`)
    smd <- g[2] #assume 1 past the context, 1st thing being from sitemap
    sm <- smd$`@id` #gi[0]
    u <- collect_pre_(gi,"urn:")
    u0 <- u[1]
    #print(f'{sm}=>{u0}')
    #return sm, u #if expect >1
    return(list(sm, u[1]))
  } else {
    return(paste0("no graph for:", url))
  }
}

prov2mappings <- function(urls){
  #use urls from p above
  sitemap2urn <- list()
  urn2sitemap <- list() #might need this more
  for (url in urls){
    key <- prov2mapping(url)[1]
    value <- prov2mapping(url)[2]
    sitemap2urn[[key]] <- value
    urn2sitemap[[value]] <- key
    value2 <- unlist(strsplit(value, ":"))[length(strsplit(value, ":"))] #so can also lookup form UUID w/o urn:... before it
    urn2sitemap[[value2]] <- key #will be in same dict, so can lookup by either
  }
  sitemap <- names(sitemap2urn)
  if (dbg){
    print(paste("prov-sitemap:", sitemap))
  }
  #return sitemap2urn, urn2sitemap
  return(list(sitemap2urn, urn2sitemap, sitemap))
}

url2json <- function(url){
  library(httr)
  r <- GET(url)
  return(content(r))
}

get_url <- function(url){
  #also in testing
  #request.get url
  library(httr)
  r <- GET(url)
  return(content(r))
}

listFD <- function(url, ext=''){
  library(rvest)
  page <- read_html(url)
  r <- c(url, page %>% html_nodes("a") %>% html_attr("href") %>% grep(ext, value = TRUE, ignore.case = TRUE, fixed = TRUE))
  return(r)
}

get_htm_dir <- function(url, ext=NULL){
  library(rvest)
  page <- read_html(url)
  if(!is.null(ext)){
    return(c(url, page %>% html_nodes("a") %>% html_attr("href") %>% grep(ext, value = TRUE, ignore.case = TRUE, fixed = TRUE)))
  } else {
    return(c(url, page %>% html_nodes("a") %>% html_attr("href")))
  }
}

url_xml <- function(url){
  library(httr)
  tryCatch({
    r <- GET(url, timeout(15, 45))
    test_xml <- content(r)
    status <- status_code(r)
    if(status == 200){
      return(test_xml)
    } else {
      print(paste0("url_xml,bad:", status, ",for:", url))
      return(NULL)
    }
  }, error = function(e){
    print(paste0("url_xml:req-execpt on:", url))
    return(NULL)
  })
}

is_bytes <- function(bs){
  return(is.raw(bs))
}

sitemap_urls <- function(url){
  test_xml <- url_xml(url)
  if(!test_xml){
    return(c())
  }
  c <- sitemap_xml2dict(test_xml)
  if(c){
    urls <- lapply(c, function(kd) kd$loc)
    return(urls)
  } else {
    print(paste0("no sitemap_urls xml for urls:", url))
    return(c())
  }
}

xmltodict_parse <- function(test_xml){
  library(xmltodict)
  if(!is_bytes(test_xml)){
    print("xml_parse no str")
    return(NULL)
  }
  tryCatch({
    d <- xmltodict::parse(test_xml)
  }, error = function(e){
    lx <- length(test_xml)
    print("xml_parse exception")
    d <- NULL
  })
  return(d)
}

sitemap_xml2dict <- function(test_xml){
  d <- xmltodict_parse(test_xml)
  if(dbg){
    print(d)
  }
  if(!d){
    print(paste0("sitemap_xml2 not found for:", test_xml))
    return(NULL)
  }
  lbr <- d$urlset
  if(lbr){
    c <- lbr$url
    return(c)
  } else {
    print(paste0("no urlset, for:", test_xml))
    return(NULL)
  }
}

sitemap_urls <- function(url){
  test_xml <- url_xml(url)
  if(!test_xml){
    return(c())
  }
  c <- sitemap_xml2dict(test_xml)
  if(c){
    urls <- lapply(c, function(kd) kd$loc)
    return(urls)
  } else {
    print(paste0("no sitemap_urls xml for urls:", url))
    #return(NULL)
    return(c()) #hope to still work
  }
}

bucket_xml <- function(url){
  return(url_xml(url))
}

bucket_xml2dict <- function(test_xml){
  #import xmltodict
  #d=xmltodict.parse(test_xml)
  d <- xmltodict_parse(test_xml)
  #print(d)
  lbr <- d$ListBucketResult
  if(lbr){
    c <- lbr$Contents
    return(c)
  } else {
    print(paste0("no ListBucketResult, for:", test_xml))
    return(NULL)
  }
}

bucket_files <- function(url){ #need to get past: <MaxKeys>1000</MaxKeys>
  #bucket_url to file listing
  test_xml <- bucket_xml(url)
  c <- bucket_xml2dict(test_xml)
  if(c){
    files <- lapply(c, function(kd) kd$Key)
    dates <- lapply(c, function(kd) kd$LastModified) #or when get prov look at file dates before the parse?
    #AttributeError: 'int' object has no attribute 'get' #had taken this out
    return(list(files, dates))
  } else {
    print(paste0("no bucket xml for files:", url))
    return(list(NULL, NULL))
  }
}

endpoint_xml2dict <- function(test_xml){
  d <- xmltodict_parse(test_xml)
  if(dbg){
    print(d)
  }
  lbr <- d$`rdf:RDF`
  return(lbr)
}

endpoint_description <- function(url="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/citesting2/sparql"){
  "get/test if endpoint ok, description xml to see that it is healthy"
  test_xml <- url_xml(url)
  ts <- test_xml %>% rawToChar()
  if(is_html(ts)){
    return("html")
  }
  if(startsWith(ts, "Service")){
    return("service_description")
  }
  c <- endpoint_xml2dict(test_xml)
  lc <- length(c) #2keys
  print(paste0("endpoint w/", lc, " descriptions"))
  des <- c$`rdf:Description`
  return(des)
}

get_file_ext_types <- function(file_list){
  file_types <- list()
  for (fn in file_list){
    base <- path_base_leaf(fn)[1]
    leaf <- path_base_leaf(fn)[2]
    ext <- file_ext(leaf)
    count <- file_types[[ext]]
    if (count){
      count <- count + 1
    } else {
      count <- 1
    }
    file_types[[ext]] <- count
  }
  return(file_types)
}

get_file_leaf_types <- function(file_list){
  file_types <- list()
  for (fn in file_list){
    base <- path_base_leaf(fn)[1]
    leaf <- path_base_leaf(fn)[2]
    count <- file_types[[leaf]]
    if (count){
      count <- count + 1
    } else {
      count <- 1
    }
    file_types[[leaf]] <- count
  }
  return(file_types)
}

get_file_base_types <- function(file_list){
  file_types <- list()
  for (fn in file_list){
    base <- path_base_leaf(fn)[1]
    leaf <- path_base_leaf(fn)[2]
    count <- file_types[[base]]
    if (count){
      count <- count + 1
    } else {
      count <- 1
    }
    file_types[[base]] <- count
  }
  return(file_types)
}

set_bucket_files <- function(bucket = NULL){
  "get+set LD_cache_ files array and types dict"
  if(is.null(bucket)){
    global ci_url
    bucket <- ci_url
  }
  global LD_cache_base, LD_cache_files, LD_cache_types
  LD_cache_base <- bucket
  LD_cache_files, LD_cache_dates <- bucket_files(bucket)
  LD_cache_types <- list()
  for(fn in LD_cache_files){
    base, leaf <- path_base_leaf(fn)
    count <- LD_cache_types[[base]]
    if(!is.null(count)){
      count <- count + 1
    } else {
      count <- 1
    }
    LD_cache_types[[base]] <- count
  }
  return(LD_cache_types)
}

get_full_key <- function(partial_key, mydict){
  "get key that has str in it"
  #fk = next(k for k,v in LD_cache_types.items() if base_type in k) #full key
  fk <- names(mydict)[grep(partial_key, names(mydict))]
  return(fk)
}

get_bucket_files <- function(base_type){
  #ask for base_type= summoned,milled,prov,.. get all full file paths
  global LD_cache_base, LD_cache_files, LD_cache_types
  if(!LD_cache_files){
    set_bucket_files()
  }
  print(paste0('get_bucket_files:',base_type))
  fe <- collect_pre_(LD_cache_files,base_type) #end of file paths
  lfe <- length(fe)
  if(lfe > 0){
    ff <- list(map(function(f) paste0(LD_cache_base,'/',f), fe)) #full file paths
  } else {
    print(paste0('WARN:no ',base_type,' in ',LD_cache_base,':',fe))
    #ff=[]
    ff <- NULL
  }
  return(ff)
}

get_oss_files_ <- function(repo = NULL, base_type = NULL, bucket = "gleaner", path = NULL, minio_endpoint_url = "https://oss.geodex.org/", full_path = TRUE){
  if(is.null(bucket)){
    bucket <- testing_bucket
  }
  if(is.null(base_type)){
    base_type <- "summonded"
  }
  if(is.null(repo)){
    repo <- repo_name
  }
  if(is.null(path)){
    path <- paste0(bucket, "/", base_type, "/", repo)
  }
  print(paste0("get_oss_files_:", path))
  return(oss_ls(path, full_path, minio_endpoint_url))
}

get_oss_files <- function(base_type){
  path <- paste0(testing_bucket, "/", base_type, "/", repo_name)
  return(oss_ls(path))
}

site_urls2UUIDs <- NULL
urn2site_urls <- NULL
UUIDs2site_urls <- list() #uuid part of urn as key
prov_sitemap <- NULL

#def URLsUUID(url):
urn2uuid <- function(url){
  "pull out the UUID from w/in the URL"
  s <- urn_leaf(url)
  leaf_base <- s if (!is.null(s)) else file_base(s)
  return(leaf_base)
}

uuid2url <- function(uuid){
  "map from uuid alone to crawl url"
  url <- UUIDs2site_urls[[uuid]]
  if (is.null(url)){
    print(paste0("bad uuid2url:", uuid))
    return(uuid)
  }
  return(url)
}

uuid2repo_url <- function(uuid){
  "uuid2url w/shorter repo:leaf.json"
  url <- uuid2url(uuid)
  if (!is.null(url)){
    return(replace_base(url))
  } else {
    print(paste0("bad uuid2repo_url:", uuid))
    return(uuid)
  }
}

is_html <- function(str){
  return(grepl("<html>", str))
}

is_http <- function(u){
  if(!is_str(u)){
    print("might need to set LD_cache")
    return(NULL)
  }
  return(startsWith(u, "http"))
}

is_urn <- function(u){
  if(!is_str(u)){
    print("might need to set LD_cache")
    return(NULL)
  }
  return(startsWith(u, "urn:"))
}

leaf <- function(u){
  if(is_http(u)){
    return(path_leaf(u))
  } else if(is_urn(u)){
    return(urn_leaf(u))
  } else {
    print(paste0("no leaf:", u))
    return(u)
  }
}

leaf_base <- function(u){
  lf <- leaf(u)
  if(!is.null(lf)){
    return(file_base(lf))
  } else {
    print(paste0("no leaf_base:", u))
    return(lf)
  }
}

fill_repo_url <- function(url, mydict, val="ok"){
  #url w/uuid ->repo:leaf as key in dict
  key <- to_repo_url(url)
  mydict[key] <- val
  print(mydict)
  return(mydict)
}

fill_repo_urls <- function(urls, mydict, val="ok"){
  ul <- length(urls)
  print(paste("frus:", ul))
  map(urls, ~fill_repo_url(., mydict, val))
  print(mydict)
  return(mydict)
}

urls2idict <- function(urls, val="ok"){
  mydict <- list()
  if(length(urls) == 0){
    print("urls2idict:no urls")
    return(mydict)
  }
  ul <- length(urls)
  print(paste("u2d:", ul))
  for(url in urls){
    key <- to_repo_url(url)
    mydict[[key]] <- val
  }
  if(dbg){
    print(mydict)
  }
  return(mydict)
}

get_vals <- function(key, dl){
  "lookup key in a list of dicts"
  rl <- lapply(dl, function(d) d[[key]])
  rl <- c(key, rl)
  return(rl)
}

csv_out <- NULL

cmp_expected_results <- function(df = NULL, df2 = "https://raw.githubusercontent.com/MBcode/ec/master/test/expected_results.csv") {
  # just show where not expected # so bad things can still be ok
  if (!is_df(df) && !is.null(csv_out)) {
    df <- csv_out
  }
  if (is_http(df2)) {
    df2 <- read.csv(df2)
  }
  print(paste("df1=", df, "df2=", df2))
  return(df_diff(df, df2))
}

csv_dropoff <- function(sitemap_url="https://raw.githubusercontent.com/MBcode/ec/master/test/sitemap.xml", #start expecte bad cases
                        bucket_url=NULL, endpoint="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/citesting2/sparql",cmp=FALSE){
  global csv_out
  print(paste0('==sitemap:',sitemap_url))
  print(paste0('==graph_endpoint:',endpoint))
  if(is.data.frame(csv_out)){
    print("already have a csv_out")
    return(csv_out)
  }
  if(!is.null(bucket_url)){
    global ci_url
    if(bucket_url != ci_url){
      print(paste0('reset from:',ci_url,' to:',bucket_url))
      ci_url <- bucket_url
    }
  }
  print(paste0('==s3_endpoint:',bucket_url))
  if(length(urn2site_urls) == 0){
    set_prov2site_mappings()
  }
  sm <- sitemap_list(sitemap_url) #can now use sitemap2urn to get sitemap into same ID space
  sm_ru <- lapply(sm,replace_base) #acts as key for each dict ;need v of replace_base w/base_url2repo, but for url
  s <- get_oss_files("summoned")
  m <- get_oss_files("milled")
  print(paste0('check,endpoint:',endpoint))
  ep_ok <- endpoint_description(endpoint)
  if(ep_ok){
    g <- get_graphs_list(endpoint) #will strip ..urn: to uuid anyway
  } else {
    print(paste0('cd:enpoing not ok:',endpoint))
    g <- NULL
  }
  print(paste0('check,endpoint:',endpoint))
  ep_ok <- endpoint_description(endpoint)
  if (ep_ok){
    g <- get_graphs_list(endpoint) #will strip ..urn: to uuid anyway
  } else {
    print(paste0('cd:enpoing not ok:',endpoint))
    g <- NULL
  }
  sml <- length(sm_ru)
  sl <- length(s)
  ml <- length(m)
  gl <- length(g)
  sd <- urls2idict(s)
  md <- urls2idict(m)
  gd <- urls2idict(g)
  dl <- list(sd, md, gd)
  print(paste0('now lookup by:', sm_ru))
  r <- lapply(sm_ru, function(k) get_vals(k, dl))
  lr <- length
  df <- as.data.frame(r)
  csv_out <- df[, c("repo:file_name", "summoned", "milled", "graph")]
  if(cmp || dbg){
    diff <- cmp_expected_results(csv_out)
    print(paste0('diff w/expected:', diff))
  }
  return(csv_out)
}

set_prov2site_mappings <- function(){
  #make sure it is run, to get mappings
  "use cached PROV to make mappings"
  pu <- get_bucket_files(paste0('prov/', repo_name)) #only the ones for the repo_name being run
  if(length(pu) > 0){
    global site_urls2UUIDs, urn2site_urls, UUIDs2site_urls, prov_sitemap
    #return prov2mappings(pu)
    #sitemap2urn,urn2sitemap,sitemap=prov2mappings(pu)
    site_urls2UUIDs,urn2site_urls,prov_sitemap <- prov2mappings(pu)
    for(k in names(urn2site_urls)){
      k2 <- urn2uuid(k)
      if(length(k2) > 0){
        UUIDs2site_urls[k2] <- urn2site_urls[[k]]
      } else {
        print(paste('bad k2 for:', k, urn2site_urls[[k]]))
      }
    }
    l1 <- length(site_urls2UUIDs)
    l2 <- length(urn2site_urls)
    l3 <- length(prov_sitemap)
    ss <- paste('set:', l1, 'site_urls2UUIDs,', l2, 'UUIDs2site_urls,', l3, 'prov_sitemap')
    print(ss)
    return(ss)
  } else {
    print(paste('no prov for site_mappings'))
    return(NULL) #so can skip out of dependcies
  }
}

prov2sitemap <- function(bucket_url = NULL, pu = NULL){ #backward compat4a bit
  #return prov_sitemap, parse prov if not there
  if(length(prov_sitemap) == 0){
    set_prov2site_mappings()
  }
  return(prov_sitemap)

prov2sitemap_ <- function(bucket_url, pu = NULL){
  #parse bucket prov2get sitemap&it's mappings
  fi <- bucket_files(bucket_url)
  if (length(fi) == 0){
    print(paste0("prov2sitemap, no bucket_files:", bucket_url))
    return(NULL)
  }
  p <- collect_pre_(fi, "prov") #only the ones for the repo_name being run
  pu <- paste0(bucket_url, "/", p)
  sitemap <- NULL
  tryCatch({
    pul <- length(pu)
    print(paste0("prov2sitemap_mapping for:", pul))
    sitemap2urn <- prov2mappings(pu)$sitemap2urn
    urn2sitemap <- prov2mappings(pu)$urn2sitemap
    sitemap <- prov2mappings(pu)$sitemap
  }, error = function(e){
    print(paste0("bad prov2sitemap_mappings, on the:", pul))
  })
  return(sitemap)
}

bucket_files2 <- function(url){
  fi <- bucket_files(url)
  s <- collect_pre_(fi, "summoned")
  m <- collect_pre_(fi, "milled")
  return(list(s, m))
}

bucket_files3 <- function(url = NULL){
  if (!is.null(url)){
    ci_url <<- url
  }
  s <- get_oss_files("summoned")
  m <- get_oss_files("milled")
  p <- get_bucket_files(paste0("prov/", repo_name)) #only the ones for the repo_name being run
  if (is.null(prov_sitemap)){
    prov2sitemap()
  }
  psl <- length(prov_sitemap)
  print(paste0("bf3,prov_sitemap:", psl))
  sitemap2urn <- site_urls2UUIDs
  urn2sitemap <- UUIDs2site_urls
  if (is.null(s)){
    print("bf3:no summoned")
  }
  if (is.null(m)){
    print("bf3:no milled")
  }
  return(list(s, m, sitemap2urn, urn2sitemap))
}


