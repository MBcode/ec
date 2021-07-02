def read_file(fn):
    "can be a url, will call pd read_.. for the ext type"
    import pandas as pd
    import os
    st=os.path.splitext(fn)
    ft=st[-1]
    if ft=='.tsv':
        df=pd.read_csv(fn, sep='\t')
    elif ft=='.csv':
        df=pd.read_csv(fn)
    else:
        df="no reader, can !wget the file"
    return df
