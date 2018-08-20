from PhotoBooth import PhotoBooth
from Config import Config
from Log import Log
from Upload import Upload
from Util import *
import time
from sched import scheduler
from Tkinter import *
from getpass import getpass

log = Log("App")

class App(object):
    def __init__(self):
        upload = Upload.getInstance()
        upload.login()
        folder = upload.findByName(raw_input('Folder: '))
        if not folder:
            raise Exception("Folder not found")
        upload.setFolder(folder['id'])
        root = self.setupScreen()
        app = PhotoBooth(root, upload)
        #~ app.startPreview()
        #~ s.enter(10, 1, app.startPreview, ())
        root.mainloop()

    def setupScreen(self):
        root = Tk()
        #~ master.geometry("{0}x{1}".format(
            #~ master.winfo_screenwidth() - pad,
            #~ master.winfo_screenheight() - pad))
        root.attributes('-fullscreen', True)
        root['background'] = 'white'
        return root

App()
