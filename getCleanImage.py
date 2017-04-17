from GammaDetection import GammaDetection
import cv2
import argparse

### Args parser
ap = argparse.ArgumentParser()
ap.add_argument("-r", "--radioactive_source", required=True,
	            help="path to essay directory of images acquire with radioactive sources")
ap.add_argument("-b", "--background", required=True,
	            help="path to essay directory of images acquire in background")
ap.add_argument("-i", "--index", required=True, type=int,
	            help="image index for the image processing in the essay directory")
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
path_source=args["radioactive_source"] # Path to the essay directory with the radioactive sources (images)
path_blackout=args["background"] # Path to the essay directory without the radioactive sources (images), the acquisition was in blackout
image_index=args["index"] # Image index for the image processing in the essay directory
file_calib_location = args["file_calib"] # Calibration file location
show = args["show"] # Show images and graphics
verbose = args["verbose"] # Verbose mode
write = args["write_images"]  # Save images

### Script
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

# Without R channel
img_diff_clean = source.setZeroChannel(0,img_diff) # deletes R channel
img_diff_clean_ocv = source.convertPILtoCV2(img_diff_clean) # to OpenCV
img_diff_clean_ocv_grid = source.convertPILtoCV2(img_diff_clean) # to OpenCV

if show==True:
    cv2.namedWindow('Image difference (without red channel)', cv2.WINDOW_NORMAL)
    cv2.imshow('Image difference (without red channel)', img_diff_clean_ocv)
    cv2.waitKey(0)
