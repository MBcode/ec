#python3 sq.py carbon | curl $dcs_url -F "dcs.c2stream=@-"
#python3 sq.py $1 | curl $dcs_url -F "dcs.c2stream=@-"
python3 sq2.py $1 | curl $dcs_url -F "dcs.c2stream=@-"
