#!/usr/bin/env python
"""Provides the grid of superpixels for gamma-ray detection.
"""
from GammaDetection import GammaDetection
import numpy as np
import cv2
import os
import sys
import warnings
import getCleanImage

__author__ = "Ariel Hernandez Estevenz"
__copyright__ = "Copyright 2017, Comision Nacional de Energia Atomica"
__credits__ = ["Ariel Hernandez Estevenz"]
__version__ = "0.1"
__maintainer__ = "Ariel Hernandez Estevenz"
__email__ = "ahernandez@cae.cnea.gov.ar, ariel.h.estevenz@ieee.org"
__status__ = "Development"

# For arguments, please check getCleanImage script
### Variables
img_location="images/" # Directory images
_ , essay_name = os.path.split(getCleanImage.path_source) # Directory essay name
if os.path.exists(getCleanImage.file_calib_location):
    try:
        file_calib = open(getCleanImage.file_calib_location, 'r')
    except IOError:
        print "Could not read file:", file_calib
        sys.exit()
else:
    print "File does not exist:", file_calib
    sys.exit()

if not os.path.exists(img_location):
    os.mkdir(img_location)

# Getting calib parameters
coor = file_calib.readline().rstrip('\n').translate(None,'()').split(",")
angle = float(file_calib.readline().rstrip('\n'))
x = int(coor[0])
y = int(coor[1])
width = int(coor[2])
height = int(coor[3])
file_calib.close()

### Script
if getCleanImage.verbose==True:
    print "\nCalibration values \n| x | y | width | height |"
    print '|',x,'|',y,'|',width,'|',height,'|'

if getCleanImage.show==True:
    getCleanImage.source.getSubtractGrayImage().show()
    getCleanImage.source.makeGrid(x, y, width, height, getCleanImage.img_diff_clean_ocv_grid)
    cv2.namedWindow('Image: Grid', cv2.WINDOW_NORMAL)
    cv2.imshow('Image: Grid', getCleanImage.img_diff_clean_ocv_grid)
    cv2.waitKey(0)

if getCleanImage.write==True:
    getCleanImage.source.makeGrid(x, y, width, height, getCleanImage.img_diff_clean_ocv_grid)
    cv2.imwrite(img_location + "img_diff_ocv_grid_" + essay_name + ".jpg", getCleanImage.img_diff_clean_ocv_grid);

mat_centroids = getCleanImage.source.getPlotSuperPixelMatrix(x, y, width, height, getCleanImage.verbose)

if getCleanImage.verbose==True:
    np.set_printoptions(precision=2)
    print "\nCentroids Matrix"
    print mat_centroids
