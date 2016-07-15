import time
from PIL import Image
import QrGenerator
import QrRecognition
from test import testSlope

def showImg(save_path):
    Image._showxv(Image.open(save_path), 'Generated QrCode')

if (False):
    # generate qr-code
    showImg(QrGenerator.generateQrCode('ID-0001-345696-TIME-0003', mode='tc'))

if (False):
    # generate slope image
    showImg(testSlope.rotate('images/generate/gen-ID-0001-345696-TIME-0003.png', 35))

if (True):
    for num in xrange(1,7):
        tm = time.strftime("%H%M%S", time.gmtime())
        orig_path = QrGenerator.generateQrCode('ID-00{0}-TIME-{1}.jpg'.format(num, tm), mode='tc')
        slope_path = testSlope.rotate(orig_path, num*5)
        data = QrRecognition.getQrData(orig_path)
        degree, path = QrRecognition.getSlopeDegree(orig_path)
        print (degree, path)
        testSlope.rotate(path, -degree)
