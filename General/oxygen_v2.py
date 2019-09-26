#######################
# Improve Parallel efficiency 
#######################
import numpy as np 
# import scipy as sp
# import pandas as pd 
from scipy.optimize import newton #, toms748
import os
import sys
import itertools
import math
# from google.colab import files

try: 
 import vtk
 from vtk.util import numpy_support
 from pyevtk.hl import gridToVTK
except:
 # !pip install vtk
 # !pip install pyevtk
 print('Nope')
 import vtk 
 from vtk.util import numpy_support
 # from pyevtk.hl import gridToVTK, pointsToVTK
try:
 del VTK_file
except:
 pass


def empty(seq):
  try:
    return all(map(empty, seq))
  except TypeError:
    return False


def arrayfun(var_1,var_2):
  out = []
  for i in range(len(var_1)):
    if empty(var_1[i]) or empty(var_2[i]):
      out_temp = float('nan')
    else:
      out_temp = np.arange(var_1[i],var_2[i]).astype(int,order='F')
    out.append(out_temp)
  return np.array(out)

def first(array):
  for i in range(len(array)):
    if array[i] == 1:
      return i
    else:
      pass
    
def last(array):
  for i in reversed(range(len(array))):
    if array[i] == 1:
      return i
    else:
      pass 
    
def indices(a, func):
    return [i for (i, val) in enumerate(a) if func(val)]
  
def offsetadd(a,b,offset):
  ndims = len(offset)
  matrix_dims = np.shape(b)
  vess_dims = np.shape(a)
  bi_min = [[],[],[]]
  bi_max = [[],[],[]]
  ai_min = [[],[],[]]
  ai_max = [[],[],[]]
  for j in range(ndims):
    bi = range(1,matrix_dims[j])
    bio = bi + offset[j]
    bio = bio.astype(int,order='F')
    bmask = np.zeros(np.shape(bio)).astype(int,order='F')
    for n in range(len(bio)):
      if bio[n] >= 0 and (bio[n]) < (np.shape(a)[j]):
        bmask[n] = 1
      else:
        bmask[n] = 0
    bi_min[j] = bi[first(bmask)]
    bi_max[j] = bi[last(bmask)]
    ai_min[j] = bio[first(bmask)]
    ai_max[j] = bio[last(bmask)]
  a_inds = arrayfun(ai_min,ai_max)
  b_inds = arrayfun(bi_min,bi_max)
  for i in range(len(a_inds[0])):         #This code is the most time consuming
    for j in range(len(a_inds[1])):       # Optimize this
      for k in range(len(a_inds[2])):
        a[i,j,k] = a[i,j,k] + b[i,j,k]
  #index = np.meshgrid(range(len(a_inds[0])),range(len(a_inds[1])),range(len(a_inds[2]))).flatten()

#   master_list = [float(a_flat[aa_flat[i]])+float(b_flat[bb_flat[i]]) for i in range(len(aa_flat))]
#   list_a = np.array([[[a[i,j,k] + b[i,j,k] for i in range(len(a_inds[0]))] for j in \
#             range(len(a_inds[1]))] for k \
#                      in range(len(a_inds[2]))]).reshape((len(a_inds[0]),\
#                                                          len(a_inds[1]),\
#        len(a_inds[2])))
#   a = a.flatten()
#   b_inds = b_inds.flatten(order='K')
#   a_inds = a_inds.flatten(order='K')
#   ax,ay,az = np.meshgrid(a_inds[0],a_inds[1],a_inds[2])
#   bx,by,bz = np.meshgrid(b_inds[0],b_inds[1],b_inds[2])
  
#   ax = ax.ravel()
#   ay = ay.ravel()
#   az = az.ravel()
#   aa = np.array([np.transpose(ax),np.transpose(ay),np.transpose(az)])
#   a_ii = np.ravel_multi_index(aa,np.shape(a))
#   A = a.ravel()
# #  print(np.ravel_multi_index(tuple(list(aa[:][1]))))

# #  aa = aa.ravel()
# #  A = a.ravel()

  
#   bx = bx.ravel()
#   by = by.ravel()
#   bz = bz.ravel()
#   bb = np.array([np.transpose(bx),np.transpose(by),np.transpose(bz)])
#   b_ii = np.ravel_multi_index(bb,np.shape(b))
#   B = b.ravel()
# #  bb = bb.ravel()
# #  B = b.ravel()
#   A[a_ii] = A[a_ii]+B[b_ii]
#   A = A.reshape(np.shape(a))
# #  A[aa] = A[aa]+B[bb]
# #   a_inds.astype(int,order='F')
# #   b_inds.astype(int,order='F')
# #   b = b.flatten()
#   #+b[bx][by][bz]
# #   a[(a_inds[0],a_inds[1],a_inds[2])] = a[(a_inds[0],a_inds[1],a_inds[2])] + b[(b_inds[0],b_inds[1],b_inds[2])]
# #   aa = list(itertools.product(a_inds[0],a_inds[1],a_inds[2]))
# #   bb = list(itertools.product(b_inds[0],b_inds[1],b_inds[2]))
# #   for index in range(len(aa)):
# #     a[aa[index]] = a[aa[index]]+b[bb[index]]
# #   return a
  
  return a
network = np.matrix('1 1 2 18.4  60.42 70.0 15.0 100.0  70.0 190.0 100.0')

network_2 = np.matrix('1 2 3 18.4 60.42 170.0 215.0 100.0 115.0 190.0 100.0;\
                     2 3 7 24.0 125.90 115.0 190.0 100.0 100.0  65.0 100.0;\
                     3 3 4 12.9 60.42 115.0 190.0 100.0 60.0 165.0 100.0;\
                     4 4 24 14.2 60.83 60.0 165.0 100.0 0.0 155.0 100.0;\
                     5 12 15 17.4 89.44 160.0 130.0 100.0 240.0 170.0 100.0;\
                     6 10 12 11.4 50.00 160.0 80.0 100.0 160.0 130.0 100.0;\
                     7 10 11 9.4 46.10 160.0 80.0 100.0 205.0 70.0 100.0;\
                     8 11 16 9.4 99.25 205.0 70.0 100.0 270.0 145.0 100.0;\
                     9  2 15 14.5 83.22 170.0 215.0 100.0 240.0 170.0 100.0;\
                    10 16 22 15.2 63.25 270.0 145.0 100.0 330.0 125.0 100.0;\
                    11 16 17 14.0 50.00 270.0 145.0 100.0 300.0 185.0 100.0;\
                    12 17 26 14.0 76.32 300.0 185.0 100.0 340.0 250.0 100.0;\
                    13 15 16 17.2 39.05 240.0 170.0 100.0 270.0 145.0 100.0;\
                    14 21 22 20.0 47.43 315.0 80.0 100.0 330.0 125.0 100.0;\
                    15 14 20 14.0 70.71 255.0 0.0 100.0 265.0 70.0 100.0;\
                    16 20 21 14.0 50.99 265.0 70.0 100.0 315.0 80.0 100.0;\
                    17 13 21 10.0 68.01 370.0 40.0 100.0 315.0 80.0 100.0;\
                    18 22 23 28.2 41.23 330.0 125.0 100.0 370.0 135.0 100.0;\
                    19 8 9 12.0 68.01 85.0 0.0 100.0 125.0 55.0 100.0;\
                    20 7 9 26.0 26.93 100.0 65.0 100.0 125.0 55.0 100.0;\
                    21 9 10 20.0 43.01 125.0 55.0 100.0 160.0 80.0 100.0;\
                    22 7 25 12.0 105.95 0.0 100.0 100.0 100.0 65.0 100.0;\
                    23 1 2 14.2 46.10 200.0 250.0 100.0 170.0 215.0 100.0;\
                    24 18 19 14.0 40.31 300.0 250.0 100.0 280.0 215.0 100.0;\
                    25 15 18 14.0 60.21 280.0 215.0 100.0 240.0 170.0 100.0;\
                    26 4 5 15.0 54.49 60.0 165.0 100.0 95.0 153.0 140.0;\
                    27 5 6 15.0 31.95 95.0 153.0 140.0 125.0 142.0 140.0;\
                    28 6 12 15.0 54.49 125.0 142.0 140.0 160.0 130.0 100.0')
np.seterr(divide='ignore')
######################################
#Progress Bar
def printProgressBar (iteration, total, prefix = 'Progress', suffix = 'Complete',
                      decimals = 1, length = 100, fill = '%'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    sys.stdout.write('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
    if iteration == total: 
        print()  
######################################

cwd = os.getcwd()
vascular_extension = '.vas'
  
  #####################
  # Grid Resolution
  #####################
  
res = 10
  
  #####################
  # Oxygen Constants
  #####################
  
D = 2*10**(-9) # Diffusivity of O2 in water m^2/s
omega = 3.0318*10**7 # Henry's Law constant
default_radius = 5*10**(-6) # Default vessel radius
  
RN = 150*10**(-6) # Effective Diffusion distance (limit) in microns
  
po = 40 # Initial partial pressure
  
asl = ((3*D*po)/omega)*((((np.sqrt(RN**2-default_radius**2))/3)*(2*default_radius**2\
        -8*RN**2)+2*RN**3*np.log((RN+np.sqrt(RN**2-default_radius**2))/default_radius))\
                          **(-1))
  
  ### Assuming the network input is an array 
  
  # Allocate the memory space for the Vessel data
  
A = len(network[:,0])
Segnum = A
data = np.matrix(np.zeros((A,8)))
  
data[:,0] = network[:,5]
data[:,1] = network[:,6]
data[:,2] = network[:,7]
data[:,3] = network[:,8]
data[:,4] = network[:,9]
data[:,5] = network[:,10]
data[:,6] = network[:,3]/2
SQ = lambda D: np.transpose(np.matrix([((D[i,0]-D[i,3])**2+(D[i,1]-D[i,4])**2\
                 +(D[i,2]-D[i,5])**2)**(1/2) for i in range(len(D[:,0]))]))
 
data[:,7] = SQ(data)
data.astype(int,order='F')
# ######################
# # All of Above is verified
# ######################
offset = int(max(data[:,6]) + 1)

data[:,0] = data[:,0] + offset
data[:,1] = data[:,1] + offset
data[:,2] = data[:,2] + offset
data[:,3] = data[:,3] + offset
data[:,4] = data[:,4] + offset
data[:,5] = data[:,5] + offset

xmax = [max(data[:,0]), max(data[:,3])]
xmax = int(np.amax(xmax)+2*offset)
ymax = [max(data[:,1]), max(data[:,4])]
ymax = int(np.amax(ymax)+2*offset)
zmax = [max(data[:,2]), max(data[:,5])]
zmax = int(np.amax(zmax)+2*offset)
  
xmax = round(xmax/res)
ymax = round(ymax/res)
zmax = round(zmax/res)
# ###### NO VERTICAL OFFSET FOR NOW

cons = asl*omega/(3*D)
rt = data[:,6]*10**(-6)
zm = data[:,7]/2*10**(-6)

Pnorms = cons*(np.power(zm,3)/3+2*np.power(RN,3)*np.log((np.sqrt(np.power(zm,2)\
         +np.power(rt,2))+zm)/rt)+np.array((np.power(rt,2)-3*np.power(RN,2)))*\
         np.array(zm))

RT = rt*10**(6)
  
A = data[:,0] - data[:,3]
B = data[:,1] - data[:,4]
C = data[:,2] - data[:,5]

theta = np.arccos(C/np.sqrt(np.power(A,2)+np.power(B,2)+np.power(C,2)))
phi = np.arctan2(B,A)
  
Cx = (data[:,0] + data[:,3])/2
Cy = (data[:,1] + data[:,4])/2
Cz = (data[:,2] + data[:,5])/2

dCx = np.array(RT)*np.array(np.cos(theta))*np.array(np.cos(phi))
dCy = np.array(RT)*np.array(np.cos(theta))*np.array(np.sin(phi))
dCz = -np.array(RT)*np.array(np.sin(theta))

absolute_ceiling = lambda x: np.array(x>0)*np.array(np.ceil(x)) + np.array(x<=0)*\
                   np.array(np.floor(x))

xperp = np.round(np.array(Cx) + np.array(absolute_ceiling(dCx)))
yperp = np.round(np.array(Cy) + np.array(absolute_ceiling(dCy)))
zperp = np.round(np.array(Cz) + np.array(absolute_ceiling(dCz)))

xperp = np.round(xperp/res)
yperp = np.round(yperp/res)
zperp = np.round(zperp/res)

limit_correction = lambda i: [1 if r in [u - 1 for u in list(filter(lambda a:\
                   a > 0, [int(i[j]<1)*(j+1) for j in range(len(i))]))] else \
                   i[r] for r in range(len(i))]

xperp = limit_correction(xperp)
yperp = limit_correction(yperp)
zperp = limit_correction(zperp)

a0 = 10**(-7)
omega = 3.0318*10**7
D = 2*10**(-9)
imdist = res*10**(-6)

C = asl*omega/(3*D)
  
data6 = np.round(data[:,6])
rop = data6*10**(-6)


def scale(a,b):
  rn = np.zeros((len(a),1))
  for n in range(len(a)):
    i = a[n]
    j = b[n]
    f = lambda rnf: np.real(C*((2*i**2-8*rnf**2)*(np.sqrt(\
        rnf**2-i**2))/3+2*(rnf**3)*np.log((rnf+np.sqrt(rnf**2-i**2))/i))-j)
    rn[n] = newton(f,float(i))
  return rn

rn = scale(rop,Pnorms)

data6 = rop
value = np.ceil(rn/imdist)
h = 2*value+1 #Something with the boundary need to be better

######################
# Find Bounds of Area to Explore
######################

X = [data[:,0], data[:,3]]
Y = [data[:,1], data[:,4]]
Z = [data[:,2], data[:,5]]

row_min = lambda k: [[min(k[0][u],k[1][u]) for u in range(len(k[0]))],[0 if \
          k[0][u]<k[1][u] else 1 for u in range(len(k[0]))]]
  
row_max = lambda k: [[max(k[0][u],k[1][u]) for u in range(len(k[0]))],[0 if \
          k[0][u]>k[1][u] else 1 for u in range(len(k[0]))]]

YMin,Minvy = row_min(Y)
YMax,Maxvy = row_max(Y)
XMin = [X[Minvy[i]][i] for i in range(len(Minvy))]
XMax = [X[Maxvy[i]][i] for i in range(len(Maxvy))]
temp_y = np.array(YMax)- np.array(YMin)
temp_x = np.array(XMax) -np.array(XMin)

#################################################
# Bounds Found
#################################################

angle = np.arctan2(temp_y,temp_x)
  
angle_correction = lambda i,j,k: [0 if i[u] == j[u] else k[u] for u \
                     in range(len(k))]
  
angle = angle_correction(Minvy,Maxvy,angle)

Length = data[:,7]
Length = (Length/2).astype(int,order='F')
Length = [Length[i,0] for i in range(len(Length))]

Ry = np.sqrt(np.power(X[0][:]-X[1][:],2)+np.power(Y[0][:]-Y[1][:],2))
stepsydom = [Ry[n]/Length[n] for n in range(len(Length))]

BF = lambda x,b: b*np.array(range(1,x+1))

array_BF = lambda x,b: [BF(x[i],b[i]) for i in range(len(x))]

Az = array_BF(Length,stepsydom)

Xpair = [0 for n in range(len(Az))]
Ypair = [0 for n in range(len(Az))]
Zpair = [0 for n in range(len(Az))]

for i in range(len(Az)):
  if angle[i] == 0:
    Xpair[i] = float(X[Minvy[i]][i]) + Az[i]*float(np.cos(angle[i]))
    Xpair[i] = Xpair[i].astype(int,order='F')
    Ypair[i] = np.ones((1,len(Az)))*data[i,1]
  else:
    Xpair[i] = float(X[Minvy[i]][i]) + Az[i]*float(np.cos(angle[i]))
    Ypair[i] = float(Y[Minvy[i]][i]) + Az[i]*float(np.sin(angle[i]))      
  Zpair[i] = np.linspace(int(Z[Minvy[i]][i]),int(Z[Maxvy[i]][i]),num=np.size(Az[i]))
  Xpair[i] = Xpair[i].astype(int,order='F')
  Ypair[i] = Ypair[i].astype(int,order='F')
  Zpair[i] = Zpair[i].astype(int,order='F')

v1 = len(Xpair)
for hh in range(v1):
  Xpair[hh] = (Xpair[hh]/res).astype(int,order='F')
  Ypair[hh] = (Ypair[hh]/res).astype(int,order='F')
  Zpair[hh] = (Zpair[hh]/res).astype(int,order='F')

outgrid = np.zeros((int(xmax),int(ymax),int(zmax)))

for i in range(Segnum):

  printProgressBar(i+1,Segnum, prefix = 'Progress:',suffix = 'Complete', length \
                   = 50)
  m,n,l = np.meshgrid(np.arange(1,abs(int(h[i]))),np.arange(1,abs(int(h[i]))),\
                      np.arange(1,abs(int(h[i]))))
  r = np.sqrt(((m-value[i])*imdist)**2+((n-value[i])*imdist)**2+((l-value[i])*\
      imdist)**2) 

  matrix = (a0*omega/(6*D))*(r**2+(2*(float(rn[i])**3))*np.reciprocal(r)-3*\
           float(rn[i])*float(rn[i]))
  matrix[r >= rn[i][0]] = 0
  matrix[r <= float(data6[i])] = (a0*omega/(6*D))*float(data6[i])**2+(2*rn[i]**3)\
                                  /float(data6[i])-3*rn[i]*rn[i]
  
  roNaN = (1*10**(-6))*np.sqrt((np.array(Cx[i])-res*np.array(xperp[i]))**2+\
          (np.array(Cy[i])-res*np.array(yperp[i]))**2+(np.array(Cz[i])-res*\
          np.array(zperp[i]))**2)
  
  sys.stdout.flush()
  
  matrix[r < roNaN-2*10**(-6)] = np.nan
  
  
  vessgrid = np.zeros((xmax,ymax,zmax))

  for j in range(Length[i]):
    posnoffset = [Xpair[i][0,j]-value[i]-1,Ypair[i][0,j]-value[i]-1,Zpair[i][j]-\
                  value[i]-1]
    vessgrid = offsetadd(vessgrid,matrix,posnoffset)

  val = vessgrid[int(xperp[i]),int(yperp[i]),int(zperp[i])]
  
  if np.isnan(val).any():
    val = np.nanmax(vessgrid)
  else:
    pass
  scale = Pnorms[i]/val
  outgrid = outgrid +float(scale)*vessgrid
  
# xxx = np.arange(0,np.shape(outgrid)[0]+1,dtype='float64')
# yyy = np.arange(0,np.shape(outgrid)[1]+1,dtype='float64')
# zzz = np.arange(0,np.shape(outgrid)[2]+1,dtype='float64')

# xxxx,yyyy,zzzz = np.meshgrid(xxx,yyy,zzz)

# out = np.array(outgrid,'f')
# flat_data_array = out.transpose(2,1,0).flatten()
# vtk_data_array = util.numpy_support.numpy_to_vtk(flat_data_array)
# image = vtk.vtkImageData() 
# points = image.GetPointData()
# points.SetScalars(vtk_data_array)
 
# image.SetDimensions(out.shape)
filename = 'VTK_results.vti'
imageData = vtk.vtkImageData()
odim = np.shape(outgrid)
imageData.SetDimensions(odim[0],odim[1],odim[2])
if vtk.VTK_MAJOR_VERSION <= 5:
  imageData.SetNumberOfScalarComponents(1)
  imageData.SetScalarTypeToDouble()
else:
  imageData.AllocateScalars(vtk.VTK_DOUBLE,1)
dims = imageData.GetDimensions()
for z in range(dims[2]):
  for y in range(dims[1]):
    for x in range(dims[0]):      
      imageData.SetScalarComponentFromDouble(x,y,z,0,outgrid[x][y][z])
writer = vtk.vtkXMLImageDataWriter()
writer.SetFileName('oxygen_results')
writer.SetInputData(imageData)
writer.Write()
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName('oxygen_results')
reader.Update()

# Convert the image to a polydata
imageDataGeometryFilter = vtk.vtkImageDataGeometryFilter()
imageDataGeometryFilter.SetInputConnection(reader.GetOutputPort())
imageDataGeometryFilter.Update()

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(imageDataGeometryFilter.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(3)

# Setup rendering
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1,1,1)
renderer.ResetCamera()

renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)

renderWindowInteractor = vtk.vtkRenderWindowInteractor()

renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.Initialize()
renderWindowInteractor.Start()