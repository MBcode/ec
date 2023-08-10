
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
