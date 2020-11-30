#/usr/bin/python3 sq2.py $1 | curl $dcs_url -F "dcs.c2stream=@-"
/usr/bin/python3 sq2.py $1 | curl $dcs_url -F "dcs.output.format=JSON"  -F "dcs.c2stream=@-"
