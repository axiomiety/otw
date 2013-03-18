#!/usr/bin/python
import operator
import sys

#kk=krypton5.keyCombi([('Y'),('L','R'),('R', 'V', 'Z','Y', 'M', 'S','P', 'X', 'T'),('R','Y'),('L')])
#[krypton5.decryptText('BELOSZ',x) for x in [krypton5.inverse(k) for k in [''.join(i) for i in kk]]]

class memoize:
  def __init__(self, function):
    self.function = function
    self.memoized = {}

  def __call__(self, *args):
    try:
      return self.memoized[args]
    except KeyError:
      self.memoized[args] = self.function(*args)
      return self.memoized[args]

@memoize
def VIGENERE_QUADRAT():
  alphabet = [chr(c) for c in range(ord('A'), ord('Z')+1)]
  offset = ord('A')
  quadrat = dict()
  for i in range(0, 26):
    quadrat[ chr(i+offset) ] = alphabet[i:] + alphabet[:i]

  return quadrat

def charIndex(c):
  return ord(c)-ord('A')

def encrypt(k,p):
  return VIGENERE_QUADRAT()[k][charIndex(p)]

def decrypt(k,c):
  return chr(VIGENERE_QUADRAT()[k].index(c)+ord('A'))

def getKeyForText(text, key):
  '''
  Needs len(text) >= len(key)
  '''
  keyLength = len(key)
  textLength = len(text)
  numRepeats = textLength / keyLength
  rem = textLength % keyLength
  return key*numRepeats + key[:rem] 

def inverse(crypt):
  text = 'E' * len(crypt)
  t = list()
  for (k, c) in zip(crypt, text):
    t.append(decrypt(c, k)) # invert key and plaintext
  return ''.join(t)

def decryptText(crypt, key):
  t = list()
  for (k, c) in zip(getKeyForText(crypt, key), crypt):
    t.append(decrypt(k, c))
  return ''.join(t)

def keyCombi(lst):
  res = [[r] for r in lst[0]]
  for i in range(1,len(lst)):
    res = [r + [k] for r in res for k in lst[i]]
  return res

def keyCombi2(ll):
  res = [[]]
  for r in ll:
    for q in r:
      res.append([subset + [q] for subset in res])
  return r

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
  freqs = {}
  for c in cyphertexts:
    txt = ''.join(cyphertexts[c])
    #print txt
    freqs[c] = freq(txt)
  return freqs

def freq(text):
  t = text.replace(' ', '')
  freqs = {}
  for c in t:
    count = freqs.get(c, 0)
    freqs[c] = count + 1
  byfreq = sorted(freqs.iteritems(), key=operator.itemgetter(1))
  byfreq.reverse()
  return (byfreq[0][0], byfreq[1][0], byfreq[2][0])
  #return (byfreq[0], byfreq[1])

def main(argv=None):
  if not argv:
    argv = sys.argv
  for f in ['found1','found2','found3']:
      #maxlen = 6
      d = {}
      #for length in range(3,maxlen):
      for length in [int(sys.argv[1])]:
        d[length] = getMonsubCyphertext(f,length)
      for (k, v) in d.iteritems():
        print 'yooooo'
        print k
        #print ''.join([b for (a,b) in v.items()])
        print v.values()
        #key = inverse(''.join(v.values()))
        #print decryptText('BELOSZ', key)
  
if __name__ == '__main__':
  main()
