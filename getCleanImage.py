import sys
from GammaDetection import GammaDetection
import cv2
import numpy as np
import argparse

# Args parser
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--source", required=True,
	help="Path to essay directory of images acquire with radioactive sources")
ap.add_argument("-b", "--background", required=True,
	help="Path to essay directory of images acquire in background")
ap.add_argument("-i", "--index", required=True, type=int,
	help="Image index for the image processing in the essay directory")
ap.add_argument("-s", "--show", default=False, type=bool,
	help="Show graphics")
args = vars(ap.parse_args())

# Variables
path_source=args["source"] # Path to the essay directory with the radioactive sources (images)
path_blackout=args["background"] # Path to the essay directory without the radioactive sources (images), the acquisition was in blackout
image_index=args["index"] # Image index for the image processing in the essay directory
show = args["show"] # Show images

# Script
source = GammaDetection(path_source, image_index) # Object with radioactive source
blackout = GammaDetection(path_blackout, image_index) # Object without radioactive source

img_src = source.getSelectedImage() # Image from essay with sources
img_blk = blackout.getSelectedImage() # Image from essay without sources
img_diff = source.getSubtractImage(img_blk) # A way to reduce the camera noise
if show==True:
    img_src.show()
    img_diff.show()

# Histograms
if show==True:
    source.getHistSelectedImage(1, "Histogram of image with sources")# Histogram of image with sources
    blackout.getHistSelectedImage(2, "Histogram of image in blackout")# Histogram of image in blackout (a lot of noise)
    source.getHistSubtractImage(3, "Histogram of the difference image")# Histogram of the difference image

# Canny Detector
img_diff_r_0 = source.setZeroChannel(0,img_diff) # deletes R channel
img_diff_r_0_ocv = source.convertPILtoCV(img_diff_r_0) # to OpenCV
edges_median=source.autoCannyDetector(img_diff_r_0_ocv) # edges

if show==True:
    cv2.namedWindow('Image difference (without red channel)', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Image edges', cv2.WINDOW_NORMAL)
    cv2.imshow('Image difference (without red channel)',img_diff_r_0_ocv)
    cv2.imshow('Image edges',edges_median)
    cv2.waitKey(0)
