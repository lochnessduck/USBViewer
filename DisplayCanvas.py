import pygame
import math
from math import pi
from PIL import Image, ImageGrab
import numpy as np


class Display:
    
    def __init__(self, size=(700, 400)):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.images = []  #pygame.sprite.group() # just call .draw to draw all
        pygame.display.set_caption("Connected to...")
        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()        
        self.exit = False
        self.size = size
        self._dirtyboxOutdated = False
        self._create_dirtybox()  # a matrix which determines invisible images
        
    def append(self, image):
        """ requires a display image, which includes coordinates of where to
            display image
        """
        #if not type(image) == type(DisplayImage()):
        #    raise UserWarning('incompatible image. Needs to be DisplayImage')
        self.images.append(image)
        self._update_dirtybox()
        self._remove_invisible_images()
        # delete any invisible sprites (which I havne't done yet)
        
        
    def draw(self):
        #self.images.draw(self.screen)
        for image in self.images:
            image.draw(self.screen)
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
        for dim in self.images:
            yield dim
            
    def __getitem__(self, index):
        return self.images[index]
    
    def __setitem__(self, index, im):
        self._dirtyboxOutdated = True
        self.images[index] = im
        
    def __nonzero__(self):
        return len(self.images)
        
    def __contains__(self, im):
        return im in self.images
    
    def __delitem__(self, index):
        self._dirtyboxOutdated = True
        del self.images[index]

    def __len__(self):
        return len(self.images)

    def _create_dirtybox(self):
        self._dirtybox = np.zeros(self.size) - 1
        for i, im in enumerate(self):
            self._dirtybox[im.xCoordinates, im.yCoordinates] = i
        self._dirtyboxOutdated = False

    def _update_dirtybox(self):
        """ call after adding an image to the canvas
        """
        i = len(self) - 1
        im = self[i]
        self._dirtybox[im.xCoordinates, im.yCoordinates] = i

    def _remove_invisible_images(self):
        if self._dirtyboxOutdated:
            self._create_dirtybox()
        for i in range(len(self) - 1, -1, -1):
            if i not in self._dirtybox:
                del self[i]  # if image is NOT visible, delete the image
                # this also tells dirtybox that it's no longer valid.
                
        
class DisplayImage(pygame.sprite.Sprite):
    
    def __init__(self, im, xy=(0,0)):
        pygame.sprite.Sprite.__init__(self)   # call parent. use Super()instead?
        self.id = 19  # eventually needs to create separate IDs
        imString = im.tostring("raw", "RGB")  # a PILLOW function, default encoder is "raw"
        # tostring will eventually be replaced by tobytes
        #imString = im.convert("RGBA").tostring(...)  # this works as well. maybe more robust
        self.size = im.size
        self.image = pygame.image.fromstring(imString, self.size, "RGB")
        self.xy = xy
        self.bbox = (xy[0], xy[1], xy[0] + self.size[0], xy[1] + self.size[1])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = xy
        self.yCoordinates = slice(xy[1], xy[1] + self.size[1])  # get y coordinates that this image occupies
        self.xCoordinates = slice(xy[0], xy[0] + self.size[0])  # get x coordinates that this image occupies
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    @classmethod
    def fromScreenshot(cls, bbox):  # bbox coordinates are top-left to bottom-right
        im = ImageGrab.grab(bbox)
        return cls(im, bbox[:2])
        #return cls(im, bbox[:2])


 
if __name__ == '__main__':
    size = (700, 400)
    display = Display(size)
    #im = Image.open('asdf.png')
    imString = '\x00\x00\x00\x00\x00\x00f\xb6\xff\xff\xff\xff\xff\xff\xb6\xff\xff\xff\xff\xdb\x90:\x00:\x90\xdb\xff\xff\xff\xff\xff\xff\xff\xff\xff\xdb\x90:\x00f\xb6\xff\xff\xff\xff\xff\xff\xff\xff\xb6f\x00\x00:\x90\xdb\xff\xff\xff\xff'
    im = Image.fromstring('RGB',(5,4), imString) 
    dim = DisplayImage(im, (0,0))
    dim2 = DisplayImage(im, (20, 20))
    display.append(dim)
    display.append(dim2)
    del display[0] # remove first image added
    for x in range(15, 30, 3):
        for y in range(15, 30, 3):
            dim = DisplayImage(im, (x, y))
            display.append(dim)
    print('should print 25:', len(display))  # should print 25, because we the 2nd image manually
                        # added will be auto-removed once it's invisible
    while display.tick():
        pass  # when display.tick() returns false that means it has quit
