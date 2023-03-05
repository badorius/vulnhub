NUM=$(curl -s stocker.htb |wc -l)
# we get 5093
ffuf -c -w /usr/share/seclists/Discovery/DNS/namelist.txt -u $1 -H 'Host: FUZZ.stocker.htb' -fs $NUM
ffuf -c -w /usr/share/seclists/Discovery/DNS/namelist.txt  -u http://stocker.htb -H 'Host: FUZZ.stocker.htb' -fs $NUM  -o ffuf_vhosts.txt
