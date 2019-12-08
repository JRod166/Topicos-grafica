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
    file=args.img_file[:-4]
    split=file.split('/')
    file=split[len(split)-1]
    cv2.imshow('Original',img)
    uncompressed(img,file)
    Compress.compress(img,file)
    decompressed=Decompress.decompress(file)
    cv2.imshow('Decompressed',decompressed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
