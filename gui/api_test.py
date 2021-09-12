#!flask/bin/python
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/qrcode', methods=['POST'])
def qrcode():
    print('get qrcode')
    data = request.get_json()
    print(data['rqcode'])
    print(data['type'])


    return "OK"


if __name__ == '__main__':
    app.run(host='192.168.10.101', debug=True)