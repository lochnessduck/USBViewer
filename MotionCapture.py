import PIL
from PIL import ImageChops, ImageGrab
from DisplayCanvas import DisplayImage, Display, BoundingBox
import time
import numpy as np
import Debug

class ScreenMonitor:

    def __init__(self, bbox=None):
        if not bbox:
            bbox = BoundingBox(0, 0, 1024, 768)  # supposed to be full screen size
        self.image = None  # ImageGrab.grab(bbox)  first instance will not have anything displayed
        self.bbox = bbox

    def get_changes_as_display_images(self, totalRefresh=False):
        newIm = ImageGrab.grab(self.bbox)
        if self.image is None or totalRefresh:  # which means it's the first time or a refresh is desired
            self.image = newIm
            return [DisplayImage(self.image, self.bbox.xy)]
        difImages = self.get_cropped_images_update(self.image, newIm)
        self.image = newIm
        return difImages

    def get_cropped_images_update(self, imOld, imNew):
        imdif = ImageChops.difference(imOld, imNew)
        difBW = imdif.convert('L')
        difBW.load()
        imArray = np.asarray(difBW, dtype='int32')
        bbox = self.create_square_from_image(imArray)
        if bbox is None or bbox.size == (0,0):  # if bbox is None or box has no size
            return []
        imCropped = imNew.crop(bbox)
        return [DisplayImage(imCropped, bbox.xy)]

    # right now this treats images as a numpy array. Maybe.. I can convert to a numpy array to make this bit easier?
    # FOUND numpy array coordinates are accessed by [y, x], whereas images are accessed by [x, y]. Please keep that in mind.
    def create_square_from_image(self, im):
        # just hem in from all four sides, looking for the first instances of white
        for y in range(im.shape[0]):
            topSlice = im[y, :]
            if sum(topSlice):
                break
        top = y
        for y in range(im.shape[0] - 1, top - 1, -1):
            bottomSlice = im[y, :]
            if sum(bottomSlice):
                y += 1  # if we found something, then that means the bounding box must be extended by one downward. So that the bounding box correctly shows the bottom part. Remember, this is where bottom -1 is included, but not bottom coordinate.
                break
        bottom = y
        for x in range(im.shape[1]):
            leftSlice = im[:, x]
            if sum(leftSlice):
                break
        left = x
        for x in range(im.shape[1] - 1, left - 1, -1):
            rightSlice = im[:, x]
            if sum(rightSlice):
                x += 1  # if we found something, then that means the bounding box to the right must extend by one (because x is not included in the image, x-1 IS)
                break
        right = x
        bbox = BoundingBox(left, top, right, bottom)
        return bbox  # top-left to bottom-right coordinates (in x, y format)


class DisplayUpdater:

    def __init__(self, display, monitor):
        self.display = display
        self.monitor = monitor

    def update(self):
        dImages = self.monitor.get_changes_as_display_images()
        self.display.extend(dImages)


if __name__ == '__main__':
    bbox = BoundingBox(0, 0, 300, 600)
    display = Display(bbox.size)
    monitor = ScreenMonitor(bbox)
    updater = DisplayUpdater(display, monitor)
    while display.tick():
        time.sleep(1)
        updater.update()
    
    
    
