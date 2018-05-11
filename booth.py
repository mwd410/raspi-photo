from Tkinter import *
import camera


class PhotoBooth(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
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
            command = camera.takePicture
        )
        self.mainButton.pack()
        
    def bindEvents(self):
        master = self.master
        master.bind('<Escape>', lambda e: master.destroy())
        


