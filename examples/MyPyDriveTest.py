from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.CommandLineAuth() 
drive = GoogleDrive(gauth)

file1 = drive.CreateFile({'title': 'Hello.txt','parents':[{'kind': 'drive#fileLink',
                                     'id': '1eHnor5HRg9eTAlpvcwGigBw74Inkb4eL'}]}) 
file1.SetContentString('Hello World!')
file1.Upload() 