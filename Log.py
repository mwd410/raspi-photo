from datetime import datetime
from Config import Config
from traceback import format_exc

__OFF = 0
__ERROR = 1
__WARN = 2
__INFO = 3
__DEBUG = 4
__TRACE = 5

def fromName(name):
    if name == 'OFF': return __OFF
    elif name == 'ERROR': return __ERROR
    elif name == 'WARN': return __WARN
    elif name == 'INFO': return __INFO
    elif name == 'DEBUG': return __DEBUG
    elif name == 'TRACE': return __TRACE
    else: raise NameError('Invalid Log level {0}'.format(name))

class Log(object):
    OFF = 0
    ERROR = 1
    WARN = 2
    INFO = 3
    DEBUG = 4
    TRACE = 5
    __level = fromName(Config.defaultLogLevel())
    
    @staticmethod
    def isValidLevel(level):
        return isinstance(level, int) and (
                level == Log.OFF or
                level == Log.ERROR or
                level == Log.WARN or
                level == Log.INFO or
                level == Log.DEBUG or
                level == Log.TRACE)
    
    @staticmethod
    def setLevel(level):
        if Log.isValidLevel(level):
            __level = level
        else: Log.__log('Log', Log.ERROR, 'Invalid level: {0}'.format(level))
    
    @staticmethod
    def level():
        return __level
        
    @staticmethod
    def levelName(level = None):
        if level == None: return Log.levelName(__level)
        elif level == Log.ERROR: return 'ERROR'
        elif level == Log.WARN: return 'WARN'
        elif level == Log.INFO: return 'INFO'
        elif level == Log.DEBUG: return 'DEBUG'
        elif level == Log.TRACE: return 'TRACE'
        else: return None
    
    def __init__(self, name):
        self.name = name
    
    @staticmethod
    def __log(name, level, msg):
        if level <= Log.__level:
            print("{0} [{1}] {2}: {3}".format(
                # TODO: millisecond time
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                Log.levelName(level),
                name,
                msg))
    
    def error(self, msg):
        self.__log(self.name, Log.ERROR, msg)
        
    def error(self, msg, e):
        self.__log(self.name, Log.ERROR, "{0}: {1}".format(msg, format_exc(e)))
    
    def warn(self, msg):
        self.__log(self.name, Log.WARN, msg)
    
    def info(self, msg):
        self.__log(self.name, Log.INFO, msg)
    
    def debug(self, msg):
        self.__log(self.name, Log.DEBUG, msg)
    
    def trace(self, msg):
        self.__log(self.name, Log.TRACE, msg)
    
    
    

