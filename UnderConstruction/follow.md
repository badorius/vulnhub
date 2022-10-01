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

Examine local files:

```shell
└──╼ $grep -Ri password *
helpers/DBHelper.js:    createUser(username, password){
helpers/DBHelper.js:        let query = 'INSERT INTO users(username, password) VALUES(?,?)';
helpers/DBHelper.js:        stmt.run(username, password);
helpers/DBHelper.js:    attemptLogin(username, password){
helpers/DBHelper.js:            db.get(`SELECT * FROM users WHERE username = ? AND password = ?`, username, password, (err, data) => {
routes/index.js:    const { username, password } = req.body;
routes/index.js:        || (password !== undefined && password.trim().length === 0)){
routes/index.js:        DBHelper.createUser(username, password);
routes/index.js:    let canLogin = await DBHelper.attemptLogin(username, password);
routes/index.js:        return res.redirect('/auth?error=Invalid username or password');
views/auth.html:                  <label for="password">Password</label>
views/auth.html:                  <input class="form-control input-lg" type="password" name="password" placeholder="password" />

```

