from __future__ import division
import matplotlib, sys
import pylab, numpy, os, glob
import math

phi = numpy.arange(0, 2*pylab.pi, pylab.pi/180)
print(phi)
r=numpy.zeros_like(phi)

for i in range(len(phi)):
    r[i]=math.sin(phi[i])

pylab.figure()
pylab.plot(phi,r)
pylab.show()
