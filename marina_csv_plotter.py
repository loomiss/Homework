import numpy as np
import matplotlib.pyplot as plt

path = "sam_lab2/"
filename = "4c.csv"


Data = np.genfromtxt('%s%s'% (path, filename), delimiter=',')


# print(Data)
# print(Data[:,1])
# print(len(Data[0,:]))
# print(len(Data[1,:]))
# print(len(Data[2,:]))

#channel 1
plt.figure()
plt.plot(Data[:,0],Data[:,1], 'b')
plt.title('CH 1 vs. Time')
plt.xlabel('Time (s)')
plt.ylabel('Signal (V)')

#channel 2
plt.figure()
plt.plot(Data[:,0],Data[:,2], 'g')
plt.title('CH 2 vs. Time')
plt.xlabel('Time (s)')
plt.ylabel('Signal (V)')

#channels 1,2
plt.figure()
plt.plot(Data[:,0],Data[:,1], 'b')
plt.plot(Data[:,0],Data[:,2], 'g')
plt.title('All Channels vs. Time')
plt.xlabel('Time (s)')
plt.ylabel('Signal (V)')

# plt.title('')
# plt.xlabel('Volts (V)')
# plt.ylabel('Current (A)')
# plt.legend(loc='best')
plt.show()

