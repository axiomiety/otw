#!/usr/bin/python
import sys
import getopt

def rotate(c, offset):
	newc = ord(c) + offset
	if newc > ord('Z'):
		newc = newc - 26
	return chr(newc) 

def decrypt(plaintext):
	for offset in xrange(0,26):
		print ''.join(map(lambda x: rotate(x, offset), plaintext))

def main(argv=None):
		if not argv:
			argv = sys.argv
		print argv
		if len(argv) == 2:
			decrypt(argv[1])

if __name__ == '__main__':
	main()
