import os
from ftplib import FTP 
IP = '122.116.123.236'
user = 'uploaduser'
password = 'antiupload3t6Q'
filename = 'sn_2020-11-11_16-35-28-000.jpg'
path = '/home/pi/download/sn_2020-11-11_16-35-28-000.jpg'
ftp=FTP() 
ftp.set_debuglevel(2)
ftp.set_pasv(False)
ftp.connect(IP) 
ftp.login(user,password)

ftp.cwd('/photo')
size = os.path.getsize(path)
print(size)
f = open(path, 'rb')

ftp.storbinary('STOR Test3.jpg', f, size) 
