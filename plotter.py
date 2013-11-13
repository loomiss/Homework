import numpy as np
import matplotlib.pyplot as plt

Data = np.genfromtxt('411labp2asmall.csv', delimiter=',', names=True)


# print(Data)
# print(Data.dtype.names)

plt.figure()

plt.plot(Data[Data.dtype.names[0]], Data[Data.dtype.names[1]], label='')
plt.plot(Data[Data.dtype.names[0]], Data[Data.dtype.names[1]], label='')
plt.plot(Data[Data.dtype.names[0]], Data[Data.dtype.names[1]], label=Data.dtype.names[1])
plt.title('Current as a function of Voltage through a small graphite rod')
plt.xlabel('Volts (V)')
plt.ylabel('Current (A)')
plt.legend(loc='best')
plt.savefig('411labp2asmall.pdf')

