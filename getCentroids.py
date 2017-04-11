from GammaDetection import GammaDetection
import numpy as np
import cv2
import os
import sys
import warnings
import getCleanImage
import matplotlib.pyplot as plt

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

x, y, width, height = (404, 314, 500, 511)#(400, 304, 516, 536)
angle = 0.0174533446603
mat_centroids = getCleanImage.source.getSquaresValues(x, y, width, height)

print mat_centroids


c = plt.pcolor(mat_centroids, edgecolors='k', linewidths=1)
plt.gca().invert_yaxis()
plt.title('thick alreve')

plt.show()
