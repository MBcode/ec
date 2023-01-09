#to show that now it has to get into ./repo dir to fix the quads &cp up to ./repo.nq
fix_runX.sh $1
#takes repo.nq loads to fusekly /repo namespace, and runs tsum.py repo to make a repo.ttl file
repo2summary.sh $1
#later could have a nt2blaze.sh to put in the store
