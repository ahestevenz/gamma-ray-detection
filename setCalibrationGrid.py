from GammaDetection import GammaDetection
import cv2
import os
import argparse
import warnings
from shutil import copyfile
import numpy as np

### Args parser
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True,
	help="path to directory of images acquire with calibration set")
ap.add_argument("-b", "--background", required=True,
	help="path to directory of images acquire in background")
ap.add_argument("-i", "--index", required=True, default=0, type=int,
	help="image index for the image processing in the directory")
ap.add_argument("-f", "--file_calib", default="./config.calib", type=str,
	help="calibration file location")
ap.add_argument("-s", "--show", default=False, type=bool,
	help="show graphics")
args = vars(ap.parse_args())

### Variables
path_images=args["directory"] # Path to directory of images acquire with calibration set
path_blackout=args["background"] # Path to the directory without the radioactive sources or LED (images), the acquisition was in blackout
image_index=args["index"] # Image index for the image processing in the directory
show = args["show"] # Show images
file_calib_location = args["file_calib"] # Calibration file location
if os.path.exists(file_calib_location):
    print "File exists. Backing up ..." # Warning: File exists, so I backed up, just in case!
    copyfile(file_calib_location, file_calib_location+'.previous')
file_calib = open(file_calib_location, 'w')

### Script
source = GammaDetection(path_images, image_index) # Object with radioactive source
blackout = GammaDetection(path_blackout, image_index) # Object without radioactive source

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
canny, thr = source.autoEdgeDetector(img_diff_ocv_canny) # edges
mask = np.zeros(canny.shape, np.uint8) # black mask

# Find Contours
image_canny, contours_canny = source.findContours(canny)
contours_canny = sorted(contours_canny, key = cv2.contourArea, reverse = True)[:10]
image_thr, contours_thr = source.findContours(thr)
contours_thr = sorted(contours_thr, key = cv2.contourArea, reverse = True)[:10]

x_c, y_c, width_c, height_c = cv2.boundingRect(contours_canny[0]) # Canny
x_t, y_t, width_t, height_t = cv2.boundingRect(contours_thr[0]) # Threshold
cv2.rectangle(img_diff_ocv_canny, (x_c, y_c), (x_c + width_c, y_c + height_c), (0,0,255), 2)
cv2.rectangle(img_diff_ocv_thr, (x_t, y_t), (x_t + width_t, y_t + height_t), (0,0,255), 2)

cv2.drawContours(img_diff_ocv_canny, contours_canny, -1, (0, 255, 0), 8)
cv2.drawContours(img_diff_ocv_thr, contours_thr, -1, (0, 255, 0), 8)

canny_ratio=float(width_c)/float(height_c)
canny_area=float(width_c)*float(height_c)
thr_ratio=float(width_t)/float(height_t)
thr_area=float(width_t)*float(height_t)

if min(canny_ratio,thr_ratio, key=lambda x:abs(x-1))==thr_ratio:
    print "Threshold detects a square"
    coor=x_t, y_t, width_t, height_t
    if canny_area > thr_area:
        warnings.warn("Warning: The area of detected ROI from Canny is greater than Threshold. Check this please!")
else:
    print "Canny detects a square"
    coor=x_c, y_c, width_c, height_c
    if thr_area > canny_area:
        warnings.warn("Warning: The area of detected ROI from Threshold is greater than Canny. Check this please!")

file_calib.write(str(coor)+'\n')
file_calib.close()

if show==True:
    print "Canny Detector shapes\n| x | y | width | height |"
    for c in contours_canny:
        x, y, width, height = cv2.boundingRect(c)
        print '|',x,'|',y,'|',width,'|',height,'|'
    print "\nThreshold Detector shapes\n| x | y | width | height |"
    for c in contours_thr:
        x, y, width, height = cv2.boundingRect(c)
        print '|',x,'|',y,'|',width,'|',height,'|'
    cv2.namedWindow('EdgeDetector: Canny and Mask', cv2.WINDOW_NORMAL)
    cv2.namedWindow('EdgeDetector: Threshold and Mask', cv2.WINDOW_NORMAL)
    cv2.imshow('EdgeDetector: Canny and Mask', img_diff_ocv_canny)
    cv2.imshow('EdgeDetector: Threshold and Mask', img_diff_ocv_thr)
    cv2.waitKey(0)
