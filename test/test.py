from PIL import Image

from zQrCode import QrRecognition
from zQrCode.test import testSlope


def showImg(save_path):
    Image._showxv(Image.open(save_path), 'Generated QrCode')

# generate qr-code
# showImg(QrGenerator.generateQrCode('ID-0001-345696-TIME-0003', mode='tc'))

# generate slope image
# showImg(testSlope.rotate('images/generate/gen-ID-0001-345696-TIME-0003.png', 35))


for num in xrange(1,7):
    degree, path = QrRecognition.getQrLineInfo(r"F:\Z_Python\imageprocess\zQrCode\images\slope\circle0{0}.jpg".format(num))
    print (degree, path)
    testSlope.rotate(path, -degree)

#     getQrLineInfo("images/slope/circle0{0}.jpg".format(num))
# getQrLineInfo("images/slope/test.png")
# showImg(detectLine.getQrLineInfo("images/generate/slope-gen-ID-0001-345696-TIME-0003.png")[0])

# for x in xrange(-90,90,5):
#     # print(x)
#     testSlope.rotate('images/generate/gen-ID-0001-345696-TIME-0003.png', x)
#     detectLine.getQrLineInfo("images/generate/slope-gen-ID-0001-345696-TIME-0003.png")
# path, degree = detectLine.getQrLineInfo("images/slope/circle01.jpg")
# showImg(testSlope.rotate(path, -degree))
