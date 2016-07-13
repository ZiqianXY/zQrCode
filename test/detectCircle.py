# -*- coding: utf-8 -*-
# this function find the lines parameters from an existed image.
# usage: python QrGenerator.py  -p img/demo.png
import argparse
import os
import cv2
import sys
import numpy as np

from zQrCode import QrRecognition
from zQrCode.test import testSlope


def getQrCircleInfo(imgPath):

    if not os.path.exists(imgPath):
        print ('wrong image path!')
        return -1

    filter_delta, filter_color, filter_space = 9, 15, 15
    threshold_indesity = 60
    opening_kernel = 1
    dilation_kernel = 21

    img = cv2.imread(imgPath, 0)
    img = cv2.resize(img, (512, 512), interpolation=cv2.INTER_LINEAR)

    filtered = cv2.bilateralFilter(img, filter_delta, filter_color, filter_space)
    cv2.imshow('filtered', filtered)
    cv2.waitKey(0)

    ret, mask = cv2.threshold(filtered, threshold_indesity, 255, cv2.THRESH_BINARY_INV)
    ret, mask = cv2.threshold(mask, threshold_indesity, 255, cv2.THRESH_BINARY_INV)
    # mask = cv2.bitwise_and(img, img, mask = mask)
    cv2.imshow('mask', mask)
    cv2.waitKey(0)
    path_tmp = 'tmp/image.jpg'
    cv2.imwrite(path_tmp, mask)
    degree,path  = QrRecognition.getQrLineInfo(path_tmp)
    print (path)
    rotatation, path_save = testSlope.rotate(path, -degree)
    cv2.imshow('rotatation', rotatation)
    cv2.waitKey(0)

    kernel = np.ones((opening_kernel, opening_kernel), np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # cv2.imshow('opening', opening)
    # cv2.waitKey(0)


    kernel = np.ones((dilation_kernel, dilation_kernel), np.uint8)
    dilation = cv2.dilate(opening, kernel, iterations=1)
    cv2.imshow('dilation', dilation)
    cv2.waitKey(0)
    # ret, mask = cv2.threshold(dilation, 100, 255, cv2.THRESH_BINARY)
    # dilation = cv2.bitwise_and(dilation, dilation, mask = mask)

    kernel = np.ones((25,25),np.uint8)
    erodation = cv2.erode(dilation,kernel,iterations=1)
    cv2.imshow('erodation', erodation)
    cv2.waitKey(0)

    edges = cv2.Canny(erodation, 50, 150, apertureSize=3)
    circles =cv2.HoughCircles(edges, cv2.cv.CV_HOUGH_GRADIENT, 1, 10,
                            param1=50, param2=30, minRadius=1, maxRadius=100)

    result = cv2.cvtColor(edges.copy(), cv2.COLOR_GRAY2RGB)
    for cicle in circles[0]:
        print cicle
        cv2.circle(result, (int(cicle[0]+1), int(cicle[1]+1)), cicle[2], (0, 0, 255))

    cv2.imshow('Result', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=False, help="path of the image file")
    args = vars(ap.parse_args())
    path = r"F:\Z_Python\imageprocess\zQrCode\images\slope\circle01.jpg"
    if (args["path"]):
        path = args["path"]
    getQrCircleInfo(path)
    sys.exit()


path = r"F:\Z_Python\imageprocess\zQrCode\images\slope\circle01.jpg"
getQrCircleInfo(path)
