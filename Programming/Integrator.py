from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import math
import time


beginning = time.clock()
#print beginning
# # Steps and Variables:

# N = 3 #Number of divisions
# start = 0
# finish = 1
# dx = (finish - start)/N

# x = np.arange(start, finish+dx/2, dx)

# # Function to integrate:

# y = math.e**x

# # Integrate:

# # Trapazoidal:

# Trapazoidal = (y[0] + y[N])*dx/2  #endpoints

# for i in range(len(y)-2):
#     Trapazoidal += y[i]*dx

# print Trapazoidal-math.e**finish+math.e**start

# Putting it all into a log stepsize/ log error plot:


# X = np.arange(1,10**7,10**4) #Range of Divisions #the program took about an hour and a half to finish

#**********************************************************
# Giving  X values of  2 4 6 8 10 for every dedactic range:  # this takes about 10 minutes

rangeCount = 0
rangeFinish = 6
X = np.zeros(5*(rangeFinish + 1))

h = 0
exponent = 0
for h in range(rangeFinish+1):   
    k = 0
    for k in range(5):
        X[h*5+k] = (k+1)*2*10**exponent
        #print h,k
    exponent +=1
#**********************************************************


Y = np.zeros_like(X)

#print X

# Integration

for j in range(len(X)-1):
    cycleStart = time.clock()
    start = 0
    finish = 1
    dx = (finish - start)/X[j]
    
    x = np.arange(start, finish+dx/2, dx)
    y = math.e**x

    Trapazoidal = (y[0]+y[X[j]])*dx/2
    Simpson = (y[0]+y[X[j]])*2*dx/6
    
    for i in range(len(y)-2):
        Trapazoidal += y[i+1]*dx
        #print i
    #print len(y)
    #for i in range(len(y)-1):

    
    if math.fmod(j/(len(X)-1)*100, 10) < .5: #Completion monitor
        complete = int(j/(len(X)-1)*100)
        timeElapsed = int(time.clock() - beginning)
        timeHour = 0
        timeMin = 0
        while timeElapsed >= 3600:
            timeElapsed -= 3600
            timeHour += 1
        while timeElapsed >= 60:
            timeElapsed -= 60
            timeMin +=1
        print "{0}% complete, Time Elapsed: {1}:{2}:{3}" .format(complete,timeHour,timeMin,timeElapsed)

    Y[j] = Trapazoidal-math.e**finish+math.e**start
    cycleStop = time.clock() - cycleStart
    print "Cycle {0},Number of divisions: {1}, took {2} seconds." .format(j+1,X[j],cycleStop)


plt.plot(np.log(X),np.log(Y))
plt.xlabel=('log N number of divisions')
plt.ylabel=('log Error of integration')
plt.title=('log error vs log number of divisions, integrating e^x')
plt.show()
