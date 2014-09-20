import DisplayCanvas as dcanv
import PIL
from PIL import ImageGrab
import time

bbox = (0, 0, 40, 40)
disp = dcanv.Display()


while disp.tick():  # when disp.tick() returns false, that means the box has been closed
    #im = ImageGrab.grab(bbox)  # can also include optional bounding box for coordinates
    #dim = dcanv.DisplayImage(im, bbox[:2])
    dim = dcanv.DisplayImage.fromScreenshot(bbox)
    disp.append(dim)
    disp.tick()
    time.sleep(1)

