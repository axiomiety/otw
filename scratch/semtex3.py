#!/usr/bin/python

a=b=c=d=e=f=g=h=0

for z in xrange(0,99999999):
  z = str(z)
  z = z.zfill(8)
  (a,b,c,d,e,f,g,h) = map(int, str(z))
  if 5*a+13*b+ 9*c-11*d+ 4*e+11*f+15*g+19*h==100 \
    and 2*a -7*b+12*c+ 9*d+17*e-17*f+31*g-12*h==100 \
    and 1*a -4*b+ 9*c+ 0*d+12*e+21*f+22*g+ 4*h==100 \
    and 7*a+ 1*b+70*c+ 5*d+ 9*e+ 5*f-12*g+ 3*h==100 \
    and 5*a+ 5*b -4*c-13*d+24*e+14*f+ 3*g- 7*h==100:
    print 'solution found! %s' % ''.join(map(str,[a,b,c,d,e,f,g,h]))
    break
