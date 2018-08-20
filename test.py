import sys
from Upload import Upload
from xml.etree import ElementTree
import gdata.photos.service

print(sys.argv)
upload = Upload.getInstance()
#upload.promptForAccount()

print("logging in...")
upload.login()

#upload.uploadFile(raw_input('file path:'))

folder = upload.findByName(raw_input('folder name: '))
print(folder)

