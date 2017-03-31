import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import glob
import sys, os
from PIL import Image
from PIL import ImageChops

class ImageProcessing:

    def __init__(self, path, index):
        self.path = path
        self.index = index
        self.img = self.getImage()
        self.description = "Image Processing and Computer Vision python class"
        self.author = "Ariel Hernandez Estevenz"

    def getSelectedImage(self):
        return self.img

    def getSubtractImage(self, img_blackout):
        self.setSubtractImage(img_blackout)
        return self.subimg

    def getHistSelectedImage(self, figure, figure_text="Histogram"):
        self.getHist(self.img, figure, figure_text)

    def getHistSubtractImage(self, figure, figure_text="Histogram"):
        self.getHist(self.subimg, figure, figure_text)

    def getListImage(self, show=False):
        image_list = []
        for path_image in sorted(glob.glob(self.path+'/*.tif')): # assuming tif
            im=Image.open(path_image)
            image_list.append(im)
            filename=os.path.basename(path_image)
            if show:
                im.show(title=filename)
            print(filename)
        return image_list

    def getImage(self, index=None):
        if index is None:
            index = self.index
        image_list = self.getListImage()
        return image_list[index]

    def setSubtractImage(self, img_blackout):
        self.subimg = ImageChops.subtract(self.img,img_blackout)

    def getHistPlotChannel(self, img, xlabel, ylabel, color):
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        n, bins, patches = plt.hist(np.array(img).ravel(), bins=256, range=(0.0, 255.0), fc='k', ec='k')
        plt.setp(patches, 'facecolor', color, 'alpha', 0.75)

    def getHist(self, img, figure, figure_text=""):
        r_img, g_img, b_img = img.split()
        plt.ion()
        plt.figure(figure)
        plt.subplot(311)
        plt.title("Histogram")
        self.getHistPlotChannel(r_img, "Bins", "$R$ channel", "r")
        plt.subplot(312)
        self.getHistPlotChannel(g_img, "Bins", "$G$ channel", "g")
        plt.subplot(313)
        self.getHistPlotChannel(b_img, "Bins", "$B$ channel", "b")
        plt.show()
        raw_input(figure_text + '. Figure '+ str(figure) +'. Press Enter to continue...')

    def setZeroChannel(self, channel_index, img = None):
        if img is None:
            img = self.img
        r_img, g_img, b_img = img.split()
        if channel_index == 0:
            r_img = Image.new('L', r_img.size)
        elif channel_index == 1:
            g_img = Image.new('L', g_img.size)
        elif channel_index == 2:
            b_img = Image.new('L', b_img.size)
        im = Image.merge("RGB", (r_img, g_img, b_img))
        return im

    def showRGBChannel(self, channel_index, img = None):
        if img is None:
            img = self.img
        r_img, g_img, b_img = img.split()
        if channel_index == 0:
            r_img.show(title="R")
        elif channel_index == 1:
            g_img.show(title="G")
        elif channel_index == 2:
            b_img.show(title="B")

    def autoCannyDetector(self, image, th_factor=3):
        if len(image.shape)==3:
            print 'Color image: Converting to gray ...'
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        im_median = cv2.medianBlur(image, 3)
        th, bw = cv2.threshold(im_median, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) # Paper: The Study on An Application of Otsu Method in Canny Operator
        th_min=th*th_factor # Empirical value
        th_max=th_min*1.3 # The max value is about 30% of the min value (test)
        edged = cv2.Canny(im_median, th_min, th_max, True)
        return edged

    def convertPILtoCV(self, image):
        image_ocv=cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        return image_ocv
