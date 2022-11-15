# Shooting star Write up

We are very screwed, but here we go! Check file.

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

check security:

```shell
gdb  ./shooting_star                                                                                                               main 
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
Reading symbols from ./shooting_star...
(No debugging symbols found in ./shooting_star)
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

Lets take a look with ghidra:




```shell
gdb ./shooting_star                                                                                                                  main 

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
Reading symbols from ./shooting_star...
(No debugging symbols found in ./shooting_star)
gdb-peda$ start
[----------------------------------registers-----------------------------------]
RAX: 0x401230 (<main>:	push   rbp)
RBX: 0x7fffffffe738 --> 0x7fffffffea08 ("/home/darthv/git/badorius/vulnhub/hackthebox/ShootingStar/Files/shooting_star")
RCX: 0x7ffff7f83760 --> 0x7ffff7f85220 --> 0x0 
RDX: 0x7fffffffe748 --> 0x7fffffffea56 ("SHELL=/bin/bash")
RSI: 0x7fffffffe738 --> 0x7fffffffea08 ("/home/darthv/git/badorius/vulnhub/hackthebox/ShootingStar/Files/shooting_star")
RDI: 0x1 
RBP: 0x7fffffffe620 --> 0x1 
RSP: 0x7fffffffe620 --> 0x1 
RIP: 0x401234 (<main+4>:	mov    eax,0x0)
R8 : 0x4012d0 (<__libc_csu_fini>:	ret)
R9 : 0x7ffff7fce890 (endbr64)
R10: 0x7fffffffe350 --> 0x800000 
R11: 0x202 
R12: 0x0 
R13: 0x7fffffffe748 --> 0x7fffffffea56 ("SHELL=/bin/bash")
R14: 0x0 
R15: 0x7ffff7ffd000 --> 0x7ffff7ffe2c0 --> 0x0
EFLAGS: 0x246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x40122f <setup+66>:	ret    
   0x401230 <main>:	push   rbp
   0x401231 <main+1>:	mov    rbp,rsp
=> 0x401234 <main+4>:	mov    eax,0x0
   0x401239 <main+9>:	call   0x4011ed <setup>
   0x40123e <main+14>:	mov    edx,0x5b
   0x401243 <main+19>:	lea    rsi,[rip+0x103e]        # 0x402288
   0x40124a <main+26>:	mov    edi,0x1
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe620 --> 0x1 
0008| 0x7fffffffe628 --> 0x7ffff7dce290 (mov    edi,eax)
0016| 0x7fffffffe630 --> 0x7fffffffe720 --> 0x7fffffffe728 --> 0x38 ('8')
0024| 0x7fffffffe638 --> 0x401230 (<main>:	push   rbp)
0032| 0x7fffffffe640 --> 0x100400040 
0040| 0x7fffffffe648 --> 0x7fffffffe738 --> 0x7fffffffea08 ("/home/darthv/git/badorius/vulnhub/hackthebox/ShootingStar/Files/shooting_star")
0048| 0x7fffffffe650 --> 0x7fffffffe738 --> 0x7fffffffea08 ("/home/darthv/git/badorius/vulnhub/hackthebox/ShootingStar/Files/shooting_star")
0056| 0x7fffffffe658 --> 0xf1973c2fba3d9131 
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Temporary breakpoint 1, 0x0000000000401234 in main ()
gdb-peda$ pattern create 1000
'AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAASAApAATAAqAAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyAAzA%%A%sA%BA%$A%nA%CA%-A%(A%DA%;A%)A%EA%aA%0A%FA%bA%1A%GA%cA%2A%HA%dA%3A%IA%eA%4A%JA%fA%5A%KA%gA%6A%LA%hA%7A%MA%iA%8A%NA%jA%9A%OA%kA%PA%lA%QA%mA%RA%oA%SA%pA%TA%qA%UA%rA%VA%tA%WA%uA%XA%vA%YA%wA%ZA%xA%yA%zAs%AssAsBAs$AsnAsCAs-As(AsDAs;As)AsEAsaAs0AsFAsbAs1AsGAscAs2AsHAsdAs3AsIAseAs4AsJAsfAs5AsKAsgAs6AsLAshAs7AsMAsiAs8AsNAsjAs9AsOAskAsPAslAsQAsmAsRAsoAsSAspAsTAsqAsUAsrAsVAstAsWAsuAsXAsvAsYAswAsZAsxAsyAszAB%ABsABBAB$ABnABCAB-AB(ABDAB;AB)ABEABaAB0ABFABbAB1ABGABcAB2ABHABdAB3ABIABeAB4ABJABfAB5ABKABgAB6ABLABhAB7ABMABiAB8ABNABjAB9ABOABkABPABlABQABmABRABoABSABpABTABqABUABrABVABtABWABuABXABvABYABwABZABxAByABzA$%A$sA$BA$$A$nA$CA$-A$(A$DA$;A$)A$EA$aA$0A$FA$bA$1A$GA$cA$2A$HA$dA$3A$IA$eA$4A$JA$fA$5A$KA$gA$6A$LA$hA$7A$MA$iA$8A$NA$jA$9A$OA$kA$PA$lA$QA$mA$RA$oA$SA$pA$TA$qA$UA$rA$VA$tA$WA$uA$XA$vA$YA$wA$ZA$x'

gdb-peda$ run
Starting program: /home/darthv/git/badorius/vulnhub/hackthebox/ShootingStar/Files/shooting_star 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/libthread_db.so.1".
🌠 A shooting star!!
1. Make a wish!
2. Stare at the stars.
3. Learn about the stars.
> 1
>> 'AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAASAApAATAAqAAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyAAzA%%A%sA%BA%$A%nA%CA%-A%(A%DA%;A%)A%EA%aA%0A%FA%bA%1A%GA%cA%2A%HA%dA%3A%IA%eA%4A%JA%fA%5A%KA%gA%6A%LA%hA%7A%MA%iA%8A%NA%jA%9A%OA%kA%PA%lA%QA%mA%RA%oA%SA%pA%TA%qA%UA%rA%VA%tA%WA%uA%XA%vA%YA%wA%ZA%xA%yA%zAs%AssAsBAs$AsnAsCAs-As(AsDAs;As)AsEAsaAs0AsFAsbAs1AsGAscAs2AsHAsdAs3AsIAseAs4AsJAsfAs5AsKAsgAs6AsLAshAs7AsMAsiAs8AsNAsjAs9AsOAskAsPAslAsQAsmAsRAsoAsSAspAsTAsqAsUAsrAsVAstAsWAsuAsXAsvAsYAswAsZAsxAsyAszAB%ABsABBAB$ABnABCAB-AB(ABDAB;AB)ABEABaAB0ABFABbAB1ABGABcAB2ABHABdAB3ABIABeAB4ABJABfAB5ABKABgAB6ABLABhAB7ABMABiAB8ABNABjAB9ABOABkABPABlABQABmABRABoABSABpABTABqABUABrABVABtABWABuABXABvABYABwABZABxAByABzA$%A$sA$BA$$A$nA$CA$-A$(A$DA$;A$)A$EA$aA$0A$FA$bA$1A$GA$cA$2A$HA$dA$3A$IA$eA$4A$JA$fA$5A$KA$gA$6A$LA$hA$7A$MA$iA$8A$NA$jA$9A$OA$kA$PA$lA$QA$mA$RA$oA$SA$pA$TA$qA$UA$rA$VA$tA$WA$uA$XA$vA$YA$wA$ZA$x'

May your wish come true!

Program received signal SIGSEGV, Segmentation fault.

[----------------------------------registers-----------------------------------]
RAX: 0x1a 
RBX: 0x7fffffffe738 ("%qA%UA%rA%VA%tA%WA%uA%XA%vA%YA%wA%ZA%xA%yA%zAs%AssAsBAs$AsnAsCAs-As(AsDAs;As)AsEAsaAs0AsFAsbAs1AsGAscAs2AsHAsdAs3AsIAseAs4AsJAsfAs5AsKAsgAs6AsLAshAs7AsMJ\354\377\377\377\177")
RCX: 0x7ffff7ea20b4 (<write+20>:	cmp    rax,0xfffffffffffff000)
RDX: 0x1a 
RSI: 0x40200c ("\nMay your wish come true!\n")
RDI: 0x1 
RBP: 0x4133414164414148 ('HAAdAA3A')
RSP: 0x7fffffffe618 ("AIAAeAA4AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAASAApAATAAqAAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyAAzA%%A%sA%BA%$A%nA%CA%-A%(A%DA%;A%)A%EA%aA%0A%FA%bA%1A%GA%cA%2A%HA%dA%3"...)
RIP: 0x4011ec (<star+170>:	ret)
R8 : 0x4012d0 (<__libc_csu_fini>:	ret)
R9 : 0x7ffff7fce890 (endbr64)
R10: 0x3 
R11: 0x202 
R12: 0x0 
R13: 0x7fffffffe748 ("WA%uA%XA%vA%YA%wA%ZA%xA%yA%zAs%AssAsBAs$AsnAsCAs-As(AsDAs;As)AsEAsaAs0AsFAsbAs1AsGAscAs2AsHAsdAs3AsIAseAs4AsJAsfAs5AsKAsgAs6AsLAshAs7AsMJ\354\377\377\377\177")
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
0000| 0x7fffffffe618 ("AIAAeAA4AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAASAApAATAAqAAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyAAzA%%A%sA%BA%$A%nA%CA%-A%(A%DA%;A%)A%EA%aA%0A%FA%bA%1A%GA%cA%2A%HA%dA%3"...)
0008| 0x7fffffffe620 ("AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAASAApAATAAqAAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyAAzA%%A%sA%BA%$A%nA%CA%-A%(A%DA%;A%)A%EA%aA%0A%FA%bA%1A%GA%cA%2A%HA%dA%3A%IA%eA%"...)
0016| 0x7fffffffe628 ("5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAASAApAATAAqAAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyAAzA%%A%sA%BA%$A%nA%CA%-A%(A%DA%;A%)A%EA%aA%0A%FA%bA%1A%GA%cA%2A%HA%dA%3A%IA%eA%4A%JA%fA"...)
0024| 0x7fffffffe630 ("A6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAASAApAATAAqAAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyAAzA%%A%sA%BA%$A%nA%CA%-A%(A%DA%;A%)A%EA%aA%0A%FA%bA%1A%GA%cA%2A%HA%dA%3A%IA%eA%4A%JA%fA%5A%KA%g"...)
0032| 0x7fffffffe638 ("AA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAASAApAATAAqAAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyAAzA%%A%sA%BA%$A%nA%CA%-A%(A%DA%;A%)A%EA%aA%0A%FA%bA%1A%GA%cA%2A%HA%dA%3A%IA%eA%4A%JA%fA%5A%KA%gA%6A%LA%"...)
0040| 0x7fffffffe640 ("iAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAASAApAATAAqAAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyAAzA%%A%sA%BA%$A%nA%CA%-A%(A%DA%;A%)A%EA%aA%0A%FA%bA%1A%GA%cA%2A%HA%dA%3A%IA%eA%4A%JA%fA%5A%KA%gA%6A%LA%hA%7A%MA"...)
0048| 0x7fffffffe648 ("AjAA9AAOAAkAAPAAlAAQAAmAARAAoAASAApAATAAqAAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyAAzA%%A%sA%BA%$A%nA%CA%-A%(A%DA%;A%)A%EA%aA%0A%FA%bA%1A%GA%cA%2A%HA%dA%3A%IA%eA%4A%JA%fA%5A%KA%gA%6A%LA%hA%7A%MA%iA%8A%N"...)
0056| 0x7fffffffe650 ("AAkAAPAAlAAQAAmAARAAoAASAApAATAAqAAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyAAzA%%A%sA%BA%$A%nA%CA%-A%(A%DA%;A%)A%EA%aA%0A%FA%bA%1A%GA%cA%2A%HA%dA%3A%IA%eA%4A%JA%fA%5A%KA%gA%6A%LA%hA%7A%MA%iA%8A%NA%jA%9A%"...)
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x00000000004011ec in star ()
gdb-peda$ AsiAs8AsNAsjAs9AsOAskAsPAslAsQAsmAsRAsoAsSAspAsTAsqAsUAsrAsVAstAsWAsuAsXAsvAsYAswAsZAsxAsyAszAB%ABsABBAB$ABnABCAB-AB(ABDAB;AB)ABEABaAB0ABFABbAB1ABGABcAB2ABHABdAB3ABIABeAB4ABJABfAB5ABKABgAB6ABLABhAB7ABMABiAB8ABNABjAB9ABOABkABPABlABQABmABRABoABSABpABTABqABUABrABVABtABWABuABXABvABYABwABZABxAByABzA$%A$sA$BA$$A$nA$CA$-A$(A$DA$;A$)A$EA$aA$0A$FA$bA$1A$GA$cA$2A$HA$dA$3A$IA$eA$4A$JA$fA$5A$KA$gA$6A$LA$hA$7A$MA$iA$8A$NA$jA$9A$OA$kA$PA$lA$QA$mA$RA$oA$SA$pA$TA$qA$UA$rA$VA$tA$WA$uA$XA$vA$YA$wA$ZA$x'
Undefined command: "AsiAs8AsNAsjAs9AsOAskAsPAslAsQAsmAsRAsoAsSAspAsTAsqAsUAsrAsVAstAsWAsuAsXAsvAsYAswAsZAsxAsyAszAB".  Try "help".
gdb-peda$ pattern search
Registers contain pattern buffer:
RBP+0 found at offset: 63
Registers point to pattern buffer:
[RBX] --> offset 359 - size ~173
[RSP] --> offset 71 - size ~203
[R13] --> offset 375 - size ~157
Pattern buffer not found in memory
Reference to pattern buffer not found in memory
gdb-peda$ 

```


CHALLENGE DESCRIPTION

Tired of exploring the never-ending world, you lie down and enjoy the crystal clear sky. Over a million stars above your head! Enjoy the silence and the glorious stars while you rest.
