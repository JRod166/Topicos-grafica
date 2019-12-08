import numpy as np

def getTree(file):
    f = open (file+".huf","r")
    content=f.read()
    f.close()
    content=content.split('\n')
    header=content[0].split('\t')
    try:
        header[header.index('')]='0'
    except:
        header=header
    del(content[0])
    for i in range(0,len(content)):
        content[i]=content[i].split('\t')
    return header,content

def reconstruct(header,content):
    rows=len(content)
    cols=len(content[0])
    newImg=np.zeros((rows,cols,3),np.uint8)
    for i in range (0,rows):
        for j in range(0,cols):
            # print(content[i][j],end=':'+'\t')
            if (content[i][j][:-4]==''):
                newImg[i][j][0]=int(header[int('0',16)],16)
                # print('0',end='\t')
            else:
                # print(content[i][j][:-4],end='\t')
                newImg[i][j][0]=int(header[int(content[i][j][:-4],16)],16)
            # print(content[i][j][-4:-2],end='\t')
            # print(content[i][j][-2:])
            newImg[i][j][1]=int(header[int(content[i][j][-4:-2],16)],16)
            newImg[i][j][2]=int(header[int(content[i][j][-2:],16)],16)
    return newImg

def reconstructdc(file1,file2,file3,file4):
    row1,col1,cha=file1.shape
    row4,col4,cha=file4.shape
    rows=row1+row4
    cols=col1+col4
    newImg=np.zeros((rows,cols,cha),np.uint8)
    newImg[0:row1,0:col1]=file1
    newImg[0:row1,col1:cols]=file2
    newImg[row1:rows,0:col1]=file3
    newImg[row1:rows,col1:cols]=file4
    return newImg

def decompress(file):
    header,content=getTree(file)
    decompressedImg=reconstruct(header,content)
    return decompressedImg
