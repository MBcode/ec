
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
