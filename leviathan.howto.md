Those write-ups don't assume much, if any, prior knowledge (I certainly didn't have much to go on when I started leviathan). So if gdb and assembly is something you're familiar with, there's much you can skip.

# Level 0

Bootstrap

# Level 1

Now that's interesting! In the other wargames (certainly bandit/krypton/vortex) each level is accompanied with some sort of description - a hint of sorts to put you in the right direction. No such luck here! We lend in a seemingly empty directory.
A quick 'ls -l' shows a .backup directory, containing a file called bookmarks.html. A quick look through the file reveals a whole bunch of links - too many to sort through manually. Thankfully a search for leviathan reveals the password to the next level.

TODO: take a closer look at the bookmarks - there might be something interesting!

# Level 2

Another 'no info' level - somehow I think this will be the norm from now on : ) We're given a binary called 'check', which asks for password. Giving the wrong password terminates the program - but there are no hints as to what the passwords might be. Passing the binary through 'strings' doesn't reveal much either. Strace is equally silent. But ltrace (library trace) opens the door for us:

    leviathan1@melissa:~$ ltrace ./check 
    __libc_start_main(0x80484d4, 1, -10236, 0x80485a0, 0x8048600 <unfinished ...>
    printf("password: ")                                                     = 10
    getchar(0x8048660, 0x8049ff4, -10408, 0x80485b9, 0xf7ea8c3dpassword: blah
    )             = 98
    getchar(0x8048660, 0x8049ff4, -10408, 0x80485b9, 0xf7ea8c3d)             = 108
    getchar(0x8048660, 0x8049ff4, -10408, 0x80485b9, 0xf7ea8c3d)             = 97
    strcmp("bla", "sex")                                                     = -1
    puts("Wrong password, Good Bye ..."Wrong password, Good Bye ...
    )                                     = 29
    +++ exited (status 0) +++
    
So it compares the first 3 characters to the word 'sex'. And sure enough:

    leviathan1@melissa:~$ ./check 
    password: sex
    $ id
    uid=12001(leviathan1) gid=12001(leviathan1) euid=12002(leviathan2) groups=12002(leviathan2),12001(leviathan1)
    
# Level 3

We are given a single binary that seemingly prints a file. Looking at the attributes, it's privilege escalation:

    leviathan2@melissa:~$ ls -l
    total 8
    -r-sr-x--- 1 leviathan3 leviathan2 7293 2012-06-28 14:54 printfile
    
Using ltrace again, we see:

    leviathan2@melissa:~$ ltrace ./printfile /tmp/mine1
    __libc_start_main(0x80484d4, 2, -10252, 0x80485b0, 0x8048610 <unfinished ...>
    access("/tmp/mine1", 4)                                                  = 0
    snprintf("/bin/cat /tmp/mine1", 511, "/bin/cat %s", "/tmp/mine1")        = 19
    system("/bin/cat /tmp/mine1" <unfinished ...>
    --- SIGCHLD (Child exited) ---
    <... system resumed> )                                                   = 0
    +++ exited (status 0) +++
    
So even though it's using snprintf (safe print), it does a call to system with whatever was pass in as an argument. The only caveat is that it checks the file we pass in for permissions (the access call) so it must exist and be owned by us. What about passing in a file whose name is essentially a command? Like '/tmp/mine;sh'

    leviathan2@melissa:~$ ./printfile "/tmp/mine;sh"
    /bin/cat: /tmp/mine: Is a directory
    $ id
    uid=12002(leviathan2) gid=12002(leviathan2) euid=12003(leviathan3) groups=12003(leviathan3),12002(leviathan2)
    
(The line about the directory is a red herring - it was probably put there by another player)

TODO: What about using symlinks??

# Level 4

That one was a rather large step above the previous level. Using ltrace didn't show any strcmp calls:

    leviathan3@melissa:~$ ltrace ./level3 
    __libc_start_main(0x8048580, 1, -10236, 0x80485b0, 0x8048610 <unfinished ...>
    __printf_chk(1, 0x80486aa, 0x80485bb, 0xf7fd2ff4, 0x80485b0)             = 20
    fgets(Enter the password> spam
    "spam\n", 256, 0xf7fd3440)                                         = 0xffffd62c
    puts("bzzzzzzzzap. WRONG"bzzzzzzzzap. WRONG
    )                                               = 19
    +++ exited (status 0) +++
    
Something happens to our input, which I assume is compared to something else in one way or another. Running 'strings' on the binary doesn't reveal much either. Just a handful of strings like snlprintf, bzzzzzap. WRONG, You've got a shell etc. To get a bit more clarity, we can dump the rodata section of the binary (where things like strings are stored - or so I'm told): 'objdump -s -j .rodata level3'. Sure enough, we see:

    leviathan3@melissa:~$ objdump -s -j .rodata level3 
    
    level3:     file format elf32-i386
    
    Contents of section .rodata:
     8048668 03000000 01000200 736e6c70 72696e74  ........snlprint
     8048678 660a005b 596f7527 76652067 6f742073  f..[You've got s
     8048688 68656c6c 5d21002f 62696e2f 73680062  hell]!./bin/sh.b
     8048698 7a7a7a7a 7a7a7a7a 61702e20 57524f4e  zzzzzzzzap. WRON
     80486a8 4700456e 74657220 74686520 70617373  G.Enter the pass
     80486b8 776f7264 3e2000                      word> .         
    
This doesn't leave us much choice apart from using gdb:

    (gdb) set disassembly-flavor intel
    (gdb) break main
    Breakpoint 1 at 0x8048583
    (gdb) run
    Starting program: /home/leviathan3/level3 
    
    Breakpoint 1, 0x08048583 in main ()
    (gdb) disassemble
    Dump of assembler code for function main:
       0x08048580 <+0>:     push   ebp
       0x08048581 <+1>:     mov    ebp,esp
    => 0x08048583 <+3>:     and    esp,0xfffffff0
       0x08048586 <+6>:     sub    esp,0x10
       0x08048589 <+9>:     mov    DWORD PTR [esp+0x4],0x80486aa
       0x08048591 <+17>:    mov    DWORD PTR [esp],0x1
       0x08048598 <+24>:    call   0x80483d0 <__printf_chk@plt>
       0x0804859d <+29>:    call   0x80484f0 <do_stuff>
       0x080485a2 <+34>:    xor    eax,eax
       0x080485a4 <+36>:    leave  
       0x080485a5 <+37>:    ret    
    End of assembler dump.
    
The function 'do_stuff' sounds interesting:

    (gdb) break do_stuff
    Breakpoint 2 at 0x80484f4
    (gdb) run
    
Once we hit the 2nd breakpoint, a quick peek through 'disassemble' yields some more information. The snippet below is of particular interest:

       0x08048525 <+53>:    call   0x80483f0 <fgets@plt>
       0x0804852a <+58>:    mov    ecx,0xb
       0x0804852f <+63>:    repz cmps BYTE PTR ds:[esi],BYTE PTR es:[edi]
       0x08048531 <+65>:    je     0x8048558 <do_stuff+104>
       0x08048533 <+67>:    mov    DWORD PTR [esp],0x8048697
    ...
    (gdb) x/s 0x8048697
    0x8048697:       "bzzzzzzzzap. WRONG"
    
Aha - we're getting closer. It sounds like if the 'repz cmps' is not successful, we'll end up with the string located at 0x8048697 and it's game over. But let's see what's being compared. For that we examine what's in esi and edi:

    (gdb) break *0x0804852f
    Breakpoint 3 at 0x804852f
    (gdb) continue
    Continuing.
    Enter the password> blah
    
    Breakpoint 3, 0x0804852f in do_stuff ()
    (gdb) x/s $edi
    0x8048670:       "snlprintf\n"
    (gdb) x/s $esi
    0xffffd5fc:      "blah\n"
    
So what I mistook for some sort of function call is actually the password? And sure enough it is!

# Level 4

A quick look through the directory reveals a hidden trash directory, containing a binary that yields what seems like a binary representation of the password (we count 10 groups, and passwords have all been 10 characters so far):

    leviathan4@melissa:~$ ls -la
    total 24
    drwxr-xr-x   3 root root       4096 2012-06-29 10:45 .
    drwxr-xr-x 128 root root       4096 2012-09-24 12:48 ..
    -rw-r--r--   1 root root        220 2011-03-31 23:20 .bash_logout
    -rw-r--r--   1 root root       3353 2011-03-31 23:20 .bashrc
    -rw-r--r--   1 root root        675 2011-03-31 23:20 .profile
    dr-xr-x---   2 root leviathan4 4096 2012-06-29 10:45 .trash
    leviathan4@melissa:~$ cd .trash/
    leviathan4@melissa:~/.trash$ ls
    bin
    leviathan4@melissa:~/.trash$ ./bin
    01010100 01101001 01110100 01101000 00110100 01100011 01101111 01101011 01100101 01101001 00001010
    
I'd guess each group of 8 bits is a character. Being eager to test that theory out, I pasted the string above in this web site and got what looked like a 10-character password for leviathan 5. And I was right ^_^

TODO: Follow-up on the below

But that's not much fun and a bit too obvious. So let's use gdb once more and see what we can find. But something's not right:

    (gdb) break main
    Breakpoint 1 at 0x8048467
    (gdb) run
    Starting program: /home/leviathan4/.trash/bin 
    
    Breakpoint 1, 0x08048467 in main ()
    (gdb) continue
    Continuing.
    
    Program exited with code 0377.
    
Exit code 0377? Looking at the manual for 'exit(3)', we see this function returns 'status & 0377' so status must have been 0xffff. Nothing much to see here. Going back to the disassembly, we see a call to fopen - so let's see what arguments are being passed:

    (gdb) break *0x0804847f
    ...
       0x0804847c <+24>:    mov    DWORD PTR [esp],eax
    => 0x0804847f <+27>:    call   0x80483a0 <fopen@plt>
    ...
    (gdb) x/s $eax
    0x8048614:       "/etc/leviathan_pass/leviathan5"
    
Okay - so it opens up the password for level 5. So far so good.

# Level 5

The binary given seems to expect a file named '/tmp/file.log'. A quick go at creating a file shows the program just outputs its content (echo 'yo' > /tmp/file.log) and then deletes the file. So why not create a symlink to the next level?

    leviathan5@melissa:~$ ln -s /etc/leviathan_pass/leviathan6 /tmp/file.log
    leviathan5@melissa:~$ ./leviathan5 
    UgaoFee4li

Mmm. Is that really it?

# Level 6

This level has a very easy solution. But after disassembling binaries for most of this game, the 'simpler' solution only came to me after spending longer than I feel comfortable admitting. My first point of call was to fire up gdb (bad habit)... The disassembly for the whole binary is actually quite small:

    Breakpoint 1, 0x080484b7 in main ()
    (gdb) disass
    Dump of assembler code for function main:
       0x080484b4 <+0>:     push   ebp
       0x080484b5 <+1>:     mov    ebp,esp
    => 0x080484b7 <+3>:     and    esp,0xfffffff0
       0x080484ba <+6>:     sub    esp,0x20
       0x080484bd <+9>:     mov    DWORD PTR [esp+0x1c],0x1bd3
       0x080484c5 <+17>:    cmp    DWORD PTR [ebp+0x8],0x2
       0x080484c9 <+21>:    je     0x80484ed <main+57>
       0x080484cb <+23>:    mov    eax,DWORD PTR [ebp+0xc]
       0x080484ce <+26>:    mov    edx,DWORD PTR [eax]
       0x080484d0 <+28>:    mov    eax,0x80485f0
       0x080484d5 <+33>:    mov    DWORD PTR [esp+0x4],edx
       0x080484d9 <+37>:    mov    DWORD PTR [esp],eax
       0x080484dc <+40>:    call   0x80483a4 <printf@plt>
       0x080484e1 <+45>:    mov    DWORD PTR [esp],0xffffffff
       0x080484e8 <+52>:    call   0x80483e4 <exit@plt>
       0x080484ed <+57>:    mov    eax,DWORD PTR [ebp+0xc]
       0x080484f0 <+60>:    add    eax,0x4
       0x080484f3 <+63>:    mov    eax,DWORD PTR [eax]
       0x080484f5 <+65>:    mov    DWORD PTR [esp],eax
       0x080484f8 <+68>:    call   0x80483b4 <atoi@plt>
       0x080484fd <+73>:    cmp    eax,DWORD PTR [esp+0x1c]
       0x08048501 <+77>:    jne    0x804851d <main+105>
       0x08048503 <+79>:    mov    DWORD PTR [esp],0x3ef
       0x0804850a <+86>:    call   0x80483d4 <seteuid@plt>
       0x0804850f <+91>:    mov    DWORD PTR [esp],0x804860a
       0x08048516 <+98>:    call   0x8048384 <system@plt>
       0x0804851b <+103>:   jmp    0x8048529 <main+117>
       0x0804851d <+105>:   mov    DWORD PTR [esp],0x8048612
       0x08048524 <+112>:   call   0x80483c4 <puts@plt>
       0x08048529 <+117>:   leave  
       0x0804852a <+118>:   ret    
    
We can spot a few things quite quickly. For instance, the call to seteuid. So the:

       0x080484fd <+73>:    cmp    eax,DWORD PTR [esp+0x1c]
       0x08048501 <+77>:    jne    0x804851d <main+105>
    
is our ticket home. Here we're comparing eax with whatever's in esp+0x1c.

    (gdb) x/d $esp+0x1c
    0xffffd70c:     7123
    
7123? Wait - isn't that the same as:

    mov    DWORD PTR [esp+0x1c],0x1bd3

at the beginning? Tada! 

Taking a step back however, it's just a case of brute-forcing the binary - and as far as I could tell, there was no induced delay. 4 digits, that's 10^4 possibilities. A simple bash expression would have meant we'd be home free pretty quickly:

    leviathan5@melissa:~$ for i in `seq -w 7000 9999`; do echo ${i};./leviathan6 ${i}; done
    ...
    7122
    Wrong
    7123
    $ whoami
    leviathan7
    
So trying the simplest solution first would have saved me some time. Heh...

And this is a last of leviathan. To be fair though, I would have liked to spend more time understanding the assembly code itself. And I think some basic understanding is definitely required. But if I were to do this full time, I'd invest some serious money into getting a license for IDAPro. Some compilers will re-arrange expressions to optimise code - and that would probably lead to even more obfuscated code. But as a starting point, this challenge has proved to be very educational and I wouldn't hesitate to whip out gdb again.
