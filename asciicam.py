import numpy
import cv2 as cv
from PIL import Image
import time

CONFIG = open('config.txt', 'rt')

CONFIG.readline() #used for something in camtodiscord.py so we skip over it
WIDTH = int(CONFIG.readline().split(' ')[2:][0][:-1]) #Get thing after space & = on line 1 but not the new line charecter
ASCII_CHARS = ['⠀','⠄','⠆','⠖','⠶','⡶','⣩','⣪','⣫','⣾','⣿']

modify = lambda pixel_value: ASCII_CHARS[pixel_value//25] # I forgot why we use 25

def asciify(image: numpy.ndarray, width = 64):
    image = Image.fromarray(image.astype('uint8'), 'RGB').convert('L') # Convert to somthing pillow likes & convert to greyscale.
    # Resize the image as required.
    orig_width, orig_height = image.size
    r = orig_height / orig_width
    # Maintaining aspect ratio by reducing image height because ASCII characters are taller than wide
    height = int(width * r * 0.6)
    image = image.resize((width, height), Image.ANTIALIAS)
    # Mapping the pixels ASCII.
    image_data = image.getdata()
    image = ''.join(map(modify,image_data))
    image = [image[index:index+int(width)] for index in range(0, len(image_data), int(width))]
    return '\n'.join(image)


cap = cv.VideoCapture(0)

if not cap.isOpened():
    raise Exception("Cannot open camera")

def getAsciiFrame(width = WIDTH) -> str:
    ret, frame = cap.read()
    if not ret: #triggers when frame is weird
        raise Exception("Can't receive frame (stream end?).")
    # Display the resulting 'frame'
    return asciify(frame, width)

release = lambda : cap.release()

if __name__ == '__main__':
    while True:
        print('\n'*5+getAsciiFrame())
        time.sleep(0.01)