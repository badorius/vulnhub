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


