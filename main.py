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

# Combines data and then limits to a specific value of items
def append_data(orig_data, items):
    data = orig_data + items
    return data[:10]

def printer_out(string):
    p = printer.send_print(spacing=5)
    p.write_out(screen_out(string, output=False))

def main():
    t = tracker.tracking()
    w = wireless.probe_traffic()
    w.packet_count = 1000
    while True:
        # Output some details about what is being found
        data = w.scan()
        stats = t.stats()
        process = [] # Used to storing for use in the web interface
        for item in data:
            t.data = item
            state = True
            if item['type'] == 'ap':
                state = t.new() # APs tend to clutter up things
            if t.insertable() and state:
                t.insert()
                process.append(item)
                print screen_out(item)
                if print_out:
                    printer_out(item)
        # Processing for storage used by the web service
        # I'll clean this up later--Pickle drove me nuts here.
        wt = tracker.web_track()
        build = None
        if build == None: # We'll build a new set of keys
            build = {}
            for x in t.stats_types:
                build[x] = [ 0 ] # Goddamn Pickle's fault for this
        for key in stats.keys():
            for item in stats[key]:
                ckey = item['type']
                item['realtime'] = time_stamp(item['time'])
                build[ckey].append(item)
        for key in build.keys(): # Limit each to 10 or something
            build[key] = build[key][:10]
        wt.overwrite(build)
        sleep(3)

if __name__ == '__main__':
    main()