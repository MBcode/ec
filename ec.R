
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

