from picamera import PiCamera
from PIL import Image
from time import sleep
from time import time
from Log import Log
from Config import Config
from sched import scheduler
import math

s = scheduler(time, sleep)

log = Log('BoothCamera')

def vecSum(A, B):
    if len(A) != len(B):
        raise Exception("{0} has a different length from {1}".format(A, B))
    v = []
    for i in range(0, len(A)):
        v.append(A[i] + B[i])
    return tuple(v)

def vecMult(vec, scale): 
    v = []
    for i in range(0, len(vec)):
        v.append(int(round(vec[i] * scale)))
    return tuple(v)

def findCenter(box):
    w, h = box
    return int(w / 2), int(h / 2)

def centerWithin(box, within):
    boxX, boxY = findCenter(box)
    inX, inY = findCenter(within)
    return inX - boxX, inY - boxY

# size = final size of new image, everything outside img is transparent
# coord = coordinate on screen where to paste the image
# offset = either (x,y) from top-left of img, or None which will center it
def padImage(img, size, coord, offset=None):
    if offset == None:
        offset = centerWithin(img.size, (0,0))
    # New image all transparent
    pad = Image.new('RGBA', size, (0, 0, 0, 0))
    pad.paste(img, vecSum(coord, offset))
    return pad

# Either (path, (x,y,w,h))
# or (path, (w,h), (x,y))
def btnOverlay(imagePath, window, size, offset=None):
    if offset == None:
        x,y,w,h = size
        size = w,h
        offset = x,y
    img = Image.open(imagePath).resize(size)
    return padImage(img, window, offset, (0, 0))

class BoothCamera(object):
    CAMERA = 'device-camera-icon.png'
    yes = "Yes.png"
    no = "No.png"
    countdown = ['three.jpg', 'two.jpg', 'one.jpg']

    def __init__(self, window):
        self.window = window
        self.camera = PiCamera()
        self.previewing = False
        self.prompting = False
        self.confirming = False
        self.promptOverlay = None
        self.confirmOverlay = None
        self.yesOverlay = None
        self.noOverlay = None

    def startPreview(self):
        log.debug("Starting Preview")
        try:
            if not Config.testMode():
                self.camera.start_preview(fullscreen = True)
        except Exception as e: 
            log.error("Error when starting preview", e)
        self.previewing = True

    def stopPreview(self):
        log.debug("Stopping Preview")
        try:
            if not Config.testMode():
                self.camera.stop_preview()
        except Exception as e: 
            log.error("Error when stopping preview", e)
        self.previewing = False
    
    def showPrompt(self, btnBox):
        if (self.prompting):
            log.warn("Tried to show prompt againt")
            return
        log.debug("Showing Prompt at {0}".format(btnBox))
        self.promptOverlay = self.addOverlay(
            btnOverlay(BoothCamera.CAMERA, self.window, btnBox)
        )
        self.prompting = True
    
    def hidePrompt(self):
        if not self.prompting:
            log.warn("Tried to hide prompt again")
            return
        log.debug("Hiding Prompt")
        self.removeOverlay(self.promptOverlay)
        self.prompting = False
    
    
    def showConfirm(self, imagePath, yesBox, noBox):
        if self.confirming:
            log.warn("Tried to show confirm again")
            return
        if Config.testMode():
            size = vecMult(self.window, 0.3)
        else: size = self.window
        log.info(size)
        img = Image.open(imagePath).resize(size)
        self.confirmOverlay = self.addOverlay(
            padImage(img, self.window, (0,0), (0,0))
        )
        yesO = btnOverlay(BoothCamera.yes, self.window, yesBox)
        noO = btnOverlay(BoothCamera.no, self.window, noBox)
        self.yesOverlay = self.addOverlay(yesO)
        self.noOverlay = self.addOverlay(noO)
        self.confirming = True
    
    def hideConfirm(self):
        if not self.confirming:
            log.warn("Tried to hide confirm again")
            return
        self.confirming = False
        self.removeOverlay(self.confirmOverlay)
        self.removeOverlay(self.yesOverlay)
        self.removeOverlay(self.noOverlay)

    def takePicture(self, imagePath, numBox):
        if not self.previewing:
            log.warn("Tried taking a picture without previewing") 
            return
        try:
            self.__displayCountdown(numBox)
            self.camera.capture(imagePath, use_video_port=True)
        except Exception as e:
            log.error("Error when taking picture", e)
    
    def __capture(self, imagePath):
        self.camera.capture(imagePath, use_video_port=True)

    def __displayCountdown(self, numBox):
        prevOverlay = None
        try:
            for filename in BoothCamera.countdown:
                #~ img = self.__getCountdownImage(filename)
                img = btnOverlay(filename, self.window, numBox)
                overlay = self.addOverlay(img)
                self.removeOverlay(prevOverlay)
                prevOverlay = overlay
                sleep(1)
        finally: self.removeOverlay(prevOverlay)

    def __getCountdownImage(self, filename, size = (128, 128)):
        img = Image.open(filename).resize(size)
        log.info('{0} {1}'.format(self.window, findCenter(self.window)))
        return padImage(img, self.window, findCenter(self.window))

    def addOverlay(self, img):
        o = self.camera.add_overlay(
            img.tobytes(), size=img.size, format='rgba')
        o.layer = 3
        o.alpha = 50
        return o

    def removeOverlay(self, o):
        if o: self.camera.remove_overlay(o)




