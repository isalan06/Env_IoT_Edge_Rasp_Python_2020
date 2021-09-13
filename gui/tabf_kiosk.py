from guizero import App, Text, TextBox, PushButton, Slider, Picture, Window, Combo
from flask import Flask
from flask import request

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
        apiserver.run((host=sListenIP, debug=True))
    except:
        bListenFail = True

print('TABF KIOSK Program start...')

apiserver = Flask(__name__)

ApiServerThread = threading.Thread(target=APIServer_DoWork)
ApiServerThread.Start()

app = App(title='TABF 報到機 Ver2.0', width=300, height = 200, layout="grid")



app.display()

if bListenFail == False:
    shutdown_server()

print('TABF KIOSK Program finish...')
