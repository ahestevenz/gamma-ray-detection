#!/usr/bin/env python
"""Provides the calibration parameters for gamma-ray detection.
"""
from GammaDetection import GammaDetection
import cv2
import os
import argparse
import warnings
from shutil import copyfile
from shutil import copytree
from shutil import rmtree
import numpy as np

__author__ = "Ariel Hernandez Estevenz"
__copyright__ = "Copyright 2017, Comision Nacional de Energia Atomica"
__credits__ = ["Ariel Hernandez Estevenz"]
__version__ = "0.1"
__maintainer__ = "Ariel Hernandez Estevenz"
__email__ = "ahernandez@cae.cnea.gov.ar, ariel.h.estevenz@ieee.org"
__status__ = "Development"

### Args parser
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True,
				help="path to directory of images acquire with the calibration set")
ap.add_argument("-b", "--background", required=True,
				help="path to directory of images acquire in background")
ap.add_argument("-i", "--index", required=True, default=0, type=int,
				help="image index for the image processing in the directory")
ap.add_argument("-m", "--frame", type=int, default=0,
	            help="frame of the image selected, the default value is 0")
ap.add_argument("-f", "--file_calib", default="./conf/config.calib", type=str,
				help="calibration file location")
ap.add_argument("-s", "--show", action='store_true',
    			help="show graphics")
ap.add_argument("-v", "--verbose", action='store_true',
				help="verbose mode")
ap.add_argument("-w", "--write_images", action='store_true',
				help="save images")
args = vars(ap.parse_args())

### Variables
path_images=args["directory"] # Path to directory of images acquire with calibration set
path_blackout=args["background"] # Path to the directory without the radioactive sources or LED (images), the acquisition was in blackout
image_index=args["index"] # Image index for the image processing in the directory
show = args["show"] # Show images
verbose = args["verbose"] # Verbose mode
write = args["write_images"]  # Save images
file_calib_location = args["file_calib"] # Calibration file location
frame = args["frame"] # Frame of the image selected, the default value is 0
dir_conf = os.path.dirname(file_calib_location) # Configuration directory location
img_location = "./images_calib" # Images location

if not os.path.exists(img_location):
    os.mkdir(img_location)
else:
    if os.path.exists(img_location + '_previous'):
	    rmtree(img_location + '_previous')
    copytree(img_location, img_location + '_previous')

if not os.path.exists(dir_conf):
    os.mkdir(dir_conf)

if os.path.exists(file_calib_location):
    print "File exists. Backing up ..." # Warning: File exists, so I backed up, just in case!
    copyfile(file_calib_location, file_calib_location +'.previous')

file_calib = open(file_calib_location, 'w')

### Script
source = GammaDetection(path_images, image_index, frame, verbose) # Object with radioactive source
blackout = GammaDetection(path_blackout, image_index, frame, verbose) # Object without radioactive source

img_src = source.getSelectedImage() # Image from essay with sources
img_blk = blackout.getSelectedImage() # Image from essay without sources
img_diff = source.getSubtractImage(img_blk) # A way to reduce the camera noise
if show==True:
    img_src.show()
    img_diff.show()

# Histograms
if show==True:
    source.getHistSelectedImage(1, "Histogram of image with LED light")# Histogram of image with sources
    blackout.getHistSelectedImage(2, "Histogram of image in blackout")# Histogram of image in blackout (a lot of noise)
    source.getHistSubtractImage(3, "Histogram of the difference image")# Histogram of the difference image

# Edge Detector
img_diff_clean = source.setZeroChannel(2,img_diff) # deletes B channel
img_diff_ocv_canny = source.convertPILtoCV2(img_diff_clean) # to OpenCV
img_diff_ocv_thr = source.convertPILtoCV2(img_diff_clean) # to OpenCV
img_diff_ocv_grid = source.convertPILtoCV2(img_diff_clean) # to OpenCV
img_diff_ocv_contour = source.convertPILtoCV2(img_diff_clean) # to OpenCV
canny, thr = source.autoEdgeDetector(img_diff_ocv_canny) # edges
mask = np.zeros(canny.shape, np.uint8) # black mask

# Find Contours
image_canny, img_diff_ocv_canny, contours_canny, x_c, y_c, width_c, height_c = source.getSquareCoordinates(canny, img_diff_ocv_canny) # Canny
image_thr, img_diff_ocv_thr, contours_thr, x_t, y_t, width_t, height_t = source.getSquareCoordinates(thr, img_diff_ocv_thr) # Threshold
angle, line = source.getRotationAngle(image_canny) # Only with Canny

canny_ratio=float(width_c)/float(height_c)
canny_area=float(width_c)*float(height_c)
thr_ratio=float(width_t)/float(height_t)
thr_area=float(width_t)*float(height_t)

if min(canny_ratio,thr_ratio, key=lambda x:abs(x-1))==thr_ratio:
    print "\nThreshold detects a square"
    x = x_t
    y = y_t
    width = width_t
    height = height_t
    if canny_area > thr_area:
        warnings.warn("Warning: The area of detected ROI from Canny is greater than Threshold. Check this please!")
else:
    print "\nCanny detects a square"
    x = x_c
    y = y_c
    width = width_c
    height = height_c
    if thr_area > canny_area:
        warnings.warn("Warning: The area of detected ROI from Threshold is greater than Canny. Check this please!")

x, y, width, height = source.makeCorrectionGrid(x, y, width, height, 0, 0, 0, 0) # I use the original ROI detected
coor = x, y, width, height

# Write ROI coordinates
file_calib.write(str(coor)+'\n')
file_calib.close()
file_calib = open(file_calib_location, 'a')
file_calib.write(str(angle)+'\n')
file_calib.close()

source.makeGrid(x, y, width, height, img_diff_ocv_grid)
img_diff_ocv_angle = source.rotateImage(img_diff_ocv_grid,angle)
source.makeGrid(x, y, width, height, img_diff_ocv_angle)

# Show info
if verbose==True:
    print "\nCanny Detector shapes\n| x | y | width | height |"
    for c in contours_canny:
        xi, yi, wi, hi = cv2.boundingRect(c)
        print '|',xi,'|',yi,'|',wi,'|',hi,'|'
    print "\nThreshold Detector shapes\n| x | y | width | height |"
    for c in contours_thr:
        xi, yi, wi, hi = cv2.boundingRect(c)
        print '|',xi,'|',yi,'|',wi,'|',hi,'|'
    print "\nCorrected Shape \n| x | y | width | height |"
    print '|',x,'|',y,'|',width,'|',height,'|'

if write==True:
	cv2.imwrite(img_location + "/img_diff_ocv_grid.jpg", img_diff_ocv_grid);
	cv2.imwrite(img_location + "/img_diff_ocv_angle.jpg", img_diff_ocv_angle);
	cv2.imwrite(img_location + "/img_diff_ocv_canny_mask.jpg", img_diff_ocv_canny);
	cv2.imwrite(img_location + "/img_diff_ocv_thr_mask.jpg", img_diff_ocv_thr);
	cv2.imwrite(img_location + "/img_diff_ocv_grid.jpg", img_diff_ocv_grid);
	cv2.imwrite(img_location + "/img_canny.jpg", image_canny);
	cv2.imwrite(img_location + "/img_thr.jpg", image_thr);

if show==True:
    cv2.namedWindow('EdgeDetector: Grid', cv2.WINDOW_NORMAL)
    cv2.imshow('EdgeDetector: Grid', img_diff_ocv_grid)
    cv2.namedWindow('EdgeDetector: Rotate', cv2.WINDOW_NORMAL)
    cv2.imshow('EdgeDetector: Rotate', img_diff_ocv_angle)
    cv2.namedWindow('EdgeDetector: Canny and Mask', cv2.WINDOW_NORMAL)
    cv2.namedWindow('EdgeDetector: Threshold and Mask', cv2.WINDOW_NORMAL)
    cv2.imshow('EdgeDetector: Canny and Mask', img_diff_ocv_canny)
    cv2.imshow('EdgeDetector: Threshold and Mask', img_diff_ocv_thr)
    cv2.namedWindow('EdgeDetector: Canny', cv2.WINDOW_NORMAL)
    cv2.namedWindow('EdgeDetector: Threshold', cv2.WINDOW_NORMAL)
    cv2.imshow('EdgeDetector: Canny', image_canny)
    cv2.imshow('EdgeDetector: Threshold', image_thr)
    cv2.waitKey(0)
