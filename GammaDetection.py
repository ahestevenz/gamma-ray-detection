from ImageProcessing import ImageProcessing

class GammaDetection(ImageProcessing):

    def __init__(self, path, index):
        ImageProcessing.__init__(self, path, index)        
        self.description = "Gamma Detection class"
        self.author = "Ariel Hernandez Estevenz"
