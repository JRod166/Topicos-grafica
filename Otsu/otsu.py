import cv2
import math
import numpy as np


threshold_values = {}
h = [1]


def Hist(img):
   row, col = img.shape
   hist = np.zeros(256)
   for i in range(0,row):
      for j in range(0,col):
         hist[img[i,j]] += 1
   return hist


def regenerate_img(img, threshold):
    row, col = img.shape
    newImg = np.zeros((row, col))
    for i in range(0,row):
        for j in range(0,col):
            if img[i,j] >= threshold:
                newImg[i,j] = 255
    return newImg

def weight(s, e):
    w = 0
    for i in range(s, e):
        w += h[i]
    return w


def mean(s, e):
    m = 0
    w = weight(s, e)
    for i in range(s, e):
        m += h[i] * i

    return m/np.float64(w)


def variance(s, e):
    v = 0
    m = mean(s, e)
    w = weight(s, e)
    for i in range(s, e):
        v += ((i - m) **2) * h[i]
    v /= np.float64(w)
    return v


def threshold(histogram):
    cnt = 0
    for i in range(0, len(h)):
        if h[i]>0:
           cnt += h[i]
    for i in range(1, len(histogram)):
        vb = variance(0, i)
        wb = weight(0, i) / float(cnt)
        mb = mean(0, i)

        vf = variance(i, len(h))
        wf = weight(i, len(h)) / float(cnt)
        mf = mean(i, len(h))

        V2w = wb * (vb) + wf * (vf)
        V2b = wb * wf * (mb - mf)**2
        if not math.isnan(V2w):
            threshold_values[i] = V2w


def get_optimal_threshold():
    min_V2w = min(threshold_values.itervalues())
    optimal_threshold = [k for k, v in threshold_values.iteritems() if v == min_V2w]
    print 'optimal threshold', optimal_threshold[0]
    return optimal_threshold[0]


img = cv2.imread('../sample1.png',0)

histogram = Hist(img)
threshold(histogram)
op_thres = get_optimal_threshold()

res = regenerate_img(img, op_thres)
cv2.imshow('otsu',res)

cv2.waitKey(0)
cv2.destroyAllWindows()
