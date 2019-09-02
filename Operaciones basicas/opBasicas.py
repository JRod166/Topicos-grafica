import argparse
import numpy as np
import cv2
import math
from math import *

##########################################
#Utils
##########################################
def toRad(angle):
    return angle*pi/180
##########################################



##########################################
#Transformations
##########################################
def rotateSquare(img):
    rows,cols = img.shape
    newImg=np.zeros((cols,rows),np.uint8)
    for i in range (0,rows):
        for j in range (0,cols):
            newImg[rows-1-j][i]=img[i][j]
    return newImg

def transpose(img, x = 0 , y = 0):
    #x'=x+k
    #y'=x+l
    rows, cols = img.shape
    newImg=np.zeros((rows+x,cols+y),np.uint8)
    for i in range (0,rows):
        for j in range (0,cols):
            newImg[i+x][j+y]=img[i][j]
    return newImg

def scale(img,resize = 1):
    #x'=kx
    #y'=ky
    rows, cols = img.shape
    newRow = int(rows * resize)
    newCol = int(cols * resize)
    channels = 3
    newImg= np.zeros((newRow,newCol),np.uint8)
    for i in range (0, rows):
        for j in range (0, cols):
            newImg[int(i*resize)][int(j*resize)]=img[i][j]
    return newImg


def rotate(img,angleR=0):
    angleR = angleR%360
    #x'=x*cos(theta)-y*sen(theta)
    #y'=x*sen(theta)+y*cos(theta)
    rows, cols = img.shape
    while angleR >= 90:
        img=rotateSquare(img)
        #cv2.imshow('try',img.T)
        rows, cols = img.shape
        angleR-=90
    xPos=0
    yPos=0
    angle=toRad(angleR)
    newRow =  int (rows*abs(cos(angle)) + cols*abs(sin(angle)))
    newCol =  int (rows*abs(sin(angle)) + cols*abs(cos(angle)))
    xPos += abs(int(cols*sin(angle)))
    newImg=np.zeros((newRow,newCol),np.uint8)
    for i in range (0,rows):
        for j in range (0,cols):
            x_1=int(i*cos(angle)-j*sin(angle)) + xPos
            y_1=int(i*sin(angle)+j*cos(angle)) + yPos
            newImg[x_1][y_1]=img[i][j]
    return newImg
##########################################

##########################################
#Color Transformations
##########################################
def logarithm(img):
    const=255/log(255,2)
    rows,cols = img.shape
    newImg =np.zeros((rows,cols),np.uint8)
    for i in range (0,rows):
        for j in range (0,cols):
            newImg[i][j]=const*log(img[i][j]+1,2)
    return newImg;

def logarithmInverse(img):
    const=255*log(255,2)
    print(const)
    rows,cols = img.shape
    newImg =np.zeros((rows,cols),np.uint8)
    for i in range (0,rows):
        for j in range (0,cols):
            newImg[i][j]=const*(1/log(img[i][j]+1,2))
    return newImg;


def negative(img):
    rows,cols=img.shape
    newImg = np.zeros((rows,cols),np.uint8)
    for i in range (0,rows):
        for j in range (0,cols):
            newImg[i][j]=255-img[i][j]
    return newImg;

def power(img,gamma=1):
    const=pow(255,gamma)/255
    rows,cols=img.shape
    newImg = np.zeros((rows,cols),np.uint8)
    for i in range (0,rows):
        for j in range (0,cols):
            newImg[i][j]=pow(img[i][j],gamma)/const
    return newImg;


##########################################





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
    parser.add_argument("-L",
                        action="store_const",
                        const=True,
                        dest="Log",
                        default=False,
                        help= "Logarithmic function")
    parser.add_argument("-I",
                        action="store_const",
                        const=True,
                        dest="LogInv",
                        default=False,
                        help= "Inverse logarithmic function")
    parser.add_argument("-P",
                        action="store",
                        type=float,
                        dest="Power",
                        default=1,
                        help= "Power function")
    parser.add_argument("-N",
                        action="store_const",
                        const=True,
                        dest="Negative",
                        default=False,
                        help= "Negative")
    args=parser.parse_args()

    img = cv2.imread(args.img_file,0) #BGR #img[rows][cols][channels]
    cv2.imshow('Original',img)
    newImg=img
    if(args.Transpose[0]!=0 and args.Transpose[1]!=0):
        newImg = transpose(newImg,args.Transpose[0],args.Transpose[1])
    if(args.Scale!=1):
        newImg = scale(newImg,args.Scale)
    if(args.Rotate!=0):
        newImg = rotate(newImg,args.Rotate)
    if(args.Log):
        newImg = logarithm(newImg)
    if(args.LogInv):
        newImg = logarithmInverse(newImg)
    if(args.Power!=1):
        newImg = power(newImg,args.Power)
    if(args.Negative):
        newImg = negative(newImg)
    cv2.imshow('Transformed',newImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
