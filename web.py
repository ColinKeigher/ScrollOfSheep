# -*- coding: utf-8 -*-

from flask import Flask, render_template
from scrollofsheep import tracker

app = Flask(__name__)
template = 'default.html'

@app.route('/')
def hello_world():
    return render_template(template)

if __name__ == '__main__':
    app.run()