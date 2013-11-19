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
plt.title('Channel 1')

#channel 2
plt.figure()
plt.plot(Data[:,0],Data[:,2], 'g')
plt.title('Channel 2')

#channels 1,2
plt.figure()
plt.plot(Data[:,0],Data[:,1], 'b')
plt.plot(Data[:,0],Data[:,2], 'g')
plt.title('Channel 1 & 2')

# plt.title('')
# plt.xlabel('Volts (V)')
# plt.ylabel('Current (A)')
# plt.legend(loc='best')
plt.show()

