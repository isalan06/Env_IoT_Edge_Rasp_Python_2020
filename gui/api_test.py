#!flask/bin/python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/qrcode', methods=['POST'])
def qrcode():
    print('get qrcode')
    return request.values


if __name__ == '__main__':
    app.run(host='192.168.10.101', debug=True)