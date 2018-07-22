from Tkinter import *
from BoothCamera import BoothCamera
from datetime import datetime
import os

def env(name, orElse=None):
    try: return os.environ[name]
    except (KeyError): return orElse

class PhotoBooth(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.camera = BoothCamera((0, 0, 640, 480), True)
        self.camera.startPreview()
        self.formatScreen()
        self.addWidgets()
        self.bindEvents()

    def formatScreen(self):
        pad = 3
        master = self.master
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth() - pad,
            master.winfo_screenheight() - pad))
        master.attributes('-fullscreen', True)
        master['background'] = 'white'

    def addWidgets(self):
        self.mainButton = Button(
            self.master,
            text = 'hello',
            command = self.takePicture
        )
        self.mainButton.pack()

    def takePicture(self):
        path = self.__imagePath()
        self.camera.takePicture(path)
        
    def bindEvents(self):
        master = self.master
        master.bind('<Escape>', self.shutdown)

    def shutdown(self, e):
        self.master.destroy()

    def __imagePath(self):
        directory = env('PHOTO_BOOTH_DIR', '/home/pi/Pictures')
        now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        return directory + '/photo-' + now + '.jpg'
        


