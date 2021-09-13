from flask import *
from threading import Thread

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
	return "Hello"


if __name__ == "__main__":
	app.run(debug=True)

#   Preparing parameters for flask to be given in the thread
#   so that it doesn't collide with main thread
	kwargs = {'host': '127.0.0.1', 'port': 5000, 'threaded': True, 'use_reloader': False, 'debug': False}

#   running flask thread
	flaskThread = Thread(target=app.run, daemon=True, kwargs=kwargs).start()

print('AAAAA')    
