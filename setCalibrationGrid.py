from GammaDetection import GammaDetection
import cv2
import argparse
import numpy as np


# Args parser
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True,
	help="path to directory of images acquire with calibration set")
ap.add_argument("-b", "--background", required=True,
	help="path to directory of images acquire in background")
ap.add_argument("-i", "--index", required=True, type=int,
	help="image index for the image processing in the directory")
ap.add_argument("-s", "--show", default=False, type=bool,
	help="show graphics")
args = vars(ap.parse_args())

# Variables
path_images=args["directory"] # Path to directory of images acquire with calibration set
path_blackout=args["background"] # Path to the directory without the radioactive sources or LED (images), the acquisition was in blackout
image_index=args["index"] # Image index for the image processing in the directory
show = args["show"] # Show images

# Script
source = GammaDetection(path_images, image_index) # Object with radioactive source
blackout = GammaDetection(path_blackout, image_index) # Object without radioactive source

img_src = source.getSelectedImage() # Image from essay with sources
img_blk = blackout.getSelectedImage() # Image from essay without sources
img_diff = source.getSubtractImage(img_blk) # A way to reduce the camera noise
#if show==True:
#    img_src.show()
#    img_diff.show()

# Histograms
#if show==True:
#    source.getHistSelectedImage(1, "Histogram of image with LED light")# Histogram of image with sources
#    blackout.getHistSelectedImage(2, "Histogram of image in blackout")# Histogram of image in blackout (a lot of noise)
#    source.getHistSubtractImage(3, "Histogram of the difference image")# Histogram of the difference image

# Canny Detector
img_diff_clean = source.setZeroChannel(2,img_diff) # deletes B channel
img_diff_ocv = source.convertPILtoCV(img_diff_clean) # to OpenCV
img_diff_ocv2 = source.convertPILtoCV(img_diff_clean) # to OpenCV
img_diff_ocv3 = source.convertPILtoCV(img_diff_clean) # to OpenCV
img_diff_ocv_hough = source.convertPILtoCV(img_diff_clean) # to OpenCV
edges_1 = source.autoCannyDetector(img_diff_ocv,1.5,10) # edges
edges_2 = source.autoCannyDetector(img_diff_ocv2,1.5,20) # edges
edges_3 = source.autoCannyDetector(img_diff_ocv3,1.5,30) # edges
edges_4 = source.autoCannyDetector(img_diff_ocv_hough,1.5) # edges

##############################
# findContours and approxPolyDP

cv2.namedWindow('Contour', cv2.WINDOW_NORMAL)
cv2.namedWindow('Edges', cv2.WINDOW_NORMAL)
cv2.namedWindow('Contour 2', cv2.WINDOW_NORMAL)
cv2.namedWindow('Edges 2', cv2.WINDOW_NORMAL)
cv2.namedWindow('Contour 3', cv2.WINDOW_NORMAL)
cv2.namedWindow('Edges 3', cv2.WINDOW_NORMAL)

#gray = cv2.bilateralFilter(gray, 11, 17, 17)
#edged = cv2.Canny(gray, 30, 200)

image, contours1, _ = cv2.findContours(edges_1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours1 = sorted(contours1, key = cv2.contourArea, reverse = True)[:10]
screenCnt1 = None

# loop over our contours
for c in contours1:
	# approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    screenCnt1 = approx #ojo
	# if our approximated contour has four points, then
	# we can assume that we have found our screen
	#if len(approx) == 4:
	#	screenCnt = approx
	#	break


image, contours2, _ = cv2.findContours(edges_2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours2 = sorted(contours2, key = cv2.contourArea, reverse = True)[:10]
screenCnt2 = None

# loop over our contours
for c in contours2:
	# approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    screenCnt2 = approx #ojo

image, contours3, _ = cv2.findContours(edges_3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours3 = sorted(contours3, key = cv2.contourArea, reverse = True)[:10]
screenCnt3 = None

# loop over our contours
for c in contours3:
	# approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    screenCnt3 = approx #ojo


#  cv2.drawContours(image, contours, contourIdx, color[, thickness[, lineType[, hierarchy[, maxLevel[, offset]]]]])
#    Parameters:

#        image - Destination image.
#        contours - All the input contours. Each contour is stored as a point vector.
#        contourIdx - Parameter indicating a contour to draw. If it is negative, all the contours are drawn.
#        color - Color of the contours.
#        thickness - Thickness of lines the contours are drawn with. If it is negative (for example, thickness=CV_FILLED ), the contour interiors are drawn.
#        lineType - Line connectivity. See line() for details.
#        hierarchy - Optional information about hierarchy. It is only needed if you want to draw only some of the contours (see maxLevel ).
#        maxLevel - Maximal level for drawn contours. If it is 0, only the specified contour is drawn. If it is 1, the function draws the contour(s) and all the nested contours. If it is 2, the function draws the contours, all the nested contours, all the nested-to-nested contours, and so on. This parameter is only taken into account when there is hierarchy available.
#        offset - Optional contour shift parameter. Shift all the drawn contours by the specified \texttt{offset}=(dx,dy) .
#        contour - Pointer to the first contour.
#        externalColor - Color of external contours.
#        holeColor - Color of internal contours (holes).

cv2.drawContours(img_diff_ocv, contours1, -1, (0, 255, 0), 8)
cv2.imshow("Contour", img_diff_ocv)
cv2.imshow("Edges", edges_1)


cv2.drawContours(img_diff_ocv2, contours2, -1, (0, 255, 0), 8)
cv2.imshow("Contour 2", img_diff_ocv2)
cv2.imshow("Edges 2", edges_2)



cv2.drawContours(img_diff_ocv3, contours3, -1, (0, 255, 0), 8)
cv2.imshow("Contour 3", img_diff_ocv3)
cv2.imshow("Edges 3", edges_3)

##############################
# HoughLinesP

cv2.namedWindow('hough', cv2.WINDOW_NORMAL)
minLineLength = 30
maxLineGap = 10
lines = cv2.HoughLinesP(edges_4,1,np.pi/180,15,minLineLength,maxLineGap)
for x in range(0, len(lines)):
    for x1,y1,x2,y2 in lines[x]:
        cv2.line(img_diff_ocv_hough,(x1,y1),(x2,y2),(0,255,0),2)

cv2.imshow('hough',img_diff_ocv_hough)
cv2.waitKey(0)

##############################

if show==True:
    cv2.namedWindow('Image edges 1', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Image edges 2', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Image edges 3', cv2.WINDOW_NORMAL)
    cv2.imshow('Image edges 1', edges_1)
    cv2.imshow('Image edges 2', edges_2)
    cv2.imshow('Image edges 3', edges_3)
    cv2.namedWindow('Corners 1', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Corners 2', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Corners 3', cv2.WINDOW_NORMAL)
    cv2.imshow('Corners 1', corners_1)
    cv2.imshow('Corners 2', corners_2)
    cv2.imshow('Corners 3', corners_3)
    cv2.waitKey(0)
