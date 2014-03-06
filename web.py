# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for
from scrollofsheep import tracker

app = Flask(__name__)
template = 'default.html'

@app.route('/')
def main():
    t = tracker.web_track()
    device_data = t.item_data()
    return render_template(template, device_data=device_data)

if __name__ == '__main__':
    app.run()