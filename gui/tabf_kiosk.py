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
Bot_index = 0
Bot_Name = ''
Bot_Area = []
PhaseNo = 2
Area_index = 0
Area_id = 0
Exam_id = 0
Area_Name = ''
Phase_Name = ''

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
    global Bot_index
    global Bot_Area
    
    test_item = _win_combo1.value
    if test_item == None:
        Bot_Name = data_location['Result'][0]['BotName']
        Bot_id = data_location['Result'][0]['BotID']
        Bot_Area = data_location['Result'][0]['BotAreaInfoList']
        Bot_index = 0
    else:
        Bot_Name = test_item
        _index = 0
        for _data in data_location['Result']:
            if _data['BotName'] == Bot_Name:
                Bot_index = _index
                Bot_id = _data['BotID']
                Bot_Area = _data['BotAreaInfoList']
                break
            _index = _index + 1
    

    print("Select Index: " + str(Bot_index))
    print("Select Id: " + str(Bot_id))
    print("Selected: " + Bot_Name)
    print("Next")

    _win_combo2.clear()
    _index2=0
    for location_data in Bot_Area:
        _win_combo2.insert(_index2, location_data['AreaName'])
        _index2=_index2+1
    window_1.hide()
    _win_combo3.select_default()
    window_2.set_full_screen('Esc')
    window_2.show()

def Window1Cancel():
    window_1.hide()

def Window2Next():
    global Area_index
    global PhaseNo
    global Area_id
    global Exam_id
    global Area_Name
    global Phase_Name

    area_item = _win_combo2.value
    if area_item == None:
        Area_id = Bot_Area[0]['AreaID']
        Exam_id = Bot_Area[0]['ExamNo']
        Area_Name = Bot_Area[0]['AreaName']
        Area_index = 0
    else:
        Area_Name = area_item
        _index = 0
        for area_data in Bot_Area:
            if area_data['AreaName'] == Area_Name:
                Area_index = _index
                Area_id = area_data['AreaID']
                Exam_id = area_data['ExamNo']
                break
            _index = _index + 1


    if _win_combo3.value == '二試':
        Phase_Name = '二試'
        PhaseNo = 4
    elif _win_combo3.value == '三試':
        Phase_Name = '三試'
        PhaseNo = 6
    else:
        Phase_Name = '一試'
        PhaseNo = 2 

    print('Select Index: ' + str(Area_index))
    print('Area id: ' + str(Area_id))
    print('Area Name: ' + Area_Name)
    print('Exam id: ' + str(Exam_id))
    print('Phase No: ' + str(PhaseNo))
    print("Next2")

    window_2.hide()
    window_3.set_full_screen('Esc')
    window_3.show()

def Window2Cancel():
    window_2.hide()

def Window3Next():
    print('Next3')

def Window3Cancel():
    window_3.hide()

print('TABF KIOSK Program start...')

apiserver = Flask(__name__)

ApiServerThread = threading.Thread(target=APIServer_DoWork)
ApiServerThread.start()

app = App(title='TABF 報到機 Ver2.0', width=600, height =350, layout="grid")

window_1 = Window(app, title="選擇考試項目", layout="grid", width=500, height =300)
window_1.hide()

window_2 = Window(app, title="選擇考試地點", layout="grid", width=500, height =300)
window_2.hide()

window_3 = Window(app, title="資訊確認", layout="grid", width=500, height=300)
window_3.hide()

_app_showLabel = Text(app, text="TABF 報到機操作介面", size=24, font="Times New Roman", color="black", grid = [0,0])
_executeProcedure = PushButton(app, grid=[0,1], command=ExecuteProcedure, text='執行報到資料下載', align="left")
_opentestform = PushButton(app, grid=[0,2], command=OpenTestForm, text='開啟報到測試模式', align="left")
_win_showLabel1 = Text(window_1, text="選擇考試項目", size=24, font="Times New Roman", color="black", grid = [0,0], align="left")
_win_combo1 = ListBox(window_1, grid=[0,1], height=300, width=500, align="left", scrollbar=True)
_win_Next1 = PushButton(window_1, grid=[0,2], width=40, command=Window1Next, text='Next', align="left")
_win_Cancel1 = PushButton(window_1, grid=[0,3], width=40, command=Window1Cancel, text='Cancel', align="left")

_win_showLabel2 = Text(window_2, text="選擇考試地點", size=24, font="Times New Roman", color="black", grid = [0,0], align="left")
_win_combo2 = ListBox(window_2, grid=[0,1], height=250, width=500, align="left", scrollbar=True)
_win_combo3 = Combo(window_2, grid=[0,2], width=50, options=["一試", "二試", "三試"])
_win_Next2 = PushButton(window_2, grid=[0,3], width=40, command=Window2Next, text='Next', align="left")
_win_Cancel2 = PushButton(window_2, grid=[0,4], width=40, command=Window2Cancel, text='Cancel', align="left")

_win_showLabel3 = Text(window_3, text="資訊確認", size=24, font="Times New Roman", color="black", grid = [0,0], align="left")
_win3_title1 = Text(window_3, text="Bot Name: ", size=20, font="Times New Roman", color="black", grid = [0,1], align="left")
_win3_value1 = Text(window_3, text="NA", size=20, font="Times New Roman", color="blue", grid = [1,1], align="left")
_win3_title2 = Text(window_3, text="Area Name: ", size=20, font="Times New Roman", color="black", grid = [0,2], align="left")
_win3_value2 = Text(window_3, text="NA", size=20, font="Times New Roman", color="blue", grid = [1,2], align="left")
_win3_title3 = Text(window_3, text="Phase Name: ", size=20, font="Times New Roman", color="black", grid = [0,3], align="left")
_win3_value3 = Text(window_3, text="NA", size=20, font="Times New Roman", color="blue", grid = [1,3], align="left")
_win_Next3 = PushButton(window_3, grid=[0,4], width=40, command=Window2Next, text='Next', align="left")
_win_Cancel3 = PushButton(window_3, grid=[0,5], width=40, command=Window2Cancel, text='Cancel', align="left")

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
