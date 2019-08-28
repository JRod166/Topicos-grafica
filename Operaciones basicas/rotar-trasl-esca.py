import numpy as np
import cv2
import math
from math import *

def toRad(angle):
    return angle*pi/180


def transpose(img, x = 0 , y = 0):
    rows, cols, channels = img.shape
    newImg=np.zeros((rows+x,cols+y,channels),np.uint8)
    for i in range (0,rows):
        for j in range (0,cols):
            newImg[i+x][j+y]=img[i][j]
    return newImg

def scale(img,resize = 1):
    #x'=kx
    #y'=ky
    rows, cols, channels = img.shape
    newRow = int(rows * resize)
    newCol = int(cols * resize)
    channels = 3
    newImg= np.zeros((newRow,newCol,channels),np.uint8)
    for i in range (0, rows):
        for j in range (0, cols):
            newImg[int(i*resize)][int(j*resize)]=img[i][j]
    return newImg


def rotate(img,angleR=0):
    angleR = angleR%360
    #x'=x*cos(theta)-y*sen(theta)
    #y'=x*sen(theta)+y*cos(theta)
    rows, cols, channels = img.shape
    while angleR > 90:
        img=rotate(img,90)
        rows, cols, channels = img.shape
        angleR-=90
    xPos=0
    yPos=0
    angle=toRad(angleR)
    newRow =  int (rows*abs(cos(angle)) + cols*abs(sin(angle)))
    newCol =  int (rows*abs(sin(angle)) + cols*abs(cos(angle)))
    xPos += abs(int(cols*sin(angle)))
    newImg=np.zeros((newRow,newCol,3),np.uint8)
    for i in range (0,rows):
        for j in range (0,cols):
            x_1=int(i*cos(angle)-j*sin(angle)) + xPos
            y_1=int(i*sin(angle)+j*cos(angle)) + yPos
            if(x_1>=0 and x_1 < newRow and y_1>=0 and y_1<newCol):
                newImg[x_1][y_1]=img[i][j]
    return newImg

img = cv2.imread('reno.jpeg',1) #BGR #img[rows][cols][channels]
cv2.imshow('image',img)
#newImg = scale(img,2)
newImg = rotate(img,719)
#newImg = transpose(img,10,20)
cv2.imshow('image2',newImg)
cv2.waitKey(0)
cv2.destroyAllWindows()
