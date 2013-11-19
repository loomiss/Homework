from __future__ import division
import matplotlib, sys
import pylab, numpy, os, glob
import math

dw=.1
w=numpy.arange(100,1000000,dw)
x=numpy.zeros_like(w)
y=numpy.zeros_like(w)
y2=numpy.zeros_like(w)
#print w[3]

cHigh=1*10**(-6)
rHigh=1*10**(3)
cLow=1*10**(-10)
rLow=1*10**(5)

magHigh=w*rHigh*cHigh/((1+w**2*rHigh**2*cHigh**2)**(1/2))
print magHigh[5]
magLow=1/((1+w**2*rLow**2*cLow**2)**(1/2))

for i in range(len(w)):
    x[i]=math.log10(w[i])
    y[i]=20*math.log10(magHigh[i]*magLow[i])
    y2[i]=-3

pylab.figure()
pylab.plot(x,y)
pylab.plot(x,y2)
pylab.title('Gain vs. Frequency of High/Low-Pass Circuit')
pylab.ylabel('20log(Vout/Vin)')
pylab.xlabel('log(\omega)')
pylab.savefig('sam_lab2/log_log.png')
pylab.show()
