def read_file(fn, ext=None):
    "can be a url, will call pd read_.. for the ext type"
    import pandas as pd
    import os
    import re
    if(ext!=None):
        ft="." + ext
    else:
        st=os.path.splitext(fn)
        ft=st[-1]
    if ft=='.tsv' or re.search('.tsv',ext):
        df=pd.read_csv(fn, sep='\t')
    elif ft=='.csv' or re.search('csv',ext):
        df=pd.read_csv(fn)
    #elif ft=='.txt' or ext=='text/plain':
    elif ft=='.txt' or re.search('text',ext):
        df=pd.read_csv(fn, sep='\n')
    else:
        df="no reader, can !wget the file"
    return df
