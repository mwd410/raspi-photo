from apiclient.discovery import build
from apiclient.http import MediaFileUpload
import google_auth_oauthlib.flow
from Log import Log
from Util import *
from getpass import getpass
import gdata.docs.service
from oauth2client import file, client, tools
from httplib2 import Http
import os

log = Log('Upload')

SCOPES = 'https://www.googleapis.com/auth/drive'


class Upload(object):
    def __init__(self, clientId, secret):
        self.clientId = clientId
        self.secret = secret
        self.folderId = None

    def upload(self, img):
        log.debug("Uploading image")
        return

    def login(self):
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build('drive', 'v3', http=creds.authorize(Http()))

    def list(self):
        results = self.service.files().list(
            pageSize=1000, fields='nextPageToken, files(id, name)').execute()
        log.info(results)
        items = results.get('files', [])
        return items

    def findByName(self, name):
        items = self.list()
        for item in items:
            if item['name'] == name:
                return item

    def setFolder(self, id):
        self.folderId = id
        log.debug("Set directory to {}".format(id))

    def uploadFile(self, filePath, mimetype='image/jpeg'):
        file_metadata = { 'name' : os.path.basename(filePath) }
        if self.folderId:
            file_metadata['parents'] = [self.folderId]
        media = MediaFileUpload(filePath,
                                mimetype='image/jpeg')
        file = self.service.files().create(body=file_metadata,
                                           media_body=media,
                                           fields='id').execute()
        log.info("Uploaded {} to {}".format(filePath, file_metadata))
        return file

    @staticmethod
    def getInstance():
        clientId = getFile('ggl_client_id')
        secret = getFile('ggl_secret')
        return Upload(clientId, secret)

