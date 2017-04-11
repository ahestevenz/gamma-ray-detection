from ImageProcessing import ImageProcessing
import numpy as np

class GammaDetection(ImageProcessing):

    def __init__(self, path, index):
        ImageProcessing.__init__(self, path, index)
        self.description = "Gamma Detection class"
        self.author = "Ariel Hernandez Estevenz"

    def getSquaresValues(self, x, y, width, height, img=None):
        if img is None:
            img = self.getSubtractGrayImage()
        x_step=width/10
        y_step=height/10
        k=0
        mat_values=np.empty([100])
        for i in range(x,x+width-x_step,x_step):
            for j in range(y,y+height-y_step,y_step):
                mat_values[k]=self.getSquareValue(i,j,x_step,y_step,img)
                k+=1
        mat_values=np.reshape(mat_values, (10, 10))
        return mat_values

    def getSquareValue(self, x, y, x_step, y_step, img=None):
        if img is None:
            img = self.getSubtractGrayImage()
        np_img = np.array(img)
        super_pixel = np_img[x:x+x_step,y:y+y_step]
        super_pixel_value = np.sum(super_pixel)/(x_step*y_step)
        return super_pixel_value
