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

def findCenter(box):
    w, h = box
    return int(w / 2), int(h / 2)

def centerWithin(box, within):
    boxX, boxY = findCenter(box)
    inX, inY = findCenter(within)
    return inX - boxX, inY - boxY

def centerOn(img, on, offset=(0,0)):
    pad = Image.new('RGBA', on, (0, 0, 0, 0))
    center = centerWithin(img.size, on)
    #~ ox,oy = offset
    #~ center = cx+ox, cy+oy
    pad.paste(img, center)
    log.trace(center)
    return pad

def scaleSize(size, scale): 
    w,h = size
    return int(round(w * scale)), int(round(h * scale))

def btnOverlay(imagePath, size, offset=None):
    if offset == None:
        x,y,w,h = size
        size = w,h
        offset = x,y
    img = Image.open(imagePath).resize(size)
    return centerOn(img, size, offset)

class BoothCamera(object):
    yes = "Yes.png"
    no = "No.png"
    countdown = ['three.jpg', 'two.jpg', 'one.jpg']

    def __init__(self, window):
        self.window = window
        self.camera = PiCamera()
        self.previewing = False
        self.prompting = False
        self.confirming = False
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
    
    def showPrompt(self):
        if (self.prompting):
            log.warn("Tried to show prompt againt")
            return
        log.debug("Showing Prompt")
        self.prompting = True
    
    def hidePrompt(self):
        if not self.prompting:
            log.warn("Tried to hide prompt again")
            return
        self.prompting = False
    
    
    def showConfirm(self, imagePath, yesBox, noBox):
        if self.confirming:
            log.warn("Tried to show confirm again")
            return
        if Config.testMode():
            size = scaleSize(self.window, 0.3)
        else: size = self.window
        log.info(size)
        img = Image.open(imagePath).resize(size)
        self.confirmOverlay = self.addOverlay(
            centerOn(img, self.window)
        )
        #~ self.yesOverlay = self.addOverlay(
            #~ btnOverlay(BoothCamera.yes, yesBox)
        #~ )
        #~ self.noOverlay = self.addOverlay(
            #~ btnOverlay(BoothCamera.no, noBox)
        #~ )
        self.confirming = True
    
    def hideConfirm(self):
        if not self.confirming:
            log.warn("Tried to hide confirm again")
            return
        self.confirming = False
        self.removeOverlay(self.confirmOverlay)
        self.removeOverlay(self.yesOverlay)
        self.removeOverlay(self.noOverlay)

    def takePicture(self, imagePath):
        if not self.previewing:
            log.warn("Tried taking a picture without previewing") 
            return
        try:
            self.__displayCountdown()
            self.camera.capture(imagePath, use_video_port=True)
        except Exception as e:
            log.error("Error when taking picture", e)
    
    def __capture(self, imagePath):
        self.camera.capture(imagePath, use_video_port=True)

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




