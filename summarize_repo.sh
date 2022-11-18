fnq.py $1
tsum.py $1 |egrep -v "not IN_COLAB|rdf_initd"|cat>$1.ttl
