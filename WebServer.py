from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def home():
    return "Hello. I am alive!"


def run():
    app.run(host='0.0.0.1', port=8080)


def StayAlive():
    t = Thread(target=run)
    t.start()
