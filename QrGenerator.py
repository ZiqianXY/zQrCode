# -*- coding: utf-8 -*-
# this function generate a demand qr-code for your data.
# usage: python QrGenerator.py -d "this is a demo." -p img/demo.png

import sys
import qrcode
import argparse
import os
from PIL import Image, ImageDraw, ImageFont

# 相关参数设置
qr_size, qr_box_size,  = 512, 10
line_original, line_width = 30, 5
circleR = 25
fontSize = 32

def generateQrCode(data='this is a demo qrcode.', save_path=None, mode=''):
    '''
    生成指定内容的二维码
    :param data: 二维码内容
    :param save_path: 图像保存路径
    :return: 文件保存路径
    '''
    filename = data
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=qr_box_size,
        border=6,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    # 归一化为标准大小
    img = img.resize((qr_size, qr_size), Image.ANTIALIAS)
    # 添加需要的信息
    if mode:
        print (mode)
        if 'l' in mode:
            img = addLines(img)
            filename = 'line-' + filename
        if 'c' in mode:
            img = addCircle(img)
            filename = 'circle-' + filename
        if 't' in mode:
            img = addText(img, data)
            filename = 'text-' + filename
    # 默认生成文件路径
    if not save_path:
        save_path = 'images/generate/gen-{0}.png'.format(filename)
    dir_ = os.path.dirname(save_path)
    if not os.path.exists(dir_):
        os.mkdir(dir_)
    # 保存图片
    img.save(save_path)
    print(save_path)
    return save_path

def addCircle(img_in):
    '''
    add three circle to the generated qr-code
    :param img_in: source img mat
    :return: new img mat
    '''
    img = img_in.copy()
    draw = ImageDraw.Draw(img)
    draw.ellipse((line_original - circleR, line_original - circleR, line_original + circleR, line_original + circleR), fill=0)
    draw.ellipse((img.size[0] - line_original - circleR, line_original - circleR, img.size[0] - line_original + circleR, line_original + circleR), fill=0)
    draw.ellipse((line_original - circleR, img.size[1] - line_original - circleR, line_original + circleR, img.size[1] - line_original + circleR), fill=0)
    del draw
    return img

def addLines(img_in):
    '''
    add two main lines to the generated qr-code
    :param img_in: source img mat
    :return: new img mat
    '''
    img = img_in.copy()
    draw = ImageDraw.Draw(img)
    # draw.line((lineOrignal, lineOrignal+(lineWidth-1)/2, img.size[0]-lineOrignal, lineOrignal+(lineWidth-1)/2), fill=0, width=lineWidth)
    # draw.line((lineOrignal+(lineWidth-1)/2, lineOrignal, lineOrignal+(lineWidth-1)/2, img.size[1]-lineOrignal), fill=0, width=lineWidth)
    draw.line((0, line_original, img.size[0], line_original), fill=0, width=line_width)
    draw.line((line_original, 0, line_original, img.size[1]), fill=0, width=line_width)
    del draw
    return img

def addText(img_in, data):
    '''
    add alert information to the generated qr-code
    :param img_in: source img mat
    :return: new img mat
    '''
    img = img_in.copy()
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', fontSize)
    draw.text((2 * line_original, img.size[0] - 2 * line_original), data, fill=0, font=font)
    del draw
    return img

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--data", required=True, help="data to generate")
    ap.add_argument("-p", "--path", required=False, help="path to save the image file")
    args = vars(ap.parse_args())
    path = generateQrCode(args["data"], args["path"])
    sys.exit()
