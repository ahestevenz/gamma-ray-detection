from GammaDetection import GammaDetection
import numpy as np
import cv2
import os
import sys
import warnings
import getCleanImage

# For arguments, please check getCleanImage script
if os.path.exists(getCleanImage.file_calib_location):
    try:
        file_calib = open(getCleanImage.file_calib_location, 'r')
    except IOError:
        print "Could not read file:", file_calib
        sys.exit()
else:
    print "File does not exist:", file_calib
    sys.exit()

x, y, width, height = (400, 304, 516, 536)

#getCleanImage.source.getSquaresValues(x, y, width, height)

v=getCleanImage.source.getSquareValues(400, 304, 51, 53)

v_sum=np.sum(v)

print v_sum
