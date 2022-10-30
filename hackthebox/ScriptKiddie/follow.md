# ScriptKiddie Write-up 


# ENUMERATION

Start with nmap:

```shell
nmap -sC -sV -Pn 10.129.95.150 -oX nmap.txt                                                     SIGINT   main 
Starting Nmap 7.92 ( https://nmap.org ) at 2022-10-30 20:03 CET
Nmap scan report for 10.129.95.150
Host is up (0.035s latency).
Not shown: 998 closed tcp ports (conn-refused)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 3c:65:6b:c2:df:b9:9d:62:74:27:a7:b8:a9:d3:25:2c (RSA)
|   256 b9:a1:78:5d:3c:1b:25:e0:3c:ef:67:8d:71:d3:a3:ec (ECDSA)
|_  256 8b:cf:41:82:c6:ac:ef:91:80:37:7c:c9:45:11:e8:43 (ED25519)
5000/tcp open  http    Werkzeug httpd 0.16.1 (Python 3.8.5)
|_http-title: k1d'5 h4ck3r t00l5
|_http-server-header: Werkzeug/0.16.1 Python/3.8.5
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.34 seconds
```

whatweb:

```shell
whatweb http://10.129.95.150:5000 --log-brief=whatweb.log
http://10.129.95.150:5000 [200 OK] Country[RESERVED][ZZ], HTTPServer[Werkzeug/0.16.1 Python/3.8.5], IP[10.129.95.150], Python[3.8.5], Title[k1d'5 h4ck3r t00l5], Werkzeug[0.16.1]

```

searchexploit with xml file generated with nmap:

```shell
searchsploit Werkzeug                                                                                          main 
-------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                                                              |  Path
-------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
Pallets Werkzeug 0.15.4 - Path Traversal                                                                                                    | python/webapps/50101.py
Werkzeug - 'Debug Shell' Command Execution                                                                                                  | multiple/remote/43905.py
Werkzeug - Debug Shell Command Execution (Metasploit)                                                                                       | python/remote/37814.rb
-------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results

```

Open in browser:

![home](IMG/web/jpg)


