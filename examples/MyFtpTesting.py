#encoding=utf8
from ftplib import FTP #載入ftp模組
IP = '122.116.123.236'
user = 'uploaduser'
password = 'antiupload3t6Q'
filename = 'sn_2020-11-11 16-35-28-000.jpg'
path = '~/download/sn_2020-11-11 16-35-28-000.jpg'
ftp=FTP() #設定變數
ftp.set_debuglevel(2) #開啟除錯級別2，顯示詳細資訊
ftp.connect(IP) #連線的ftp sever和埠
print(ftp.welcome())
ftp.login(user,password)#連線的使用者名稱，密碼
try:
    ftp.cwd('/upload/fire_smoke/photo')
    ftp.storbinary('STOR %s'%filename, open(path, 'rb',8192)) 
    print('success')
except:
    print('fail')