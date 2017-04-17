import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import glob
import sys, os
from PIL import Image
from PIL import ImageChops

class ImageProcessing:

    def __init__(self, path, index, frame=0, verbose=False):
        self.path = path
        self.index = index
        self.verbose = verbose
        self.frame = frame
        self.img = self.getImage()
        self.description = "Image Processing and Computer Vision python class"
        self.author = "Ariel Hernandez Estevenz"

    def getSelectedImage(self):
        return self.img

    def getSubtractImage(self, img_blackout=None):
        if img_blackout is None:
            return self.subimg
        self.setSubtractImage(img_blackout)
        return self.subimg

    def getSubtractGrayImage(self, img_blackout=None):
        if img_blackout is None:
            return self.subgimg
        self.setSubtractImage(img_blackout)
        return self.subgimg

    def getHistSelectedImage(self, figure, figure_text="Histogram"):
        self.getHist(self.img, figure, figure_text)

    def getHistSubtractImage(self, figure, figure_text="Histogram"):
        self.getHist(self.subimg, figure, figure_text)

    def getListImage(self, show=False):
        image_list = []
        for path_image in sorted(glob.glob(self.path+'/*.tif')): # assuming tif
            try:
                im=Image.open(path_image)
            except IOError:
                print "Error opening file :: "  + path_image
                print "Application halt! "
                sys.exit(1)
            image_list.append(im)
            filename=os.path.basename(path_image)
            if show:
                im.show(title=filename)
            if self.verbose==True: print(filename)
        return image_list

    def getImageFrame(self, frame=None, img=None):
        if img is None:
            img = self.img
        if frame is None:
            frame = self.frame
        try:
            img.seek(frame)
        except EOFError:
            print "Error getting frame :: "  + str(frame)
            print "Application halt!"
            sys.exit(1)
        if self.verbose==True: print "The image frame selected is: " + str(img.tell())
        return img

    def getImage(self, frame=None, index=None):
        if index is None:
            index = self.index
        if frame is None:
            frame = self.frame
        image_list = self.getListImage()
        try:
            im = self.getImageFrame(frame,image_list[index])
        except IndexError as e:
            print "Error getting image:: "  + str(e)
            print "Application halt!"
            sys.exit(1)
        return im

    def setSubtractImage(self, img_blackout):
        self.subimg = ImageChops.subtract(self.img,img_blackout)
        self.subgimg = self.subimg.convert('L')

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

    def convertCV2ColortoGray(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image

    def autoEdgeDetector(self, image, th_factor=1, SigmaColor=15, diag_factor=0.01, SigmaColorCanny=20, diag_factor_canny=0.1):
        if len(image.shape)==3:
            if self.verbose==True: print 'Color image: Converting to gray ...'
            image = self.convertCV2ColortoGray(image)
        h, w = image.shape
        if self.verbose==True: print 'Thresholding: Processing ...'
        diag = np.sqrt(h**2 + w**2)
        SigmaSpace = diag_factor*diag # diag_factor=0.01 is better for Threshold Detector
        im_bilateral = cv2.bilateralFilter(image, -1, SigmaColor, SigmaSpace) # Paper: Bilateral Filtering for Gray and Color Images
        _, edged_binary = cv2.threshold(im_bilateral, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) # Paper: The Study on An Application of Otsu Method in Canny Operator
        if self.verbose==True: print 'Canny: Processing ...'
        SigmaSpace = diag_factor_canny*diag # diag_factor=0.1 is better for Canny Detector
        im_bilateral = cv2.bilateralFilter(image, -1, SigmaColorCanny, SigmaSpace) # Paper: Bilateral Filtering for Gray and Color Images
        th, _ = cv2.threshold(im_bilateral, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) # Paper: The Study on An Application of Otsu Method in Canny Operator
        th_min=th*th_factor # 1 is an empirical value
        th_max=th_min*1.1 # The max value is about 10% of the min value (test)
        edged = cv2.Canny(im_bilateral, th_min, th_max, True)
        return edged, edged_binary

    def convertPILtoCV2(self, image):
        image_ocv=cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        return image_ocv

    def openMorphEdgeImage(self, edges):
        kernel = np.ones((5,5),np.uint8)
        edges_median = cv2.medianBlur(edges, 3)
        edge_opening = cv2.morphologyEx(edges_median, cv2.MORPH_OPEN, kernel)
        return edges_opening

    def closeMorphEdgeImage(self, edges):
        kernel = np.ones((5,5),np.uint8)
        edges_median = cv2.medianBlur(edges, 3)
        edge_closing = cv2.morphologyEx(edges_median, cv2.MORPH_CLOSE, kernel)
        return edges_closing

    def rotateImage(self, image, angle):
        image_center = tuple(np.array(image.shape)[:2]/2)
        mat = cv2.getRotationMatrix2D(image_center,angle,1.0)
        image_rot = cv2.warpAffine(image, mat, image.shape[:2],flags=cv2.INTER_LINEAR)
        return image_rot

    def findContours(self, edges):
        im2, contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
        return im2, contours

    def makeCorrectionGrid(self, x, y, width, height, increase_x=1.2, increase_y=3.5, reduction_w=3.1, reduction_h=4.6):
        # I saw a few differences (default parameters) between the detected ROI and the original square in the image.
        y=int(round(y*(1+increase_y/100)))
        height=int(round(height*(1-reduction_h/100)))
        x=int(round(x*(1+increase_x/100)))
        width=int(round(width*(1-reduction_w/100)))
        return x, y, width, height

    def makeGrid(self, x, y, width, height, img):
        x_step=int(width/10)
        y_step=int(height/10)
        for i in range(x, x+width+1, x_step):
            cv2.line(img,(i,y),(i,y+height),(255,0,0),3)
        for j in range(y, y+height+1, y_step):
            cv2.line(img,(x,j),(x+width,j),(255,0,0),3)

    def getSquareCoordinates(self, img_edges, img_diff):
        im, contours = self.findContours(img_edges)
        x, y, width, height = cv2.boundingRect(contours[0])
        cv2.rectangle(img_diff, (x, y), (x + width, y + height), (0,0,255), 2)
        cv2.drawContours(img_diff, contours, -1, (0, 255, 0), 8)
        return im, img_diff, contours, x, y, width, height

    def getRotationAngle(self, img_canny):
        # This operation has been done with Canny Detector. The results are better than Threshold detector
        lines_canny = cv2.HoughLines(img_canny, 1, np.pi/180, 70)
        lines_canny_p = cv2.HoughLinesP(img_canny, 1, np.pi/180, 70)
        k=0
        angle=lines_canny[k][0][1]
        while ((np.pi-angle) > 0.5): # detect only horizontal lines
            angle=lines_canny[k][0][1]
            line=lines_canny_p[k][0]
            k+=1
        return np.pi-angle, line
