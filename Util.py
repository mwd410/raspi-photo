

def getFile(filename):
    f = open(filename)
    try:
        return f.read()
    finally: f.close()
