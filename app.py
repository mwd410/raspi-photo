from booth import *
from Config import Config
from Log import Log

log = Log("App")

class App(object):
    def __init__(self):
        root = self.setupScreen()
        app = PhotoBooth(root)
        app.startPreview()
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
