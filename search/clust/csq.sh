#/usr/bin/python3 sq2.py $1 | curl $dcs_url -F "dcs.c2stream=@-"
python3 sq2.py $1 | curl $dcs_url -F "dcs.output.format=JSON"  -F "dcs.c2stream=@-"
