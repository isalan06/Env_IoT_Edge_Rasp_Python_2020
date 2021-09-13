from guizero import App, Text, TextBox, PushButton, Slider, Picture, Window, Combo
from flask import Flask
from flask import request
import threading

sListenIP = '127.0.0.1'
bOpenTestForm = False
bListenFail = False

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def APIServer_DoWork():
    global bListenFail
    try:
        apiserver.run(host=sListenIP, debug=True)
    except:
        bListenFail = True

def ExecuteProcedure():
    print('ExecuteProcedure')

def OpenTestForm():
    global bOpenTestForm
    bOpenTestForm = True
    app.destroy()

def CloseTestForm():
    app2.destroy()

print('TABF KIOSK Program start...')

apiserver = Flask(__name__)

ApiServerThread = threading.Thread(target=APIServer_DoWork)
ApiServerThread.start()

app = App(title='TABF 報到機 Ver2.0', width=600, height =350, layout="grid")

_app_showLabel = Text(app, text="TABF 報到機操作介面", size=24, font="Times New Roman", color="black", grid = [0,0])
_executeProcedure = PushButton(app, grid=[0,1], command=ExecuteProcedure, text='執行報到資料下載', align="left")
_opentestform = PushButton(app, grid=[0,2], command=OpenTestForm, text='開啟報到測試模式', align="left")


app.display()

if bOpenTestForm == True:
    app2 = App(title='TABF 報到機 測試畫面', width=600, height =350, layout="grid")
    app2.set_full_screen('Esc')

    _app2_showLabel = Text(app2, text="TABF 報到測試模式", size=24, font="Times New Roman", color="black", grid = [0,0])
    _closetestform = PushButton(app2, grid=[1,0], command=CloseTestForm, text='關閉', align="right")
    _app2_image = Picture(app2, image="/home/pi/project/test/Env_IoT_Edge_Rasp_Python_2020/gui/user.png", width=200, height = 300, grid = [0, 1])

    app2.display()

if bListenFail == False:
    shutdown_server()

print('TABF KIOSK Program finish...')
