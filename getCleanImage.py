import sys
from GammaDetection import GammaDetection

# Variables
path_source=sys.argv[1] # Path to the essay directory with the radioactive sources (images)
path_blackout=sys.argv[2] # Path to the essay directory without the radioactive sources (images), the acquisition was in blackout
image_index=int(sys.argv[3]) # Image index for the image processing in the essay directory

# Script
source = GammaDetection(path_source, image_index) # Object with radioactive source
blackout = GammaDetection(path_blackout, image_index) # Object without radioactive source

img_src = source.getSelectedImage()# Image from essay with sources
img_blk = blackout.getSelectedImage()# Image from essay without sources
img_src.show()

# A way to reduce the camera noise
img_diff = source.getSubtractImage(img_blk)
img_diff.show()

# Histograms
source.getHistSelectedImage(1, "Histogram of image with sources")# Histogram of image with sources
blackout.getHistSelectedImage(2, "Histogram of image in blackout")# Histogram of image in blackout (a lot of noise)
source.getHistSubtractImage(3, "Histogram of the difference image")# Histogram of the difference image
