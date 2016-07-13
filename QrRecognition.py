# -*- coding: utf-8 -*-
# this function recognize the data from an existed image..
# usage: python QrGenerator.py  -p img/demo.png

import argparse
from PIL import Image
import zbar
import os
import cv2
import math
import numpy as np
from collections import Counter


def getQrCodeInfo(imgPath):
    """
    get information in a qr-code
    :param imgPath: the path of qr-code image
    :return: data or None
    """

    if not os.path.exists(imgPath):
        print ('wrong image path!')
        return -1

    scanner = zbar.ImageScanner()
    scanner.parse_config("enable")
    pil = Image.open(imgPath).convert('L')
    width, height = pil.size
    raw = pil.tobytes()
    image = zbar.Image(width, height, 'Y800', raw)
    scanner.scan(image)
    data = ''

    # deal with wrong encoding issue
    for symbol in image:
        try:
            data += symbol.data.decode('utf-8').encode('sjis').decode('utf-8')
        except:
            data += symbol.data
    # post-progress
    del image
    return data if data else None


def getQrLineInfo(imgPath):
    """
    get the main lines info
    :param imgPath: path of the source image
    :return: [output_path, degree_of_image_rotate]
    """
    if not os.path.exists(imgPath):
        print ('wrong image path!')
        return None
    dirpath = os.path.split(imgPath)
    path_save = os.path.join(dirpath[0], 'line-' + dirpath[1])
    # read image and normalize
    img = cv2.imread(imgPath, 0)
    img = cv2.resize(img, (512, 512), interpolation=cv2.INTER_LINEAR)
    # reduce noise
    filtered = cv2.bilateralFilter(img, 9, 15, 15)

    # get edges and lines
    edges = cv2.Canny(filtered, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 60)

    # generate a directory
    dic = Counter((lines[0][:, 1]))
    # sort the directory
    sort = sorted(dic.items(), key=lambda e: e[1], reverse=True)
    # get the first two degree as the main lines
    first = sort[0][0]
    second = sort[1][0]
    output = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    for rho, theta in lines[0]:
        if (theta not in [first, second]):
            continue
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(output, (x1, y1), (x2, y2), (0, 0, 255), 1)

    cv2.imwrite(path_save, output)
    first, second = [max(first, second) / 3.1415 * 180.0 - 90, min(first, second) / 3.1415 * 180.0 - 90]
    sign = 1 if math.fabs(first) > math.fabs(second) else -1
    degree = sign * min(math.fabs(first), math.fabs(second))
    # print('%7.1f%7.1f%7.1f%5.0f' % (first, second, degree, first-second))
    return degree, path_save


def resolve(imgPath):
    """
    resolve the information odf a qr-code with position info
    :param imgPath: path of the source image
    :return: [data, output_path, degree_of_image_rotate]
    """
    data = getQrCodeInfo(imgPath)
    degree, path = getQrLineInfo(imgPath)
    return [data, degree, path] if data else None


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=True, help="image path")
    args = vars(ap.parse_args())
    dataGot = resolve(args["path"])
    print(dataGot)
