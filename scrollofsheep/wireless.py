# -*- coding: utf-8 -*-

from scapy.all import *
from time import time
from bluetooth import discover_devices

class probe_traffic():
    def __init__(s, iface='mon0'):
        s.iface = iface
        s.packet_count = 100

    def _sniff(s):
        s.data = [] # Clear the data since we track it in a db anyway
        sniff(iface=s.iface, count=s.packet_count, prn=s._sniff_packet)

    def _sniff_packet(s, packet):
        output = { 'time': time() }
        if packet.haslayer(Dot11):
            if packet.type == 0 and packet.subtype in [ 4, 8 ]:
                dm = device_manufacturer(packet.addr2)
                if packet.subtype == 8:
                    output['type'] = 'ap'
                if packet.subtype == 4:
                    output['type'] = 'client'
                output['bssid'] = packet.addr2
                if packet.info != '':
                    output['ssid'] = packet.info
                else:
                    output['ssid'] = '(Unidentified)'
                output['device'] = dm.output()
                s.data.append(output)

    def _translate(s, item):
        return item.info

    def scan(s):
        s._sniff()
        return s.data

class probe_bt():
    def __init__(s):
        s._probe()

    def _probe(s):
        s.data = []
        s.nearby = [ x for x in discover_devices() ]

    def _output(s, item):
        dm = device_manufacturer(item)
        output = { 'time': time(), 'type': 'bt', 'ssid': '(Bluetooth)' }

class device_manufacturer():
    def __init__(s, mac_addr):
        s.mac_addr = mac_addr
        s.dev_manu = None
        s._cut_mac()
        s._mac_id()

    # Slices the MAC address in half
    def _cut_mac(s):
        s.mac_addr = s.mac_addr[:8]

    def _mac_id(s):
        ouis = { 
            'alfa': [ '00:c0:ca' ],
            'apple': [ '7c:d1:c3', '00:26:08', '00:22:41', '34:c0:59', '0c:77:1a', '14:8f:c6',
                        '7c:fa:df', '50:ea:d6', 'f0:dc:e2', 'e4:25:e7', '14:5a:05', '40:b3:95',
                        '58:b0:35', '18:20:32' ],
            'asus': [ '08:60:6e' ],
            'canon': [ '18:0c:ac' ],
            'liteon': [ '74:e5:43' ],
            'lg': [ '40:b0:fa', 'c4:43:8f', 'a8:16:b2', '10:68:3f' ],
            'intel': [ '00:24:d7', '10:0b:a9', '8c:a9:82' ],
            'nintendo': [ '00:21:47', '00:21:bd' ],
            'sony': [ '8c:7c:b5', 'a8:e3:ee' ],
            'samsung': [ '50:b7:c3', '90:18:7c', '5c:0a:5b', 'b8:5e:7b', '88:32:9b', '20:13:e0' ],
            'generic': [ 'c0:f8:da', '94:39:e5', '00:23:4e', '00:26:ab',
                            '60:21:c0', '00:08:ca', '00:03:2a', '00:23:4d',
                            '00:1a:73', '5c:f8:a1' ], # For things made by FoxConn et al
        }
        for key in ouis.keys():
            if s.mac_addr in ouis[key]:
                s.dev_manu = key
        if s.dev_manu == None:
            s.dev_manu = 'unknown'

    def _real_name(s, name):
        output = name
        names = { 
            'alfa': 'Alfa wireless adapter',
            'apple': 'Apple iOS device',
            'asus': 'ASUS computer',
            'canon': 'CANON camera',
            'generic': 'Generic mobile device',
            'liteon': 'Liteon wireless adapter',
            'lg': 'LG Electronics phone',
            'intel': 'Intel-based laptop',
            'nintendo': 'Nintendo gaming device',
            'sony': 'Sony gaming device',
            'samsung': 'Samsung mobile device',
            'unknown': 'Unidentified manufacturer',
            }
        if name in names.keys():
            output = names[name]
        return output

    def output(s):
        return s._real_name(s.dev_manu)
