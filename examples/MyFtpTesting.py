
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
    ftp.cwd('/photo')
    f = open(path, 'rb')  
    ftp.storbinary('STOR %s'%filename, f) 
    print('success')
except:
    print('fail')