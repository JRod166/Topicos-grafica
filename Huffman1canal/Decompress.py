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
    newImg=np.zeros((rows,cols),np.uint8)
    for i in range (0,rows):
        for j in range(0,cols):
            if(content[i][j] == ''):
                content[i][j]='0'
    for i in range (0,rows):
        for j in range(0,cols):
            newImg[i][j]=int(header[int(content[i][j],16)],16)
    return newImg


def decompress(file):
    header,content=getTree(file)
    decompressedImg=reconstruct(header,content)
    return decompressedImg
