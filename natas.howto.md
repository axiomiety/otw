# Level 0

View source

# Level 1

View source (but you can't use the right-click menu - use your browser's menu for that)

# Level 2

The source reveals the source of an image as being 'files/pixel.png'. We can list the contents of this [directory](http://natas2.natas.labs.overthewire.org/files), and users.txt contains the password for the next level.

# Level 3

That one is more interesting. The source gives us a hint by saying Google won't find it. Most sites have a file called [robots.txt](http://www.javascriptkit.com/howto/robots.shtml) - and sure enough [this](http://natas3.natas.labs.overthewire.org/robots.txt) gives us the name of another [directory](http://natas3.natas.labs.overthewire.org/s3cr3t/) containing another users.txt file.

# Level 4

The landing page for this level tells us we are being referred from the wrong page (natas4 instead of natas5). But we do not have access to natas5 yet. What index.php is doing is checking the Referer tag in the headers. This can easily be tweaked by using the 'Modify Headers' addon for Firefox. Just set the 'Referer' tag to http://natas5.natas.labs.overthewire.org, start the addon and refresh the page. It will now give us the next password.

# Level 5

The initial message is a bit cryptic. It seems we're not logged in, but looking at the source doesn't reveal anything. What about cookies? Sure enough the site stored a cookie with us. Using an addon such as 'Cookie Manager+', we see natas5 stored a cookie named 'loggedin' with content set to 0. Changing that to 1 and reload the page gets us in.

# Level 6

The source (using the link on the page, not from the browser) yields this piece of code:

    include "includes/secret.inc";

    if(array_key_exists("submit", $_POST)) {
        if($secret == $_POST['secret']) {

So we're looking for the value of $secret. By accessing the [include file](http://natas6.natas.labs.overthewire.org/includes/secret.inc) we get hold of that value. We insert it in the form and we're done.

# Level 7

The hint in the page's source tells us the password is located in /etc/natas_webpass/natas8. We also see the index.php page takes an argument referencing a section (home, about), which could well be a path on the file system. And indeed referencing the [password file](http://natas7.natas.labs.overthewire.org/index.php?page=/etc/natas_webpass/natas8) above gets us in.

# Level 8

The source listing tells us how user input is transformed before being compared to the 'right' value. Reading the transformation function from inside out, input is first encoded in base64, then reversed (strrev) and then converted from binary to hexadecimal. So in order to reverse the encoded value we need to perform the reverse.

1.  bin2hex converts an ASCII string into hexadecimal. 3d3d516343746d4d6d6c315669563362 -> ==QcCtmMml1ViV3b
2.  strrev reverses the string - so unreversing it: ==QcCtmMml1ViV3b -> b3ViV1lmMmtCcQ==
3.  and decoding it from base64: b3ViV1lmMmtCcQ== -> oubWYf2kBq

Using this as the input secret gets us there.

# Level 9

At first glance the code snippet allows us to look for a particular word (case insensitive) in a file called dictionary.txt. I first thought the password would be in the file somehow - and to display it all, grepping for new line (\n) does list the contents. However a quick glance through the file doesn't reveal anything interesting. But as we have free reign with the input, we can just as easily grep through anything else. In level 7 we were told some password files were located in /etc/natas_webpass. And by [crafting our input](http://natas9.natas.labs.overthewire.org/?needle=\n%20/etc/natas_webpass/natas10&submit=Search) (\n /etc/natas_webpass/natas10) we can get the script to display its contents.

# Level 10

Very similar to the previous level. However this time characters like ';' and '&' are not allowed. Not a problem since we didn't use any. However the input we used previously doesn't seem to work. Maybe there are no new lines in this file. Instead we grab any letter (remember it's case insensitive) by using '[a-z] /etc/natas_webpass/natas11' and voila.

# Level 11
