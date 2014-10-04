import PIL
from PIL import ImageChops, ImageGrab
import DisplayCanvas
import time
import numpy as np

class ScreenMonitor:

    def __init__(self, bbox=None):
        if not bbox:
            bbox = (0,0, 1024, 768)  # supposed to be full screen size
        self.image = ImageGrab.grab(bbox)
        size = (bbox[2] - bbox[0], bbox[3] - bbox[1])
        self.bbox = bbox
        #self.displayBuffer = DisplayCanvas.DisplayBuffer(size)  # when given an image to display, will send via serial
                # to USBviewer. While sending, if it notes that a newer image is available, it will remove the old one
                # from sync queue and update with newer image.
        self.maxImageSize = (50, 50)

    def update(self):
        newIm = ImageGrab.grab(self.bbox)
        if self.image is None:
            self.image = newIm
            return
        difIms = self.get_image_difference_images(self.image, newIm)
        self.image = newIm
        return difIms
        

    #---------------- this will work
            #--------------------
    #http://stackoverflow.com/a/20220680
            # rectangular decomposition of binary images

            # or try this
            #http://www.ee.surrey.ac.uk/Projects/Labview/minimisation/karnaugh.html        

    # right now this treats images as a numpy array. Maybe.. I can convert to a numpy array to make this bit easier?
    def create_square_from_image(self, im):
        # just hem in from all four sides, looking for the first instances of white
        for y in range(im.shape[1]):
            topSlice = im[:, y]
            if True in topSlice:
                break
        top = y
        for y in range(im.shape[1] - 1, top - 1, -1):
            bottomSlice = im[:, y]
            if True in bottomSlice:
                break
        bottom = y
        for x in range(im.shape[0]):
            leftSlice = im[x, :]
            if True in leftSlice:
                break
        left = x
        for x in range(im.shape[0] - 1, left - 1, -1):
            rightSlice = im[x, :]
            if True in rightSlice:
                break
        right = x
        return (left, top, right, bottom)  # top-left to bottom-right coordinates (in x, y format)

    def split_bbox_into_limited_size_bboxes(self, bbox, limit):
        xmin, ymin, xmax, ymax = bbox
        bboxes = []
        for y in range(ymin, ymax, limit):
            height = min(ymax - y, limit)
            for x in range(xmin, xmax, limit):
                width = min(xmax - x, limit)
                bbox = (x, y, x + width, y + height)
                bboxes.append(bbox)
        return bboxes

    def get_difference_image_bboxes(self, im):
        self.croppedBbox = self.create_square_from_image(im)
        #raise
        #diffSquare = im.slice(coordinate[0], coordinate[1])
        bboxes = self.split_bbox_into_limited_size_bboxes(self.croppedBbox, 50)
        return bboxes  # put the difference square in a list. Next time you
                        #should expect to be giving multiple squares of difference

    def get_image_difference_images(self, imOld, imNew):
        imdif = ImageChops.difference(imOld, imNew)
        self.difBW = imdif.convert('L')
        self.difBW.load()
        #raise  # I get an error when trying to load image as an array of type int
        self.imArray = np.asarray(self.difBW, dtype='int32')
        #raise  # accessing the array (when loading as type 'bool') errors when accessing imArray[-1,-1] or [:,x]
        bboxes = self.get_difference_image_bboxes(self.imArray)
        imChunks = []
        for bbox in bboxes:
            imChunk = imNew.crop(bbox)
            imChunks.append(imChunk)
        return imChunks

if __name__ == '__main__':
    sm = ScreenMonitor()
    time.sleep(3)
    ims = sm.update()
    
    
