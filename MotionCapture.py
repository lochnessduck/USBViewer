import PIL
from PIL import ImageChops, ImageGrab
from DisplayCanvas import DisplayImage, Display, BoundingBox
import time
import numpy as np
import copy
from timeit import timeit
#import Debug


class ScreenMonitor:

    def __init__(self, bbox=None):
        if not bbox:
            bbox = BoundingBox(0, 0, 1024, 768)  # supposed to be full screen size
        self.image = None  # first instance will not have anything displayed
        self.bbox = bbox  # this bbox is for capturing image. Putting image
          # onto display requires xy = (0,0)

    def get_screen_changes_as_display_images(self, totalRefresh=False):
        imOld = self.image
        imNew = ImageGrab.grab(self.bbox)
        self.image = imNew  # the timing of where to set self.image is critical
          # if it's later than this, first-run will never reach past the if-statement
        if imOld is None or totalRefresh:  # which means it's the first time or a refresh is desired
            return [DisplayImage.from_image(imNew)]
        updateImages = self._get_update_images(imOld, imNew)
        return updateImages

    def _get_update_images(self, imOld, imNew):
        bbox = self._get_bounding_box_for_differences_between_images(imOld, imNew)
        if bbox is None or bbox.size == (0,0):
            imChunks = []
        else:
            imCropped = self._crop_image_to_bbox(imNew, bbox)
            imChunks = self._split_image_into_chunks(imCropped)
        return imChunks
    
    def _crop_image_to_bbox(self, im, bbox):
        dimNew = DisplayImage.from_image(im)  # image here will start at 0
        return dimNew.crop(bbox)
    
    def _split_image_into_chunks(self, im, limit=50):
        images = []
        width, height = im.size
        for x in range(0, width, limit):
            for y in range(0, height, limit):
                cropWidth = min(width - x, limit)
                cropHeight = min(height - y, limit)
                bbox = BoundingBox.using_size((x, y), (cropWidth, cropHeight))
                imCropped = im.crop(bbox)
                images.append(imCropped)
        return images

    # numpy arrays: [y,x]... images: [x,y]... Please keep that in mind.
    def _get_bounding_box_for_differences_between_images(self, imOld, imNew):
        imdif = ImageChops.difference(imOld, imNew)
        grayscale = imdif.convert('L')  # convert color to grayscale.
        grayscale.load()
        array = np.asarray(grayscale, dtype='int32')  # numpy array
        if not sum(sum(array)):
            print('no difference in images!', sum(sum(array)))
            return BoundingBox(0, 0, 0, 0)
        # just hem in from all four sides, looking for the first positive values
        for y in range(array.shape[0]):
            topSlice = array[y, :]
            if sum(topSlice):
                break
        top = y
        for y in range(array.shape[0] - 1, top - 1, -1):
            bottomSlice = array[y, :]
            if sum(bottomSlice):
                y += 1  # compensate for the outer edge of bbox
                break
        bottom = y
        for x in range(array.shape[1]):
            leftSlice = array[:, x]
            if sum(leftSlice):
                break
        left = x
        for x in range(array.shape[1] - 1, left - 1, -1):
            rightSlice = array[:, x]
            if sum(rightSlice):
                x += 1  # compensate for outer edge of bbox
                break
        right = x
        bbox = BoundingBox(left, top, right, bottom)
        return bbox  # top-left to bottom-right coordinates (in x, y format)


class DisplayUpdater:

    def __init__(self, display, monitor):
        self.display = display
        self.monitor = monitor

    def update(self):
        dImages = self.monitor.get_screen_changes_as_display_images()
        self.display.extend(dImages)


if __name__ == '__main__':
    bbox = BoundingBox.using_size((0, 0), (600, 600))
    display = Display(bbox.size)
    monitor = ScreenMonitor(bbox)
    updater = DisplayUpdater(display, monitor)
    while display.tick():
        updater.update()

