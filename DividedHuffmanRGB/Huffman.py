import argparse
import numpy as np
import cv2
import math
import Compress
import Decompress
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
    cv2.waitKey(0)
    cv2.destroyAllWindows()
