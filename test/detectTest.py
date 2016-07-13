# -*- coding: utf-8 -*-
# this function find the lines parameters from an existed image.
# usage: python QrGenerator.py  -p img/demo.png
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
from collections import Counter

def getQrLineInfo(imgPath):
    if not os.path.exists(imgPath):
        print ('wrong image path!')
        return -1

    dirpath = os.path.split(imgPath)
    path_save = os.path.join('images','detected','line-'+dirpath[1])
    # print path_save
    # print dirpath
    img = cv2.imread(imgPath, 0)
    img = cv2.resize(img, (512, 512), interpolation=cv2.INTER_LINEAR)
    original = img.copy()

    filtered = cv2.bilateralFilter(img,9,15,15)

    ret, mask = cv2.threshold(filtered, 100, 255, cv2.THRESH_BINARY)
    # img = cv2.bitwise_and(img, img, mask = mask)

    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    kernel = np.ones((21,21),np.uint8)
    dilation = cv2.dilate(opening,kernel,iterations =1)

    # ret, mask = cv2.threshold(dilation, 100, 255, cv2.THRESH_BINARY)
    # dilation = cv2.bitwise_and(dilation, dilation, mask = mask)

    kernel = np.ones((5,5),np.uint8)
    erodation = cv2.erode(dilation,kernel,iterations=1)

    output = cv2.bitwise_and(mask, erodation)

    edges = cv2.Canny(filtered, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges,1,np.pi/180,80)
    # print lines[0][:,1]
    dic = Counter(lines[0][:,1])
    # print dic
    sort=sorted(dic.items(),key=lambda e:e[1],reverse=True)   #排序
    # print sort

    first = sort[0][0]
    second = sort[1][0]
    print(first, second, (first-second)/3.1415*180.0)


    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    for rho, theta in lines[0]:
        if(theta in [first,second]):
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),1)
    # cv2.imshow('output',img)
    cv2.imwrite(path_save,img)

    # plt.subplot(241),plt.imshow(original,cmap = 'gray')
    # plt.title('Original'), plt.xticks([]), plt.yticks([])
    # plt.subplot(242),plt.imshow(filtered,cmap = 'gray')
    # plt.title('filtered'), plt.xticks([]), plt.yticks([])
    # plt.subplot(243),plt.imshow(opening,cmap = 'gray')
    # plt.title('opening'), plt.xticks([]), plt.yticks([])
    # plt.subplot(244),plt.imshow(mask,cmap = 'gray')
    # plt.title('mask'), plt.xticks([]), plt.yticks([])
    # plt.subplot(245),plt.imshow(dilation,cmap = 'gray')
    # plt.title('dilation'), plt.xticks([]), plt.yticks([])
    # plt.subplot(246),plt.imshow(erodation,cmap = 'gray')
    # plt.title('erodation'), plt.xticks([]), plt.yticks([])
    # plt.subplot(246),plt.imshow(output,cmap = 'gray')
    # plt.title('output'), plt.xticks([]), plt.yticks([])
    # plt.subplot(246),plt.imshow(img,cmap = 'gray')
    # plt.title('lines'), plt.xticks([]), plt.yticks([])
    # plt.show()
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


for num in xrange(0,7):
    getQrLineInfo("images/slope/circle0{0}.jpg".format(num))
getQrLineInfo("images/slope/test.png")
