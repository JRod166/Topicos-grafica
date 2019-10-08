import argparse
import numpy as np
import cv2
import math
from math import *
from PIL import Image

# Utils Start
# def normalized(image):
    # //rows,cols=image.shape
    # print(max(image))
    # print(min(image))

    # return newImg
# Utils End

#Conversions Start
def RGBToCMY(image):
    rows,cols,channels=image.shape
    newImg = np.zeros((rows,cols,3),np.uint8)
    for i in range (0,rows):
        for j in range (0,cols):
            newImg[i][j][0]=(255-(image[i][j][0]))
            newImg[i][j][1]=(255-(image[i][j][1]))
            newImg[i][j][2]=(255-(image[i][j][2]))
    return newImg

def RGBToHSV(image):
    rows,cols,channels=image.shape
    newImgH = np.zeros((rows,cols),np.uint8)
    newImgS = np.zeros((rows,cols),np.uint8)
    newImgV = np.zeros((rows,cols),np.uint8)
    for i in range (0,rows):
        for j in range (0,cols):
            R=(image[i][j][0])/255.0
            G=(image[i][j][1])/255.0
            B=(image[i][j][2])/255.0
            V=max(R,G,B)
            m=min(R,G,B)
            if V==R:
                H=60*(G-B)/(V-m)
            elif V==G:
                H=60*(B-R)/(V-m)+120
            else:
                H=60*(R-G)/(V-m)+240
            if V!=0:
                S=(V-m)/V
            else:
                S=0
            newImgH[i][j]=H/300.0*255.0
            newImgS[i][j]=S*255.0
            newImgV[i][j]=V*255.0
    cv2.imshow('H',newImgH)
    cv2.imshow('S',newImgS)
    cv2.imshow('V',newImgV)

def RGBToHSI(image):
    rows,cols,channels=image.shape
    newImgH = np.zeros((rows,cols),np.uint8)
    newImgS = np.zeros((rows,cols),np.uint8)
    newImgI = np.zeros((rows,cols),np.uint8)
    for i in range (0,rows):
        for j in range (0,cols):
            R=(image[i][j][0])/255.0
            G=(image[i][j][1])/255.0
            B=(image[i][j][2])/255.0
            I=((R+G+B)/3.0)*255.0
            num = (1/2.)*( (R - G) + (R - B) )  # numerador
            dem = math.sqrt( (R - G)**2 + (R - B)*(G - B) )  # denominador
            if(dem!=0): div = num/dem
            else: div = 0
            theta = np.arccos(div)
            if B<=G:
                H=theta
            else:
                H=360-theta
            S=1-(3/(R+G+B))*min(R,G,B)
            newImgH[i][j]=H/360.0*255.0
            newImgS[i][j]=S*255.0
            newImgI[i][j]=I

    cv2.imshow('H',newImgH)
    cv2.imshow('S',newImgS)
    cv2.imshow('I',newImgI)

def RGBToYUV(image):
    rows,cols,channels=image.shape
    newImgY = np.zeros((rows,cols),np.uint8)
    newImgU = np.zeros((rows,cols),np.uint8)
    newImgV = np.zeros((rows,cols),np.uint8)
    for i in range (0,rows):
        for j in range (0,cols):
            R=(image[i][j][0])/255.0
            G=(image[i][j][1])/255.0
            B=(image[i][j][2])/255.0
            Y=0.299*R + 0.587*G + 0.114*B
            U=-0.147*R-0.289*G+0.436*B
            V=0.615*R-0.515*G-0.1*B
            newImgY[i][j]=Y*255.0
            newImgU[i][j]=abs(U/0.872*255.0)
            newImgV[i][j]=abs(V/1.23*255.0)
    cv2.imshow('Y',newImgY)
    cv2.imshow('U',newImgU)
    cv2.imshow('V',newImgV)

def RGBToYIQ(image):
    rows,cols,channels=image.shape
    newImgY = np.zeros((rows,cols),np.uint8)
    newImgU = np.zeros((rows,cols),np.uint8)
    newImgV = np.zeros((rows,cols),np.uint8)
    for i in range (0,rows):
        for j in range (0,cols):
            R=(image[i][j][0])/255.0
            G=(image[i][j][1])/255.0
            B=(image[i][j][2])/255.0
            newImgY[i][j]= (0.299*R + 0.587*G + 0.114*B)*255.0
            newImgU[i][j]= abs((0.596*R - 0.275*G - 0.321*B)/1.192*255.0)
            newImgV[i][j]= abs(0.596*R - 0.275*G - 0.321*B*255.0/1.192)
    cv2.imshow('Y',newImgY)
    cv2.imshow('I',newImgU)
    cv2.imshow('Q',newImgV)

def RGBToYCrCb(image):
    rows,cols,channels=image.shape
    newImgY = np.zeros((rows,cols),np.uint8)
    newImgCb = np.zeros((rows,cols),np.uint8)
    newImgCr = np.zeros((rows,cols),np.uint8)
    for i in range (0,rows):
        for j in range (0,cols):
            R=(image[i][j][0])/255.0
            G=(image[i][j][1])/255.0
            B=(image[i][j][2])/255.0
            Y=16+65.738*R+129.057*G+25.064*B
            Cb=128-37.945*R-74.494*G+112.439*B
            Cr=128+112.439*R-94.154*G-18.285*B
            newImgY[i][j]=Y/235.856*255.0
            newImgCb[i][j]=abs(Cb/352.878*255.0)
            newImgCr[i][j]=abs(Cr*255.0/349.878)
    cv2.imshow('Y',newImgY)
    cv2.imshow('Cb',newImgCb)
    cv2.imshow('Cr',newImgCr)

#Conversions End

img = cv2.imread('../lena.jpg')
cv2.imshow('Original To CMY',img)
newImg = RGBToCMY(img)
cv2.imshow('CMY',newImg)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imshow('Original to hsv',img)
RGBToHSV(img)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imshow('Original to hsi',img)
RGBToHSI(img)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imshow('Original to yuv',img)
RGBToYUV(img)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imshow('Original to yiq',img)
RGBToYIQ(img)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imshow('Original to YCrCb',img)
RGBToYCrCb(img)
cv2.waitKey(0)
cv2.destroyAllWindows()
