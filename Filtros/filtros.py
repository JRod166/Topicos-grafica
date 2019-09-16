import argparse
import numpy as np
import cv2
import math
from math import *


def media(img,mask):
    rows,cols=img.shape
    radio= (mask-1)/2
    newImg = img.copy()
    for i in range (0,rows):
        for j in range (0,cols):
            aux=0.0
            for x in range (radio*-1,radio+1):
                for y in range (radio*-1,radio+1):
                    if i+x<rows and j+y<cols:
                        aux += img[i+x][j+y]
            aux = aux / (mask*mask)
            newImg[i][j]=aux
    return newImg;


def mediana(img,mask):
    rows,cols=img.shape
    new_image = img.copy()
    radio=(mask-1)/2
    for i in range(0, rows):
        for j in range(0, cols):
            lista=[]
            for x in range(i-radio,i+radio+1):
                for y in range(j-radio,j+radio+1):
                    if(x > 0 and x < rows and y > 0 and y < cols ):
                        lista.append(int(img[x][y]))
                    else:
                        lista.append(0)
            lista.sort()
            newImg[i][j]=lista[int((mask*mask)/2)]
    return newImg

def maximo(img,mask):
    rows,cols=img.shape
    new_image = img.copy()
    radio=(mask-1)/2
    for i in range(radio, rows-radio):
        for j in range(radio, cols-radio):
            lista=[]
            for x in range(i-radio,i+radio+1):
                for y in range(j-radio,j+radio+1):
                    lista.append(int(img[x][y]))
            lista.sort()
            newImg[i][j]=lista[int((mask*mask)-1)]
    return newImg;


def minimo(img,mask):
    rows,cols=img.shape
    new_image = img.copy()
    radio=(mask-1)/2
    for i in range(radio, rows-radio):
        for j in range(radio, cols-radio):
            lista=[]
            for x in range(i-radio,i+radio+1):
                for y in range(j-radio,j+radio+1):
                    lista.append(int(img[x][y]))
            lista.sort()
            newImg[i][j]=lista[0]
    return newImg;

def gauss(img,mask):
    gauss3=[[1,2,1],
            [2,4,2],
            [1,2,1]]
    gauss5=[[1,4,7,4,1],
            [4,16,26,16,4],
            [7,26,41,26,7],
            [4,16,26,16,4],
            [1,4,7,4,1]]
    if (mask == 3):
        gauss=gauss3
        radio=1
        centro=1
        max=16
    if (mask ==5):
        gauss=gauss5
        radio=2
        centro=2
        max=273
    ###################
    #  1  #  2  #  1  #
    ###################
    #  2  #  4  #  2  #
    ###################
    #  1  #  2  #  1  #
    ###################

    rows, cols = img.shape
    newImg = np.zeros((rows,cols),np.uint8)
    for i in range(1, rows-radio):
        for j in range(1, cols-radio):
            aux=0
            for x in range (radio*-1,radio+1):
                for y in range (radio*-1,radio+1):
                    aux+=img[i+x][j+y]*gauss[centro+x][centro+y]
            newImg[i][j]=aux/max
    return newImg;


def laPlace(img):
    ###################
    #  0  #  1  #  0  #
    ###################
    #  1  # -4  #  1  #
    ###################
    #  0  #  1  #  0  #
    ###################
    laplace = [[0,1,0],
               [1,-4,1],
               [0,1,0]]
    rows, cols = img.shape
    newImg = img.copy()

    for i in range(1, rows-1):
        for j in range(1, cols-1):
            aux=0
            for x in range (-1,2):
                for y in range (-1,2):
                    aux+=img[i+x][j+y]*laplace[1+x][1+y]
            if(aux > 255):
                newImg[i][j] = 255
            elif(aux < 0):
                newImg[i][j] = 0
            else:
                newImg[i][j] = aux
    return newImg

def sobel(img):

    Sx = [ [1,0,-1],
           [2,0,-2],
           [1,0,-1]]
    Sy = [ [-1,-2,-1],
          [0,0,0],
          [1,2,1]]
    rows, cols = img.shape

    Gx = img.copy()
    Gy = img.copy()

    for i in range(1, rows-1):
        for j in range(1, cols-1):
            aux=0
            for x in range (-1,2):
                for y in range (-1,2):
                    aux+=img[i+x][j+y]*Sx[1+x][1+y]
            if(aux > 255):
                Gx[i][j] = 255
            elif(aux < 0):
                Gx[i][j] = 0
            else:
                Gx[i][j] = aux
            aux=0
            for x in range (-1,2):
                for y in range (-1,2):
                    aux+=img[i+x][j+y]*Sy[1+x][1+y]
            if(aux > 255):
                Gy[i][j] = 255
            elif(aux < 0):
                Gy[i][j] = 0
            else:
                Gy[i][j] = aux

    newImg = Gx + Gy
    return newImg

def roberts(image_path):

    #Rx = [[0,0,0],
    #      [0,-1,0],
    #      [0,0,1]]
    #Ry = [[0,0,0],
    #      [0,0,-1],
    #      [0,1,0]]
    rows, cols = img.shape

    Gx = img.copy()
    Gy = img.copy()


    for i in range(1, rows-1):
        for j in range(1, cols-1):
            sumx = -1*int(img[i-1][j-1]) + int(img[i][j])
            if(sumx > 255):
                Gx[i][j] = 255
            elif(sumx < 0):
                Gx[i][j] = 0
            else:
                Gx[i][j] = sumx

            sumy = -1*int(img[i-1][j]) + int(img[i][j-1])
            if(sumy > 255):
                Gy[i][j] = 255
            elif(sumy < 0):
                Gy[i][j] = 0
            else:
                Gy[i][j] = sumy

    newImg = Gx + Gy
    return newImg

def prewitt(image_path):

     ####################################
    # Sx = [  -1   ,   0   ,   1  ,
    #         -1   ,   0   ,   1  ,
    #         -1   ,   0   ,   1  ]

    # Sy = [  -1  ,   -1  ,   -1  ,
    #         0   ,   0   ,   0   ,
    #         1   ,   1   ,   1   ]

    #####################################
    Sx = [ [-1,0,1],
           [-1,0,1],
           [-1,0,1]]
    Sy = [ [-1,-1,-1],
          [0,0,0],
          [1,1,1]]
    rows, cols = img.shape

    Gx = img.copy()
    Gy = img.copy()

    for i in range(1, rows-1):
        for j in range(1, cols-1):
            aux=0
            for x in range (-1,2):
                for y in range (-1,2):
                    aux+=img[i+x][j+y]*Sx[1+x][1+y]
            if(aux > 255):
                Gx[i][j] = 255
            elif(aux < 0):
                Gx[i][j] = 0
            else:
                Gx[i][j] = aux
            aux=0
            for x in range (-1,2):
                for y in range (-1,2):
                    aux+=img[i+x][j+y]*Sy[1+x][1+y]
            if(aux > 255):
                Gy[i][j] = 255
            elif(aux < 0):
                Gy[i][j] = 0
            else:
                Gy[i][j] = aux

    newImg = Gx + Gy
    return newImg



img = cv2.imread('../circuit.jpg',0) #BGR #img[rows][cols][channels]
cv2.imshow('Original',img)

# newImg=media(img,7)
# cv2.imshow('media',newImg);
# newImg=mediana(img,7)
# cv2.imshow('mediana',newImg);
# newImg=maximo(img,3)
# cv2.imshow('maximo',newImg)
# newImg=minimo(img,3)
# cv2.imshow('minimo',newImg)
# newImg=gauss(img,3)
# cv2.imshow('gauss',newImg)
newImg=laPlace(img)
cv2.imshow('laplace',newImg)
newImg=sobel(img)
cv2.imshow('sobel',newImg)
newImg=roberts(img)
cv2.imshow('roberts',newImg)
newImg=prewitt(newImg)
cv2.imshow('prewitt',newImg)
cv2.waitKey(0)
cv2.destroyAllWindows()
