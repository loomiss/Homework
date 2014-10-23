import numpy as np
from mayavi import mlab

X = np.array([.49,.98,1.47,1.96,2.45,.49,.98,1.47,1.96,2.45,.49,.98,1.47,1.96,2.45,.49,.98,1.47,1.96,2.45,.49,.98,1.47,1.96,2.45])
Y = np.array([.49,.49,.49,.49,.49,.98,.98,.98,.98,.98,1.47,1.47,1.47,1.47,1.47,1.96,1.96,1.96,1.96,1.96,2.45,2.45,2.45,2.45,2.45])
Z = np.array([0,.0078,.0245,.0485,.0784,.0230,.0235,.0358,.0578,.0887,.0583,.0505,.0573,.0760,.1034,.1005,.0892,.0916,.1078,.1318,.1593,.1507,.1421,.1504,.1715])

#X = np.array([0,1,0,1,.75])
#Y = np.array([0,0,1,1,.75])
#Z = np.array([1,1,1,1,2])

pts = mlab.points3d(X,Y,Z,Z)

mesh = mlab.pipeline.delaunay2d(pts)

pts.remove()

surf = mlab.pipeline.surface(mesh)

mlab.xlabel("Fx (N)")
mlab.ylabel("Fy (N)")
mlab.zlabel("Delta Potential (J)")
mlab.show()