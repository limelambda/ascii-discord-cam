import numpy
import cv2 as cv
from PIL import Image
import time


ASCII_CHARS = ['⠀','⠄','⠆','⠖','⠶','⡶','⣩','⣪','⣫','⣾','⣿']

modify = lambda pixel_value: ASCII_CHARS[pixel_value//25] # I forgot why we use 25

def asciify(image: numpy.ndarray, new_width=640):
    image = Image.fromarray(image.astype('uint8'), 'RGB').convert('L') # Convert to somthing pillow likes & convert to greyscale.
    # Resize the image as required.
    orig_width, orig_height = image.size
    r = orig_height / orig_width
    # Maintaining aspect ratio by reducing image height because ASCII characters are taller than wide
    height = int(new_width * r * 0.5)
    image = image.resize((new_width, height), Image.ANTIALIAS)
    # Mapping the pixels ASCII.
    image_data = image.getdata()
    image = ''.join(map(modify,image_data))
    image = [image[index:index+int(new_width)] for index in range(0, len(image_data), int(new_width))]
    return '\n'.join(image)


cap = cv.VideoCapture(0)

if not cap.isOpened():
    raise Exception("Cannot open camera")

def getAsciiFrame() -> str:
    ret, frame = cap.read()
    if not ret: #triggers when frame is weird
        raise Exception("Can't receive frame (stream end?).")
    # Display the resulting 'frame'
    return asciify(frame, 64)

release = lambda : cap.release()

if __name__ == '__main__':
    while True:
        print('\n'*5+getAsciiFrame())