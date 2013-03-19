# Level 0

The aim of level 0 is to add up 4 unsigned ints recv'ed by the server, send the total, and read back the credentials for level 1. Fairly straight forward, though I did get caught out by the uint32 overflow (the server expects an unsigned int back, even if the sum overflows).

Takeaways: make sure to read the brief fully.

Taking it further: write a C program to look at how overflows are handled

# Level 1

Looking at the code behind `/vortex/vortex1`, it looks like an underflow (not overflow) will force the binary to drop us a shell with the required privileges. We see that for this to happens, `ptr & 0xff000000` must equal `0xca000000`. So essentially, `ptr` must be `0xcaXXXXXX` (we don't care about the X, as X & 0 = 0 for all X). Ptr is initialised at buf + 256. So if we input `'\'` 256 times, we will have `ptr == buf`. But that still doesn't allow us to overwrite ptr's value. For this, we need to go back one more and then we can pass in `'\xca'` - now all we need is an extra character to trigger e().
While this gives us a shell however, it somehow seems to terminate abruptly. After some frustrating trial and error, I decided to backtrack and re-examine `vortex1.c`. `/bin/sh` was invoked with `sh` and `-i`. Out of interest (as in, by luck), I did an `ls -l` on `/bin/sh` and found out it pointed to something called dash. Executing `dash` dropped me in a shell, and an `echo $SHELL` let me know I was actually using bash. So `e()` actually calls a  bash-like shell to execute sh in interactive mode.
The problem with interactive mode is that it will exit as soon as it gets an EOF. And somehow the pipe we send generates an EOF before we get to pass in any commands - making the exploit a bit moot (we've got a shell we can't do anything with...). So the solution would seem to be either to stop EOF from being sent, or having the shell ignore it - and I made no progress on either. I did however manage to find this link which states that when bash is invoke with sh, it will execute the file in the ENV variable. Sure enough, creating a file with the command I wanted to run (`cat /etc/vortext_pass/vortex2`) and setting this in ENV before underflowing ptr yielded the password for Level 2. Wah!

Takeaways: it took me a while before I decided to try the code out locally. If source is available, a bunch of debug statements can prove very handy.

Taking it further: compile with debug statements, use gdb to step through and trigger the exploit

# Level 2

We have to create a 'special' tar file. A quick look on `man tar` (if you need to) will show that `tar -cf file.tar 1 2 3` will create file.tar, including files 1, 2 and 3. `$$` in bash will return the pid of the running process. I'm not entirely sure what's expected at this point in time - except that I would very like to get the contents of `/etc/vortex_pass/vortex3`. A quick look at `/vortex/vortex2` shows that this executable is owned by vortex3 - so it will execute tar with vortex3 permissions!
Sure enough, we can add `/etc/vortex_pass/vortex3` to the archive and extract it locally to get hold of the password. Job done!

Takeaways: 'knowing' how to use a tool probably covers about 20% of the use-cases used 80% of the time

Taking it further: N/A

# Level 3

Some more buffer-based exploitation?
