from picamera import PiCamera
from PIL import Image
from time import sleep


def findCenter(box):
    w, h = box
    return int(w / 2), int(h / 2)

def centerWithin(box, within):
    boxX, boxY = findCenter(box)
    inX, inY = findCenter(within)
    return inX - boxX, inY - boxY

def centerOn(img, on):
    x,y,w,h = on
    pad = Image.new('RGBA', (w,h), (0, 0, 0, 0))
    centerX,centerY = centerWithin(img.size, (w,h))
    pad.paste(img, (0,0))
    return pad

class BoothCamera(object):
    countdown = ['three.jpg', 'two.jpg', 'one.jpg']

    def __init__(self, window, fullscreen=True):
        # The portion of screen the camera will be drawn
        # (x,y,width,height)
        self.adjust(window, fullscreen)
        self.camera = PiCamera()
        self.previewing = False

    def pos(self):
        x,y,w,h = self.window
        return x,y

    def size(self):
        x,y,w,h = self.window
        return w,h

    def adjust(self, window, fullscreen):
        self.window = window
        self.fullscreen = fullscreen

    def startPreview(self):
        #self.camera.start_preview(
        #    fullscreen = self.fullscreen,
        #    window = self.window)
        self.previewing = True

    def stopPreview(self):
        #self.camera.stop_preview()
        self.previewing = False

    def takePicture(self, imagePath):
        wasPreviewing = self.previewing
        wasFullscreen = self.fullscreen
        try:
            self.fullscreen = True
            self.startPreview()
            self.__displayCountdown()
            self.camera.capture(imagePath, use_video_port=True)
            #return imagePath
        except e:
            print(e)
            self.stopPreview()
        finally:
            self.fullscreen = wasFullscreen
            if wasPreviewing: self.startPreview()
            else: self.stopPreview()

    def __displayCountdown(self):
        prevOverlay = None
        try:
            for filename in BoothCamera.countdown:
                img = self.__getCountdownImage(filename)
                overlay = self.addOverlay(img)
                self.removeOverlay(prevOverlay)
                prevOverlay = overlay
                sleep(1)
        finally: self.removeOverlay(prevOverlay)

    def __getCountdownImage(self, filename, size = (128, 128)):
        img = Image.open(filename).resize(size)
        return centerOn(img, self.window)

    def addOverlay(self, img):
        o = self.camera.add_overlay(
            img.tobytes(), size=img.size, format='rgba')
        o.layer = 3
        o.alpha = 50
        return o

    def removeOverlay(self, o):
        if o: self.camera.remove_overlay(o)




