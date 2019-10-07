import numpy as np
from math import sqrt,exp
import cv2

# Utils Start
def normalize(image):
    rows,cols=image.shape
    new_image=np.zeros((rows,cols),np.uint8)
    min=image.min()
    max=image.max()
    longitud=max-min

    if(longitud == 0):
        return new_image

    for u in range(0,rows):
        for v in range(0,cols):
            new_image[u][v]=(image[u][v]-min)*255/longitud
    return new_image


def shift(image):
    rows,cols=image.shape
    newImg=np.zeros((rows,cols),image.dtype)
    m=rows//2
    n=cols//2
    newImg[0:m,0:n]=image[m:rows,n:cols]
    newImg[0:m,n:cols]=image[m:rows,0:n]
    newImg[m:rows,0:n]=image[0:m,n:cols]
    newImg[m:rows,n:cols]=image[0:m,0:n]
    return newImg
# Utils End

#Fourier Start
# f(u,v) = Sum_(x=0)^(M) Sum_(y=0)^(N) f(x,y) . e ^ (-pi*2j(ux/M+vy/N))
# f(u,v) = Sum_(x=0)^(M) Sum_(y=0)^(N) f(x,y) . e ^ (-pi*2jux/M).e ^ (-pi*2jvy/N))
# exp1 = e ^ (-pi*2jux/M)
# exp2 = e ^ (-pi*2jvy/N))
# Sum1 = Sum_(x=0)^(M)
# Sum 2 = Sum_(y=0)^(N)
# f(u,v) = Sum1 Sum2 f(x,y).exp1.exp2
# f(u,v) = Sum1 exp2 Sum2 f(x,y).exp1
# f(u,v) = Sum1 exp2 . (f(x,y) dot exp1)
# f(u,v) = (exp2 dot (f(x,y) dot exp1) )
#exp2 (dot (e^-pi*2juy/n) dot f(x,y))
#exp2 dot (exp1 dot image)
def fourier(image):
    rows,cols=image.shape

    x = np.arange(rows, dtype = float)
    y = np.arange(cols, dtype = float)

    u = x.reshape((rows,1))
    v = y.reshape((cols,1))

    exp_1 = pow(np.e, -2j*np.pi*u*x/rows)
    exp_2 = pow(np.e, -2j*np.pi*v*y/cols)
    dft=np.dot(exp_2, np.dot(exp_1,image).transpose())/(rows*cols)

    return dft




def inverse_fourier(image,name):
    rows,cols=image.shape
    x = np.arange(rows, dtype = float)
    y = np.arange(cols, dtype = float)

    u = x.reshape((rows,1))
    v = y.reshape((cols,1))

    exp_1 = pow(np.e, 2j*np.pi*u*x/rows)
    exp_2 = pow(np.e, 2j*np.pi*v*y/cols)
    idft=np.dot(exp_2, np.dot(exp_1,image).transpose())

    x=np.abs(idft)

    cv2.imshow(name,normalize(x))

# Fourier End

# High Pass Filters Start

def HPIdeal(image,threshold):
    rows,cols = image.shape
    newImg=np.zeros((rows,cols))
    rowsCenter = rows/2
    colsCenter = cols/2
    for u in range (0,rows):
        for v in range (0,cols):
            d=sqrt(pow(u-rowsCenter,2)+pow(v-colsCenter,2))
            if (d <= threshold):
                newImg[u][v] = 0
            else:
                newImg[u][v]=1
    return shift (newImg)*image

def HPButterworth(image,threshold,n):
    rows,cols=image.shape
    newImg=np.zeros((rows,cols))
    rowsCenter=rows/2
    colsCenter=cols/2
    for u in range(0,rows):
        for v in range(0,cols):
            d=sqrt(pow(u-rowsCenter,2)+pow(v-colsCenter,2))
            if(d==0):
                d=0.0001
            newImg[u][v]=1/(1+pow(threshold/d,2*n))
    return shift(newImg)*image

def HPgauss(image,d0):
    rows,cols=image.shape
    newImg=np.zeros((rows,cols))
    rowsCenter=rows/2
    colsCenter=cols/2
    for u in range(0,rows):
        for v in range(0,cols):
            d=sqrt(pow(u-rowsCenter,2)+pow(v-colsCenter,2))
            newImg[u][v]=1-exp(-(d*d)/(2*d0*d0))

    return shift(newImg)*image

# High Pass Filters End



# Low Pass Filters Start
def LPIdeal(image,threshold):
    rows,cols=image.shape
    newImg=np.zeros((rows,cols))
    rowsCenter=rows/2
    colsCenter=cols/2
    for u in range(0,rows):
        for v in range(0,cols):
            d=sqrt(pow(u-rowsCenter,2)+pow(v-colsCenter,2))
            if(d<=threshold):
                newImg[u][v]=1
            else:
                newImg[u][v]=0

    return shift(newImg)*image

def LPButterworth(image,threshold,n):
    rows,cols=image.shape
    newImg=np.zeros((rows,cols))
    rowsCenter=rows/2
    colsCenter=cols/2
    for u in range(0,rows):
        for v in range(0,cols):
            d=sqrt(pow(u-rowsCenter,2)+pow(v-colsCenter,2))
            newImg[u][v]=1/(1+pow(d/threshold,2*n))

    return shift(newImg)*image

def LPGauss(image,d0):
    rows,cols=image.shape
    newImg=np.zeros((rows,cols))
    rowsCenter=rows/2
    colsCenter=cols/2
    for u in range(0,rows):
        for v in range(0,cols):
            d=sqrt(pow(u-rowsCenter,2)+pow(v-colsCenter,2))
            newImg[u][v]=exp(-(d*d)/(2*d0*d0))

    return shift(newImg)*image
# Low Pass Filters End


bottom=0
right=0
image=cv2.imread('../circuit.jpg',0)
rows,cols=image.shape
if(rows%2!=0):
    bottom=1
if(cols%2!=0):
    right=1

image=cv2.copyMakeBorder(image,0,bottom,0,right,cv2.BORDER_CONSTANT)
rows,cols=image.shape

newImg=fourier(image)
idealHP=HPIdeal(newImg,20)
bwHP=HPButterworth(newImg,20,2)
gaussHP=HPgauss(newImg,20)


idealLP=LPIdeal(newImg,20)
bwLP = LPButterworth(newImg,20,2)
gaussLP = LPGauss (newImg,20)

inverse_fourier(idealHP,"Ideal High Pass")
inverse_fourier(bwHP,"Butterworth High Pass")
inverse_fourier(gaussHP,"Gauss High Pass")
inverse_fourier(idealLP,"Ideal Low Pass")
inverse_fourier(bwLP,"Butterworth Low Pass")
inverse_fourier(gaussLP,"Gauss Low Pass")
cv2.imshow('Imagen original',image)
cv2.waitKey(0)
cv2.destroyAllWindows()
