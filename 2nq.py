#!/usr/bin/env python3
#mike b, take a triple file w/every line ending in " ." and use filename to make a quad, needed for gleaner/testing
#potentially useful elsewhere; eg. if added repo: could use this in my workflow to make quads
import os
#from ec.py ;below can go in utils as well, but as cli right now
def file_ext(fn):
    st=os.path.splitext(fn)
    #add2log(f'fe:st={st}')
    return st[-1]

def file_base(fn):
    st=os.path.splitext(fn)
    #add2log(f'fb:st={st}')
    return st[0]

def is_str(v):
    return type(v) is str

def is_http(u):
    if not is_str(u):
        print("might need to set LD_cache")
        return None
    return u.startswith("http")

def os_system(cs):
    "run w/o needing ret value"
    os.system(cs)
   #add2log(cs)

def os_system_(cs):
    "system call w/return value"
    s=os.popen(cs).read()
    #add2log(cs)
    return s

def path_leaf(path):
    "everything after the last /"
    import ntpath
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def wget(fn):
    #cs= f'wget -a log {fn}'  #--quiet
    cs= f'wget --tries=2 -a log {fn}' 
    os_system(cs)
    return path_leaf(fn) #new

#DF's gleaner uses the shah of the jsonld to name the .rdf files which are actually .nt files
# but then there are lots of .nq files that are actually .nt files, but should be able to get them w/this
#maybe someplace in nabu this is done, but by then I can't have the files to load them

#use filename to convert .rdf file to a .nq file
#▶<102 a09local: /milled/geocodes_demo_datasets> mo 09517b808d22d1e828221390c845b6edef7e7a40.rdf
#_:bcbhdkms5s8cef2c4s7j0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://schema.org/Dataset> .
#goes to:
#_:bcbhdkms5s8cef2c4s7j0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://schema.org/Dataset> "urn:09517b808d22d1e828221390c845b6edef7e7a40".
#fn = "09517b808d22d1e828221390c845b6edef7e7a40.rdf"

#https://stackoverflow.com/questions/3675318/how-to-replace-the-some-characters-from-the-end-of-a-string
def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail

def fn2nq(fn):
    "read in .nt put out .nq"
    fnb = file_base(fn)
    fn2 = fnb + ".nq"
    replace_with = f' <urn:{fnb}> .'
    with open(fn2,'w') as fd_out:
        with open(fn,'r') as fd_in:
            for line in fd_in:
                #line_out = line.replace(" .",f' "urn:{fnb}" .')
                #replace_with = f' "urn:{fnb}" .'
                ll=len(line)
                if ll>9:
                    line_out = replace_last(line, " .", replace_with)
                    fd_out.write(line_out)
    return fn2

def riot2nq(fn):
    "process .jsonld put out .nq"
    fnb = file_base(fn)
    fn2 = fnb + ".nq"
    replace_with = f' <urn:{fnb}> .'
    nts = os_system_(f'riot --stream=nt {fn}')
    fd_in = nts.split("\n") 
    lin=len(fd_in)
    print(f'got {lin} lines')
    with open(fn2,'w') as fd_out:
        for line in fd_in:
            ll=len(line)
            if ll>9:
                line_out = replace_last(line, " .", replace_with)
                fd_out.write(line_out)
                fd_out.write('\n')
    return fn2

#if .nt as before, if .jsonld then riot .jsonld to .nt 1st, then dump as .nq
if __name__ == '__main__':
    import sys
    if(len(sys.argv)>1):
        fn = sys.argv[1]
        if is_http(fn):
            fn=wget(fn)
        print(f'fn2nq on:{fn}')
        ext = file_ext(fn)
        print(f'2nq file_ext:{ext}')
        fn2="Not Found"
        if ext==".nt":
            fn2=fn2nq(fn)
        if ext==".jsonld":
            fn2=riot2nq(fn)
        print(f'gives:{fn2}')
