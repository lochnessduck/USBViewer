import PIL
from PIL import ImageChops

def create_square_from_image(im):
    # just hem in from all four sides
    for y in range(im.size.y):
        topSlice = im[:, y]
        if sum(topSlice) > 0:
            break
    top = y
    for y in range(im.size.y - 1, top - 1, -1):
        bottomSlice = im[:, y]
        if sum(bottomSlice) > 0:
            break
    bottom = y
    for x in range(im.size.x):
        leftSlice = im[x, :]
        if sum(leftSlice) > 0:
            break
    left = x
    for x in range(im.size.x - 1, left - 1, -1):
        rightSlice = im[x, :]
        if sum(rightSlice) > 0:
            break
    right = x
    return ((left, top), (right, bottom))  # top-left to bottom-right coordinates (in x, y format)

def get_difference_image_squares(im):
    coordinate = create_square_from_image(im)
    diffSquare = im.slice(coordinate[0], coordinate[1])
    if diffSquare.size.x == 0:
        return []
    return [diffSquare]  # put the difference square in a list. Next time you
                    #should expect to be giving multiple squares of difference

def remove_covered_images():
    canvas = []  # this is the canvas
    imagesAndOrder = []
    for image in canvas:
        imagesAndOrder.append((image.order, image))
    imagesAndOrder.sort()  # sort in order of images in front??
    images = [image for order, image in imagesAndOrder]  # separate only images
    for im in images:
        
    
