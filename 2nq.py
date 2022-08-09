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

#DF's gleaner uses the shah of the jsonld to name the .rdf files which are actually .nt files
# but then there are lots of .nq files that are actually .nt files, but should be able to get them w/this
#maybe someplace in nabu this is done, but by then I can't have the files to load them

#use filename to convert .rdf file to a .nq file
#▶<102 a09local: /milled/geocodes_demo_datasets> mo 09517b808d22d1e828221390c845b6edef7e7a40.rdf
#_:bcbhdkms5s8cef2c4s7j0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://schema.org/Dataset> .
#goes to:
#_:bcbhdkms5s8cef2c4s7j0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://schema.org/Dataset> "urn:09517b808d22d1e828221390c845b6edef7e7a40".
#fn = "09517b808d22d1e828221390c845b6edef7e7a40.rdf"

def fn2nq(fn):
    fnb = file_base(fn)
    fn2 = fnb + ".nq"
    with open(fn2,'w') as fd_out:
        with open(fn,'r') as fd_in:
            for line in fd_in:
                line_out = line.replace(" .",f' "urn:{fnb}" .')
                fd_out.write(line_out)
    return fn2

if __name__ == '__main__':
    import sys
    if(len(sys.argv)>1):
        fn = sys.argv[1]
        print(f'fn2nq on:{fn}')
        fn2=fn2nq(fn)
        print(f'gives:{fn2}')
