#!/usr/bin/python3
#MyGoogleDrive.py

import os

import MyParameter

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

if os.getenv('C', '1') == '0':
    ANSI_RED = ''
    ANSI_GREEN = ''
    ANSI_YELLOW = ''
    ANSI_CYAN = ''
    ANSI_WHITE = ''
    ANSI_OFF = ''
else:
    ANSI_CSI = "\033["
    ANSI_RED = ANSI_CSI + '31m'
    ANSI_GREEN = ANSI_CSI + '32m'
    ANSI_YELLOW = ANSI_CSI + '33m'
    ANSI_CYAN = ANSI_CSI + '36m'
    ANSI_WHITE = ANSI_CSI + '37m'
    ANSI_OFF = ANSI_CSI + '0m'

sSoftwareVersion='1.0.0.0'

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def UpdateImageToGoogleDrive(filename, fileString, deletefile):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    try:
        if MyParameter.PhotoFolderID != 'NA':

            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'client_secrets.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())

            service = build('drive', 'v3', credentials=creds)

            print("Google Drive Play 1")

            folder_id = MyParameter.PhotoFolderID
            file_metadata = {
                'name': filename,
                'parents': [folder_id]
            }

            print("Google Drive Play 2")

            media = MediaFileUpload(fileString,
                        mimetype='image/jpeg',
                        resumable=True)

            print("Google Drive Play 3")
            
            _file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
            print("\033[1;34mUpdate Picture To Google Drive Success\033[0m")
            print('File ID: %s' % _file.get('id'))
            

            if deletefile == True:
                try: 
                    os.remove(fileString)
                    print(ANSI_GREEN + "    Delete Picture Success" + ANSI_OFF)
                except:
                    print(ANSI_RED + "    Delete Picture Failure" + ANSI_OFF)
        
        else:
            print(ANSI_YELLOW + "    There is no update folder ID" + ANSI_OFF)
    except Exception as e:
        print(e)
        print("\033[1;31mUpdate Picture To Google Drive Failure\033[0m")

   