#simple recommender demo
# sparql qry that when you pick one result you can get an ordered list or related ones
#there is a colab NoteBook version as well
import sys
if(len(sys.argv)>1):
    qry_str=sys.argv[1]
else:
    qry_str = "norway"
#/Users/mbobak/dwn/ai/disc/ml/src/codeheroku/Introduction-to-Machine-Learning/Building a Movie Recommendation Engine
#should have just swapped "name" in csv w/"subj" ;subj w/subj this time
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
###### helper functions. Use them when needed #######
def get_subj_from_index(index):
	return df[df.index == index]["subj"].values[0]

def get_index_from_subj(subj):
	return df[df.subj == subj]["index"].values[0]
##################################################
#base_fn = "main4.rq"
base_fn = "../qry/main4.rq"
# ?lit bds:search "${q}" . #has norway instead right now

def get_txtfile(fn):
    with open(fn, "r") as f:
        return f.read()

def sq2df(qry_str):
    "sparql to df"
    import sparqldataframe
    endpoint = "https://graph.geodex.org/blazegraph/namespace/nabu/sparql"
    gqs=get_txtfile(base_fn)
    q=gqs.replace('norway',qry_str)
    #print(f'q:{q}')
    df = sparqldataframe.query(endpoint, q)
    df.describe()
    return df
##################################################

##Step 1: Read CSV File
##df = pd.read_csv("movie_dataset.csv")
#df = pd.read_csv("norway2.csv")
#df2 = sq2df("norway")
df2 = sq2df(qry_str) #from cli
df2.insert(0,'index',range(0,len(df2)))
print(df2)
df=df2
#df2['index']=range(len(df2)) #also works
print(df.columns)
df.set_index('index')
##Step 2: Select Features

features = ['kw','name','description','pubname']
##Step 3: Create a column in DF which combines all selected features
for feature in features:
	df[feature] = df[feature].fillna('')

def combine_features(row):
	try:
		return row['kw'] +" "+row['name']+" "+row["description"]+" "+row["pubname"]
	except:
		print("Error:", row)	

df["combined_features"] = df.apply(combine_features,axis=1)

#print "Combined Features:", df["combined_features"].head()

##Step 4: Create count matrix from this new combined column
cv = CountVectorizer()

count_matrix = cv.fit_transform(df["combined_features"])

##Step 5: Compute the Cosine Similarity based on the count_matrix
cosine_sim = cosine_similarity(count_matrix) 
#movie_user_likes = "Avatar"
#should pick one of the ones from the df randomly, or can do them all
#movie_user_likes = "https://www.bco-dmo.org/dataset/752737"
movie_user_likes = df['subj'][0]
#print(f'look for {movie_user_likes}')

def get_related(likes):
    dataset_index = get_index_from_subj(likes)
    similar_datasets =  list(enumerate(cosine_sim[dataset_index]))
    sorted_similar_datasets = sorted(similar_datasets,key=lambda x:x[1],reverse=True)
    i=0
    print(f'look for related to: {likes}')
    for element in sorted_similar_datasets:
                    print(get_subj_from_index(element[0]))
                    i=i+1
                    if i>50:
                            break
    #could also stop when relatedness falls beyond a threshold
### Step 6: Get index of this movie from its subj
#movie_index = get_index_from_subj(movie_user_likes)
#
#similar_movies =  list(enumerate(cosine_sim[movie_index]))
#
### Step 7: Get a list of similar movies in descending order of similarity score
#sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)
#
### Step 8: Print subjs of first 50 movies
#i=0
#for element in sorted_similar_movies:
#		print(get_subj_from_index(element[0]))
#		i=i+1
#		if i>50:
#			break

#get_related(movie_user_likes)
for ds in df['subj']:
    get_related(ds)
