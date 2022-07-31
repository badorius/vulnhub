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

