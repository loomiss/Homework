from __future__ import division
import matplotlib, sys
import pylab, numpy, os, glob
import math

dx = 0.01
D=2000
vinit=500.
V=.5
k=V/vinit
lam=(math.sqrt(4+2*k**2*D**2)-2)/(k*D**2)
x=numpy.arange(0,D,dx)
y=lam*x*(D-x)
yprime=lam*(D-2*x)

#time integral:
i=0
t=0
for i in range(len(x)-1):
    t+=(dx*(1+(1/2)*yprime[i]**2))/(vinit*(1+k*y[i]))
print(t)

pylab.figure()
pylab.plot(x,y)
pylab.title('Flightpath')
pylab.ylabel('Miles North')
pylab.ylim([0,2000])
pylab.xlabel('Miles East of Town O')
pylab.savefig('Flightpath.png')
print(y[len(x)/2])

pylab.show()
