import pygame
import math
from math import pi
from PIL import Image


class Display:
    
    def __init__(self, size=(700, 400)):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.images = []  #pygame.sprite.group() # just call .draw to draw all
        pygame.display.set_caption("Connected to...")
        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()        
        self.exit = False
        
    def __append__(self, image):
        """ requires a display image, which includes coordinates of where to
            display image
        """
        if not type(image) == type(DisplayImage()):
            raise UserWarning('incompatible image. Needs to be DisplayImage')
        self.images.append(image)
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
        
        
        
class DisplayImage(pygame.sprite.Sprite):
    
    def __init__(self, im, coordinates=(0,0)):
        pygame.sprite.Sprite.__init__(self)   # call parent. use Super()instead?
        self.id = 19  # eventually needs to create separate IDs
        imString = im.tostring("raw", "RGB")  # a PILLOW function, default encoder is "raw"
        # tostring will eventually be replaced by tobytes
        #imString = im.convert("RGBA").tostring(...)  # this works as well. maybe more robust
        self.size = im.size
        self.image = pygame.image.fromstring(imString, self.size, "RGB")
        self.coordinates = coordinates
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coordinates
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    


 
if __name__ == '__main__':
    size = (700, 400)
    display = Display(size)
    im = Image.open('C:\\Users\\PC\\Downloads\\asdf.png')
    dim = DisplayImage(im, (0,0))
    dim2 = DisplayImage(im, (20, 40))
    display.images.append(dim)
    display.images.append(dim2)
    while display.tick():
        pass  # when display.tick() returns false that means it has quit
