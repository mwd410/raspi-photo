from picamera import PiCamera
from PIL import Image
from time import sleep
import math


camera = PiCamera()

countdown = ['three.jpg', 'two.jpg', 'one.jpg']

def findCenter(box):
    w, h = box
    return int(w / 2), int(h / 2)

def centerWithin(box, within):
    boxX, boxY = findCenter(box)
    inX, inY = findCenter(within)
    return inX - boxX, inY - boxY

def centerOn(img, on):
    pad = Image.new('RGBA', on, (0, 0, 0, 0))
    center = centerWithin(img.size, on)
    pad.paste(img, center)
    return pad

def getCountdownImage(filename, size=(128, 128)):
    img = Image.open(filename).resize(size)
    return centerOn(img, camera.resolution)

def addOverlay(img):
    o = camera.add_overlay(img.tobytes(), size=img.size, format='rgba')
    o.layer = 3
    o.alpha = 50
    return o

def removeOverlay(o):
    camera.remove_overlay(o)


def displayCountdown():
    prevO = None
    for filename in countdown:
        img = getCountdownImage(filename)
        o = addOverlay(img)
        if prevO:
            removeOverlay(prevO)
        prevO = o
        sleep(1)
    removeOverlay(prevO)


def main():
    camera.start_preview()
    displayCountdown()
    camera.capture('/home/pi/Desktop/image.jpg',use_video_port=True)
    camera.stop_preview()
    
    

main()
