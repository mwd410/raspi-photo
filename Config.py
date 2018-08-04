import os


class Config(object):

    @staticmethod
    def env(name, orElse=None):
        try: return os.environ[name]
        except (KeyError): return orElse
    
    @staticmethod
    def testMode(): 
        return bool(Config.env('TEST_MODE', 'True'))
    
    # TODO: Add Log.levelFromName
    @staticmethod
    def defaultLogLevel(): 
        return Config.env('LOG_LEVEL', 'DEBUG')

