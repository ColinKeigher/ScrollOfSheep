# -*- coding: utf-8 -*-

from scrollofsheep import printer, wireless, tracker
from time import sleep, strftime, localtime

print_out = False

# Makes a friendly date time
def time_stamp(string):
    str_time = '%H:%M:%S'
    return strftime(str_time, localtime(string))

# Prints on screen for BSides Vancouver
def screen_out(string, output=True):
    data = []
    data.append('SSID: %s' % string['ssid'])
    data.append('BSSID: %s' % string['bssid'])
    if string['type'] == 'client':
        data.append('(%s)' % string['device'])
    if output:
        stamp = '[%s]' % time_stamp(string['time'])
        out = '%s %s' % (stamp, ' :: '.join(data))
    else:
        out = data
    return out

def printer_out(string):
    p = printer.send_print(spacing=5)
    p.write_out(screen_out(string, output=False))

def main():
    t = tracker.tracking()
    w = wireless.probe_traffic()
    w.packet_count = 1000
    while True:
        data = w.scan()
        for item in data:
            t.data = item
            state = True
            if item['type'] == 'ap':
                state = t.new() # APs tend to clutter up things
            if t.insertable() and state:
                t.insert()
                print screen_out(item)
                if print_out:
                    printer_out(item)
        sleep(3)

if __name__ == '__main__':
    main()