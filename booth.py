from Tkinter import *
from BoothCamera import BoothCamera
from datetime import datetime
from Config import Config
from Log import Log

log = Log('PhotoBooth')

def btnBox(btn):
    return btn.winfo_rootx(), btn.winfo_rooty(), btn.winfo_width(), btn.winfo_height()

class PhotoBooth(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.camera = BoothCamera(
            (master.winfo_screenwidth(),
             master.winfo_screenheight())
        )
        self.addWidgets()
        self.bindEvents()
        self.confirmPath = None

    def addWidgets(self):
        self.pack(fill='both', expand=1)
        # Prompt Frame
        promptFrame = Frame(self,
            background = 'red')
        promptFrame.pack(side='right', fill='y')
        # Take Picture Button
        btnTakePicture = Button(
            promptFrame,
            text = 'hello',
            command = self.takePicture,
            state = 'disabled'
        )
        btnTakePicture.pack(side='bottom', ipady=50, ipadx=50, pady=25, padx=25)
        self.btnTakePicture = btnTakePicture
        # Yes/No frame
        yesNoFrame = Frame(self,
            background = 'green')
        self.btnYes = Button(yesNoFrame,
            text = 'Yes',
            command = self.confirm,
            state = 'disabled'
        )
        self.btnNo = Button(yesNoFrame,
            text = 'No',
            command = self.reject,
            state = 'disabled'
        )
        self.btnNo.pack(side='right', ipady=50, ipadx=50, pady=25, padx=25)
        self.btnYes.pack(side='right', ipady=50, ipadx=50, pady=25, padx=25)
        yesNoFrame.pack(side='bottom', fill='x')
    
    def __hideConfirm(self):
        self.camera.hideConfirm()
        self.btnYes['state'] = 'disabled'
        self.btnNo['state'] = 'disabled'
        self.confirmPath = None
        self.startPreview()
    
    
    def __showConfirm(self, path):
        self.stopPreview()
        try: 
            self.camera.showConfirm(path, 
                btnBox(self.btnYes), 
                btnBox(self.btnNo)
            )
        except Exception as e:
            log.error("Error when showing confirm", e)
        self.btnYes['state'] = 'normal'
        self.btnNo['state'] = 'normal'
        self.confirmPath = path
    
    def confirm(self):
        if self.confirmPath == None:
            log.warn("Nothing to confirm")
            return
        self.__hideConfirm()
        log.info("Confirmed picture")
    
    def reject(self):
        if self.confirmPath == None:
            log.warn("Nothing to reject")
            return
        self.__hideConfirm()
        log.info("Rejected picture")
    
    def startPreview(self):
        self.camera.startPreview()
        self.__showPrompt()
    
    def stopPreview(self):
        self.camera.stopPreview()
        self.__hidePrompt()
    
    def __hidePrompt(self):
        self.camera.hidePrompt()
        self.btnTakePicture['state'] = 'disabled'
        
    def __showPrompt(self):
        self.camera.showPrompt()
        self.btnTakePicture['state'] = 'normal'

    def takePicture(self):
        path = self.imagePath()
        self.__hidePrompt()
        self.camera.takePicture(path)
        self.__showConfirm(path)
    
        
    def bindEvents(self):
        master = self.master
        master.bind('<Escape>', self.shutdown)

    def shutdown(self, e):
        log.info("Shutting down")
        self.master.destroy()

    @staticmethod
    def imagePath():
        directory = Config.env('PHOTO_BOOTH_DIR', '/home/pi/Pictures')
        now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        return directory + '/photo-' + now + '.jpg'
        


