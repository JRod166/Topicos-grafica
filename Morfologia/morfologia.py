import argparse
import numpy as np
import cv2
import math
from math import *


def binario(image):
    rows,cols=image.shape
    for i in range (0,rows):
        for j in range (0,cols-1):
            if (image[i][j]>=128):
                image[i][j]=255
            else:
                image[i][j]=0
    return image

#1
vertical=[[-1,0],[0,0],[1,0]]
#2
cruz=[[-1,0],[0,0],[1,0],[0,-1],[0,1]]
#3
horizontal=[[0,-1],[0,0],[0,1]]
#4
chacana=[[-2,0],[-1,-1],[-1,0],[-1,1],[0,-2],[0 ,-1],[0 ,0],[0, 1],[0,2],[1 ,-1],[1, 0],[1,1],[2,0]]
#5
vacio=[[-1,0],[-1,1],[0,1]]



def erosion(image,structure):
    rows,cols=image.shape
    newImg=np.zeros((rows,cols),np.uint8)
    for i in range (0,rows):
        for j in range (0,cols):
            value = True
            for x in structure:
                if(i+x[0]<rows and j+x[1] < cols and image[i+x[0]][j+x[1]]==0):
                    value=False
                    break
            if (value):
                newImg[i][j]=255
    return newImg

def dilatacion(image,structure):
    rows,cols=image.shape
    newImg=np.zeros((rows,cols),np.uint8)
    for i in range (0,rows):
        for j in range (0,cols):
            if (image[i][j]==255):
                for x in structure:
                    if(i+x[0]<rows and j+x[1] < cols):
                        newImg[i+x[0]][j+x[1]]=255
    return newImg

def opening(image,structure):
    return dilatacion(erosion(image,structure),structure)

def closing(image,structure):
    return erosion(dilatacion(image,structure),structure)

def HitOrMiss(image,structure1,structure2):
    rows,cols=image.shape
    # newImg=np.zeros((rows,cols),np.uint8)
    # complement=np.zeros((rows,cols),np.uint8)
    # for i in range (0,rows):
    #     for j in range (0,cols):
    #         if(image[i][j]==0):
    #             complement[i][j]=255
    complement = cv2.bitwise_not(image)
    cv2.imshow('complement',complement)
    first = erosion (image,structure1)
    second = erosion (complement,structure2)
    cv2.imshow('first',first)
    cv2.imshow('second',second)
    # for i in range (0,rows):
    #     for j in range (0,cols):
    #         if(first[i][j] == second[i][j]):
    #             newImg[i][j]=first[i][j]
    return cv2.bitwise_or(first,second)



img = cv2.imread('../sample1.png',0)
img=binario(img)
cv2.imshow('Original',img)
#cv2.imshow('erosion',erosion(mascara,img))
#cv2.imshow('dilatacion',dilatacion(mascara,img))
#cv2.imshow('opening',erosion(mascara,img))
#cv2.imshow('closing',erosion(mascara,img))
cv2.imshow('HitOrMiss',HitOrMiss(img,chacana,chacana))


cv2.waitKey(0)
cv2.destroyAllWindows()
