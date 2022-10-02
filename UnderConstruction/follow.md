# Enumeration

nmap and gobuster:
```shell
└──╼ $nmap -sC -sV -Pn $SERVERIP -oN nmap.txt
Starting Nmap 7.92 ( https://nmap.org ) at 2022-09-25 21:04 CEST
Nmap scan report for 64.227.43.55
Host is up (0.035s latency).
Not shown: 905 filtered tcp ports (no-response), 94 closed tcp ports (conn-refused)
PORT      STATE SERVICE VERSION
30951/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).

└──╼ $gobuster dir -w /usr/share/wordlists/dirb/common.txt -u http://64.227.43.55:30163 -o gobuster.txt
===============================================================
Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://64.227.43.55:30163
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Timeout:                 10s
===============================================================
2022/09/25 21:12:01 Starting gobuster in directory enumeration mode
===============================================================
/auth                 (Status: 200) [Size: 2149]
/logout               (Status: 302) [Size: 27] [--> /auth]
                                                          
===============================================================
2022/09/25 21:12:16 Finished
```

After examine downloaded files, we fouces our investigation on JWT:

```shell
cat helpers/JWTHelper.js                                                                                                      main 
const fs = require('fs');
const jwt = require('jsonwebtoken');

const privateKey = fs.readFileSync('./private.key', 'utf8');
const publicKey  = fs.readFileSync('./public.key', 'utf8');

module.exports = {
    async sign(data) {
        data = Object.assign(data, {pk:publicKey});
        return (await jwt.sign(data, privateKey, { algorithm:'RS256' }))
    },
    async decode(token) {
        return (await jwt.verify(token, publicKey, { algorithms: ['RS256', 'HS256'] }));
    }

```
Lets register admin/admin User on web:

![register admin/admin](IMG/register_admin.jpg)

Login with admin user:

![login admin/admin](IMG/login_admin.jpg)

Get JWT info from burpsuite:

![burp jwt](IMG/burp_jwt.jpg)

Read information about [JWT](https://book.hacktricks.xyz/pentesting-web/hacking-jwt-json-web-tokens), download jwt_tool from git and let's try 



We see on DBHelper.js file some interesting information. There are vars inside sql sentences, so may we can try inject some sql code with jwt_tool help.
```shell
cat ../../files/helpers/DBHelper.js ter 
const sqlite = require('sqlite3');

const db = new sqlite.Database('./database.db', err => {
    if (!!err) throw err;
    console.log('Connected to SQLite');
});

module.exports = {
    getUser(username){
        return new Promise((res, rej) => {
            db.get(`SELECT * FROM users WHERE username = '${username}'`, (err, data) => {
                if (err) return rej(err);
                res(data);
            });
        });
    },
    checkUser(username){
        return new Promise((res, rej) => {
            db.get(`SELECT * FROM users WHERE username = ?`, username, (err, data) => {
                if (err) return rej();
                res(data === undefined);
            });
        });
    },
    createUser(username, password){
        let query = 'INSERT INTO users(username, password) VALUES(?,?)';
        let stmt = db.prepare(query);
        stmt.run(username, password);
        stmt.finalize();
    },
    attemptLogin(username, password){
        return new Promise((res, rej) => {
            db.get(`SELECT * FROM users WHERE username = ? AND password = ?`, username, password, (err, data) => {
                if (err) return rej();
                res(data !== undefined);
            });
        });
    }
}
```

Let's go ahead with first try:

```shell
./jwt_tool.py eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicGsiOiItLS0tLUJFR0lOIFBVQkxJQyBLRVktLS0tLVxuTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUE5NW9UbTlETnpjSHI4Z0xoalphWVxua3RzYmoxS3h4VU9vencwdHJQOTNCZ0lwWHY2V2lwUVJCNWxxb2ZQbFU2RkI5OUpjNVFaMDQ1OXQ3M2dnVkRRaVxuWHVDTUkyaG9VZkoxVm1qTmVXQ3JTckRVaG9rSUZaRXVDdW1laHd3dFVOdUV2MGV6QzU0WlRkRUM1WVNUQU96Z1xuaklXYWxzSGovZ2E1WkVEeDNFeHQwTWg1QUV3YkFENzMrcVhTL3VDdmhmYWpncHpIR2Q5T2dOUVU2MExNZjJtSFxuK0Z5bk5zak5Od281blJlN3RSMTJXYjJZT0N4dzJ2ZGFtTzFuMWtmL1NNeXBTS0t2T2dqNXkwTEdpVTNqZVhNeFxuVjhXUytZaVlDVTVPQkFtVGN6Mncya3pCaFpGbEg2Uks0bXF1ZXhKSHJhMjNJR3Y1VUo1R1ZQRVhwZENxSzNUclxuMHdJREFRQUJcbi0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLVxuIiwiaWF0IjoxNjY0NzIxMjg1fQ.dxo7Z1PNUiH8cCnIEsB2DFdXiDNnyluY12d4JjaSmHCD_5os3iLzChVu9hJjNK9mDbX76qcX83kYoZYlkH5MuM_RT-3llOw4MTWACbb08M2Z0QOkFuoRKK3Zy7dFKSPOKzSuvlHHFOqMAYqlvlyE_Ao4vxsZmR0I7DzVO6VqMCJAygTtuRMLauD89wdAdsXlVYSqgcu70VY8J8oeDlQRKjDw5ua6xODjbfR7b3jFFZqnJBto0qq1IuGFvdvi0bKRW_9NlLtE96eohuXdHtTMln79DHZhyfGDQlbmR_lPwpcjGfmLmVYxI1ldOawNi4YMXzNGt99lh1tk81KxDntmRQ

        \   \        \         \          \                    \ 
   \__   |   |  \     |\__    __| \__    __|                    |
         |   |   \    |      |          |       \         \     |
         |        \   |      |          |    __  \     __  \    |
  \      |      _     |      |          |   |     |   |     |   |
   |     |     / \    |      |          |   |     |   |     |   |
\        |    /   \   |      |          |\        |\        |   |
 \______/ \__/     \__|   \__|      \__| \______/  \______/ \__|
 Version 2.2.6                \______|             @ticarpi      

Original JWT: 

=====================
Decoded Token Values:
=====================

Token header values:
[+] alg = "RS256"
[+] typ = "JWT"

Token payload values:
[+] username = "admin"
[+] pk = "-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA95oTm9DNzcHr8gLhjZaY
ktsbj1KxxUOozw0trP93BgIpXv6WipQRB5lqofPlU6FB99Jc5QZ0459t73ggVDQi
XuCMI2hoUfJ1VmjNeWCrSrDUhokIFZEuCumehwwtUNuEv0ezC54ZTdEC5YSTAOzg
jIWalsHj/ga5ZEDx3Ext0Mh5AEwbAD73+qXS/uCvhfajgpzHGd9OgNQU60LMf2mH
+FynNsjNNwo5nRe7tR12Wb2YOCxw2vdamO1n1kf/SMypSKKvOgj5y0LGiU3jeXMx
V8WS+YiYCU5OBAmTcz2w2kzBhZFlH6RK4mquexJHra23IGv5UJ5GVPEXpdCqK3Tr
0wIDAQAB
-----END PUBLIC KEY-----
"
[+] iat = 1664721285    ==> TIMESTAMP = 2022-10-02 16:34:45 (UTC)

----------------------
JWT common timestamps:
iat = IssuedAt
exp = Expires
nbf = NotBefore
----------------------

```



