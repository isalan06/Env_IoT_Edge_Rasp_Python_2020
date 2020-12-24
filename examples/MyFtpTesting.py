
from ftplib import FTP 
IP = '122.116.123.236'
user = 'uploaduser'
password = 'antiupload3t6Q'
filename = 'sn_2020-11-11 16-35-28-000.jpg'
path = '~/download/sn_2020-11-11 16-35-28-000.jpg'
ftp=FTP() 
ftp.set_debuglevel(2) 
ftp.connect(IP) 
ftp.login(user,password)
try:
    ftp.cwd('/upload/fire_smoke/photo')
    ftp.storbinary('STOR %s'%filename, open(path, 'rb',8192)) 
    print('success')
except:
    print('fail')