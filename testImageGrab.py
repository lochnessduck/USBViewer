import PIL
from PIL import ImageGrab

im = ImageGrab.grab()  # can also include optional bounding box for coordinates
bbox = (200, 200, 400, 400)
#im = ImageGra.grab(bbox)
im.save('C:\\Users\\PC\\Downloads\\asdf.png')  # works!