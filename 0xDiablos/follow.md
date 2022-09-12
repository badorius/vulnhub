# Enumeration

Download file 'You know 0xDiablos.zip' extract file with 7z:

```shell
7z x You\ know\ 0xDiablos.zip                                                                                                       main 

7-Zip [64] 17.04 : Copyright (c) 1999-2021 Igor Pavlov : 2017-08-28
p7zip Version 17.04 (locale=en_US.UTF-8,Utf16=on,HugeFiles=on,64 bits,16 CPUs x64)

Scanning the drive for archives:
1 file, 3058 bytes (3 KiB)

Extracting archive: You know 0xDiablos.zip
--
Path = You know 0xDiablos.zip
Type = zip
Physical Size = 3058

    
Enter password (will not be echoed):hackthebox
Everything is Ok

Size:       15656
Compressed: 3058
```

Take a look on vuln file extracted:
```shell
file vuln                                                                                                                           main 
vuln: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=ab7f19bb67c16ae453d4959fba4e6841d930a6dd, for GNU/Linux 3.2.0, not stripped
```


