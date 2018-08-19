import sys
from Upload import Upload
from xml.etree import ElementTree
import gdata.photos.service

print(sys.argv)
upload = Upload.getInstance()
#upload.promptForAccount()

print("logging in...")
upload.login()

print("Listing photos")
items = upload.listPhotos()
print(items)

