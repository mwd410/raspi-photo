from apiclient.discovery import build
import google_auth_oauthlib.flow
from Log import Log
from Util import *
from getpass import getpass
import gdata.docs.service
from oauth2client import file, client, tools
from httplib2 import Http

log = Log('Upload')

SCOPES = 'https://www.googleapis.com/auth/photoslibrary'


class Upload(object):
    def __init__(self, clientId, secret):
        self.clientId = clientId
        self.secret = secret
        self.email = None
        self.password = None

    def upload(self, img):
        log.debug("Uploading image")
        return

    def login(self):
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build('photos', 'v1', http=creds.authorize(Http()))

    def listPhotos(self):
        results = self.service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        return items

    # This is a seriously awful place for this...
    def promptForAccount(self):
        email = raw_input('Email: ')
        password = getpass('Password: ')
        self.setAccount(email, password)

    def setAccount(self, email, password):
        self.email = email
        self.password = password

    @staticmethod
    def getInstance():
        clientId = getFile('ggl_client_id')
        secret = getFile('ggl_secret')
        return Upload(clientId, secret)

