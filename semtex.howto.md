# Level 0

We need to open a connection to the given host:port (for your current architecture) - and discard every second byte. That's about 10 lines of python (see semtex0.py in /otw/scratch).

# Level 1
I wish I could say there was some consistent approach but it was a lot of trial and error. Using the `-v` flag I noticed the chain is always 100 repetitions long. And that by changing a single letter in the plaintext, a single letter in the ciphertext changed. However the position at which it changed differed depending on the length of the input. And clearly the encryption wasn't symmetric (encrypting the resulting ciphertext did not yield the plaintext - had to try...).first

I then tried encrypting a string of 10 characters composed of the same letter ('AAAAAAAAAA'). Using the verbose input, some sort of pattern emerged. The chain was repeated every 10 blocks, with the ciphertext/plaintext following one another. And if encrypted the corresponding ciphertext ('AZZZYYXWVT'), the verbose output would display the plaintext periodically. And somehow the intermediary results (`-v`) seemed to match. That's when it struck me that it might simply be some sort of iterative process.

However for the length of the given encrypted text (13 chars), it was harder to see a similar pattern. But the chaining of the results was clear so I decided to feed the ciphertext back to the encryption tool, thinking that 'at some point' the plaintext was going to appear in the chain. But how was I going to figure out what the plaintext was? I whipped up the below to check:

    semtex1@melissa:/semtex$ ./semtex1 AAAAAAAAAAAAA
    encrypting "AAAAAAAAAAAAA"
    encryption finished: AXMDNNPKTEKUL
    semtex1@melissa:/semtex$ a='AXMDNNPKTEKUL';for i in {1..520};do echo $a;a=`./semtex1 $a | grep finished | cut -d' ' -f3`;done > /var/tmp/s1.1          semtex1@melissa:/semtex$ grep -n AAAAA /var/tmp/s1.1
    364:AAAAAAAAAAAAA

Trying with different plaintexts always led to those being repeated on the same line (520 = 26*20 - an educated guess as to the maximum number of iterations needed before the plaintext shows itself in the chain). Repeating the procedure above with a='HRXDZNWEAWWCP' and grabbing line 364 of the output gave me the required result.

# Level 2

It looks like we need to change our EUID to 666. A quick look at `semtex2` through `strace`:

    munmap(0xf7fd8000, 20942)               = 0
    geteuid32()                             = 6002
    fstat64(1, {st_mode=S_IFCHR|0620, st_rdev=makedev(136, 8), ...}) = 0
    mmap2(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0xfffffffff7fdd000
    write(1, "EUID == 6002\n", 13EUID == 6002
    )          = 13
    write(1, "This is not the devils number. T"..., 50This is not the devils number. Think dynamically!
    ) = 50
    exit_group(0)

shows the `getuid32` call. The hint is pretty clear about what needs to be done, so let's see if we can intercept that call and replace it with something else:

    #include <unistd.h>
    #include <sys/types.h>
    
    uid_t
    geteuid(void)
    {
      unsigned int euid = 666;
      return euid;
    }
    
(uid_t is just an unsigned int: http://www.cs.fsu.edu/~baker/devices/lxr/http/source/linux/arch/x86/include/asm/posix_types_32.h#L30).

One thing to note however (which delayed me for a while) is that this is a *32bit* call - and the target machine is *64bit*. So when compiling this with `gcc`, make sure you pass in the `m32` flag. Once you've got your shared library, load it up using `LD_PRELOAD` as such:

    export LD_PRELOAD=/var/tmp/ss2.so; ./semtex2

And voila.

# Level 3

Right - not so much a wargame as much as a maths one (or something you might get in some annoying RPG). Pressing 1-8 changes locks L1-L5 by a particular amount:

    #| L1| L2|L3|L4| L5
    -------------------
    1|  5|  2| 1| 7|  5
    2| 13| -7|-4| 1|  5
    3|  9| 12| 9|70| -4
    4|-11|  9| 0| 5|-13
    5|  4| 17|12| 9| 24
    6| 11|-17|21| 5| 14
    7| 26| 14|43|-7| 17
    8| 19|-12| 4| 3| -7

We notice some somehow be added to either negate or magnify some changes. For instance the 5/6 or 6/5 combination leaves L2 untouched. So ideally we want to find a series of moves which end up moving all locks in lockstep (haha). But who am I kidding - seeing the above brought back memories of simlutaneous equations. The only downside however is that we have more unknowns than equations:

    5*a+13*b+ 9*c-11*d+ 4*e+11*f+15*g+19*h=100
    2*a -7*b+12*c+ 9*d+17*e-17*f+31*g-12*h=100
    1*a -4*b+ 9*c+ 0*d+12*e+21*f+22*g+ 4*h=100
    7*a+ 1*b+70*c+ 5*d+ 9*e+ 5*f-12*g+ 3*h=100
    5*a+ 5*b -4*c-13*d+24*e+14*f+ 3*g- 7*h=100

and online simultaneous equations solvers didn't yield much. So instead I wrote a quick brute force solver under certain assumptions (eg, each lock needs to be activated at most 9 times). It's not efficient at all but it took me 2mns to write and got me a solution while I was making a cup of tea, so time well spent. Head over to `otw/scratch` for the source (I should note the solver gives the number of times each lock should be activated).

# Level 4
