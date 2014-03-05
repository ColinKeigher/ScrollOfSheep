# -*- coding: utf-8 -*-

from scrollofsheep import printer, wireless, tracker
from time import sleep, strftime, localtime

# Makes a friendly date time
def time_stamp(string):
    str_time = '%H:%M:%S'
    return strftime(str_time, localtime(string))

# Prints on screen for BSides Vancouver
def screen_out(string):
    data = []
    data.append('SSID: %s' % string['ssid'])
    data.append('BSSID: %s' % string['bssid'])
    if string['type'] == 'client':
        data.append('(%s)' % string['device'])
    out = '[%s] %s' % (time_stamp(string['time']), ' '.join(data))
    return out

def printer_out(string):
    p = printer.send_print(spacing=5)
    p.write_out("test")

t = tracker.tracking()
w = wireless.probe_traffic()
w.packet_count = 1000
while True:
    data = w.scan()
    for item in data:
        t.data = item
        if t.insert_recent():
            t.insert()
            print screen_out(item)
    sleep(3)