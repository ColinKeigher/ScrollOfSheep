# -*- coding: utf-8 -*-

from scapy.all import *
from time import time

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
            'apple': [ '7c:d1:c3', '00:26:08', '00:22:41', '34:c0:59' ],
            'lg': [ '40:b0:fa', 'c4:43:8f' ],
            'intel': [ '00:24:d7', '10:0b:a9' ],
            'nintendo': [ '00:21:47' ],
            'sony': [ '8c:7c:b5' ],
            'generic': [ 'c0:f8:da' ], # For things made by FoxConn et al
        }
        for key in ouis.keys():
            if s.mac_addr in ouis[key]:
                s.dev_manu = key
            if s.dev_manu == None:
                s.dev_manu = 'unknown'

    def _real_name(s, name):
        output = name
        names = { 
            'apple': 'Apple iOS device',
            'generic': 'Generic mobile device',
            'lg': 'LG Electronics phone',
            'intel': 'Intel-based laptop',
            'nintendo': 'Nintendo gaming device',
            'sony': 'Sony gaming device',
            'unknown': 'Unidentified manufacturer',
            }
        if name in names.keys():
            output = names[name]
        return output

    def output(s):
        return s._real_name(s.dev_manu)
