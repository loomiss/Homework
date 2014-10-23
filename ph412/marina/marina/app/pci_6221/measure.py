
#measure.py

from contAcquireNChan import *
from pylab import *
import time

def acquire(points):
    times = []
    SetupTask()
    StartTask()
    data = ReadSamples(points)
    acqTime = points/sampleRate.value
    StopAndClearTask()
    t = linspace(0,acqTime,points)
    clf()
    plot(t,data)
    axis([0,acqTime,-10,10])
    ylabel("Volts")
    xlabel("time (sec)")
    grid(True)
    return data
