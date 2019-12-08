import numpy as np


def getHist(img):
   row, col = img.shape
   y = np.zeros(256)
   for i in range(0,row):
      for j in range(0,col):
         y[img[i,j]] += 1
   return y

def uncompressed(img,file):
    row,col=img.shape
    f = open(file+".unc","w")
    for i in range(0,row):
        f.write(str(img[i][0]))
        for j in range(1,col):
            f.write('\t')
            f.write(hex(img[i][j]).lstrip("0x"))
    f.close()



def getProbabilities(histogram,pixels):
    for i in range (0,histogram.shape[0]):
        if (histogram[i] != 0):
            histogram[i] = histogram[i]/pixels
        else:
            histogram[i] = 0
    return histogram

def getOrder(probabilites):
    probabilitiesOrder=[]
    max=1;
    while max != 0:
        maxArray=np.where(probabilites == np.amax(probabilites))[0]
        # print(maxArray)
        for i in maxArray:
            # print(probabilites[i])
            probabilites[i]=0
            probabilitiesOrder.append(i)
        max=np.amax(probabilites)
    return probabilitiesOrder

def setTree(probabilitiesOrder,file):
    treeStructure = [0]*len(probabilitiesOrder)
    maxPosition = len(probabilitiesOrder)-1
    while(maxPosition!=0):
        for i in range (0,maxPosition):
            treeStructure[i]+=1
            # print(hex(treeStructure[i]).lstrip("0x"))
        maxPosition-=1
    # print(order)
    f = open(file+".huf", "w")
    f.write(hex(probabilitiesOrder[0]).lstrip("0x"))
    for i in range(1,len(probabilitiesOrder)):
        f.write('\t')
        f.write(hex(probabilitiesOrder[i]).lstrip("0x"))
    f.write('\n')
    f.close()

def compressionMethod(probabilitiesOrder,img,file):
    row, col = img.shape
    f = open(file+".huf", "a")
    for i in range (0,row-1):
        f.write(hex(probabilitiesOrder.index(img[i][0])).lstrip("0x"))
        # print(hex(probabilitiesOrder.index(img[i][0])).lstrip("0x"),end='\t')
        for j in range (1,col):
            f.write('\t')
            aux = hex(probabilitiesOrder.index(img[i][j])).lstrip("0x")
            # print(aux,end='\t')
            f.write(aux)
        f.write('\n')
        # print('\n')
    f.write(hex(probabilitiesOrder.index(img[row-1][0])).lstrip("0x"))
    for j in range (1,col):
        f.write('\t')
        aux = hex(probabilitiesOrder.index(img[row-1][j])).lstrip("0x")
        # print(aux,end='\t')
        f.write(aux)
    f.close()

def compress(img,file):
    row, col = img.shape
    pixels= row*col
    histogram = getHist(img)
    probabilites = getProbabilities(histogram,pixels)
    order= getOrder(probabilites)
    setTree(order,file)
    compressionMethod(order,img,file)
