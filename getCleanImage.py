import sys
from GammaDetection import GammaDetection
import cv2
import numpy as np


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

# HASTA ACA ES EL SCRIPTT POSTA


im = cv2.cvtColor(np.array(img_diff), cv2.COLOR_RGB2BGR)
#im = cv2.imread('/home/ahestevenz/1.jpg', 0)
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.namedWindow('image grayscale', cv2.WINDOW_NORMAL)
cv2.namedWindow('image edges', cv2.WINDOW_NORMAL)
imgs = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
th, bw = cv2.threshold(imgs, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
edges = cv2.Canny(imgs, th*0.9, th)
cv2.imshow('image',im)
cv2.imshow('image grayscale',imgs)
cv2.imshow('image edges',edges)
cv2.waitKey(0)
