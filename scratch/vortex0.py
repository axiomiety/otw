#!/usr/bin/python
'''
References:
http://docs.python.org/library/socket.html
http://docs.python.org/library/struct.html
'''

import socket
import struct

hostname='vortex.labs.overthewire.org'
port=5842

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((hostname, port))

data = list()
for i in xrange(4): # 4 integers in host byte order, which we know is x86 (little endian)
	data.append(struct.unpack('<I', s.recv(4))[0])

# the sum of our 4 ints need to overflow into an int and not a long
# as the sender expects an int back (stated in the brief)
s.send(struct.pack('<I', sum(data) % 2**32))
print s.recv(2048) # arbitrary length, but should be enough
s.close()
