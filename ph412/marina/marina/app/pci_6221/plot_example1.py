
#plot_example1.py

from scipy import *
from pylab import *
import time


from contAcquireNChan import *


def acquire(points):
    SetupTask()
    StartTask()
    tstart = time.time()
    data = ReadSamples(points)
    StopAndClearTask()
    return data

#Capture 600ms of data
sample_rate=sampleRate.value
t=r_[0:0.6:1/sample_rate]
N=len(t)
s=acquire(N)
S=fft(s)
f=sample_rate*r_[0:(N/2)]/N
n=len(f)
clf()
plot(f,abs(S[0:n])/N)
show()
grid(True)
