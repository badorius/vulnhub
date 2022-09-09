# ENUMERATION

Nmap: 
```shell
└─$ sudo nmap -sC -sV -Pn 10.129.96.142 -oN nmap.txt
Starting Nmap 7.92 ( https://nmap.org ) at 2022-09-09 21:27 CEST
Nmap scan report for 10.129.96.142
Host is up (0.032s latency).
Not shown: 995 closed tcp ports (reset)
PORT    STATE SERVICE      VERSION
21/tcp  open  ftp          Microsoft ftpd
| ftp-syst: 
|_  SYST: Windows_NT
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| 02-03-19  12:18AM                 1024 .rnd
| 02-25-19  10:15PM       <DIR>          inetpub
| 07-16-16  09:18AM       <DIR>          PerfLogs
| 02-25-19  10:56PM       <DIR>          Program Files
| 02-03-19  12:28AM       <DIR>          Program Files (x86)
| 02-03-19  08:08AM       <DIR>          Users
|_02-25-19  11:49PM       <DIR>          Windows
80/tcp  open  http         Indy httpd 18.1.37.13946 (Paessler PRTG bandwidth monitor)
|_http-trane-info: Problem with XML parsing of /evox/about
| http-title: Welcome | PRTG Network Monitor (NETMON)
|_Requested resource was /index.htm
|_http-server-header: PRTG/18.1.37.13946
135/tcp open  msrpc        Microsoft Windows RPC
139/tcp open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp open  microsoft-ds Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2022-09-09T19:27:50
|_  start_date: 2022-09-09T19:26:28
| smb-security-mode: 
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.23 seconds
zsh: segmentation fault  sudo nmap -sC -sV -Pn 10.129.96.142 -oN nmap.txt

```

Let's take a look on this anonymous FTP:

```shell
└─$ ftp 10.129.96.142
Connected to 10.129.96.142.
220 Microsoft FTP Service
Name (10.129.96.142:darthv): anonymous
331 Anonymous access allowed, send identity (e-mail name) as password.
Password: 
230 User logged in.
Remote system type is Windows_NT.
ftp> dir
229 Entering Extended Passive Mode (|||49735|)
150 Opening ASCII mode data connection.
02-03-19  12:18AM                 1024 .rnd
02-25-19  10:15PM       <DIR>          inetpub
07-16-16  09:18AM       <DIR>          PerfLogs
02-25-19  10:56PM       <DIR>          Program Files
02-03-19  12:28AM       <DIR>          Program Files (x86)
02-03-19  08:08AM       <DIR>          Users
02-25-19  11:49PM       <DIR>          Windows
226 Transfer complete.
ftp> cd Users
250 CWD command successful.
ftp> dir
229 Entering Extended Passive Mode (|||49738|)
150 Opening ASCII mode data connection.
02-25-19  11:44PM       <DIR>          Administrator
02-03-19  12:35AM       <DIR>          Public
226 Transfer complete.
ftp> cd Administrator
550 Access is denied. 
ftp> cd Public
250 CWD command successful.
ftp> dir
229 Entering Extended Passive Mode (|||49748|)
150 Opening ASCII mode data connection.
02-03-19  08:05AM       <DIR>          Documents
07-16-16  09:18AM       <DIR>          Downloads
07-16-16  09:18AM       <DIR>          Music
07-16-16  09:18AM       <DIR>          Pictures
09-09-22  03:27PM                   34 user.txt
07-16-16  09:18AM       <DIR>          Videos
226 Transfer complete.
ftp> bin
200 Type set to I.
ftp> mget user.txt
mget user.txt [anpqy?]? y
229 Entering Extended Passive Mode (|||49754|)
150 Opening BINARY mode data connection.
100% |***********************************************************************************************************************************************************************************************|    34        1.05 KiB/s    00:00 ETA
226 Transfer complete.
34 bytes received in 00:00 (1.04 KiB/s)
ftp> exit
221 Goodbye.
                                                                                                                                                                                                                                            
└─$ cat user.txt  
11818424d2c2af5e637c4cdaacc740b4
                                                                                                                                                                                                                                            
```

uoooohhh!



