#!/usr/bin/env python3
from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def getMainPage():
    return render_template('main.html')

if (__name__ == '__main__'):
    app.debug = True
    app.run(host='0.0.0.0', port = 5000)