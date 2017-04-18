#!/usr/bin/env python
"""Gamma Detection class.
"""
from ImageProcessing import ImageProcessing
import matplotlib.pyplot as plt
import numpy as np

__author__ = "Ariel Hernandez Estevenz"
__copyright__ = "Copyright 2017, Comision Nacional de Energia Atomica"
__credits__ = ["Ariel Hernandez Estevenz"]
__version__ = "0.1"
__maintainer__ = "Ariel Hernandez Estevenz"
__email__ = "ahernandez@cae.cnea.gov.ar, ariel.h.estevenz@ieee.org"
__status__ = "Development"

class GammaDetection(ImageProcessing):

    def __init__(self, path, index, frame=0, verbose=False):
        ImageProcessing.__init__(self, path, index, frame, verbose)
        self.description = "Gamma Detection class"
        self.author = "Ariel Hernandez Estevenz"

    def getSquaresValues(self, x, y, width, height, verbose_mode=False, img=None):
        if img is None:
            img = self.getSubtractGrayImage()
        if verbose_mode==True:
            file_matrix = open("matrix_values_structure.txt", 'w')
            file_matrix.write("| SuperPixel Block Information |\n")
            file_matrix.write("| X_init | X_init + X_step |\n")
            file_matrix.write("| Y_init | Y_init + Y_step |\n")
            file_matrix.write("| Matrix index | X | Y | SuperPixel Value |\n")
        x_step=int(round(width/10))
        y_step=int(round(height/10))
        k=0
        mat_values=np.empty([100])
        for j in range(y,y+height-y_step+1,y_step):
            for i in range(x,x+width-x_step+1,x_step):
                mat_values[k]=self.getSquareValue(i,j,x_step,y_step,img)
                if verbose_mode==True:
                    file_matrix.write(str(i) +","+ str(i+x_step) + "\n")
                    file_matrix.write(str(j) +","+ str(j+y_step) + "\n")
                    file_matrix.write(str(k) +","+ str(i) +","+ str(j) +","+ str(mat_values[k]) + "\n")
                k+=1
        mat_values=np.reshape(mat_values, (10, 10))
        if verbose_mode==True: file_matrix.close
        return mat_values

    def getSquareValue(self, x, y, x_step, y_step, img=None):
        if img is None:
            img = self.getSubtractGrayImage()
        np_img = np.array(img)
        super_pixel = np_img[y:y+y_step,x:x+x_step]
        super_pixel_value = np.sum(super_pixel)/(x_step*y_step)
        return super_pixel_value

    def getPlotSuperPixelMatrix(self, x, y, width, height, verbose_mode=False, img=None):
        mat_values = self.getSquaresValues(x, y, width, height, verbose_mode=False, img=None)
        c = plt.pcolor(mat_values, edgecolors='k', linewidths=1, cmap='jet')
        plt.gca().invert_yaxis()
        plt.colorbar()
        plt.title('SuperPixels 10x10 Matrix values')
        plt.show()
        return mat_values
