from __future__ import division
import numpy as np
import matplotlib
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import math



lam0 = 514.5*10**(-9) #meters
om0 = 5*10**(-3) #meters
beamd = 3 #meters
c0 = 3*10**8 #meters per second
n = 1 #index of refraction
l = 10 # assigned value 
p = 2 # assigned value



#prelim calculations
omz = om0*(1+ (lam0*beamd/(np.pi*n*om0**2))**2)**(1/2) # 1/e beam waist


max=omz*np.pi
dx=max/1000

x= np.arange(-max,max,dx)
y= np.arange(-max,max,dx)
X, Y = np.meshgrid(x,y)

E_r=np.zeros_like(X)
Intense=np.zeros_like(X)

lag = 2*( 33*omz**4-12*omz**2*X**2+X**4-12*omz**2*Y**2+2*X**2*Y**2+Y**4)/omz**4 #mathematica generated leguerre for l=10, p=2

mx=E_r[0,0]
mn=E_r[0,0]
Imn = Intense[0,0]
Imx = Intense[0,0]

for i in range(len(X[0])):
	for j in range(len(Y[0])):
			E_r[i,j] = (-1)**p*((2*(X[i,j]**2+Y[i,j]**2)**(1/2))/omz)**l*lag[i,j]*math.exp(-(X[i,j]**2+Y[i,j]**2)/omz**2)*math.cos(l*math.atan(Y[i,j]/X[i,j]))
			Intense[i,j]=E_r[i,j]**2
			if (i == j == 0):
				Imx = Intense[0,0]
			if Intense[i,j] > Imx:
				Imx = Intense[i,j]
			if E_r[i,j] > mx:
				mx= E_r[i,j]
			if E_r[i,j] < mn:
				mn = E_r[i,j]
dlvls =(mx-mn)/100
levels = np.arange(mn,mx+dlvls/2,dlvls)

Imn=-Imx
Idlvls = (Imx-Imn)/100
Ilevels = np.arange(Imn,Imx+Idlvls/2,Idlvls)


plt.figure()
CS = plt.contourf(X,Y,E_r,levels)
plt.title('Electric Field Contour Plot')
plt.colorbar(CS)


plt.figure()
CS = plt.contour(X,Y,E_r,levels)
plt.title('Electric Field Contour Plot')
plt.colorbar(CS)

plt.figure()
CS = plt.contourf(X,Y,Intense,Ilevels)
plt.title('Intensity Contour Plot')
plt.colorbar(CS)


plt.figure()
CS = plt.contour(X,Y,Intense,Ilevels)
plt.title('Intensity Contour Plot')
plt.colorbar(CS)
plt.show()



#path = "sam_lab2/"
#filename = "4c.csv"


#Data = np.genfromtxt('%s%s'% (path, filename), delimiter=',')


# print(Data)
# print(Data[:,1])
# print(len(Data[0,:]))
# print(len(Data[1,:]))
# print(len(Data[2,:]))

#channel 1
#plt.figure()
#plt.plot(Data[:,0],Data[:,1], 'b')
#plt.title('Channel 1')

#channel 2
#plt.figure()
#plt.plot(Data[:,0],Data[:,2], 'g')
#plt.title('Channel 2')

#channels 1,2
#plt.figure()
#plt.plot(Data[:,0],Data[:,1], 'b')
#plt.plot(Data[:,0],Data[:,2], 'g')
#plt.title('Channel 1 & 2')

# plt.title('')
# plt.xlabel('Volts (V)')
# plt.ylabel('Current (A)')
# plt.legend(loc='best')
#plt.show()



