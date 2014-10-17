import pygame
import math
from math import pi
from PIL import Image, ImageGrab
import numpy as np
import copy
import time


class Display:
    
    def __init__(self, size=(700, 400)):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.surfaces = []  #pygame.sprite.group() # just call .draw to draw all
        pygame.display.set_caption("Connected to...")
        self.clock = pygame.time.Clock()  # Used to manage how fast the screen updates
        self.exit = False
        self.size = size

    def append(self, image):
        """ requires a display image, which includes coordinates of where to
            display image
        """
        self.surfaces.append(image)

    def extend(self, images):
        """ requires iterable of display images
        """
        for im in images:
            self.append(im)
        
    def draw(self):
        for dImage in self.surfaces:  #displayImage
            dImage.draw(self.screen)
        pygame.display.flip()
        
    def tick(self):
        """ called to update the display screen. Should be called as often as
            possible
        """
        if self.exit:  # already quit, return False to calling function
            return not self.exit
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("User asked to quit.")
                self.exit = True # Flag that we are done so we exit this loop
            elif event.type == pygame.KEYDOWN:
                print("User pressed a key.")
            elif event.type == pygame.KEYUP:
                print("User let go of a key.")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("User pressed a mouse button")         
        self.draw()        
        # --- Limit to 60 frames per second
        self.clock.tick(60)
        if self.exit:
            pygame.quit()
        return not self.exit
        
    def quit(self):
        self.exit = True
        pygame.quit()
        
    def __iter__(self):
        for dim in self.surfaces:
            yield dim
            
    def __getitem__(self, index):
        return self.surfaces[index]
    
    def __setitem__(self, index, im):
        self.surfaces[index] = im
        
    def __nonzero__(self):
        return len(self.surfaces)
        
    def __contains__(self, im):
        return im in self.surfaces
    
    def __delitem__(self, index):
        del self.surfaces[index]

    def __len__(self):
        return len(self.surfaces)
        
class DisplayImage(pygame.sprite.Sprite):
    
    def __init__(self, im, bbox=None):
        pygame.sprite.Sprite.__init__(self)   # call parent. use Super()instead?
        self.id = 19  # eventually needs to create separate IDs
        imString = im.tostring("raw", "RGB")  # a PILLOW function, default encoder is "raw"
        if not bbox:
            bbox = BoundingBox.using_size(xy, im.size)
        self.surface = pygame.image.fromstring(imString, bbox.size, "RGB")
        self.surface.convert()  # loads / converts image for much faster operation
        self.bbox = bbox
        self.size = im.size
        
    @classmethod
    def from_string(cls, imString, bbox):
        im = pygame.image.fromstring(imString, bbox.size, "RGB")
        return cls(im, bbox)
    
    @classmethod
    def fromScreenshot(cls, bbox):  # bbox points are left-top, right-bottom
        im = ImageGrab.grab(bbox)
        return cls(im, bbox)

    def draw(self, screen):
        screen.blit(self.surface, self.bbox.rect)
        
    def crop(self, bbox):  # must use a BoundingBox
        """ crop always assumes that surface starts at (0,0)
            it does NOT take into account it's own bbox. 
            But after cropping, the bbox will be calculated
            relative to its original bbox.
        """
        surfaceCroppedChild = self.surface.subsurface(bbox.rect)  # still relates to parent!
        surfaceCropped = surfaceCroppedChild.copy()  # copy will give us an independent surface
        other = self.copy()
        other.surface = surfaceCropped
        other.bbox = self.bbox.crop(bbox)
        other.size = bbox.size
        return other
        
    def copy(self):
        return copy.deepcopy(self)
        
        
class BoundingBox:

    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.w = right - left
        self.width = self.w
        self.h = bottom - top
        self.height = self.h
        self.size = (self.w, self.h)
        self.xy = (left, top)
        self.x = left
        self.y = top
        self.rect = pygame.Rect(self.xy, self.size)
        
    @classmethod
    def using_size(cls, xy, size):
        x, y = xy
        w, h = size
        return cls(x, y, x + w, y + h)
    
    def crop(self, bbox):
        """ assumes that crop operates on this instance starting at (0,0)
        """
        x, y = self.x + bbox.x, self.y + bbox.y
        w, h = bbox.w, bbox.h
        return BoundingBox.using_size((x, y), (w, h))
        
    def __iter__(self):
        for coordinate in [self.left, self.top, self.right, self.bottom]:
            yield coordinate
    
    def __repr__(self):
        return '(' + str(self.left) + ', ' + str(self.top) + ', ' + str(self.right) + ', ' + str(self.bottom) + ')'

            
 
if __name__ == '__main__':
    size = (700, 400)
    display = Display(size)
    width, height = 50, 40
    im = ImageGrab.grab(BoundingBox(0,0, width, height))
    for x in range(150, 300, 30):
        for y in range(150, 300, 30):
            bbox = BoundingBox.using_size((x, y), (width, height))
            dim = DisplayImage(im, bbox)
            display.append(dim)
    while display.tick():
        pass  # when display.tick() returns false that means it has quit
