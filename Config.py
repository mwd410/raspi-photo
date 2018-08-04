import os


class Config(object):

    @staticmethod
    def env(name, orElse=None):
        try: return os.environ[name]
        except (KeyError): return orElse
    
    @staticmethod
    def testMode(): 
        return 'True' == Config.env('TEST_MODE', 'False')
    
    # TODO: Add Log.levelFromName
    @staticmethod
    def defaultLogLevel(): 
        return Config.env('LOG_LEVEL', 'DEBUG')

