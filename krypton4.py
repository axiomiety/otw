#!/usr/bin/python
import operator
import sys

def getMonsubCyphertext(f, keylength=6):
	cyphertexts = {}
	with open(f, 'r') as fh:
		for line in fh:
			# remove spaces
			s = line.replace(' ', '')
			for k in range(0, keylength):
				cyphertexts[k] = list()
				for i in range(k, len(s), keylength):
					cyphertexts[k].append(s[i])
	for c in cyphertexts:
		txt = ''.join(cyphertexts[c])
		print txt
		freq(txt)

def freq(text):
	t = text.replace(' ', '')
	freqs = {}
	for c in t:
		count = freqs.get(c, 0)
		freqs[c] = count + 1
	byfreq = sorted(freqs.iteritems(), key=operator.itemgetter(1))
	byfreq.reverse()
	for (c, f) in byfreq:
		print '%s=%s' % (c, f)


def main(argv=None):
	if not argv:
		argv = sys.argv
	getMonsubCyphertext(sys.argv[1])

if __name__ == '__main__':
	main()
