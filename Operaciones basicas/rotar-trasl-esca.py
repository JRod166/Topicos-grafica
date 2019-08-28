import argparse
import numpy as np
import cv2
import math
from math import *

def toRad(angle):
    return angle*pi/180

def rotateSquare(img):
    rows,cols,channels = img.shape
    newImg=np.zeros((cols,rows,channels),np.uint8)
    for i in range (0,rows):
        for j in range (0,cols):
            newImg[j][i]=img[i][j]
    return newImg

def transpose(img, x = 0 , y = 0):
    #x'=x+k
    #y'=x+l
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
    while angleR >= 90:
        img=rotateSquare(img)
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

if __name__ == '__main__':
    #Setup logger
    parser = argparse.ArgumentParser(description="Operaciones basicas de PDI",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("img_file",
                        action="store",
                        help="Input image file")
    parser.add_argument("-T",
                        nargs=2,
                        action="store",
                        type=int,
                        dest="Transpose",
                        default=[0,0],
                        help="Transpose image")
    parser.add_argument("-S",
                        action="store",
                        dest="Scale",
                        default=1,
                        type=float,
                        help="Scale image")
    parser.add_argument("-R",
                        action="store",
                        dest="Rotate",
                        type=float,
                        default=0,
                        help="Rotate image")
    args=parser.parse_args()

    img = cv2.imread(args.img_file,1) #BGR #img[rows][cols][channels]
    cv2.imshow('Original',img)
    newImg=img
    newImg = transpose(newImg,args.Transpose[0],args.Transpose[1])
    newImg = scale(newImg,args.Scale)
    newImg = rotate(newImg,args.Rotate)
    cv2.imshow('Transformed',newImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
