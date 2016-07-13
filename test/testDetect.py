# -*- coding: utf-8 -*-
# this function find the lines parameters from an existed image.
# usage: python QrGenerator.py  -p img/demo.png
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt


def getQrLineInfo(imgPath):
    if not os.path.exists(imgPath):
        print ('wrong image path!')
        return -1
    img = cv2.imread(imgPath, 0)
    img = cv2.resize(img, (512, 512), interpolation=cv2.INTER_LINEAR)

    filtered = cv2.bilateralFilter(img,9,75,75)

    ret, mask = cv2.threshold(filtered, 150, 255, cv2.THRESH_BINARY)
    # img = cv2.bitwise_and(img, img, mask = mask)

    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    kernel = np.ones((15,15),np.uint8)
    dilation = cv2.dilate(opening,kernel,iterations =1)

    ret, mask = cv2.threshold(dilation, 100, 255, cv2.THRESH_BINARY)
    dilation = cv2.bitwise_and(dilation, dilation, mask = mask)

    kernel = np.ones((5,5),np.uint8)
    erodation = cv2.erode(mask,kernel,iterations=1)

    plt.subplot(231),plt.imshow(img,cmap = 'gray')
    plt.title('Original'), plt.xticks([]), plt.yticks([])
    plt.subplot(232),plt.imshow(filtered,cmap = 'gray')
    plt.title('filtered'), plt.xticks([]), plt.yticks([])
    plt.subplot(233),plt.imshow(mask,cmap = 'gray')
    plt.title('mask'), plt.xticks([]), plt.yticks([])
    plt.subplot(234),plt.imshow(dilation,cmap = 'gray')
    plt.title('dilation'), plt.xticks([]), plt.yticks([])
    plt.subplot(235),plt.imshow(erodation,cmap = 'gray')
    plt.title('erodation'), plt.xticks([]), plt.yticks([])
    plt.subplot(236),plt.imshow(opening,cmap = 'gray')
    plt.title('opening'), plt.xticks([]), plt.yticks([])

    plt.show()

    #
    # img = cv2.medianBlur(dilation,5)
    gray = img.copy()
    ret, mask = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)
    img1_mask = cv2.bitwise_and(gray, gray, mask = mask)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    output = img.copy()

    gauss = cv2.GaussianBlur(gray, (3, 3), 0)
    canny = cv2.Canny(gauss, 50, 150, apertureSize=3)

    # canny = cv2.Canny(gray, 50, 150, apertureSize=3)
    # detect circles in the image
    circles = cv2.HoughCircles(gauss, cv2.cv.CV_HOUGH_GRADIENT, 1, 100,
                               param1=50, param2=30, minRadius=0, maxRadius=40)
    # ensure at least some circles were found
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            print (x, y, r)
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

            # show the output image
    print (gray.shape, img.shape, output.shape)
    # cv2.imshow("process", np.hstack([gray,dilation, gauss, canny]))
    # cv2.imshow("mask", np.hstack([gray ,mask,img1_mask]))
    print (img1_mask.shape)
    # cv2.imshow("output", np.hstack([img, output]))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# getQrLineInfo("generate/ID-0001-345696-TIME-0003.png")
# getQrLineInfo(r"circle\circle01.jpg")
# getQrLineInfo(r"circle\circle02.jpg")
# getQrLineInfo(r"circle\circle03.jpg")
# getQrLineInfo(r"circle\circle04.jpg")
# getQrLineInfo(r"circle\circle05.jpg")
# getQrLineInfo(r"circle\circle06.jpg")
# getQrLineInfo(r"circle\detect_circles_soda.jpg")
getQrLineInfo("images/generate/test.jpg")