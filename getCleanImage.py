import sys
from GammaDetection import GammaDetection
import cv2
import numpy as np
import argparse

#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--images", required=True,
#	help="path to input dataset of images")
#args = vars(ap.parse_args())

# Variables
path_source=sys.argv[1] # Path to the essay directory with the radioactive sources (images)
path_blackout=sys.argv[2] # Path to the essay directory without the radioactive sources (images), the acquisition was in blackout
image_index=int(sys.argv[3]) # Image index for the image processing in the essay directory

# Script
source = GammaDetection(path_source, image_index) # Object with radioactive source
blackout = GammaDetection(path_blackout, image_index) # Object without radioactive source

img_src = source.getSelectedImage()# Image from essay with sources
img_blk = blackout.getSelectedImage()# Image from essay without sources
#img_src.show()

# A way to reduce the camera noise
img_diff = source.getSubtractImage(img_blk)
#img_diff.show()

# Histograms
#source.getHistSelectedImage(1, "Histogram of image with sources")# Histogram of image with sources
#blackout.getHistSelectedImage(2, "Histogram of image in blackout")# Histogram of image in blackout (a lot of noise)
#source.getHistSubtractImage(3, "Histogram of the difference image")# Histogram of the difference image

# Canny Dettector Tests
img_diff_r_0 = source.setZeroChannel(0,img_diff)
im = cv2.cvtColor(np.array(img_diff_r_0), cv2.COLOR_RGB2BGR)

cv2.namedWindow('image edges (Median)', cv2.WINDOW_NORMAL)
cv2.namedWindow('image edges auto_canny (Median)', cv2.WINDOW_NORMAL)
cv2.namedWindow('image edges (Gauss)', cv2.WINDOW_NORMAL)
cv2.namedWindow('image edges auto_canny (Gauss)', cv2.WINDOW_NORMAL)

gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
im_median = cv2.medianBlur(gray, 3)
im_gauss = cv2.GaussianBlur(gray, (5, 5), 0)

th, bw = cv2.threshold(im_median, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
th_min=th*3
th_max=th_min*1.3
edges_median = cv2.Canny(im_median, th_min, th_max, True)

th, bw = cv2.threshold(im_gauss, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
th_min=th*3
th_max=th_min*1.3
edges_gauss = cv2.Canny(im_gauss, th_min, th_max, True)

edge_auto_median=source.auto_canny(im_median,20)
edge_auto_gauss=source.auto_canny(im_gauss,20)

cv2.imshow('image edges (Median)',edges_median) # It's the best
cv2.imshow('image edges auto_canny (Median)',edge_auto_median) # It is not working
cv2.imshow('image edges (Gauss)',edges_gauss) # I didn't have good results. Several squares were broken
cv2.imshow('image edges auto_canny (Gauss)',edge_auto_gauss) # Similar to edges_median, but I think that it is not the best.
cv2.waitKey(0)
