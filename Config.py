import os
from Tkinter import *


class Config(object):
    testModeVar = None

    @staticmethod
    def env(name, orElse=None):
        try: return os.environ[name]
        except (KeyError): return orElse
    
    
    @staticmethod
    def testMode(): 
        return Config.testModeVar.get() == '1'
    
    @staticmethod
    def setTestMode(var):
        Config.testModeVar = var
        print("TestMode: {}".format(Config.testMode()))
    
    # TODO: Add Log.levelFromName
    @staticmethod
    def defaultLogLevel(): 
        return Config.env('LOG_LEVEL', 'DEBUG')

