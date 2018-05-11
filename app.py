from booth import *

class AppConfig(object):
    def __init__(self, testMode=True):
        self.testMode = testMode
    

class App(object):
    def __init__(self, appConfig):
        self.config = appConfig
        root = Tk()
        app = PhotoBooth(root)
        root.mainloop()
        
App(AppConfig())
