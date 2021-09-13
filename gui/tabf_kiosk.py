from guizero import App, Text, TextBox, PushButton, Slider, Picture, Window, Combo, ListBox
from flask import Flask
from flask import request
import threading
import requests

sListenIP = '127.0.0.1'
bOpenTestForm = False
bListenFail = False

payload = {}
headers= {}
data_location = {}
Bot_id = 0
Bot_Name = ''

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
    global data_location
    print('ExecuteProcedure')

    url = "http://svc.tabf.org.tw/_webservice/GetBotInfoForIdentityPhoto.ashx"
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        data_location = response.json()
        print('ErrorMsg:' + data_location['ErrorMsg'])
        if data_location['ErrorMsg'] == '':
            _win_combo1.clear()
            _index=0
            for test_data in data_location['Result']:
                _win_combo1.insert(_index, test_data['BotName'])
                _index=_index+1
            window_1.set_full_screen('Esc')
            window_1.show()
        else:
            print('Get Location Error')
    except:
        print('Get Location Error')


    

def OpenTestForm():
    global bOpenTestForm
    bOpenTestForm = True
    app.destroy()

def CloseTestForm():
    app2.destroy()

def Window1Next():
    global Bot_id
    global Bot_Name
    test_item = _win_combo1.value
    if test_item == None:
        Bot_Name = data_location['Result'][0]['BotName']
        Bot_id = 0
    else:
        Bot_Name = test_item
        _index = 0
        for _data in data_location['Result']:
            if _data['BotName'] == Bot_Name:
                Bot_id = _index
                break
            _index = index + 1

    print("Select Id: " + str(Bot_id))
    print("Selected: " + Bot_Name)
    print("Next")

def Window1Cancel():
    window_1.hide()

print('TABF KIOSK Program start...')

apiserver = Flask(__name__)

ApiServerThread = threading.Thread(target=APIServer_DoWork)
ApiServerThread.start()

app = App(title='TABF 報到機 Ver2.0', width=600, height =350, layout="grid")

window_1 = Window(app, title="選擇考試項目", layout="grid", width=500, height =300)
window_1.hide()

_app_showLabel = Text(app, text="TABF 報到機操作介面", size=24, font="Times New Roman", color="black", grid = [0,0])
_executeProcedure = PushButton(app, grid=[0,1], command=ExecuteProcedure, text='執行報到資料下載', align="left")
_opentestform = PushButton(app, grid=[0,2], command=OpenTestForm, text='開啟報到測試模式', align="left")
_win_showLabel1 = Text(window_1, text="選擇考試項目", size=24, font="Times New Roman", color="black", grid = [0,0], align="left")
_win_combo1 = ListBox(window_1, grid=[0,1], height=300, width=500, align="left", scrollbar=True)
_win_Next1 = PushButton(window_1, grid=[0,2], width=40, command=Window1Next, text='Next', align="left")
_win_Cancel1 = PushButton(window_1, grid=[0,3], width=40, command=Window1Cancel, text='Cancel', align="left")

app.display()

if bOpenTestForm == True:
    app2 = App(title='TABF 報到機 測試畫面', width=600, height =350, layout="grid")
    app2.set_full_screen('Esc')

    _app2_showLabel = Text(app2, text="TABF 報到測試模式", size=24, font="Times New Roman", color="black", grid = [0,0])
    _closetestform = PushButton(app2, grid=[1,0], command=CloseTestForm, text='關閉', align="right")
    _app2_image = Picture(app2, image="/home/pi/project/test/Env_IoT_Edge_Rasp_Python_2020/gui/user.png", width=150, height = 200, grid = [0, 3])
    _id_label = Text(app2, text="身分證:", size=20, font="Times New Roman", color="black", grid = [1,1], align="left")
    _id_text =  Text(app2, text="0000000000", size=20, font="Times New Roman", color="blue", grid = [2,1], align="left")
    _temperature_label = Text(app2, text="   溫度(C): ", size=20, font="Times New Roman", color="black", grid = [3,1], align="left")
    _temperature_text =  Text(app2, text="0.0", size=20, font="Times New Roman", color="blue", grid = [4,1], align="left")
    _time_label = Text(app2, text="時間:", size=20, font="Times New Roman", color="black", grid = [1,2], align="left")
    _time_text =  Text(app2, text="NA", size=20, font="Times New Roman", color="blue", grid = [2,2], align="left")

    app2.display()

if bListenFail == False:
    shutdown_server()

print('TABF KIOSK Program finish...')
