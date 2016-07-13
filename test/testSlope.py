# -*- coding: utf-8 -*-
import argparse

import cv2
import os
import sys


def rotate(imgPath, angle):
    """
    rotate the image with given degree
    :param imgPath:
    :param angle:
    :return: saved_path
    """

    if not os.path.exists(imgPath):
        print ('wrong image path!')
        return -1
    dirpath = os.path.split(imgPath)
    path_save = os.path.join(dirpath[0], 'slope-'+dirpath[1])

    img = cv2.imread(imgPath, flags=cv2.COLOR_BGR2GRAY)
    # thr, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)
    # 得到图像大小
    # print img.shape
    width = img.shape[0]
    height = img.shape[1]
    # 计算图像中心点
    center_x = width / 2.0
    center_y = height / 2.0
    # 获得旋转变换矩阵
    scale = 0.9
    trans_mat = cv2.getRotationMatrix2D((center_x, center_y), angle, scale)
    # 仿射变换
    img = cv2.warpAffine(img, trans_mat, (width, height))
    # thr, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite(path_save, img)
    return img, path_save


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--degree", required=True, help="data to generate")
    ap.add_argument("-p", "--path", required=False, help="path to save the image file")
    args = vars(ap.parse_args())
    path = rotate(args["path"], args["degree"])
    sys.exit()
