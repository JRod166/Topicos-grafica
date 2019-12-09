import argparse
import numpy as np
import cv2
import math
import Compress
import Decompress
import sys
import os
from math import *

def uncompressed(img,file):
    row,col,channels=img.shape
    f = open(file+".unc","w")
    for i in range(0,row):
        for c in range(0,channels):
            f.write(hex(img[i][0][c]).lstrip("0x").zfill(2))
        for j in range(1,col):
            f.write('\t')
            for c in range(0,channels):
                f.write(hex(img[i][j][c]).lstrip("0x").zfill(2))
        f.write('\n')
    f.close()

def distance(first,second):
    sum=0
    for i in range(0,len(first)):
        sum+= pow((first[i]-second[i]),2)
    return sqrt(sum)


def MSE(img,newImg):
    rows1,cols1,channels=img.shape
    rows2,cols2,channels=newImg.shape
    rows=min(rows1,rows2)
    cols=min(cols1,cols2)
    sum=0
    for i in range(0,rows):
        for j in range (0,cols):
            sum=pow(distance(img[i][j],newImg[i][j]),2)
    sum=sum/(rows*cols)
    return sum

def PSNR(mseVal,pixels):
    e=sys.float_info.epsilon
    a=pixels/(pow(mseVal,2)+e)
    b=math.log(a,10)
    psnrVal = 10*b
    return psnrVal

def getSize(filename):
    st=os.stat(filename)
    return st.st_size


if __name__ == '__main__':
    #Setup logger
    parser = argparse.ArgumentParser(description="Operaciones basicas de PDI",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("img_file",
                        action="store",
                        help="Input image file")

    args=parser.parse_args()

    img = cv2.imread(args.img_file,1) #BGR #img[rows][cols][channels]
    rows,cols,channels = img.shape
    pixels=rows*cols
    file=args.img_file[:-4]
    split=file.split('/')
    file=split[len(split)-1]
    cv2.imshow('Original',img)
    rowHalf=int(rows/2)
    colHalf=int(cols/2)
    upLeft=img[0:rowHalf,0:colHalf]
    upRight=img[0:rowHalf,colHalf:cols]
    downLeft=img[rowHalf:rows,0:colHalf]
    downRight=img[rowHalf:rows,colHalf:cols]
    Compress.compress(upLeft,file+"1")
    Compress.compress(upRight,file+"2")
    Compress.compress(downLeft,file+"3")
    Compress.compress(downRight,file+"4")
    decompressed1 = Decompress.decompress(file+"1")
    decompressed2 = Decompress.decompress(file+"2")
    decompressed3 = Decompress.decompress(file+"3")
    decompressed4 = Decompress.decompress(file+"4")
    decompressed=Decompress.reconstructdc(decompressed1,decompressed2,decompressed3,decompressed4)
    cv2.imshow('Decompressed',decompressed)
    uncompressed(img,file)


    mseVal = MSE(img,decompressed)
    psnrVal = PSNR(mseVal,pixels)
    compressedfile=getSize(file+"1.huf")+getSize(file+"2.huf")+getSize(file+"3.huf")+getSize(file+"4.huf")
    uncompressedfile=getSize(file+".unc")
    compressionRate = uncompressedfile/compressedfile
    bpp = compressedfile/pixels

    f=open("DividedRGB.csv","a")
    f.write(file)
    f.write(',')
    print("Compression Rate: ",compressionRate)
    f.write(str(compressionRate))
    f.write(',')
    print("MSE: ",mseVal)
    f.write(str(mseVal))
    f.write(',')
    print("PSNR: ",psnrVal)
    f.write(str(psnrVal))
    f.write(',')
    print("BPP: ",bpp)
    f.write(str(bpp))
    f.write('\n')
    f.close()

    cv2.waitKey(0)
    cv2.destroyAllWindows()
